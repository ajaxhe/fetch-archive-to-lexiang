## 3 The Benchmark / 评测集

Tencent WorkBuddy Bench is organized into four complementary subsets – Code, Web, Office, and Security – each targeting a distinct class of realistic agentic tasks while sharing a common task format and scoring philosophy. This section introduces the Code subset; the following sections cover Web, Office, and Security in turn.

Tencent WorkBuddy Bench 由四个互补的子集构成——Code、Web、Office 与 Security——各自面向一类不同的真实智能体任务，同时共享统一的任务格式与评分理念。本节先介绍 Code 子集；随后各节依次介绍 Web、Office 与 Security。

### 3.1 Code / Code 子集

The Code subset measures whether an agent can carry out a real, role-played engineering request against a full open-source repository – not a single-file toy problem, and not a bug report handed to it pre-diagnosed. The agent is dropped into a project checked out at a baseline commit, must locate the relevant code across modules, make the change, and keep the project's hidden tests green. What sets the subset apart is its role and task-type diversity: every task is voiced by one of five requester roles – developer, algorithm engineer (algo), product manager (pm), quality assurance (qa), and operations (ops) – and spans far more than bug-fix work (Table 4, Figure 2(a)).

Code 子集衡量智能体能否针对完整的开源仓库完成一条真实的、角色扮演式工程请求——而不是单文件玩具题，也不是已经预先诊断好的缺陷报告。智能体被放入一个检出到基线提交的项目中，必须跨模块定位相关代码、完成修改，并保持项目的隐藏测试全部通过。该子集的独特之处在于角色与任务类型的多样性：每道题都由五种请求者角色之一发出——developer（开发）、algorithm engineer（algo，算法工程师）、product manager（pm，产品经理）、quality assurance（qa，质量保障）与 operations（ops，运维）——并且远不止缺陷修复一类工作（表 4，图 2(a)）。

Task provenance. Each task expresses its target change as a natural-language, role-played request, so solving it requires reading and reasoning about the repository itself. Of the 80 tasks, 34 are anchored to a real upstream commit against an actual OSS snapshot (Family A); the remaining 46 have no upstream code and divide – with an approximate internal split – between clean-room reimplementations (Family B, 24 tasks, including the 4 tasks that port JavaScript/TypeScript/Rust targets into Python) and fully synthetic workspaces (Family C, 22 tasks), as summarized in Table 3. Published repository counts vary with whether clean-room and ported targets are included, so we do not report an aggregate count.

任务来源。每道题都以自然语言、角色扮演式请求来表达目标变更，因此求解必须阅读并推理仓库本身。在 80 道题中，34 道锚定到真实开源软件快照上的一次真实上游提交（Family A）；其余 46 道没有上游代码，并按大致的内部划分——净室再实现（Family B，24 道，其中包括将 JavaScript/TypeScript/Rust 目标移植为 Python 的 4 道）与完全合成的工作区（Family C，22 道），如表 3 所示。已公布的仓库数量会因是否计入净室与移植目标而变化，因此我们不报告合计数量。

Table 3. Code subset provenance families. Counts sum to the 80-task release: A = 34, B + C = 46.

表 3. Code 子集的来源族。计数合计为 80 题发布集：A = 34，B + C = 46。

| Family<br>族 | Definition<br>定义 | Count<br>数量 | Example<br>示例 |
| --- | --- | --- | --- |
| A | Real OSS snapshot at an upstream commit; the gold patch is the actual human fix<br>真实开源软件在某次上游提交处的快照；gold patch（参考补丁）即为实际的人工修复 | 34 | Django, Flask, pytest, Black, Pydantic, httpx, Celery (≈18 repositories)<br>Django、Flask、pytest、Black、Pydantic、httpx、Celery（≈18 个仓库） |
| B | Clean-room *_like reimplementation of a target library's public API, no original code copied; includes the 4 cross-language ports (JS/TS/Rust originals in Python)<br>对目标库公开 API 的净室 *_like 再实现，不复制任何原始代码；包含 4 个跨语言移植（JS/TS/Rust 原作移植为 Python） | 24 | fastapi_like/openapi.py stub rather than FastAPI itself<br>fastapi_like/openapi.py 桩实现，而非 FastAPI 本身 |
| C | Fully synthetic workspace with CSV/JSON fixtures, authored to exercise a role's workflow directly<br>完全合成的工作区，带有 CSV/JSON 夹具，直接用于演练某一角色的工作流 | 22 | algo workspaces (12) and pm data workspaces (10)<br>algo 工作区（12）与 pm 数据工作区（10） |

