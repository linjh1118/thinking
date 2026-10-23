---
title: "MiniMax M3.1 Flash — Agent 性价比、推理预算与评测边界"
type: model-note
authors: ["MiniMax"]
year: 2026
url: "https://www.minimax.io/blog/minimax-m31f"
tags: [base-model, minimax, agent-training, coding, inference-efficiency]
status: read
created: 2026-10-19
updated: 2026-10-23
---

# MiniMax M3.1 Flash：更值得研究的是每个成功任务的成本

> [!tldr] 我的判断
> M3.1 Flash 的主要价值不是“所有榜单第一”，而是把多步工具、软件开发和计算机任务推到更低成本区间。10/23 巡检新增读到官方 HF 模型卡与公开权重文件：约 428B 总参数、23B 激活，全文稀疏注意力、量化感知训练和 DSpark；这些已能替换旧笔记的架构留白。Automation 博客总表 62.2、HF 表 62.8 仍应并列，DeepSWE 73.7、ALE 29.6 不变。推理 effort、成功率、账单和工具成本一起验收，不能把 200+ TPS 当整链加速。

> [!warning] 资料充分度：训练精读未达到完整技术报告标准
> **现在已有 GA 原卡、配置、chat template、DSpark 配置和部署说明，但缺少独立 M3.1 训练报告、完整数据混合、RL recipe 和关键消融，本笔记仍达不到 GLM-5.3-Flash / Kimi-K3 完整报告精读的训练深度。** 原卡链接的 2606.13392 是《MiniMax Sparse Attention》，可以解释背景机制，不冒充 M3.1 全部后训练的独立报告。旧“无 HF 原卡、权重尚未开放”已纠正；本轮只做文本/配置归档与 HTTP HEAD 可达性核验，不下载 PDF 或权重、不执行远程代码。四张原图来自发布博客。

## 日期、Preview 与主线归属

发布正文明确标注 **2026-10-19**，宣布 M3.1 Flash 正式 rollout，并称 API、M Plan、MiniMax Code 已可用。本节点日期表示这次**正式发布阶段**，不声称它是整个 M3.1 family 首次可用的日期。

官方产品渠道在此之前已经出现 M3.1-Flash-Preview。本轮没有核实 Preview 的首次开放日，也没有证据证明 Preview 与 GA 权重完全相同，因此不把今天伪装成 Preview 首发，不把它们拆成多个正代。后续核实预览日期后应在同一 family 内补充阶段，保留本次 GA 日期。

M3.1 Flash 是 MiniMax 通用基模主线的发布阶段，不因 Flash 命名就降为专项支线。官网提到 Pro 后续推出，不代表现在已经发布，不能预建 Pro 叶子。匿名版本 Space Bunny 的“处理超过 200T tokens”描述的是运行使用量，**不是训练 token 数**。

**10/23 可见性更新，不伪造首发日：** 本次 HF 完整目录发现 `MiniMaxAI/MiniMax-M3.1-Flash`；原卡可读，仓库 API 标 `gated=false / disabled=false`，权重索引可见，代表性主权重及 draft 文件 HEAD 核验见 manifest。10/23 是本轮确认可见的日期，README 没有写出独立的权重首次开放日，因此不把仓库 createdAt/lastModified 当发布日，不在近 30 天表里再造一个 10/23 正代。维持 10/19 正式发布节点，Preview 最早日和权重实际开放日分别待核。

## 为什么不是只看一个综合分

Agent 的一次任务包含多轮生成、工具执行、文件操作、重试与验证。token 单价低并不必然让任务总成本低：更多推理 token、失败重试或昂贵工具都可能抵消优势。M3.1 Flash 的发布主张同时涉及能力、稀疏推理、吞吐与账单，应拆开核验。

10/19 博客只披露“更激进的稀疏性”；现在新增原卡和配置能明确区分三种效率机制：**注意力只读部分历史块、MoE 每 token 只激活部分专家、draft 先提议再验证 token**。它们分别影响长上下文读取、FFN 计算与解码，不能把三者的收益简单相乘，也不能把 23B 激活量当成完整模型的显存占用。

## 架构补充：本次 HF 原卡与配置能支撑的部分

