# LemonDecider 4B

**Model ID:** `lemondecider-4b-20261112-v3.1`

本目录是完整的本地推理包：复制整个目录即可使用，不需要额外下载基座、adapter 或实验代码。
只接受文本/JSON 状态，输出 choice、noul、score 三类决策；不生成聊天文本，不支持图片或视频。

## 1. 环境

- 推荐 Python 3.12（已验证）；安装与硬件匹配的 PyTorch 和 torchvision（已测 PyTorch 2.9 / torchvision 0.24）。
- 建议至少 16 GB 显存；权重约 8.5 GiB，长输入还需要额外运行内存。CPU 可用但较慢。
- PPU/其他厂商环境须保留厂商 PyTorch，**不要用通用 CUDA wheel 覆盖**。
- 在已有 PyTorch 环境中安装其余依赖：

```bash
# 在 lemondecider-4b-20261112-v3.1 目录内运行
python -m pip install -r requirements.txt
python verify.py
```

快速路径可选安装与硬件兼容的 flash-linear-attention；未安装时由 transformers 使用兼容实现。
依赖安装需要网络，但模型加载和推理仅访问本目录。
请保留随包 tokenizer，不要根据通用 tokenizer 警告自动替换正则或词表；这会改变输入编码。

## 2. 一条命令推理

```bash
python model.py --device cuda:0 --input example.json
# 自动选择设备：
python model.py --input example.json
# CPU：
python model.py --device cpu --input example.json
```

`example.json` 是可直接运行的中文示例，包含三种题型。任意工作目录也可调用：

```bash
python /path/to/model-folder/model.py --device cuda:0 --input /path/to/request.json
```

输入格式：

```json
{"state":"客户希望申请退款","questions":{"intent":{"type":"choice","instructions":"判断主要诉求","criteria":{"refund":"退款","delivery":"物流"}}}}
```

- `state`：字符串、列表或 JSON 对象。
- `questions`：以问题名为 key 的对象，一次最多 256 个问题；每个问题独立处理。
- `choice`：`criteria` 是 1–255 个选项的对象；返回选项概率、`choice` 和 `confidence`。
- `noul`：返回 `noul`，范围 0–1，表示肯定答案的概率；可选 `criteria={"false":"否的含义","true":"是的含义"}`。
- `score`：`criteria` 是 2–255 个有序描述；返回 **从 0 开始的等级期望值**及分布，不保证为整数。

温度和输入渲染由运行配置自动应用，**不要再次除以温度或自行套聊天模板**。
输入上限 8192 tokens（包含模板）；超限会明确报错，不会静默截断。

## 3. Python

在模型目录中，或将该目录加入 Python 模块搜索路径：

```python
import json
from model import DecisionModel

engine = DecisionModel(device="cuda:0")
request = {"state":"我想退款", "questions":{
    "intent":{"type":"choice","criteria":{"refund":"退款","other":"其他"}}
}}
print(json.dumps(engine.predict(request), ensure_ascii=False, indent=2))
```

每进程只初始化一次 `DecisionModel`，随后复用。HF `AutoModel` 仅提供底层前向；
普通用户应使用此入口，由它完成渲染、marker 位置与类型化答案转换。

## 4. HTTP 服务

默认只监听本机：

```bash
python model.py --serve --device cuda:0 --port 8000
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/v1/systemone \
  -H 'Content-Type: application/json' --data-binary @example.json
```

需要跨机器访问时，先设置自己的 API key，再监听外部地址：

```bash
# 在 shell 中设置 LEMONDECIDER_API_KEY；不要把真实密钥写入代码或提交到版本库。
python model.py --serve --host 0.0.0.0 --port 8000 --device cuda:0
curl -s http://127.0.0.1:8000/v1/systemone \
  -H "Authorization: Bearer ${LEMONDECIDER_API_KEY}" \
  -H 'Content-Type: application/json' --data-binary @example.json
```

设置 API key 后，`/health`、`/v1/models` 和 `/v1/systemone` 均需认证。
生产环境应置于 HTTPS 反向代理及访问控制之后。响应不会返回本地 checkpoint 路径。
错误码：401 未授权；413 请求过大；422 输入不合法、不支持或超过容量；500 推理失败。

## 5. 常见问题

- 缺少 `qwen3_5`：按 requirements 安装对应 transformers 版本。
- GPU 内存不足：单进程运行，缩短输入；不要通过截断来改变原始问题。
- 输出不是聊天回复：这是决策模型，请使用上述三种题型。
- 完整性检查失败：重新复制完整目录，勿混用其他版本的配置和代码。

许可证与版权归属见 `LICENSE`、`LICENSE.code`、`NOTICE`。