Scale and release. Code comprises 80 tasks. Each ships as a self-contained Harbor-style task directory – instruction.md, task.toml metadata, an environment/ Docker snapshot of the target repository, and a tests/ directory holding hidden tests plus a diagnostic gold.patch – following the task-directory format of Section 2.

规模与发布。Code 包含 80 道题。每道题都以自包含的 Harbor 风格任务目录发布——instruction.md、task.toml 元数据、目标仓库的 environment/ Docker 快照，以及存放隐藏测试与诊断用 gold.patch 的 tests/ 目录——遵循第 2 节的任务目录格式。

Oracle-gated admission. Each candidate Code task passes a two-run validation before admission. The task image is first built and its verifier is run against the unchanged baseline workspace. The task's solution/solve.sh then applies the diagnostic gold patch, after which the verifier is run again. Admission requires baseline reward \leq 0.3 and oracle reward = 1.0. This removes tasks whose initial workspace already satisfies too much of the intended contract, as well as tasks whose gold patch cannot achieve full verifier reward. The gold patch is a diagnostic reference for this validation, not the unique correct solution; any patch that satisfies the hidden tests receives the corresponding reward.

Oracle 门控准入。每道候选 Code 任务在准入前都要经过两次运行校验。首先构建任务镜像，并在未改动的基线工作区上运行其校验器。随后任务的 solution/solve.sh 应用诊断用 gold patch（参考补丁），再运行一次校验器。准入要求基线奖励分 \leq 0.3，且 oracle（参考解）奖励分 = 1.0。这会剔除初始工作区已过多满足既定契约的任务，以及 gold patch 无法拿到满分校验器奖励的任务。gold patch 只是本次校验的诊断参考，并非唯一正确答案；任何通过隐藏测试的补丁都会获得相应奖励分。

Domains and difficulty. Tasks carry one of 18 fine-grained categories, merged into six usage domains for readability (Figure 2(a)). Bug fixing accounts for only 10 of the 80 tasks; the other five domains – feature and interface work, code engineering, testing, algorithm engineering, and product/data analytics – carry the remaining 70, a deliberate expansion beyond the “fix a bug, add a feature” framing of earlier benchmarks. Difficulty comes chiefly from cross-module exploration – finding where to edit rather than how – and grows with repository size and structure as tasks

领域与难度。任务带有 18 个细分类别之一，为便于阅读合并为六个用途域（图 2(a)）。缺陷修复仅占 80 题中的 10 题；其余五个域——功能与接口工作、代码工程、测试、算法工程，以及产品/数据分析——承担剩下的 70 题，这是对早期评测集「修一个缺陷、加一个功能」框架的有意扩展。难度主要来自跨模块探索——找出该改哪里，而不是怎么改——并随着仓库规模与结构，在任务

Table 4. Code subset composition (80-task open release).

表 4. Code 子集构成（80 题开放发布集）。

| Dimension<br>维度 | Breakdown<br>构成 |
| --- | --- |
| Roles<br>角色 | developer 30 · algo 19 · pm 15 · ops 10 · qa 6<br>开发 30 · 算法 19 · 产品 15 · 运维 10 · 质保 6 |
| Difficulty (editorial)<br>难度（编审标定） | easy 7 · medium 31 · hard 42<br>易 7 · 中 31 · 难 42 |
| Difficulty (L-ladder)<br>难度（L 阶梯） | L2 4 · L3 27 · L4 40 · L5 9 (centered on L4)<br>L2 4 · L3 27 · L4 40 · L5 9（以 L4 为中心） |
| Admission gate<br>准入门控 | baseline ≤ 0.3, oracle (gold patch) = 1.0 against hidden tests<br>基线 ≤ 0.3，oracle（gold patch）对照隐藏测试 = 1.0 |

climb the L-ladder, a repository-complexity scale running from L2 (small, few modules) to L5 (large multi-module codebases). Table 4 gives the role and difficulty distributions.

沿 L 阶梯攀升而增加，该阶梯是从 L2（小型、模块很少）到 L5（大型多模块代码库）的仓库复杂度量表。表 4 给出了角色与难度分布。

Figure 2. Code and Web task composition. (a) Six Code usage domains merged from 18 fine-grained categories; bug fixing accounts for 10 of 80 tasks. (b) Seven Web task categories. (c) Six Web lifecycle modes; From Scratch accounts for 35 of 70 tasks.

图 2. Code 与 Web 任务构成。(a) 由 18 个细分类别合并而成的六个 Code 用途域；缺陷修复占 80 题中的 10 题。(b) 七个 Web 任务类别。(c) 六种 Web 生命周期模式；From Scratch 占 70 题中的 35 题。

![Figure 2](images/fig02.png)