| 层面 | 已读一手证据 | 解读与边界 |
|---|---|---|
| 参数/接口 | 卡写约 428B total、23B activated；文本/图像/视频输入，文本输出 | 原生多模态通用 family，不另外造视觉支线 |
| 文本主干 | 60 层、hidden 6144；64 query heads、4 KV heads、head dim 128 | 配置不等于完整训练 recipe，不能仅凭参数算术保证吞吐 |
| MoE | 128 routed experts、每 token 4 个，另 1 shared；前 3 层 `moe_layer_freq=0`，后续为 1 | **前 3 层非 MoE 不等于前 3 层非稀疏注意力**，这是两套开关 |
| 注意力 | 卡说原先前 3 层 full attention 改为 sparse；配置 60 个 `sparse_attention_freq` 均为 1 | MSA throughout 有当前配置支撑；不是从旧 Preview 猜测 |
| 稀疏索引 | topk blocks 16、block size 128、4 index heads、index dim 128，另 local block | 不把 16×128 简写为全部可见上下文上限；具体索引/局部块组合依赖实现 |
| 长上下文 | 卡写 up to 1,000,000；配置 max positions 1,048,576 | 规格/位置表上限不同口径；可用长度取决于显存、图像 tokens 与 serving |
| 视觉 | 32 层、hidden 1280、patch 14；动态分辨率与 patch merge | 配置中的 image size、grid 与视频分段值不是任意图片/视频质量保证 |
| 量化 | 主配置 `mxfp8`、activation dynamic；MoE 算法 `NVFP4`、group size 16 | 路由器、embedding、vision/projector 等有豁免列表，不能称“全模型所有张量都 FP4” |

### QAT：能力与运行时格式是两件事

新卡明确 routed MoE experts 和 attention paths 在训练中量化；配置进一步给出上述混合格式。因此已经能写“有 QAT”，但量化损失、校准数据、各模块精度消融以及不同硬件 kernel 的行为仍未披露完整。HF 表也明确按官方权重报告，不能把任意第三方量化的结果默认视为等价。

### DSpark：发布了 draft，不代表自动拿到固定加速比

卡写 DSpark 替换早期类 EAGLE 的 MTP，并随发布带 draft head。独立配置是 **5 层 draft**、block size 7、target layer IDs `[3,17,31,45,59]`、Markov rank 256；`use_mtp=false`、`num_mtp_modules=0`，与旧 MTP 方案分开。draft 的 sliding window 4096 不应误写为目标模型只有 4096 上下文。

这里的直觉是：让较小组件提出候选，再由目标模型验证。实际加速还依赖接受率、batch、长上下文、采样与兼容实现；block size 7 **不等于每次固定接受 7 token，更不是 7 倍提速**。当前没有独立 DSpark 延迟/接受率曲线，不把部署配置写成已实测性能。

部署卡推荐 SGLang、vLLM、TokenSpeed，另列 FlagOS 多芯片入口；同时注明 Transformers 等集成仍在进行。`library_name: transformers` 或配置中的版本号不能代替“标准 Transformers 已完整支持”的验证。生成配置建议 temperature 1.0 / top_p .95，chat template 接受 low/medium/high/xhigh/max；性能比较要记录实际模板与 effort。归档源码未执行，不提供未经测试的本机一键运行承诺。

模板还有可直接影响 Agent 数据构造的契约：`root` 映射到高优先级 system，而输入的 system/developer 映射到 developer；不能把别的模型的 role 规则原样套用。tool arguments 递归转为 XML，mapping 中的 None 字段被省略，**缺字段与显式 null 不总等价**。effort 优先读 `reasoning_effort`，缺失时可读 `effort`；回放轨迹还需核对 reasoning 与工具响应的序列化。它们是已读模板的格式事实，不是安全隔离或任务成功保证。

FlagOS 文档进一步说明九家芯片版本由原始 QAT NVFP4 **转换/重新量化为 W8A8**。这些是部署衍生格式，不是原始训练全部改成 W8A8，也不拆成九个新正代。文中的 T-Head TP=8 是该示例配置，不推广成所有芯片统一八卡；跨芯片吞吐、质量和 DSpark 支持仍须逐平台验证。

## 官方全表：优势、弱项与空白一起读

![官方能力总表与完整评测脚注](src/assets/official_figure_1.png)

*图 1｜MiniMax 官方原图，保留完整脚注。对照列为发布方整理，并非本次统一 harness 重跑；空白不是 0 分。文字正文 CyberGym 为约 82%，图中精确到 82.2。*

