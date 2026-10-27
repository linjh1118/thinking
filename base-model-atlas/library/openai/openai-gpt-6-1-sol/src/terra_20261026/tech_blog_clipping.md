# GPT-6.1 Terra — 官方网页阅读记录

原文：https://openai.com/zh-Hans-CN/index/introducing-gpt-6-1-terra/

2026-10-27 在浏览器实际打开并完整阅读 main 正文。此文件是转述的阅读记录，不是原始 HTML 或逐字全文镜像。英文及中文普通 HTTP 抓取均返回 403；本轮失败记录保留。完整 System Card HTML 另存于 system_card.html；31 张系统卡官方图保存于上层 src/assets。

## 核对到的发布信息

- Terra 主打视觉、计算机操作、自然写作与高频专业任务，较 5.6 Terra 提升；与 6.1 Sol 组成同一代际的不同预算点。
- Agents’ Last Exam v1：medium 较 5.6 Terra 高15个百分点、任务成本约三分之一；max 相较 Opus5.5 的任务费用优势为官方评测估计，不能推广所有任务。
- MMMU-Pro 和 OSWorld2.1 显示较旧Terra提升，但没有在此文件从动态图猜具体未抄录分数。
- 困难事实提示 low 错误率53.6%→16.7%，max4.3%；这不是普通生产流量错误率。
- Terminal-Bench4.0 max50.3%，旧Terra21.5%；复杂代码任务官方仍推荐Sol/Astra。
- API ID gpt-6.1-terra；标准每百万tokens输入$1、缓存输入$0.05、输出$5。
- 文章说发布即覆盖Plus/Pro/Enterprise/Edu的Work/Codex与API。首发日期由官方news及SystemCard的10月26日交叉确定，而不是抓取日期。
- 训练架构与完整配方未披露；安全细节以独立SystemCard正文为准。

这是一份来源阅读痕迹；详细解释、反例和研究判断在模型根目录GPT-6.1-Sol.md中。