Early evaluation runs during construction showed what failure looks like at repository scale: the dominant zero-score modes were agents looping on test-file edits until timeout, and agents losing their way in a large codebase and editing entirely the wrong files – evidence that difficulty comes from navigation and grounding rather than code synthesis.

构建期间的早期评测运行揭示了仓库规模下的失败形态：占主导的零分模式是智能体反复改测试文件直到超时，以及智能体在大型代码库中迷失方向、改到完全错误的文件——这表明难度来自导航与定位，而非代码生成。

A representative role-played request (product manager, product-analytics, signup_funnel, hard): / 一条代表性的角色扮演式请求（product manager、product-analytics、signup_funnel、hard）：

"The checkout-copy experiment finished; I want to know first whether the new version is better. The data has impression and purchase events – please compute per-group conversion, revenue, and a simple conclusion, and don't count purchases that happen long afterward."

「结账文案实验已经结束；我首先想知道新版本是否更好。数据里有曝光和购买事件——请计算各组转化率、收入，并给出一个简单结论，且不要计入很久之后才发生的购买。」

The request states an intent and a constraint, not an implementation plan: it names neither the relevant file, the expected schema, nor how the attribution window for excluding late purchases should be drawn, leaving the agent to recover that context from the repository itself.

该请求陈述的是意图与约束，而不是实现方案：它既没有点名相关文件、预期模式，也没有说明排除延迟购买的归因窗口应如何划定，而是把这些上下文留给智能体从仓库中自行还原。

Scoring. Each task is scored by a per-task verifier run inside its Docker image after the agent's patch is applied; the headline Code metric is the run-level score, the per-run average of per-task hidden-test scores. Section 4 gives the three verifier forms, gold-patch handling, and the reference readings in full. Figure 3 summarizes this task and evaluation workflow.

评分。每道题在智能体补丁应用后，由任务专属校验器在其 Docker 镜像内运行打分；Code 的主指标是运行级分数，即单次运行中各题隐藏测试分数的平均值。第 4 节完整给出三种校验器形态、gold patch 的处理方式以及参考读数。图 3 概括了该任务与评测工作流。

Figure 3. Code task and evaluation workflow. The coding agent reads a natural-language request, explores the repository, and emits a patch (left); the patch is graded by hidden unit tests and, as a diagnostic reference, by a rubric-weighted LLM judge (center). The headline Code metric is the hidden-test score; the LLM-judge reading and its blend are reported as reference values only and never enter the headline metric (right).

图 3. Code 任务与评测工作流。编程智能体阅读自然语言请求、探索仓库并输出补丁（左）；补丁由隐藏单元测试评分，并作为诊断参考由按评分细则加权的 LLM 评判打分（中）。Code 主指标是隐藏测试分数；LLM 评判读数及其混合值仅作为参考值报告，从不进入主指标（右）。

![Figure 3](images/fig03.png)

### 3.2 Web / Web 子集

The Web subset tests whether a model can deliver a runnable, checkable front-end artifact – not simply emit plausible-looking HTML in a chat turn. Every task carries an artifact-not-chat contract: the agent must produce a runnable artifact at a declared output path (for example, an HTML entry point); a well-written answer with no artifact at that path fails regardless of content. Across its 70 tasks, coverage spans front-end artifact generation, modification, analysis, and quality assurance in one task space: page implementation, page interaction, data visualization, visual design, analytical reporting, code testing, and document conversion.

Web 子集检验模型能否交付可运行、可核验的前端产物——而不是在一轮对话中只生成看起来像样的 HTML。每道题都带有「产物而非对话」契约：智能体必须在声明的输出路径（例如 HTML 入口）生成可运行产物；若该路径没有产物，即使文字回答写得再好也判定失败。在全部 70 道题中，覆盖范围把前端产物的生成、修改、分析与质量保障放在同一任务空间：页面实现、页面交互、数据可视化、视觉设计、分析报告、代码测试与文档转换。

Tasks are organized into seven categories (Figure 2(b)): page interaction (21 tasks) and data visualization (15) dominate, together accounting for 36 of the 70 tasks, while the remainder covers visual design, front-end project analysis, code testing, page implementation, and document conversion – work that traditional front-end generation benchmarks rarely exercise.

任务被组织为七个类别（图 2(b)）：页面交互（21 道）与数据可视化（15 道）占主导，合计占 70 题中的 36 题，其余覆盖视觉设计、前端项目分析、代码测试、页面实现与文档转换——这些工作是传统前端生成评测集很少练到的。

Orthogonally, each task is authored to exercise one point in the web-development lifecycle (Figure 2(c)). From Scratch alone would only probe generation ability, so half the suite instead requires fixing front-end state, runtime, or visual defects, extending an existing page or application, reviewing Web project evidence, generating regression tests, or converting source material into a front-end-facing deliverable – so that models which can only create, and not maintain, are not rewarded disproportionately. In panel (c), From Scratch holds exactly half the suite (35 of 70 tasks), with the other half split across bug fix (8), feature extension (8), review & analysis (7), test generation (7), and format conversion (5).