| 任务面 | Benchmark / 版本 | M3.1 Flash | 必须保留的解释 |
|---|---|---:|---|
| CoWork | Automation-Bench v1.0.6 | 博客 62.2 / HF 62.8 | 600 个公开任务；保留两份官方来源差异，不声称权重升分 |
| CoWork | BankerToolBench | 76.2 | OpenCode 1.17.18；MiniMax-M2.7 作 judge |
| CoWork | GDP.pdf AA | 20.8 | 来自 Artificial Analysis；低于图中 GPT-5.6 Sol 的 27.2 |
| CoWork | Terminal-Bench 4.0 | 38.1 | Codex 0.149.1；低于 V4.1 Flash-1017 的 42.3 |
| CoWork | LOCA-Bench 256K | 60.3 | 官方实现；不能代替所有长上下文任务 |
| Computer Use | Agents’ Last Exam | 29.6 | 官方 Overall 全集；未参加全套的模型留空 |
| Computer Use | OSWorld 2.0 | 61.7 | 推荐 0808 Full release；图中 Opus 5 为 70.6 |
| Coding | PostTrain Bench v1.1 | 39.3 | Claude Code 2.1.251、512K context |
| Coding | DeepSWE v1.1 | 73.7 | mini-SWE-agent 2.4.5、512K context；1017 对照 77.0 |
| Coding | NL2Repo-Bench | 61.2 | Claude Code 2.1.233、512K；修正两题、reward hacking 判 0 |
| Coding | SWE Refactor Bench | 23.0 | Claude Code 2.1.220、200K；Opus 5 对照 31.0 |
| Cyber | CyberGym | 82.2 | Claude Code 2.1.263、1M context；GLM-5.3 对照 84.5 |
| General | BabyVision with tools | 91.0 | Claude Code 2.1.285，图像最短边 1,500 pixels |
| General | HLE without tools | 43.4 | 仅 2,158 道 text-only 子集，不代表 HLE 全集 |
| General | CharXiv RQ | 82.5 | GPT-5.5 作 judge；并非无模型裁判的确定性指标 |

这不是“全面压倒国内外模型”：总表里 GDP.pdf、Terminal、DeepSWE、NL2Repo、SWE Refactor、CyberGym 与 HLE 都存在更高对照。Automation 的优势值得重视，但不能外推成所有业务、所有模型配置的胜出。各表未提供置信区间，本笔记不宣称小差距统计显著。

OSWorld 的脚注明确：通常取各模型发布时最高成绩，但 DS-V4.1 是内部复现；不能把所有格子写成同一实验条件重跑。ALE 只比较官方 Overall 全集，不用 CLI 子集补空格。NL2Repo 的修题会改变可比性，需要保存该修正版而不是只留一个分数。

## 三张成本图，其实对应三套口径

![官方 Automation-Bench 分数与单任务成本](src/assets/official_figure_2.png)

*图 2｜官方原图。横轴为每任务美元成本、对数刻度；公开模型数据截至 10 月 18 日，harness 为 Claude Code。DeepSeek-1017 使用特定 peak rates，其余模型按官方价格，不能外推为当前所有时段账单。*

Automation 成本图中 effort 从 low→medium→high→xhigh→max 的 M3.1 分数分别为 **52.8 /57.7 /59.2 /61.2 /62.8%**。同一模型的额外预算可以带来明显变化，但 **博客总表 62.2 与图中 max 62.8 不一致；现在 HF 总表也写 62.8**。来源未充分解释这些运行是否完全相同，不能据此宣布一次新权重带来 +0.6 提升。图内未逐点给精确美元值，不从图片坐标猜造完整费用表。

![官方 DeepSWE 分数与单任务成本](src/assets/official_figure_3.png)

*图 3｜官方原图。M3.1 high /xhigh /max 为 68.1 /72.1 /73.7%；成本单位是每任务，不是整个评测集。图脚注标公开数据截至 2026-09-22，却包含较晚命名的 1017 对照，时间标注存在疑点，不能据此认证所有对照的新鲜度。*

DeepSWE 曲线的高 effort 有收益，但发布图上 DeepSeek-1017 max 更高，不能说 M3.1 以最低成本取得绝对最高分。换算注明 **1 USD = 6.6862 CNY**，这是该图的转换条件，不是本笔记提供的实时汇率。图 1 使用的 mini-SWE-agent 2.4.5 与图 3 的来源/版本需各自追溯，不因同名 Benchmark 就假定全部条件一致。

![官方 ALE 通过率与整套成本](src/assets/official_figure_4.png)

*图 4｜官方原图。152 tasks、ALE-v1 Overall、各模型 best harness / effort。M3.1 使用 Claude Code、max effort。横轴明确是 estimated total cost：$111 是整套估算成本，不是每题 $111。*

29.6% 与 $111 一起体现成本位置，但不是最高通过率：图里 Opus 5.5 仍更高。除以 152 约为 $0.73 / task，这是按官方总价和题数计算的平均值，**不是官方逐任务收费，也不是每成功任务成本**。cost-performance frontier 虚线只表达这组选点的边界，不表示对所有任务分布存在支配关系。

## 价格与速度：token 费率不等于任务经济性

发布页给出的固定费率为每百万 tokens：未缓存输入 **$0.15**、输出 **$0.60**、缓存输入 **$0.015**。下面只是按该费率做核算，不是本次实测账单。

