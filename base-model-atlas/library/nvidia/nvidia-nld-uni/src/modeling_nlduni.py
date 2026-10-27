from pathlib import Path
import math
import torch
from torch import nn
from PIL import Image
from transformers import AutoTokenizer
from transformers.generation import GenerationMixin
from transformers.modeling_outputs import CausalLMOutputWithPast
from transformers.utils.hub import cached_file
from .configuration_nlduni import NLDUniConfig
from .core import Ministral3Model, Ministral3PreTrainedModel
from .attention import MinistralFlexAttention
from .bridge import PackedLinearImageCodec
from .vq import Emu3VQ, Emu3ImageProcessor
from .vision import RadioVisionTower
from .projector import RadioHProjector
from .positions import _build_2d_sincos_position_embedding, GENERATION_2D_SINCOS_SCALE
from .markers import strip_image_row_markers
from .chat_utils import generate_with_prefix_cache_block_diff
from .sampling import text_to_image as sample_image
from .image_utils import process_images, fix_one_prompt, tokenizer_image_token
from .conversation import Conversation
from .tree import BalancedSemanticTree, production_semantic_tree_contract

class NLDUniBackbone(Ministral3Model):
    def __init__(self, config):
        super().__init__(config)
        self.vision_tower=RadioVisionTower()
        self.mm_projector=RadioHProjector(config)
        self.image_newline=nn.Parameter(torch.empty(config.hidden_size))
        self.vqvae=Emu3VQ()
        self.image_processor_gen=Emu3ImageProcessor()
        self.gen_embedding=nn.Embedding(131072+256,4096)
        self.gen_predictor=nn.Linear(4096,131072,bias=False)
        self.packed_image_codec=PackedLinearImageCodec(4096,norm_eps=1e-6)
        self.downsample_gen=None
        self.upsample_gen=None
        self.downsample_gen_enc=None
        self.gen_embedding_2=None
        self.gen_predictor_2=None
        self.extra_gen_dit=None
    def get_vision_tower(self):
        return self.vision_tower
    def get_gen_tokenizer(self):
        return self.vqvae
    def call_gen_token_embedding(self, token_ids):
        return self.gen_embedding(token_ids)
    def call_gen_fixed_token_embedding(self, token_ids):
        return self.gen_embedding(token_ids)*self.config.generation_embedding_scale
    def call_gen_embedding(self, token_ids=None, gen_shape=None, enc=False, child_embeddings=None,
                           spatial_compression=True, add_spatial_position=True):
        values=self.gen_embedding(token_ids) if child_embeddings is None else child_embeddings
        if spatial_compression:
            values=self.packed_image_codec.compress_fixed_grid(values,gen_shape)
        scale=self.config.generation_embedding_scale
        if spatial_compression:scale*=self.config.generation_downsample_scale
        values=values*scale
        if add_spatial_position:
            h,w=gen_shape
            if spatial_compression:h,w=h//2,w//2
            pos=_build_2d_sincos_position_embedding(h,w,values.shape[-1],marker_column=not enc,device=values.device,dtype=values.dtype)
            values=values+pos.unsqueeze(0)*GENERATION_2D_SINCOS_SCALE
        return values
    def call_gen_predictor(self, hidden_states, gen_shape=None, timesteps=None):
        h,w=gen_shape
        states=self.packed_image_codec.expand_fixed_grid(hidden_states.reshape(-1,(h//2)*(w//2),4096),gen_shape)
        return self.gen_predictor(states.flatten(0,1))

class NLDUniForCausalLM(Ministral3PreTrainedModel, GenerationMixin):
    config_class=NLDUniConfig
    base_model_prefix=''
    def __init__(self, config):
        super().__init__(config)
        self.encoder=NLDUniBackbone(config)
        self.diffusion_head=nn.Linear(config.hidden_size,config.vocab_size,bias=False)
        self.mask_token_id=100
        self.vocab_size=config.vocab_size
        self._tokenizer=None
        self._asset_root=None
        self.post_init()
    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *args, **kwargs):
        model=super().from_pretrained(pretrained_model_name_or_path,*args,**kwargs)
        target=model[0] if isinstance(model,tuple) else model
        options={k:kwargs[k] for k in ('revision','cache_dir','local_files_only','token','subfolder') if k in kwargs}
        target._tokenizer=AutoTokenizer.from_pretrained(pretrained_model_name_or_path,**options)
        tree=cached_file(pretrained_model_name_or_path,'pca_tree.pt',**options)
        BalancedSemanticTree.from_artifact(production_semantic_tree_contract(tree))
        target.config.image_token_tree_path=tree
        target.eval()
        return model
    def save_pretrained(self, save_directory, **kwargs):
        import shutil
        destination = Path(save_directory)
        destination.mkdir(parents=True, exist_ok=True)
        super().save_pretrained(destination, **kwargs)
        self.tokenizer.save_pretrained(destination)
        asset = Path(self.config.image_token_tree_path)
        if asset.resolve() != (destination / 'pca_tree.pt').resolve():
            shutil.copyfile(asset, destination / 'pca_tree.pt')
    @property
    def model(self):return self.encoder
    def get_model(self):return self.encoder
    def get_vision_tower(self):return self.encoder.vision_tower
    def get_input_embeddings(self):return self.encoder.embed_tokens
    def set_input_embeddings(self, value):self.encoder.embed_tokens=value
    def get_output_embeddings(self):return self.diffusion_head
    def set_output_embeddings(self,value):self.diffusion_head=value
    @property
    def tokenizer(self):
        if self._tokenizer is None:raise RuntimeError('Load with from_pretrained before inference')
        return self._tokenizer
    def forward(self,input_ids=None,inputs_embeds=None,attention_mask=None,position_ids=None,past_key_values=None,use_cache=False,**kwargs):
        result=self.encoder(input_ids=input_ids,inputs_embeds=inputs_embeds,attention_mask=attention_mask,position_ids=position_ids,past_key_values=past_key_values,use_cache=use_cache,**kwargs)
        return CausalLMOutputWithPast(logits=self.diffusion_head(result.last_hidden_state),past_key_values=result.past_key_values)
    def prepare_inputs_labels_for_multimodal(self, input_ids, position_ids, attention_mask,
             past_key_values, labels, images, modalities=None, image_sizes=None, return_inputs=False, **kwargs):
        embeds=self.encoder.embed_tokens(input_ids.clamp_min(0))
        if images:
            features=[]
            for pixels,grid in images:
                visual=self.encoder.vision_tower(pixels).squeeze(0)
                features.append(self.encoder.mm_projector(visual,grid.to(visual.device)))
            visual=torch.cat(features)
            mask=input_ids.eq(-500)
            if int(mask.sum())!=len(visual):raise ValueError('Image placeholder count does not match vision features')
            embeds[mask]=visual.to(embeds)
        result=(None,position_ids,attention_mask,past_key_values,embeds,labels)
        return result+(input_ids,) if return_inputs else result
    def encode_image_gen(self, images, enc=False):
        ref=next(self.encoder.vqvae.parameters())
        quant,_,(_,_,ids)=self.encoder.vqvae.encode(images.to(ref))
        return ids.reshape(len(images),-1),tuple(quant.shape[-2:])
    def decode_image_gen(self, codes, height, width):
        shape=(height//16,width//16)
        if codes.shape[-1] != math.prod(shape):
            codes=strip_image_row_markers(codes,shape,markers_per_row=2)
        if (codes>=131072).any():raise ValueError('Unresolved image tokens at decoding')
        quant=self.encoder.vqvae.quantize.get_codebook_entry(codes)
        quant=quant.reshape(len(codes),*shape,256).permute(0,3,1,2).contiguous()
        pixels=self.encoder.vqvae.decode(quant).float().clamp(-1,1)
        return ((pixels+1)/2*255).permute(0,2,3,1).cpu().numpy().astype('uint8')
    def _sample(self,prompt,*,image=None,resolution=1024,steps=64,refinement_steps=4,guidance_scale=3.,image_guidance_scale=2.,temperature=.8,seed=None,top_k=0,top_p=1.,shift=5.,show_progress=False):
        if resolution not in (256,512,1024):raise ValueError('resolution must be 256, 512, or 1024')
        if steps<1 or not math.isfinite(temperature) or temperature<=0:raise ValueError('steps and temperature must be positive')
        # A supplied seed is local to this call and does not disturb caller RNG state.
        devices=[self.device.index if self.device.index is not None else torch.cuda.current_device()] if self.device.type=='cuda' else []
        with torch.random.fork_rng(devices=devices,enabled=seed is not None):
            if seed is not None:torch.manual_seed(seed)
            return sample_image(self,prompt,tokenizer=self.tokenizer,edit_image=image,image_processor=self.encoder.vision_tower.image_processor,
                image_resolution=resolution,n_tokens=(resolution//16)**2,n_steps=steps,image_embedding_refinement_steps=refinement_steps,
                guidance_scale=guidance_scale,guidance_scale_image=image_guidance_scale,temperature=temperature,
                confidence_policy='stratified',shift=shift,schedule='shift',alg_temp=5.,dynamic_temperature=True,
                min_temperature=.5,schedule_temp='cosine2',top_k=top_k,top_p=top_p,disable_tqdm=not show_progress,
                micro_cond=f'ORIGINAL WIDTH : {resolution}; ORIGINAL HEIGHT : {resolution}; TOP : 0; LEFT : 0; SCORE : 7.110;',
                template='Generate an image with the caption:\n <prompt>',edit_mode=1 if image is not None else 0)
    @torch.inference_mode()
    def text_to_image(self,prompt,*,resolution=1024,steps=64,refinement_steps=4,guidance_scale=3.,temperature=.8,seed=None,top_k=0,top_p=1.,shift=5.,show_progress=False):
        """Generate one PIL image using the checkpoint's semantic-tree sampler."""
        return self._sample(prompt,resolution=resolution,steps=steps,refinement_steps=refinement_steps,guidance_scale=guidance_scale,temperature=temperature,seed=seed,top_k=top_k,top_p=top_p,shift=shift,show_progress=show_progress)
    @torch.inference_mode()
    def image_edit(self,image,prompt,*,resolution=1024,steps=64,refinement_steps=4,guidance_scale=1.6,image_guidance_scale=2.,temperature=.8,seed=None,top_k=0,top_p=1.,shift=5.,crop_to_source=True,show_progress=False):
        """Edit a PIL image or local image path; return a PIL image."""
        if isinstance(image,(str,Path)):image=Image.open(image)
        image=image.convert('RGB')
        result=self._sample(prompt,image=image,resolution=resolution,steps=steps,refinement_steps=refinement_steps,guidance_scale=guidance_scale,image_guidance_scale=image_guidance_scale,temperature=temperature,seed=seed,top_k=top_k,top_p=top_p,shift=shift,show_progress=show_progress)
        if crop_to_source:
            w,h=image.size; scale=resolution/max(w,h)
            cw,ch=round(w*scale),round(h*scale)
            left,top=(resolution-cw)//2,(resolution-ch)//2
            result=result.crop((left,top,left+cw,top+ch)).resize((w,h),Image.Resampling.LANCZOS)
        return result
    @torch.inference_mode()
    def generate(self,prompt=None,*,image=None,inputs=None,input_ids=None,max_new_tokens=16000,block_length=32,steps_per_block=32,threshold=.9,temperature=0.,return_token_ids=False,**kwargs):
        """Visual/text understanding, using greedy block diffusion without thinking."""
        if kwargs:raise TypeError(f'Unknown inference options: {sorted(kwargs)}')
        if max_new_tokens<1 or block_length<1 or steps_per_block<1:raise ValueError('Token and step counts must be positive')
        if not 0<=threshold<=1:raise ValueError('threshold must be between 0 and 1')
        if isinstance(prompt,torch.Tensor):input_ids,prompt=prompt,None
        if inputs is not None:input_ids=inputs
        if input_ids is None:
            if not isinstance(prompt,str):raise TypeError('prompt must be a string, or provide input_ids')
            conv=Conversation(); images=[]
            if image is not None:
                if isinstance(image,(str,Path)):image=Image.open(image)
                images=process_images([image.convert('RGB')],self.encoder.vision_tower.image_processor,self.config)
                prompt='<image>\n'+prompt
            conv.append_message(conv.roles[0],prompt)
            conv.append_message(conv.roles[1],None)
            rendered=conv.get_prompt()
            if images:
                grid=images[0][1]
                rendered=fix_one_prompt(rendered,self.config,[(int(grid[0,1])//2,int(grid[0,2])//2)])
            input_ids=tokenizer_image_token(rendered,self.tokenizer,return_tensors='pt',constant_version='ministral').unsqueeze(0).to(self.device)
            embeds=self.prepare_inputs_labels_for_multimodal(input_ids,None,None,None,None,images)[4]
        else:
            if image is not None:raise ValueError('Use a string prompt when providing image')
            input_ids=input_ids.to(self.device)
            embeds=self.encoder.embed_tokens(input_ids)
        length=math.ceil(max_new_tokens/block_length)*block_length
        ids,_=generate_with_prefix_cache_block_diff(self,prompt_embeds=embeds,gen_length=length,steps=steps_per_block*(length//block_length),block_length=block_length,temperature=temperature,mask_id=100,threshold=threshold,shift_logits=True,causal_context=True,eos_token_id=11)
        ids=ids[:, :max_new_tokens]
        if return_token_ids:return ids
        return self.tokenizer.decode(ids[0],skip_special_tokens=True).strip()

from .positions import _generation_grid_shape as _bundle_positions

from .core import rotate_half as _bundle_core

from .refinement import _validate_refinement_steps as _bundle_refinement

from .conversation import Conversation
from .tree import BalancedSemanticTree, production_semantic_tree_contract as _bundle_conversation

from .constants import NemotronMinistralDLMConstant as _bundle_constants

from .chat_utils import SimpleOutputWithPast as _bundle_chat_utils

from .tree import _plain_positive_int as _bundle_tree

from .schedules import cosine_schedule_2 as _bundle_schedules

from .radio_cls import ClsToken as _bundle_radio_cls

from .padding import resolve_source_padding_vq_lock as _bundle_padding

from .pmj import stratified_random as _bundle_pmj

from .image_utils import pad_to_square_and_resize as _bundle_image_utils

from .sampling import _load_prediction_image as _bundle_sampling

from .markers import _validate_markers_per_row as _bundle_markers

from .radio_patch import ViTPatchGenerator as _bundle_radio_patch

from .vision import RadioBackbone as _bundle_vision

from .sbd_attention import build_image_attention_doc_ids as _bundle_sbd_attention

from .attention import fused_flex_attention as _bundle_attention

from .vq import Codebook as _bundle_vq

from .utils import pad_along_last_dim as _bundle_utils

from .vq_model import nonlinearity as _bundle_vq_model

from .projector import SquaredReLU as _bundle_projector

from .bridge import PackedLinearImageCodec as _bundle_bridge
from .token_constants import IMAGE_PAD_TOKEN_INDEX as _bundle_token_constants