与此正交，每道题都被编写为演练 Web 开发生命周期中的一个节点（图 2(c)）。若只有 From Scratch，就只会探测生成能力，因此套件中有一半转而要求修复前端状态、运行时或视觉缺陷，扩展已有页面或应用，审阅 Web 项目证据，生成回归测试，或将源材料转换成面向前端的交付物——以免只会创建、不会维护的模型获得不成比例的奖励。在面板 (c) 中，From Scratch 恰好占套件的一半（70 题中的 35 题），另一半分布在缺陷修复（8）、功能扩展（8）、审阅与分析（7）、测试生成（7）与格式转换（5）。

A third axis tracks interaction and state complexity. Twenty-five tasks are noninteractive front-end project artifacts, while 45 require interaction or state: single-flow state changes (15), persistence, offline, or cross-state behavior (13), multi-step workflows (9), and light interaction (8). This axis keeps the subset from collapsing into static page generation: many tasks require the artifact's state to change, recover, or stay consistent under user actions.

第三条轴跟踪交互与状态复杂度。25 道题是非交互的前端项目产物，另有 45 道要求交互或状态：单流程状态变化（15）、持久化、离线或跨状态行为（13）、多步工作流（9）以及轻度交互（8）。这条轴避免子集坍缩为静态页面生成：许多任务要求产物的状态在用户操作下发生变化、恢复或保持一致。

Figure 4. Web task and evaluation workflow, from query and agent rollout to the delivered artifact (left), through rule, LLM/VLM, and agent judges over extracted evidence (center), to rubric-item checklist scoring (right), combining deterministic checks, semantic and visual judgment, and live interaction over the delivered artifact.

图 4. Web 任务与评测工作流：从查询与智能体 rollout 到已交付产物（左），经规则、LLM/VLM 与智能体评判对抽取证据打分（中），再到评分细则条目清单打分（右），将确定性检查、语义与视觉判断以及对已交付产物的实时交互结合起来。

![Figure 4](images/fig04.png)

A representative request from the page-interaction category (mobile store booking): / 一条来自页面交互类别的代表性请求（移动店铺预约）：

"I want a mobile store-booking page: users pick a service and a time slot, fill in contact details, and confirm. Full slots must not be selectable, and there should be a review step before submitting."

「我要一个移动端店铺预约页：用户选择服务和时间段，填写联系方式并确认。已满的时段不能被选中，提交前还应有确认步骤。」

The ask names an intent and a couple of constraints – slot capacity, a review step before submission – not a full specification, leaving the agent to produce a runnable artifact that a rubric can verify against the requested behavior.

该请求点明了一个意图和若干约束——时段容量、提交前的确认步骤——而不是完整规格，把生成可运行产物、并让评分细则按所请求行为核验的工作留给智能体。

Figure 4 summarizes this artifact-centered workflow, from query interpretation and agent rollout to evidence extraction, complementary judges, and checklist scoring.

图 4 概括了这一以产物为中心的工作流，从查询解释与智能体 rollout，到证据抽取、互补评判与清单打分。

Scoring uses rubric items judged by rule checks, LLM/VLM judges, and an agent-judge. Rule checks cover deterministic delivery constraints such as files, formats, prechecks, and executable tests; LLM/VLM judges review textual, structured, DOM, screenshot, and visual evidence; and the agent-judge drives the running artifact to inspect workflows, state changes, and persistence. A run must still deliver the declared artifact at the declared output path, and tasks run with no access to the live internet, external accounts, keys, or live data. Section 4 gives the item counts, aggregation rule, and model-judge risk in full.

评分使用由规则检查、LLM/VLM 评判与 agent-judge（智能体校验器）判定的评分细则条目。规则检查覆盖确定性交付约束，例如文件、格式、预检查与可执行测试；LLM/VLM 评判审阅文本、结构化、DOM、截图与视觉证据；agent-judge 驱动正在运行的产物，以检查工作流、状态变化与持久化。一次运行仍必须在声明的输出路径交付声明的产物，且任务运行时不能访问实时互联网、外部账号、密钥或实时数据。第 4 节完整给出条目数量、聚合规则以及模型评判风险。

### 3.3 Office / Office 子集

Figure 5. Composition of the 50-task Office release by construction route and calibrated difficulty.

图 5. 50 题 Office 发布集按构建路径与标定难度的构成。

![Figure 5](images/fig05.png)