| 项目 | 可计算的部分 | 不能默认为已计入 |
|---|---|---|
| 模型 token 费用 | 输入、缓存输入、输出分别乘各自费率 | 搜索、工具、沙箱、失败重试和人工复核 |
| 单任务均值 | 整套美元费用 / 总任务数 | 成功任务成本、长尾任务费用 |
| 成功任务成本 | 同一冻结集总费用 / 实际成功任务数 | 不同难度集合间直接比较 |
| 输出 TPS | 官方称可达 200+、P50 稳定 170+ | TTFT、prefill、网络、工具等待、端到端耗时 |

官网另称 online inference 近 3×、Agent 总使用成本降低 70%，但未在已读正文充分展开基准 predecessor 的配置、负载分布、缓存命中率与统计协议。**这些是发布方主张，不是本次验证过的普遍收益**。不能用输出 TPS 自动推算 TTFT 降低三倍，也不能给每个业务承诺节省 70%。

## 读不到的训练部分，应明确留白

这次原卡/配置补齐了参数、专家与稀疏结构、量化配置、draft 与运行时入口，旧“没有 GA 模型卡”的判断已失效。但它们仍不足以复现训练：具体训练 tokens、数据混合、RL reward/grader、QAT/DSpark 组件消融与统一硬件吞吐协议依然缺失。卡引用 MSA 报告可以列为背景报告，不假装已经有独立 M3.1 后训练报告。

仓库使用自定义 **MiniMax Community License**，不写成 Apache/MIT 或无条件商业使用。完整条款归档于 `src/reference/LICENSE`；“权重能读”不等于无使用限制，实际使用前按具体 revision 核对条款及依赖。本轮未接受协议、申请授权或运行模型。

Preview 相关产品页说明它早已可用，但不能单凭相似名字证明 GA 与 Preview 的参数、context、默认 reasoning effort 和 SDK 字段完全一致。上线前应以当前官方 API 文档与账号实测确认 model ID、输出上限、推理字段及错误行为。这里没有执行任何登录、付费调用或推理。

## 对 Agent Training 的启发：让预算比较回到同一个实验

> [!insight] 能力—成本曲线比单个最高点更能指导训练
> 如果训练数据只奖励“最终成功”，却不惩罚重复工具调用、过长推理或无效重试，就可能只把曲线往高预算端移动。这个发布最值得转成实验的问题是：在冻结环境、相同 effort 和费用口径下，训练能否同时提高成功率并减少每成功任务成本？官方发布没有披露实现该目标的具体训练算法，不能倒推出它已经使用某种效率 RL。

可做三组对照：固定 harness 与每题预算，比较不同模型；固定模型，扫描 effort；固定权重，改变缓存与工具并发。每组都记录输入/输出与缓存 tokens、工具次数、失败重试、TTFT、端到端 P50/P95、任务成功与人工验收。金融工作流额外用确定性算式和引用核验，避免把厂商 judge 对写作风格的偏好当成真实财务正确性。

对数据构建而言，保留完整成功与失败轨迹、原始工具响应、文档版本和最终状态验证。把“花更多 token 得到的提升”与“训练得到的更好策略”分开；成本图上的不同 effort 点本身不是不同模型代际。

## 来源与关联

- [Tech Blog｜M3.1 Flash 正式发布](https://www.minimax.io/blog/minimax-m31f)：本地 `src/official_release.html` 保留原始 HTML；`src/official_release.html.txt` 为静态正文。四张图片保存在 `src/assets/`，SHA256 见 `src/retrieval_manifest.json`。
- [官方 M Plan](https://www.minimax.io/m-plan)：证明存在 Preview 产品阶段，不作为首次发布日期证据。
- 🤗 [HF Model Card｜M3.1 Flash](https://huggingface.co/MiniMaxAI/MiniMax-M3.1-Flash)：本地 `src/hf_model_card.md`；配置、DSpark、模板、许可证和芯片文档归档在 `src/reference/`。10/23 为本轮可见性确认日，非已核实首次开放日。
- 📄 [Tech Report｜MiniMax Sparse Attention](https://arxiv.org/abs/2606.13392)：原卡直接链接的 MSA 背景报告，不当作 M3.1 独立后训练报告；不下载 PDF。
- [官方 HF collections](https://huggingface.co/MiniMaxAI/collections)：本次已发现并归档当前官方原卡，不再保留“未见仓库”的旧状态。
- [[Topics/13_base_model/MiniMax/2606_MiniMax_M3/MiniMax-M3-Frontier-Coding-1M-Context-Native-Multimodality|MiniMax M3]]：前代主线，架构与训练资料独立阅读，不直接迁移到 M3.1 GA。

> 📊 相关可视化：[[Topics/13_base_model/MiniMax/261019_MiniMax_M3_1_Flash/minimax_m3_1_flash_poster_zh.html|MiniMax M3.1 Flash 中文 Poster]]
