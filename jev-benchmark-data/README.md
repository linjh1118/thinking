# Jev Benchmark Observatory

[打开看板](https://linjh1118.github.io/thinking/jev_benchmarks.html) · [Jev Atlas](https://linjh1118.github.io/thinking/jev_atlas.html)

2026-10-04 核对的公开结果快照：31 组评测来源、177 张按协议分开的结果表、1,519 条模型 / 配置记录。包含 JevBench v1.4.2.2 的全部 95 个系统（91 个官方排名），Jevals 的 3 类决策任务，以及 CSS、Nimble、中文决策、分类、检索、Judge、工作流与论文评测。

页面提供资源地图、模型覆盖矩阵、完整排行榜、指标切换、目标差距、成本 / 延迟散点图、CSV 和 JSON 导出。榜单数据仍内嵌 HTML，没有外部脚本或字体依赖；原题浏览器按需读取本站的子集 JSON，需通过 HTTP 打开。

## 数据与口径

`data.json` 是人工核对后的规范化数据源；`../jev_benchmarks.html` 内嵌同一份数据。数据来自公开评测 API、GitHub 结果文件和论文表格。本次没有运行模型推理，也没有把内部讨论、实验或私有文档发布到仓库。

- `sources`：一手来源 URL、版本、读取日期及源文件 SHA-256；网页 / 论文定位无文件哈希时明确留空。哈希标识本次读取内容，不表示上游页面今后不变。
- `catalog`：评测来源组、主题、适用范围、关联结果表和缺口。31 组来源不等于 31 个完全独立的数据集，一些来源复用了同名公开任务。
- `boards`：每张表有独立协议、版本、样本范围、指标定义、排序方向和限制说明。同名任务在不同 harness 下不合并。
- `rows`：模型原始名称、用于导航的家族、原始数值、推理条件及来源附加字段。家族归类不表示不同版本、量化或配置具有相同能力。
- `metrics`：百分数已经转换为 0–100；其余保留指标原始尺度。方向 `desc` 为越高越好，`asc` 为越低越好。`null` 是未披露，0 是真实报告的零值。

静态看板只反映已收录的来源。覆盖矩阵的空白表示本快照未收录，不代表该模型没有做过这项评测。跨榜不合成总排名；成本与延迟的硬件、估价和测量口径不同，必须结合行详情使用。部分单系统结果仅作为参考入口。

JevBench 保留上游 `official_rank` / `ranked`，4 条未排名记录不会成为可排名系统的目标。Jevals 的 `official_rank` 是原始 `rank_ub` 统计名次，不等于按点估计排序；置信区间随 Decision Score 展示。Jevals 数据署名：**Jevals / Jevals Contributors，suite 0.1.0，CC-BY-4.0**；来源见 [结果 API](https://jevals.com/api/v1/board) 和 [数据仓库](https://github.com/Jevals/jevals-data)。其余来源保留各自许可与所有权，本仓库不重新授权上游原始内容。

重点口径：

- JevBench 的 534 道历史题、308 道封存题与可下载 public231 不同；综合分是带门槛的多轴分数，不是 Accuracy。
- CSS 收录逐任务 CSV 全部 580 行；不同模型任务覆盖不齐，不人为计算共同总榜。
- 中文 v0.2 使用 378 条材料、467 个问题的新版主表，未沿用旧版 179 条的叙述。
- Jevals 的 Decision Score 允许负值。质量指标、成本和延迟均保留对应原始单位。
- 厂商工作流评测、模型作者自测及论文系统成功率单列，不冒充独立模型排行榜。
- 对齐审计、名字偏差、SimpleBench harness 和 LongSeq 仍有尚未收录数值或不适用多模型榜单的缺口，地图中明示。

## 更新

1. 读取目标来源最新的结果文件或论文表格，确认版本、样本、候选标签、推理设置与费用单位。
2. 更新 `data.json`。新增协议用独立 `board.id`，同时维护所属 `catalog.boards`；改变评测协议时不要覆盖成看似可比的旧榜。
3. 更新读取日期、来源版本和文件哈希。论文定位应保留版本与表号；缺失指标显式填 `null`。
4. 修改展示时编辑 `../scripts/jev-benchmarks/template.html`，不要手改生成的根目录 HTML。
5. 从仓库根目录构建：

```bash
python3 scripts/jev-benchmarks/build.py
python3 -m http.server 8768 --bind 127.0.0.1
```

打开 `http://127.0.0.1:8768/jev_benchmarks.html`，检查榜单切换、指标方向、覆盖跳转、导出及移动端。构建器检查唯一 ID、来源引用、指标完整性及有限数值；人工仍需核对原始数据和协议说明。推送 `master` 后由现有 GitHub Actions 发布，首页通过 HTML 的 `index:` 元数据自动收录。


## 原题浏览器 · 2026-10-07

[直接打开 Dataset Viewer](https://linjh1118.github.io/thinking/jev_benchmarks.html#questions/jevbench)

已接入61个子集、12,151条评测记录：JevBench public231、Jevals 900、Nimble 3,880、Eikos 42任务7,140。记录数不代表跨套件去重后的独立题数。其他来源明确显示“尚未接入原题”，不据此判断上游是否公开。

支持子集选择、全文字段搜索、20条分页、原题全文、折叠答案、原始JSON、单题URL和子集下载。保留原始语言，未添加自动翻译或生成示例。Jevals选项金标同时显示索引与标签名称；原始索引不变。Eikos展示公开builder的冻结转换/生成结果，排除重复JevBench副本，不能称作原始上游数据集原题。

来源：此前固定公开上游版本生成的step1_prepare_data。仅导出公开suite的原始记录，不包含训练数据、模型响应、私有题或凭据。`questions/manifest.json`记录源文件SHA-256、上游链接和Eikos数据revision。各数据保留上游许可与归属，不重新授权；Jevals / Jevals Contributors，CC-BY-4.0，底层许可见task元数据。

重建原题：`python3 scripts/jev-benchmarks/prepare_questions.py /path/to/step1_prepare_data`，再运行`build.py`。展示代码在`questions.js`，构建时嵌入页面；公开记录按子集加载，避免进入榜单就下载整套题库。