The Office subset tests whether an agent can complete a natural-language work request in a local workspace containing mixed-format files. Inputs include spreadsheets, documents, PDFs, JSON exports, Markdown notes, and file trees; outputs include updated workbooks, reports, structured records, state files, and handoff material. The agent must produce the requested deliverables, keep information consistent across files, update related state, preserve evidence for review, and respect task-specific execution constraints. Evaluation examines the final workspace, which catches failures that a text-answer score misses, such as writing a plausible summary without updating the workbook it describes or creating a file while leaving dependent state inconsistent.

Office 子集检验智能体能否在含有混合格式文件的本地工作区中完成一条自然语言工作请求。输入包括电子表格、文档、PDF、JSON 导出、Markdown 笔记与文件树；输出包括更新后的工作簿、报告、结构化记录、状态文件与交接材料。智能体必须产出所请求的交付物，保持跨文件信息一致，更新相关状态，保留可供审阅的证据，并遵守任务特定的执行约束。评测检查最终工作区，从而抓住纯文本答案分数会漏掉的失败，例如写出一篇像样的摘要却不更新它所描述的工作簿，或创建了文件却让依赖状态不一致。

Scale and coverage. Figures 5 and 6 summarize the Office release. The first separates construction route and calibrated difficulty; the second places task type, scenario, output family, and evaluation mechanism in one aligned row. The open release contains 50 tasks built through two routes: 30 tasks reconstructed from task specifications and target capabilities, and 20 tasks expanded from abstracted office workflows. Both routes produce the same release package and follow the same verification protocol. At the broad task-family level used in this coverage view, the release contains 24 data, spreadsheet, or structured-processing tasks; 17 document, report, or presentation tasks; and 9 workspace-automation or stateful-workflow tasks. The figure also groups tasks into six office scenarios: data and finance analysis (16 tasks), documents and presentation material (11), reconciliation and back-office operations (8), engineering and tool workflows (5), stateful workflows (5), and compliance and evidence organization (5). These groups describe benchmark coverage rather than estimate production request traffic.

规模与覆盖。图 5 与图 6 概括了 Office 发布集。前者区分构建路径与标定难度；后者把任务类型、场景、输出族与评测机制放在同一对齐行中。开放发布集包含经两条路径构建的 50 道题：30 道由任务规格与目标能力重建，20 道由抽象办公工作流扩展。两条路径产出相同的发布包，并遵循同一核验协议。在本覆盖视图所用的粗粒度任务族层面，发布集包含 24 道数据、电子表格或结构化处理任务；17 道文档、报告或演示任务；以及 9 道工作区自动化或有状态工作流任务。该图还将任务归入六个办公场景：数据与财务分析（16 道）、文档与演示材料（11）、对账与后台运营（8）、工程与工具工作流（5）、有状态工作流（5），以及合规与证据整理（5）。这些分组描述的是评测集覆盖，而不是对生产请求流量的估计。

Difficulty is reported in three calibrated tiers: 13 easy, 24 medium, and 13 hard tasks. Output families use multi-label counts: 24 tasks produce spreadsheets, 20 Markdown, 15 JSON, 6 plain text, and 5 workspace or state outputs, with smaller coverage of presentation, CSV, manifest, filesystem, and audit-log deliverables. The release is text-first: its core tasks and evaluation do not require OCR, a vision-language model, or pixel-level layout judgment.

难度按三个标定档报告：13 道 easy、24 道 medium、13 道 hard。输出族使用多标签计数：24 道产出电子表格，20 道 Markdown，15 道 JSON，6 道纯文本，5 道工作区或状态输出，并对演示文稿、CSV、清单、文件系统与审计日志类交付物有较小覆盖。该发布集以文本为先：其核心任务与评测不要求 OCR、视觉语言模型或像素级版式判断。

Construction and difficulty. Each task starts from a target capability or workflow. We then build the agent-visible workspace and separate evaluation assets, test the evaluator on saved submissions, calibrate difficulty, and run release checks. During execution, the agent sees only the request and declared inputs; reference answers, expected state, rule checks, semantic rubrics, and evaluation support files are used only after the agent finishes. Before release, saved-submission replays check that the evaluator covers the objective requirements, provides enough evidence for the semantic rubrics, and does not penalize valid high-quality outputs.

构建与难度。每道题都从一项目标能力或工作流出发。随后我们构建智能体可见的工作区与单独的评测资产，在已保存的提交上测试评测器，标定难度，并运行发布检查。执行期间，智能体只能看到请求与声明的输入；参考答案、期望状态、规则检查、语义评分细则与评测支持文件仅在智能体完成后使用。发布前，对已保存提交的回放会检查评测器是否覆盖客观要求、是否为语义评分细则提供足够证据，以及是否不会惩罚有效的高质量输出。

