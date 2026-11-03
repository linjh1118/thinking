模型参数参考 | LongCat API Docs
Docs
使用指南
快速开始
Token资源包
API按量付费
常见问题
更新日志
API 文档
API 概述
视觉理解
对话接口
POST
OpenAI Chat Completion API
POST
OpenAI Responses API
POST
Anthropic API
参数参考
模型参数参考
模型接口
GET
模型列表
GET
模型详情
工具
AI 工具总览
Claude Code 配置
Codex 配置
OpenCode 配置
CatPaw 配置
Cline 配置
Kilo Code 配置
Cherry Studio 配置
Chatbox 配置
CodeBuddy 配置
OpenClaw 配置
Hermes Agent 配置
CC Switch 配置
WorkBuddy 配置
DeepSeek Harness 配置
定价
LongCat-2.5
English
API开放平台 ↗
Docs
搜索文档
⌘K
简体中文
English
简体中文
API开放平台
使用指南
API 文档
工具
定价
API 概述
视觉理解
对话接口
POST
OpenAI Chat Completion API
POST
OpenAI Responses API
POST
Anthropic API
参数参考
模型参数参考
模型接口
GET
模型列表
GET
模型详情
复制
模型参数参考
​
对比 LongCat 各模型的默认参数、可调范围与使用约束。
模型能力对比
​
上下文长度为单次请求可处理的最大 Token 总量（含输入与输出）。
LongCat-2.5
上下文长度
1,048,576（1M）
max_tokens
上限
262,144（256K）
采样与生成参数
​
参数
类型
默认值
范围 / 约束
temperature
number
1.0（开启思考）
0.7（关闭思考）
固定值，传入其他值将被覆盖
top_p
number
0.95
(0, 1]
top_k
integer
-1
[-1, 100]
repetition_penalty
number
1
[1, 1.5]
thinking_budget
integer
—
最大 262,144
参数说明
​
temperature
​
采样温度，控制输出的随机性：值越高输出越随机多样，值越低输出越确定。
开启思考时固定为
1.0
，关闭思考时固定为
0.7
。传入其他值不会报错，将被覆盖为对应状态下的默认值。
top_p
​
核采样（nucleus sampling）的概率阈值：从累积概率达到阈值的最小 Token 集合中采样。值越高候选范围越大，输出越多样。
top_k
​
将采样候选限制为概率最高的 K 个 Token，值越小输出越集中。
-1
表示不启用该限制。
repetition_penalty
​
重复惩罚：降低已出现过的 Token 再次出现的概率，值越大惩罚越强。
1
表示不惩罚。
max_tokens
​
限制单次调用生成的最大 Token 数，只限制输出长度，不含输入。生成达到上限时内容会被截断，此时响应的
finish_reason
为
length
。
thinking_budget
​
思考过程的 Token 预算上限，最大
262144
。
范围校验
​
top_p
、
top_k
、
repetition_penalty
、
max_tokens
传入超出范围的值将返回
400
错误（
invalid_request_error
/
invalid_parameter
），错误信息逐条指出越界参数，例如：
json
{
"error"
: {
"message"
:
"参数校验失败:
\n
/top_p: 2 is not less or equal to 1
\n
/repetition_penalty: 3 is not less or equal to 1.5
\n
"
,
"type"
:
"invalid_request_error"
,
"code"
:
"invalid_parameter"
}
}
思考开关
​
通过
thinking
参数控制思考模式：
{"type":"enabled"}
开启思考，
{"type":"disabled"}
关闭思考。
temperature
的固定值随思考开关变化（见上文）。
上一页
Anthropic API
下一页
模型列表
本页目录
模型能力对比
采样与生成参数
参数说明
temperature
top_p
top_k
repetition_penalty
max_tokens
thinking_budget
范围校验
思考开关