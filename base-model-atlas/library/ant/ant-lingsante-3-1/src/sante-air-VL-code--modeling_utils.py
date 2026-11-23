#!/usr/bin/env python3
# coding=utf-8
# Copyright (c) Ant Group. All rights reserved.
from typing import Callable, Optional, Tuple, Dict, Any

import torch
import torch.nn as nn
import torch.nn.functional as F

from bailingmm.common.logger import logger


def encode_image_post_processing(image_embeds: torch.Tensor, n_query=None, bilinear_interpolation=False):
    if n_query is None:
        return image_embeds
    b, n, c = image_embeds.shape
    if n == n_query:
        return image_embeds
    sqrt_n = int(n**0.5)
    image_embeds = image_embeds.permute(0, 2, 1).view(b, c, sqrt_n, sqrt_n)
    stride = int(sqrt_n // (n_query**0.5))
    if not bilinear_interpolation:
        image_embeds = F.avg_pool2d(image_embeds, kernel_size=(stride, stride), stride=stride)
    else:
        image_embeds = nn.functional.interpolate(image_embeds, [int(n_query**0.5), int(n_query**0.5)], mode="bilinear")
    image_embeds = image_embeds.view(b, c, -1).permute(0, 2, 1).contiguous()
    return image_embeds


def get_model_input_handler(model_type: str):
    if "qwen2" in model_type.lower():
        from .qwen2_utils import prepare_model_inputs

        return prepare_model_inputs
    elif "llama" in model_type.lower():
        # todo
        return None
    else:
        raise ValueError(f"model type {model_type} is not supported")


def unwrap_feats(feats: torch.Tensor, feats_lengths: torch.Tensor):
    """
    The input feats are in the "wrapped" format, which means that features from (at most) N audios are concatenated
    as a single sample feats[i]. In this case, each row of feats_lengths contains the lengths of the concatenated
    feature. This function unwraps the features.
    For samples with less than N segments, one should pad feats_lengths with 0. The result will contain valid
    segments only.

    feats: torch.Tensor, size = [B, L1 + L2 + ... + LN, ...]
    feats_lengths: torch.LongTensor, size = [B, N]

    Example ('X' for padding):
    Inputs:
        feats = [[A, A, A, A, X],
                 [B, B, C, C, C]]
        feats_lengths = [[4, 0],
                         [2, 3]]
    Outputs:
        feat_segs = [[A, A, A, A],
                     [B, B, X, X],
                     [C, C, C, X]]
        feat_seg_lengths = [4, 2, 3]
    """
    num_segs = int((feats_lengths > 0).sum().item())
    max_length_seg = int(feats_lengths.max().item())
    feat_segs_batch = feats.new_zeros((num_segs, max_length_seg, *feats.shape[2:]))
    feat_seg_lengths = []
    for i in range(feats_lengths.shape[0]):
        feat_index = 0
        for j in range(feats_lengths.shape[1]):
            feat_len = feats_lengths[i, j].item()
            if feat_len == 0:
                break
            feat_segs_batch[len(feat_seg_lengths), :feat_len] = feats[i, feat_index : feat_index + feat_len]
            feat_seg_lengths.append(feat_len)
            feat_index += feat_len
    feat_seg_lengths = torch.tensor(feat_seg_lengths, dtype=torch.long, device=feats.device)
    return feat_segs_batch, feat_seg_lengths


def wrap_feats(feat_segs: torch.Tensor, feats_lengths: torch.Tensor, feats_seg_lengths: Optional[torch.Tensor] = None):
    """
    Wrap segmented features back to the wrapped format.
    This function is the inverse operation of unwrap_feats(). See its documentation for details.
    Note that the feats_lengths value does not matter a lot. We only check the location of the first 0 to determine the
    number of feature segments.
    """
    max_length_wrapped = 0
    feat_idx = 0
    for i in range(feats_lengths.shape[0]):
        length_wrapped = 0
        for j in range(feats_lengths.shape[1]):
            feat_len = int(feats_lengths[i, j].item())
            if feat_len == 0:
                break
            if feats_seg_lengths is not None:
                feat_len = int(feats_seg_lengths[feat_idx].item())
            length_wrapped += feat_len
            feat_idx += 1
        max_length_wrapped = max(max_length_wrapped, length_wrapped)
    feats = feat_segs.new_zeros((feats_lengths.shape[0], max_length_wrapped, *feat_segs.shape[2:]))
    feat_idx = 0
    feats_locs_buffer = []
    feats_lengths_buffer = []
    for i in range(feats_lengths.shape[0]):
        feat_locs_buffer = []
        feat_lengths_buffer = []
        feat_total_len = 0
        for j in range(feats_lengths.shape[1]):
            feat_len = int(feats_lengths[i, j].item())
            if feat_len == 0:
                break
            if feats_seg_lengths is not None:
                feat_len = int(feats_seg_lengths[feat_idx].item())
            feats[i, feat_total_len : feat_total_len + feat_len] = feat_segs[feat_idx, :feat_len]
            feat_locs_buffer.append(feat_total_len)
            feat_lengths_buffer.append(feat_len)
            feat_idx += 1
            feat_total_len += feat_len
        feats_locs_buffer.append(torch.tensor(feat_locs_buffer, dtype=torch.long))
        feats_lengths_buffer.append(torch.tensor(feat_lengths_buffer, dtype=torch.long))
    feats_locs = torch.nn.utils.rnn.pad_sequence(feats_locs_buffer, True).to(feats_lengths.device)
    feats_new_lengths = torch.nn.utils.rnn.pad_sequence(feats_lengths_buffer, True).to(feats_lengths.device)
    return feats, feats_locs, feats_new_lengths


def encode_audio_segments(
    encoder: Callable[[torch.Tensor, torch.Tensor], Tuple[torch.Tensor, torch.Tensor]],
    proj_layer: torch.nn.Module,
    downsampler_args: Dict[str, Any],
    wav_feats: Optional[torch.Tensor] = None,
    wav_feats_lengths: Optional[torch.Tensor] = None,
    waveforms: Optional[torch.Tensor] = None,
    waveforms_lengths: Optional[torch.Tensor] = None,
    use_waveform: bool = False,
    offload_activation_layers: list = None,
    freeze_proj: bool = False
):
    """
    Apply audio encoder to input audio features in wrapped format.
    See the documentation of unwrap_feats() for details about 'wrapped format'.
    """
    if offload_activation_layers is None:
        offload_activation_layers = []

    # Forward audio encoder.
    if use_waveform:
        assert waveforms is not None and waveforms_lengths is not None
        # Unwrap the waveforms so each waveform is placed at an independent row.
        waveform_segs_batch, waveform_seg_lengths = unwrap_feats(waveforms, waveforms_lengths)
        audio_feats_seg, audio_feat_seg_lengths = encoder(
            waveform_segs_batch,
            waveform_seg_lengths.to(waveform_segs_batch.device),
            offload_activation_layers=offload_activation_layers,
        )
    else:
        assert wav_feats is not None and wav_feats_lengths is not None
        # Unwrap the features so the feature of each waveform is placed at an independent row.
        feat_segs_batch, feat_seg_lengths = unwrap_feats(wav_feats, wav_feats_lengths)
        audio_feats_seg, audio_feat_seg_lengths = encoder(
            feat_segs_batch,
            feat_seg_lengths.to(feat_segs_batch.device),
            offload_activation_layers=offload_activation_layers,
        )[:2]
    with torch.set_grad_enabled(not freeze_proj):# proj_layer 会一直保持可训练，不被freeze
        # Forward audio projector layer.
        audio_feats_seg_proj = proj_layer(audio_feats_seg.transpose(-1, -2)).transpose(-1, -2)
        audio_feat_seg_lengths = (
            audio_feat_seg_lengths + 2 * (downsampler_args["padding"]) - downsampler_args["kernel_size"]
        ) // downsampler_args["stride"] + 1

        # Wrap the features so the 1st dim represents batch_size.
        input_lengths = waveforms_lengths if use_waveform else wav_feats_lengths
        assert input_lengths is not None
        audio_feats, _, audio_feats_lengths = wrap_feats(audio_feats_seg, input_lengths, audio_feat_seg_lengths)
        audio_feats_proj, _, audio_feats_lengths2 = wrap_feats(audio_feats_seg_proj, input_lengths, audio_feat_seg_lengths)
        assert torch.all(audio_feats_lengths == audio_feats_lengths2), f"{audio_feats_lengths}, {audio_feats_lengths2}"

        return audio_feats_proj, audio_feats, audio_feats_lengths


class Transpose(nn.Module):
    def __init__(self, dim0: int, dim1: int):
        super().__init__()
        self.dim0 = dim0
        self.dim1 = dim1

    def forward(self, x):
        return x.transpose(self.dim0, self.dim1)


def patch_continuous_features(
    input_embeddings: torch.Tensor,
    placeholder_loc_lens: torch.Tensor,
    encoded_feats: torch.Tensor,
    encoded_feat_lens: torch.Tensor,
):
    """
    Patch continuous features into input embeddings, while keeping a valid gradient flow.

    input_embeddings: torch.Tensor, size = [B, C?, T, D]
    placeholder_loc_lens: torch.LongTensor, size = [B, N, 2]
        Each 2-tuple represents (start, length) of a placeholder.
    encoded_feats: torch.Tensor, size = [B, L1 + L2 + ... + LN, ...]
    encoded_feat_lens: torch.LongTensor, size = [B, N]

    Example ('X' for patch placeholder tokens):
    Inputs:
        input_embeddings = [[1, 2, 3, X, X, X, 4, 5, 6, X, X, X, 7, 8]]
        placeholder_loc_lens = [[[3, 3]], [[9, 3]]]
        encoded_feats = [[A, A, A, B, B]]
        encoded_feat_lens = [[3], [2]]
    Outputs:
        embeddings = [[1, 2, 3, A, A, A, 4, 5, 6, B, B, X, 7, 8]]
    """
    batch_size = input_embeddings.size(0)
    for i in range(batch_size):
        audio_feat_start = 0
        for j in range(placeholder_loc_lens.shape[1]):
            placeholder_start: int = int(placeholder_loc_lens[i, j, 0].item())
            placeholder_len: int = int(placeholder_loc_lens[i, j, 1].item())
            if placeholder_len <= 0:
                break
            feat_len = int(encoded_feat_lens[i, j].item())
            real_feat_len = feat_len
            if feat_len > placeholder_len:
                logger.warning(
                    f"Feature length ({feat_len}) > placeholder length ({placeholder_len}). This is not expected. Please "
                    "check the implementation of estimate_audio_feature_length(). We truncate the feature to avoid errors."
                )
                feat_len = placeholder_len
            target_len = min(feat_len, placeholder_len)
            input_embeddings[i, placeholder_start : placeholder_start + target_len] = encoded_feats[
                i, audio_feat_start : audio_feat_start + target_len
            ]
            audio_feat_start += real_feat_len
    return input_embeddings


def build_modality_mask(placeholder_loc_lens: torch.Tensor, shape: torch.Size):
    mask = torch.zeros(shape, dtype=torch.bool)
    for i in range(placeholder_loc_lens.shape[0]):
        for j in range(placeholder_loc_lens.shape[1]):
            start: int = int(placeholder_loc_lens[i, j, 0].item())
            length: int = int(placeholder_loc_lens[i, j, 1].item())
            if length <= 0:
                break
            mask[i, start : start + length] = True
    return mask