Figure 6. Office coverage across task type, diagnostic scenario, output family, and evaluation mechanism, arranged as a single row of four bar charts. Output families and mechanisms use multi-label counts; scenario groups describe benchmark coverage and are not estimates of production request traffic.

图 6. Office 在任务类型、诊断场景、输出族与评测机制上的覆盖，排列为单行四张柱状图。输出族与机制使用多标签计数；场景分组描述评测集覆盖，而不是对生产请求流量的估计。

![Figure 6](images/fig06.png)

Difficulty comes from the solution path rather than file count alone. Common requirements include cross-file key matching and alias resolution, temporal or state dependencies, rule priority, conflicting or missing evidence, and consistency across multiple deliverables. A hard task may require an agent to reconcile several sources, preserve unresolved conflicts, update both a primary deliverable and a state record, and avoid prohibited side effects. These requirements help distinguish model capabilities without depending on live services or undisclosed accounts.

难度来自求解路径，而不仅仅是文件数量。常见要求包括跨文件键匹配与别名解析、时间或状态依赖、规则优先级、冲突或缺失的证据，以及多个交付物之间的一致性。一道 hard 任务可能要求智能体调和多个来源、保留尚未解决的冲突、同时更新主交付物与状态记录，并避免被禁止的副作用。这些要求有助于在不依赖实时服务或未公开账号的情况下区分模型能力。

A representative task, hospital_bed_utilization, provides a ward configuration table, an admission log, and a bed-status policy table. The agent must compute monthly utilization by ward and bed type and write a two-sheet workbook containing utilization detail and ward-level summaries. A plausible-looking percentage is insufficient: the submission must resolve keys across sources, normalize dates, apply the correct reporting period and policy denominator, preserve the requested schema, and keep detail and summary sheets mutually consistent. The task therefore tests the reliability of a complete file workflow rather than a single calculation.

一道代表性任务 hospital_bed_utilization 提供病房配置表、入院日志与床位状态策略表。智能体必须按病房与床位类型计算月度利用率，并写出包含利用率明细与病房级汇总的两表工作簿。一个看起来像样的百分比是不够的：提交必须跨来源解析键、规范化日期、应用正确的报告期与策略分母、保持所请求的模式，并使明细表与汇总表相互一致。因此该任务检验的是完整文件工作流的可靠性，而不是单次计算。

Scoring. Every Office task uses two scoring components: deterministic rule checks and an evidence-grounded LLM Judge. Rule checks are binary tests of objective requirements that can be evaluated exactly, such as required files, schemas, values, source relations, state transitions, side effects, and execution constraints. Each semantic rubric defines one binary quality condition that the Judge evaluates from fixed evidence generated after the task ends, including submitted deliverables and task-specific state or source summaries. The Judge does not inspect a live workspace or alter recorded rule-check outcomes. All 50 tasks use both components. For selected tasks, state differences (10 tasks), controlled environments (6), execution traces (5), or runtime boundaries (3) provide evidence for rule checks or semantic rubrics; they are not additional scoring channels. Section 4 defines how each task combines Rule and Judge scores, how trials are aggregated, and how unavailable Judge results are handled. Figure 7 summarizes the evaluation flow.

评分。每道 Office 任务使用两个评分分量：确定性规则检查与基于证据的 LLM Judge。规则检查是可精确评测的客观要求二元测试，例如必需文件、模式、取值、来源关系、状态转移、副作用与执行约束。每条语义评分细则定义一个二元质量条件，由 Judge 根据任务结束后生成的固定证据来判定，包括已提交的交付物以及任务特定的状态或来源摘要。Judge 不会检查实时工作区，也不会改写已记录的规则检查结果。全部 50 道题都使用这两个分量。对部分任务而言，状态差异（10 道）、受控环境（6）、执行轨迹（5）或运行时边界（3）为规则检查或语义评分细则提供证据；它们不是额外的评分通道。第 4 节定义每道题如何组合 Rule 与 Judge 分数、如何聚合多次试验，以及如何处理不可用的 Judge 结果。图 7 概括了评测流程。

### 3.4 Security / Security 子集

Figure 7. Office task, evaluation, and scoring flow. The agent acts on the workspace and leaves a final state (left); deterministic rule checks evaluate the verifiable workspace state while the LLM Judge evaluates only fixed post-task evidence (center); each task combines the two scores with its own weight, trials are averaged within each task, and task scores are macro-averaged with equal weight (right).

图 7. Office 任务、评测与评分流程。智能体对工作区采取行动并留下最终状态（左）；确定性规则检查评测可核验的工作区状态，而 LLM Judge 只评测任务结束后的固定证据（中）；每道题按各自权重组合这两个分数，题内对多次试验取平均，再对各题分数等权宏平均（右）。

