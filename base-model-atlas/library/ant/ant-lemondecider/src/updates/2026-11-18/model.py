# Author:浅斟
"""LemonDecider 4B local Python, CLI and HTTP entrypoints. See QUICKSTART.md."""
import argparse
import hashlib
import hmac
import importlib.util
import json
import os
from pathlib import Path
import sys
import threading


def _runtime():
    # Resolve relative to this file, not cwd or a project checkout on PYTHONPATH.
    name = '_lemondecider_runtime_' + hashlib.sha256(str(Path(__file__).resolve()).encode()).hexdigest()[:12]
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name,Path(__file__).with_name('decision_runtime.py'))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


class DecisionModel:
    def __init__(self, checkpoint=None, device='auto'):
        import torch
        from transformers import AutoModel, AutoProcessor
        self.rt = _runtime()
        checkpoint = Path(checkpoint or Path(__file__).resolve().parent).resolve()
        if device == 'auto':
            device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.device = device
        # All artifacts must exist locally. No base/adapter downloads or external code paths.
        self.model = AutoModel.from_pretrained(
            str(checkpoint),trust_remote_code=True,local_files_only=True,use_safetensors=True,
            dtype=torch.bfloat16,device_map=device,attn_implementation='sdpa').eval()
        self.processor = AutoProcessor.from_pretrained(str(checkpoint),trust_remote_code=True,local_files_only=True)
        self.processor.tokenizer.padding_side = 'left'
        self.config = self.model.config
        if self.config.inference_protocol.get('version') != 1:
            raise ValueError('Unsupported inference protocol')
        if tuple(self.model.readout.weight.shape) != (self.config.max_options,self.config.text_config.hidden_size):
            raise ValueError('Readout shape does not match configuration')
        for code, tid in zip(self.config.codes,self.config.token_ids,strict=True):
            if self.processor.tokenizer.encode(code,add_special_tokens=False) != [tid]:
                raise ValueError('Tokenizer option mapping mismatch')
        self._lock = threading.Lock()

    def predict(self, request):
        """Return typed answers for {state, questions}; never generate text or truncate."""
        import torch
        state, questions = self.rt.validate_request(request)
        answers = {}
        with self._lock, torch.inference_mode():
            for name, question in questions.items():
                inputs = self.rt.prepare_question(self.processor,self.config,state,question,self.device)
                logits = self.model(**inputs).logits[0][:len(self.rt.options(question)[0])].float()
                if not bool(torch.isfinite(logits).all()):
                    raise RuntimeError('Nonfinite model output')
                probabilities = torch.softmax(logits/self.config.temperature,-1).tolist()
                answers[name] = self.rt.answer(question,probabilities)
        return {'model':self.config.model_id,'answers':answers}

    def predict_np(self, features, trace_id=None):
        """Optional synchronous adapter: request JSON bytes -> response JSON string."""
        raw = features.get('request')
        try:
            if isinstance(raw,bytes): raw = raw.decode('utf-8')
            result = self.predict(json.loads(raw))
            return 0, 'ok', {'response':json.dumps(result,ensure_ascii=False,allow_nan=False)}
        except (ValueError,TypeError):
            return 1, 'Invalid or over-capacity request', {}


def create_app(engine):
    from fastapi import FastAPI, Header, HTTPException, Request
    from starlette.concurrency import run_in_threadpool
    app = FastAPI(title='LemonDecider 4B',version='3.1',docs_url=None,redoc_url=None,openapi_url=None)
    api_key = os.environ.get('LEMONDECIDER_API_KEY','')

    def authenticate(authorization):
        if api_key and not hmac.compare_digest((authorization or '').encode(),f'Bearer {api_key}'.encode()):
            raise HTTPException(401,'Missing or invalid API key')

    @app.get('/health')
    def health(authorization: str | None = Header(default=None)):
        authenticate(authorization)
        return {'status':'ready','model':engine.config.model_id,'modalities':['text']}

    @app.get('/v1/models')
    def models(authorization: str | None = Header(default=None)):
        authenticate(authorization)
        return {'models':[{'name':engine.config.model_id}]}

    @app.post('/v1/systemone')
    async def systemone(request: Request, authorization: str | None = Header(default=None)):
        authenticate(authorization)
        chunks=[]; size=0
        async for chunk in request.stream():
            size+=len(chunk)
            if size > 8_000_000:
                raise HTTPException(413,'Request body is too large')
            chunks.append(chunk)
        try:
            body=json.loads(b''.join(chunks))
        except (ValueError,UnicodeError,RecursionError):
            raise HTTPException(422,'Invalid JSON request') from None
        try:
            return await run_in_threadpool(engine.predict,body)
        except (ValueError,TypeError,RecursionError):
            raise HTTPException(422,'Invalid or unsupported request; no input was truncated') from None
        except Exception:
            # Do not return internal filenames, stack traces or user payloads.
            raise HTTPException(500,'Inference failed') from None

    return app


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--checkpoint',default=str(Path(__file__).resolve().parent))
    ap.add_argument('--device',default='auto',help='auto, cuda:0 or cpu')
    ap.add_argument('--input',help='JSON request file, or - for stdin; defaults to example.json')
    ap.add_argument('--serve',action='store_true')
    ap.add_argument('--host',default='127.0.0.1')
    ap.add_argument('--port',type=int,default=8000)
    args=ap.parse_args()
    if args.serve and args.host not in ('127.0.0.1','localhost','::1') and not os.environ.get('LEMONDECIDER_API_KEY'):
        ap.error('Set LEMONDECIDER_API_KEY before binding to a non-loopback address')
    engine=DecisionModel(args.checkpoint,args.device)
    if args.serve:
        import uvicorn
        uvicorn.run(create_app(engine),host=args.host,port=args.port,access_log=False)
    else:
        text=sys.stdin.read() if args.input=='-' else Path(args.input or Path(__file__).with_name('example.json')).read_text()
        print(json.dumps(engine.predict(json.loads(text)),ensure_ascii=False,allow_nan=False,indent=2))


if __name__=='__main__':
    main()