![Figure 7](images/fig07.png)

The Security subset covers the security-team spectrum – red-team discovery and safe exploitation, malware analysis, security operations, and agent-security assessment – asking a sharper question than the bug-fix tasks in Code: can an agent locate a real vulnerability and safely reproduce it in a sandboxed environment the way a security researcher does, analyze a malware artifact or triage an alert stream the way a malware analyst or SOC operator does, and probe a tool-using agent the way an AI red-teamer does. Given a task, the agent must earn each step in turn, with no defect location or expected behavior handed to it up front, and every task runs inside a sandboxed evaluation environment. What distinguishes the subset from the rest of the suite is that it carries no LLM judge anywhere: every task ships a deterministic scoring program that turns agent output directly into a numeric reward, backed by a five-layer anti-cheat infrastructure that closes off hardcoding and enumeration.

Security 子集覆盖安全团队的工作谱系——红队发现与安全利用、恶意软件分析、安全运营，以及智能体安全评估——并提出一个比 Code 中缺陷修复任务更尖锐的问题：智能体能否像安全研究员那样在沙箱环境中定位真实漏洞并安全地复现，像恶意软件分析师或 SOC 运营人员那样分析恶意软件产物或分诊告警流，并像 AI 红队成员那样探测使用工具的智能体。给定一道题，智能体必须逐步挣得每一步，事先不会被告知缺陷位置或期望行为，且每道题都在沙箱评测环境中运行。该子集有别于套件其余部分的一点是：任何地方都不使用 LLM judge；每道题都带有确定性评分程序，把智能体输出直接变成数值奖励，并由五层反作弊基础设施堵住硬编码与枚举。

The Security subset comprises 60 tasks, spanning six fine-grained domains rolled up into four blocks across both red-team and blue-team disciplines (Table 5, Figure 8). Grouped by discipline the suite is red-team-heavy – 38 tasks against 22 blue-team tasks – but still exercises the full defend/detect loop, and difficulty skews hard by design, reflecting the balance of real security work, where difficult cases outnumber easy ones.

Security 子集包含 60 道题，覆盖六个细粒度域，并汇总为横跨红队与蓝队学科的四个区块（表 5，图 8）。按学科分组，该套件偏红队——38 道对 22 道蓝队任务——但仍演练完整的防御/检测闭环，且难度按设计偏向 hard，以反映真实安全工作的平衡：难例多于易例。

Every task's deterministic scorer executes inside an isolated Docker container and writes a numeric reward directly, so the same output re-scored twice returns the same number (Figure 8, right). Section 4 gives the per-scorer definitions – PoC and flag verification, IOC matching, YARA match rate under a zero-false-positive constraint, and macro-F1/Kendall-tau report scoring.

每道题的确定性评分器都在隔离的 Docker 容器内执行，并直接写出数值奖励，因此同一输出评分两次会得到同一个数（图 8，右）。第 4 节给出各评分器定义——PoC 与 flag 核验、IOC 匹配、零误报约束下的 YARA 匹配率，以及 macro-F1/Kendall-tau 报告评分。

Table 5. The Security subset's composition, shown at four-block granularity (60 tasks). The vulnerability discovery & exploitation block subdivides into whitebox source audit, blackbox binary exploitation, and web exploitation, giving the six fine-grained domains referenced in the text.

表 5. Security 子集的构成，按四区块粒度展示（60 道题）。漏洞发现与利用区块再分为白盒源码审计、黑盒二进制利用与 Web 利用，从而得到正文所述的六个细粒度域。

| Block<br>区块 | Role<br>角色 | Tasks<br>题数 | Discipline<br>阵营 |
| --- | --- | --- | --- |
| Vulnerability discovery & exploitation<br>漏洞发现与利用 | Security researcher<br>安全研究员 | 32 | Red<br>红队 |
| Malware analysis<br>恶意软件分析 | Anti-virus engineer<br>反病毒工程师 | 14 | Blue<br>蓝队 |
| Security operations<br>安全运营 | SOC analyst / detection eng.<br>SOC 分析师 / 检测工程师 | 8 | Blue<br>蓝队 |
| Agent security<br>智能体安全 | AI red-team<br>AI 红队 | 6 | Red<br>红队 |

Difficulty skews hard by design.

难度按设计偏向 hard。

The discovery & exploitation block spans whitebox source-audit, blackbox binary-exploitation, and web-exploitation tasks. The whitebox audits reproduce real, historical CVEs in widely deployed upstream projects – binutils, curl, nginx, vim, jq, and fluent-bit – under a two-step find-vuln → poc-verify structure in which the second step is gated on clearing the first. In a representative task of this kind, e.g. one targeting binutils, step one gives the agent only the source tree and asks it to read the parser, trace the data flow, and locate the vulnerable code path, scored against a threshold before the environment unlocks step two; only then can the agent submit a proof-of-concept input, which passes only if it reproducibly triggers an ASAN crash inside the sandboxed container – a pacing meant to mirror a real audit-then-exploit engagement rather than hand over the defect's location up front. The web-exploitation cases are built around specific, named techniques (e.g., House of Apple2 and ECDSA nonce reuse) rather than generic vulnerability classes. The six agent-security tasks probe attack surfaces specific to tool-using AI agents – agent-to-agent prompt injection, ReAct chain hijacking, multimodal prompt-chain injection, tool-schema confusion, data exfiltration via a summarization tool, and delayed-trigger attacks – and each requires the agent to return a structured findings report with a CVSS severity rating, mirroring the deliverable a security team would expect from a pre-launch agent security review.

发现与利用区块涵盖白盒源码审计、黑盒二进制利用与 Web 利用任务。白盒审计在广泛部署的上游项目——binutils、curl、nginx、vim、jq 与 fluent-bit——中复现真实的历史 CVE，采用两步 find-vuln → poc-verify 结构，第二步须通过第一步才能解锁。在这类代表性任务中，例如针对 binutils 的一题，第一步只给智能体源码树，要求它阅读解析器、追踪数据流并定位脆弱代码路径，对照阈值打分后环境才解锁第二步；此后智能体才能提交概念验证输入，且仅当它在沙箱容器内可复现地触发 ASAN 崩溃才算通过——这种节奏意在镜像真实的「先审计再利用」交锋，而不是事先交出缺陷位置。Web 利用案例围绕具体的、具名的技术构建（例如 House of Apple2 与 ECDSA nonce 重用），而不是泛化的漏洞类别。六道智能体安全任务探测使用工具的 AI 智能体特有的攻击面——智能体间提示注入、ReAct 链劫持、多模态提示链注入、工具 schema 混淆、经由摘要工具的数据外泄，以及延迟触发攻击——每道都要求智能体返回带有 CVSS 严重性评级的结构化发现报告，以镜像安全团队在上线前智能体安全评审中期望的交付物。

Figure 8. WorkBuddy Bench Security overview. Tasks are built from real, historical vulnerabilities and authored scenarios into reproducible, self-contained cases (left); they span six red- and blue-team task types – whitebox source audit, blackbox binary exploitation, web exploitation, agent security, malware analysis, and security operations – across 38 red-team and 22 blue-team tasks (center); and each is scored by a per-task deterministic program inside an isolated Docker container that emits a numeric reward (right).

图 8. WorkBuddy Bench Security 概览。任务由真实历史漏洞与编写场景构建为可复现、自包含的案例（左）；它们覆盖六类红队与蓝队任务类型——白盒源码审计、黑盒二进制利用、Web 利用、智能体安全、恶意软件分析与安全运营——共计 38 道红队与 22 道蓝队任务（中）；每道题由隔离 Docker 容器内的任务专属确定性程序评分，并输出数值奖励（右）。

![Figure 8](images/fig08.png)

**Anti-cheat.** To keep scores meaningful under fully automated, non-judge verification, every task sits behind a five-layer anti-cheat infrastructure that closes off hardcoding and enumeration along the input, code, and output axes:

**反作弊。** 为了在全自动、无评判的核验下让分数有意义，每道题都置于五层反作弊基础设施之后，沿输入、代码与输出三个轴堵住硬编码与枚举：

- *Banned-literal scanning* against hardcoded answers. / *Banned-literal scanning*（禁用字面量扫描），用于拦截硬编码答案。
- *Renamed-input tests* that check whether an extractor parses structure rather than keying off a filename. / *Renamed-input tests*（重命名输入测试），检查抽取器是否解析结构，而不是按文件名取键。
- *Overlay/tamper tests* against trailing-data manipulation. / *Overlay/tamper tests*（叠加/篡改测试），用于拦截对尾部数据的操纵。
- *Encoding-dependence tests* that require detection rules to anchor on bytes rather than plaintext. / *Encoding-dependence tests*（编码依赖测试），要求检测规则锚定字节而非明文。
- *Low-weight decoy fields* that suppress reward from blind enumeration. / *Low-weight decoy fields*（低权重诱饵字段），抑制盲目枚举带来的奖励。

Like the other subsets, Security is scored under both the CodeBuddy Code and Claude Code harnesses in think mode, averaged over three runs; results appear in Section 5.

与其他子集一样，Security 在 CodeBuddy Code 与 Claude Code 两套 harness 的 think 模式下评分，对三次运行取平均；结果见第 5 节。
