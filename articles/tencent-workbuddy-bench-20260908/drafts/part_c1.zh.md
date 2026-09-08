## 4 Evaluation Harness and Scoring / 评测框架与计分

A benchmark's numbers are only as trustworthy as the machinery that produces them. Tencent WorkBuddy Bench treats that machinery as a first-class contribution rather than an implementation detail: every task, regardless of track, ships as a self-contained task directory and is executed inside a sandboxed container under one shared harness, and the benchmark is released fully open – task directories, environment images, evaluation code, grading tests, and reference/gold solutions are all public. An external party needs no special access to the benchmark's internal infrastructure and no bespoke evaluation path per subset: a score can be reproduced, and any individual task re-run and audited directly, from the public release alone. This section describes that harness, how agents connect to models under evaluation, and the scoring rule applied per track; the per-subset sections above defer their scoring detail here.

基准的数字只有在产生它们的机制可信时才可信。Tencent WorkBuddy Bench 把这套机制视为一等贡献，而非实现细节：无论属于哪条赛道，每个任务都以自包含的任务目录交付，并在统一评测框架下于沙箱容器中执行；该基准完全开放发布——任务目录、环境镜像、评测代码、评分测试以及参考/金牌解答全部公开。外部方无需对基准内部基础设施的特殊访问，也无需为各子集定制评测路径：仅凭公开发布即可复现分数，并直接重跑、审计任一任务。本节描述该评测框架、智能体如何连接被评模型，以及各赛道的计分规则；上文各子集章节将计分细节推迟到此处。

Sandboxed execution and model connectivity. Each trial runs a task's environment inside an isolated container; the agent sees only the task's declared workspace, and task-specific evaluation assets are introduced into the sandbox or invoked by the evaluation pipeline only after the agent has finished acting, so grading never leaks into the agent's context. Model and sandbox concerns are kept deliberately separate: the harness can reach a model backend either directly or through a local proxy that performs protocol translation, model-name rewriting, and request logging, and it can execute the sandbox either on a local machine or on a remote, isolated sandbox backend. When the sandbox runs remotely, no benchmark-side proxy is ever placed inside it – any protocol handling that would otherwise be the proxy's job is left to the model service itself – and the one combination of sandbox backend and connection mode that cannot satisfy this separation is disabled outright rather than silently falling back to another path. One access asymmetry is disclosed for completeness: the HY (Hunyuan) endpoint used in this evaluation is served first-party by its provider, whereas all other models are accessed through third-party serving endpoints; third-party parameter configuration and request handling may affect metrics.

沙箱执行与模型连通。每次试次在隔离容器中运行任务环境；智能体只能看到任务声明的工作区，任务特定的评测资产仅在智能体完成行动之后才被引入沙箱或由评测流水线调用，因此评分不会泄漏到智能体的上下文中。模型侧与沙箱侧被刻意分开处理：评测框架既可直接访问模型后端，也可通过执行协议转换、模型名改写和请求日志的本地代理访问，并且沙箱既可在本机执行，也可在远程隔离的沙箱后端执行。当沙箱远程运行时，基准侧代理从不被放入沙箱——原本由代理承担的协议处理交由模型服务本身完成——无法满足这一分离的沙箱后端与连接模式组合会被直接禁用，而不是静默回退到另一路径。为完整起见披露一处访问不对称：本次评测所用的 HY（混元）端点由其提供商第一方服务，而所有其他模型均通过第三方服务端点访问；第三方的参数配置与请求处理可能影响指标。

Harness backends. The default execution harness is CodeBuddy Code; Claude Code, which speaks the Anthropic protocol directly, is supported as an alternative wherever a model's own protocol makes that route available. All four tracks are run and reported under both harnesses side by side (dual-harness reporting), since relative rankings can shift between the two – a model that leads under one harness need not lead under the other (Section 5). Reasoning mode (think vs. nothink) is one further configuration axis the harness records per model, alongside the sampling hyperparameters described below; the leaderboard in Section 5 reports the think-mode configuration throughout. Across both harnesses the protocol fixes reasoning effort to high, unifies the context window at 200k tokens with a common auto-compaction threshold, and disables the WebSearch and AskUserQuestion tools; each model otherwise runs with its provider-default inference hyperparameters, as recorded below. Reported results are tied to the specific builds of the two harnesses used in this evaluation, and metrics may shift as harness versions evolve.

评测框架后端。默认执行评测框架是 CodeBuddy Code；直接使用 Anthropic 协议的 Claude Code，在模型自身协议允许该路径时作为替代方案得到支持。全部四条赛道均在两种评测框架下并排运行并报告（双评测框架报告），因为相对排名可能在两者之间变化——在一种评测框架下领先的模型不必在另一种下领先（第 5 节）。推理模式（think 与 nothink）是评测框架按模型记录的又一配置轴，与下文所述采样超参数并列；第 5 节排行榜全程报告 think 模式配置。在两种评测框架上，协议都将推理力度固定为 high，将上下文窗口统一为 200k token 并采用共同的自动压缩阈值，且禁用 WebSearch 与 AskUserQuestion 工具；各模型其余推理超参数使用提供商默认值，如下文记录。所报告结果绑定于本次评测使用的两个评测框架的特定构建，指标可能随评测框架版本演进而变化。

Scoring formalism. Every task t in a track's task set T yields a verifier reward r_{t} \in [0, 1] , and a model's track score is the unweighted mean

计分形式化。赛道任务集 T 中的每个任务 t 产生一个校验器奖励 r_{t} \in [0, 1]，模型的赛道分数为未加权均值

\[
S = \frac {1}{| \mathcal {T} |} \sum_ {t \in \mathcal {T}} r _ {t}, \tag {1}
\]

averaged over independent runs where a track scores more than one. The per-task reward differs by track. For Code, r_{t} is the hidden-test pass rate of the agent's patch. For Web, the reward is computed from a task-specific set of scored rubric items: each item returns pass/fail; let F_{t} be the set of failed non-fatal items, each with penalty p_{t,i} ; and any fatal failure sets the task reward to zero:

在赛道进行多次独立运行时取平均。任务级奖励因赛道而异。对 Code，r_{t} 是智能体补丁的隐藏测试通过率。对 Web，奖励由任务特定的一组计分评分细则项计算：每项返回通过/失败；令 F_{t} 为失败的非致命项集合，每项带有惩罚 p_{t,i}；任一致命失败将任务奖励置零：

\[ r _ {t} = \left\{ \begin{array}{l l} 0, & \text { if any fatal item fails }, \\ \max (0, 1 - \sum_ {i \in F _ {t}} p _ {t, i}), & \text { otherwise }, \end{array} \right. \tag {2}
\]

For Office, the task reward is a task-specific blend of a deterministic Rule score and an evidence-grounded Judge score, defined below; and for Security, the per-task deterministic scorer combines three programmatic terms, r_{t} = w_{1} artifact + w_{2} correctness + w_{3} robustness (Figure 8), averaged over three runs.

对 Office，任务奖励是下文定义的确定性 Rule 分数与证据锚定 Judge 分数的任务特定混合；对 Security，任务级确定性评分器组合三项程序化项，r_{t} = w_{1} artifact + w_{2} correctness + w_{3} robustness（图 8），对三次运行取平均。

Per-track scoring. Every task is packaged and executed the same way, but the reward computed from it is track-specific:

分赛道计分。每个任务的打包与执行方式相同，但从中计算的奖励是赛道特定的：

- Code – the run-level score computed by the Harbor harness [6]: the per-run average of per-task hidden-test scores, which is the headline Code metric throughout this report. The verifier takes one of three forms – a pytest-injected suite (22 of 80 tasks), functional boolean assertions needing no pytest or network access (54 of 80), or a JSON-report scorer for repository-understanding tasks (4 of 80); the gold patch is diagnostic only, and any satisfying patch scores full marks. A task-level aggregate unit-test pass rate and an LLM-judge score are recorded as reference values only. / Code——由 Harbor 评测框架 [6] 计算的运行级分数：各任务隐藏测试分数的每次运行平均值，是本报告全程的 Code 主指标。校验器取三种形式之一——注入 pytest 的套件（80 个任务中的 22 个）、无需 pytest 或网络访问的功能性布尔断言（80 个任务中的 54 个），或面向仓库理解任务的 JSON 报告评分器（80 个任务中的 4 个）；金牌补丁仅作诊断，任何满足要求的补丁均可满分。任务级汇总单元测试通过率和 LLM 评判分数仅作为参考值记录。
- Web – rubric scoring over 786 scored items. Rule checks cover 62 deterministic delivery and precheck items; LLM/VLM judges cover 676 items over text, code, structured content, DOM summaries, screenshots, and visual evidence; and the agent-judge covers 48 items that require operating the running artifact, such as workflow completion, state changes, persistence, and cross-state consistency. Failed items subtract configured penalties (0.1/0.2/0.3), while fatal failures set the task reward to zero. Every task must still deliver a runnable artifact at the declared output path, with no live-internet, external-account, or key access. / Web——对 786 个计分项进行评分细则计分。Rule 检查覆盖 62 项确定性交付与预检项；LLM/VLM 评判覆盖 676 项，涉及文本、代码、结构化内容、DOM 摘要、截图和视觉证据；agent-judge（智能体评判）覆盖 48 项，需操作正在运行的产物，例如工作流完成、状态变化、持久化与跨状态一致性。失败项扣除配置的惩罚（0.1/0.2/0.3），致命失败则将任务奖励置零。每个任务仍须在声明的输出路径交付可运行产物，且不得使用实时互联网、外部账户或密钥访问。
- Office – two separately retained scoring channels, each composed of binary checks. Deterministic rule checks verify objective facts in files, structure, values, cross-file relations, state changes, side effects, and execution boundaries. Each semantic rubric specifies one binary, evidence-based quality condition evaluated by an LLM Judge after the task ends. The Judge receives the public task instruction, the complete set of rule-check results, and only the fixed evidence named by the rubric being evaluated; it does not inspect the live workspace or alter recorded rule-check outcomes. Each task preconfigures how the two channel scores are combined. / Office——两条分别保留的计分通道，各自由二元检查组成。确定性规则检查核实文件、结构、取值、跨文件关系、状态变化、副作用和执行边界中的客观事实。每条语义评分细则指定一个二元、基于证据的质量条件，由 LLM Judge 在任务结束后评估。Judge 收到公开任务指令、完整的规则检查结果，以及仅由当前被评评分细则点名的固定证据；它不检查实时工作区，也不改写已记录的规则检查结果。每个任务预先配置两条通道分数的组合方式。
- Security – hidden-test verification, no LLM judge: every task ships a scoring.py, run in an isolated container, writing a numeric reward directly – exploitation tasks verify a PoC or captured flag, malware-analysis tasks compare IOCs to ground truth, YARA-rule tasks check match rate under a zero-false-positive constraint, and SOC-report tasks score via macro-F1/Kendall-tau against a reference report. Each score averages three independent runs. A five-layer anti-cheat infrastructure (banned-literal scanning, renamed-input tests, overlay/tamper tests, encoding-dependence tests, and low-weight decoy fields) guards against hardcoding across the input, code, and output axes. / Security——隐藏测试校验，无 LLM 评判：每个任务附带 scoring.py，在隔离容器中运行，直接写出数值奖励——利用类任务验证 PoC 或捕获的 flag，恶意软件分析任务将 IOC 与真值比较，YARA 规则任务在零误报约束下检查匹配率，SOC 报告任务相对参考报告以 macro-F1/Kendall-tau 计分。每个分数对三次独立运行取平均。五层反作弊基础设施（禁用字面量扫描、重命名输入测试、覆盖/篡改测试、编码依赖测试，以及低权重诱饵字段）防止在输入、代码和输出轴上硬编码。

Office Rule–Judge composition. For model m on trial a of Office task i, let P_{m,i,a} be the number of the task's N_{i} deterministic rule checks that pass. The Rule score is

Office Rule–Judge（规则检查/评判）组合。对模型 m 在 Office 任务 i 的试次 a，令 P_{m,i,a} 为该任务 N_{i} 项确定性规则检查中通过的数量。Rule 分数为

\[
R _ {m, i, a} = \frac {P _ {m , i , a}}{N _ {i}}. \tag {3}
\]

If task i has K_{i} semantic rubrics and rubric k returns b_{m,i,a,k} \in \{0,1\} , the Judge score is

若任务 i 有 K_{i} 条语义评分细则且评分细则 k 返回 b_{m,i,a,k} \in \{0,1\}，则 Judge 分数为

\[
J _ {m, i, a} = \frac {1}{K _ {i}} \sum_ {k = 1} ^ {K _ {i}} b _ {m, i, a, k}. \tag {4}
\]

The trial score uses the task's preconfigured rule weight w_{i} :

试次分数使用该任务预先配置的规则权重 w_{i}：

\[
S _ {m, i, a} = w _ {i} R _ {m, i, a} + (1 - w _ {i}) J _ {m, i, a}. \tag {5}
\]

Each task fixes w_{i} between 0.70 and 0.95; Office does not use a single global Rule weight. Let A_{i} be the number of available trials for task i. These trials are averaged first, \bar{S}_{m,i} = A_{i}^{-1} \sum_{a} S_{m,i,a} . If T tasks have at least one available trial, the Office score is their equal-weight macro-average,

每个任务将 w_{i} 固定在 0.70 与 0.95 之间；Office 不使用单一的全局 Rule 权重。令 A_{i} 为任务 i 的可用试次数。这些试次先取平均，\bar{S}_{m,i} = A_{i}^{-1} \sum_{a} S_{m,i,a}。若有 T 个任务至少有一次可用试次，则 Office 分数是它们的等权宏平均，

\[
\text { Overall } _ {m} = \frac {1}{T} \sum_ {i = 1} ^ {T} \bar {S} _ {m, i}. \tag {6}
\]

Rule and Judge sub-scores use the same two-level aggregation and remain available for diagnosis. A failed evidence extraction or Judge call assigns zero only to the affected rubric; the remaining rubrics continue. If a trial has no Judge score because the Judge input exceeds the supported length or every Judge call fails, the evaluator retains the Rule score and error state, marks the combined trial score as unavailable, and excludes that trial from both aggregation levels.

Rule 与 Judge 子分数使用相同的两级聚合，并保留供诊断。证据提取或 Judge 调用失败只将受影响的评分细则记为零；其余评分细则继续。若某次试次因 Judge 输入超出支持长度或每一次 Judge 调用都失败而没有 Judge 分数，评估器保留 Rule 分数与错误状态，将组合试次分数标为不可用，并从两级聚合中排除该试次。

Judge-based components and scoring risk. Three components in the suite are model-judged rather than programmatic: Web's LLM/VLM and agent-judge rubric items, whose penalties are configured per task; Office's LLM-judge layer for semantic-quality checks; and Code's LLM-judge score, which is recorded as a reference value only and never enters the headline metric. The known risk is model-judge bias – a judge model can systematically favor particular output styles or its own model family. The exposure is bounded by construction: the headline metrics rest on deterministic verification for Code (hidden tests) and Security (per-task deterministic scorer, no LLM judge); Office reduces, but does not eliminate, LLM Judge risk by binding every binary semantic rubric to fixed post-task evidence, retaining deterministic Rule outcomes as a separate score, and preventing Judge conclusions from altering those outcomes; and Web retains deterministic rule checks for delivery and precheck constraints while grounding LLM/VLM and agent judgments in recorded evidence from the final artifact.

基于评判的组件与计分风险。套件中有三个组件由模型评判而非程序化：Web 的 LLM/VLM 与 agent-judge 评分细则项，其惩罚按任务配置；Office 用于语义质量检查的 LLM 评判层；以及 Code 的 LLM 评判分数，仅作为参考值记录，从不进入主指标。已知风险是模型评判偏差——评判模型可能系统性地偏爱特定输出风格或其自身模型家族。暴露面在构造上被限定：主指标建立在 Code（隐藏测试）与 Security（任务级确定性评分器，无 LLM 评判）的确定性校验之上；Office 通过将每条二元语义评分细则绑定到固定的任务后证据、将确定性 Rule 结果保留为单独分数、并阻止 Judge 结论改写这些结果，来降低（但并非消除）LLM Judge 风险；Web 则保留交付与预检约束的确定性规则检查，同时将 LLM/VLM 与智能体评判锚定在最终产物的已记录证据上。

Inference hyperparameters. A model's effective sampling behavior can be set at three different layers – the vendor's own server-side default, the benchmark's routing/gateway layer, and an explicit override in the job configuration – so the project maintains a per-model hyperparameter record (covering fields such as temperature, top-p, max tokens, and the reasoning/thinking toggle) to avoid conflating the three. This bookkeeping currently spans a schema populated for the seven evaluated models. In practice, most models are run without an explicit sampling override, and the one parameter the benchmark deliberately fixes and reports per model is the reasoning mode.

推理超参数。模型的有效采样行为可在三个不同层设置——厂商自身的服务端默认值、基准的路由/网关层，以及作业配置中的显式覆盖——因此项目维护按模型的超参数记录（覆盖 temperature、top-p、max tokens 以及推理/thinking 开关等字段），以免将三者混为一谈。该台账目前覆盖为七个被评模型填充的 schema。实践中，大多数模型在没有显式采样覆盖的情况下运行，基准刻意固定并按模型报告的唯一参数是推理模式。

Disclosure policy. Tencent WorkBuddy Bench is released as a fully open benchmark: task directories, environment images, evaluation code, grading tests, and reference/gold solutions are all made public alongside the aggregate leaderboard, following the SWE-bench-style convention of publishing the full task set rather than an aggregate-only score. The terms “hidden tests” (for Code) and “held-out evaluation assets” (more generally) describe solve-time visibility, not secrecy: they are unavailable to the agent’s own context during a run and are introduced or invoked only after the agent has finished acting (see above), but they are public in the released dataset like every other task artifact. Contamination resistance instead rests on task freshness at authoring time – tasks are built from content excluded from model-pretraining corpora before the release date – not on withholding task content after release.

披露政策。Tencent WorkBuddy Bench 作为完全开放基准发布：任务目录、环境镜像、评测代码、评分测试以及参考/金牌解答随汇总排行榜一并公开，遵循 SWE-bench 风格的惯例——发布完整任务集，而非仅发布汇总分数。“hidden tests”（对 Code）和“held-out evaluation assets”（更一般地）描述的是求解时可见性，而非保密：它们在运行期间对智能体自身上下文不可用，仅在智能体完成行动之后才被引入或调用（见上文），但在已发布数据集中与其他任务产物一样公开。污染抗性转而建立在撰写时的任务新鲜度之上——任务由发布日期之前被排除在模型预训练语料之外的内容构建——而非发布后扣留任务内容。

## 5 Results / 结果

This section reports the Tencent WorkBuddy Bench leaderboard, read against the question the suite is built to answer: how does agent capability rank across four distinct classes of real work – Code, Web, Office, and Security – and how robust is that ranking when the harness itself changes. Every score is the average of three independent runs in think mode, and all four subsets are scored under both the CodeBuddy Code (cbc) and Claude Code (cc) harnesses. Every model is scored on every track/harness combination; one cell – Claude Opus 4.8’s Code score under Claude Code – comes from a modified-instruction run, marked ‡ in Table 6 and described in its caption.

本节报告 Tencent WorkBuddy Bench 排行榜，对照该套件要回答的问题来读：智能体能力如何在四类不同的真实工作——Code、Web、Office 和 Security——中排名，以及当评测框架本身变化时该排名有多稳健。每个分数都是 think 模式下三次独立运行的平均值，全部四个子集都在 CodeBuddy Code（cbc）和 Claude Code（cc）两种评测框架下计分。每个模型在每一种赛道/评测框架组合上都计分；有一格——Claude Opus 4.8 在 Claude Code 下的 Code 分数——来自修改指令运行，在表 6 中标为 ‡，并在表注中说明。

| | Code<br>代码 | | Web<br>网页 | | Office<br>办公 | | Security<br>安全 | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model<br>模型 | cbc | cc | cbc | cc | cbc | cc | cbc | cc |
| Claude Opus 4.8 | 74.43 | 77.90‡ | 68.14 | 69.86 | 82.37 | 83.23 | 64.37 | 65.87 |
| GPT-5.5 | 72.90 | 76.63 | 61.14 | 64.86 | 81.96 | 86.05 | 64.39 | 77.91 |
| GLM-5.2 | 71.54 | 77.06 | 67.43 | 60.71 | 79.60 | 79.57 | 76.32 | 80.86 |
| HY-3 | 62.90 | 66.26 | 67.71 | 66.43 | 82.08 | 80.08 | 64.50 | 65.59 |
| MiniMax-M3 | 60.14 | 66.42 | 58.00 | 52.57 | 78.28 | 76.30 | 74.14 | 59.30 |
| DeepSeek-V4-Pro | 58.92 | 64.59 | 54.57 | 51.57 | 79.11 | 78.71 | 70.04 | 58.73 |
| DeepSeek-V4-Flash | 55.73 | 61.89 | 47.29 | 50.29 | 77.47 | 77.54 | 67.11 | 53.90 |

Table 6. Tencent WorkBuddy Bench leaderboard. Scores are 0–100, think mode, averaged over three runs, under the CodeBuddy Code (cbc) and Claude Code (cc) harnesses. Bold on shaded cells marks the best score in each column. ‡Claude Opus 4.8’s Code score under Claude Code comes from a modified-instruction run: on top of the disabled AskUserQuestion tool (Section 4), an explicit do-not-ask, complete-in-one-pass instruction was added, so its setup differs slightly from the other runs.

表 6. Tencent WorkBuddy Bench 排行榜。分数为 0–100，think 模式，三次运行平均，分别在 CodeBuddy Code（cbc）与 Claude Code（cc）评测框架下。阴影格加粗标出各列最佳分数。‡Claude Opus 4.8 在 Claude Code 下的 Code 分数来自修改指令运行：在已禁用 AskUserQuestion 工具（第 4 节）之上，又增加了明确的“不要提问、一次完成”指令，因此其设置与其他运行略有不同。

Per-track leaders. No single model tops every board. Across the eight boards in Table 6, leadership splits three ways: Claude Opus 4.8 leads five – Code under both harnesses (74.43 under cbc; 77.90 under cc, from the modified-instruction run noted ‡ in the table caption), Web under both harnesses (68.14 under cbc, 69.86 under cc), and Office under cbc (82.37), where HY-3 (82.08) is the Office runner-up just below it; GLM-5.2 leads two – Security under both harnesses (76.32 under cbc, 80.86 under cc); and GPT-5.5 leads one, Office under cc (86.05). That an open-weight model, GLM-5.2, tops both Security boards outright is itself a finding: on this suite the gap between open-weight and closed frontier models is board-dependent rather than uniform.

各赛道领先者。没有单一模型在每块榜上都居首。在表 6 的八块榜中，领先地位一分为三：Claude Opus 4.8 领先五块——两种评测框架下的 Code（cbc 下 74.43；cc 下 77.90，来自表注中标为 ‡ 的修改指令运行）、两种评测框架下的 Web（cbc 下 68.14，cc 下 69.86），以及 cbc 下的 Office（82.37），其中 HY-3（82.08）是紧随其后的 Office 亚军；GLM-5.2 领先两块——两种评测框架下的 Security（cbc 下 76.32，cc 下 80.86）；GPT-5.5 领先一块，即 cc 下的 Office（86.05）。开权模型 GLM-5.2 在两块 Security 榜上直接夺冠，这本身就是一项发现：在本套件上，开权模型与闭源前沿模型之间的差距取决于榜单，而非整齐划一。

Harness sensitivity. With all four tracks scored under both harnesses, the harness is visibly not a neutral measurement instrument – and the four tracks are affected to very different degrees. Code shifts the most uniformly: the rank order of models on Code differs between the two harnesses — GPT-5.5 sits ahead of GLM-5.2 under cbc (72.90 vs. 71.54) but behind it under cc (76.63 vs. 77.06) — and Claude Opus 4.8's modified-instruction cc run likewise sits higher than its cbc score.¹ Web is more mixed under Claude Code: four of seven dual-scored models drop, by margins from −1.28 (HY-3) to −6.72 (GLM-5.2), while three rise – Claude Opus 4.8 (+1.72), DeepSeek-V4-Flash (+3.00), and GPT-5.5 (+3.72); the signed mean shift is −1.14, and Claude Opus 4.8 leads Web under both harnesses. Office moves least: five of the seven dual-scored models shift by under two points (median absolute shift 0.86), the exceptions being GPT-5.5 (+4.09) and HY-3 (−2.00). Security shows the largest reordering between harnesses: the mean absolute shift across the seven dual-scored models is 8.6 points. GLM-5.2 leads Security under both harnesses, but below it the board reorders substantially: GPT-5.5 climbs from sixth under cbc to second under cc, while MiniMax-M3 falls from second to fifth.

评测框架敏感性。四条赛道都在两种评测框架下计分时，评测框架显然不是中性的测量仪器——四条赛道受影响的程度也大不相同。Code 的变化最均匀：Code 上的模型名次在两种评测框架之间不同——GPT-5.5 在 cbc 下领先 GLM-5.2（72.90 对 71.54），但在 cc 下落后（76.63 对 77.06）——Claude Opus 4.8 的修改指令 cc 运行同样高于其 cbc 分数。¹ Web 在 Claude Code 下更为混杂：七个双评测框架计分模型中有四个下降，幅度从 −1.28（HY-3）到 −6.72（GLM-5.2），另有三个上升——Claude Opus 4.8（+1.72）、DeepSeek-V4-Flash（+3.00）和 GPT-5.5（+3.72）；带符号均值偏移为 −1.14，Claude Opus 4.8 在两种评测框架下都领先 Web。Office 变动最小：七个双评测框架计分模型中有五个变动不足两分（中位绝对偏移 0.86），例外是 GPT-5.5（+4.09）和 HY-3（−2.00）。Security 在评测框架之间的重排最大：七个双评测框架计分模型的平均绝对偏移为 8.6 分。GLM-5.2 在两种评测框架下都领先 Security，但在其之下榜单大幅重排：GPT-5.5 从 cbc 下的第六升至 cc 下的第二，而 MiniMax-M3 从第二降至第五。

**Refusals on Security.** A small number of Security runs ended in task-level refusals on security-flavored requests. Across the three runs, Claude Opus 4.8 recorded 13 refusals under Claude Code (none under CodeBuddy Code), GPT-5.5 recorded 2 under CodeBuddy Code, and all other models recorded none. These counts are reported for context; the leaderboard scores average over all runs as executed.

**Security 上的拒绝。** 少数 Security 运行在带安全色彩的请求上以任务级拒绝结束。三次运行中，Claude Opus 4.8 在 Claude Code 下记录了 13 次拒绝（CodeBuddy Code 下没有），GPT-5.5 在 CodeBuddy Code 下记录了 2 次，其余模型均无。这些计数供背景参考；排行榜分数对所有已执行运行取平均。

**Coding versus Data & Algo gap.** The Code subset's own category taxonomy separates coding proper from data- and algorithm-style work, and the gap between them is systematic rather than incidental: a per-category breakdown (not shown in Table 6, drawn from the subset's internal per-category results) finds that model/harness configurations almost uniformly score higher on Data & Algorithm tasks than on Coding tasks, at an average of roughly 74% versus roughly 65%. The reading offered alongside that breakdown is that data- and algorithm-style tasks are rarely hard as code – they are hard in business or data semantics – whereas precisely fixing a real repository under an existing contract is the more discriminating skill. Table 6 is consistent with this: in every model/harness configuration scored on both tracks, the Code score sits below the same configuration's Office score, often by ten points or more, whereas the Code score sits above the same configuration's Web score in all but one case – HY-3 is the sole exception, scoring higher on Web than on Code under both harnesses, clearly under cbc (67.71 vs. 62.90) and marginally under cc (66.43 vs. 66.26).

**编码 vs 数据与算法差距。** Code 子集自身的类别分类法把真正的编码工作与数据/算法风格工作分开，两者之间的差距是系统性的，而非偶然：按类别分解（未在表 6 中展示，取自该子集内部的按类别结果）发现，模型/评测框架配置几乎一律在 Data & Algorithm 任务上高于 Coding 任务，平均大约为 74% 对大约 65%。与该分解一并给出的解读是：数据与算法风格任务就代码本身而言很少算难——难在业务或数据语义——而在既有契约下精确修复真实仓库，才是更具区分度的技能。表 6 与此一致：在同时计分两条赛道的每一种模型/评测框架配置中，Code 分数都低于同一配置的 Office 分数，常常低十分或更多；而 Code 分数在除一种情况外都高于同一配置的 Web 分数——HY-3 是唯一例外，在两种评测框架下 Web 都高于 Code，cbc 下差距明显（67.71 对 62.90），cc 下仅略高（66.43 对 66.26）。

**Which Code categories are hardest.** A per-category breakdown of the Code subset (mean reward averaged over all valid configurations) makes the same point at finer grain. The two hardest categories are bug_fix (mean 0.47) and api_contract (mean 0.47) – real-repository regression fixing and precise, contract-honoring interface work – while the easiest are feature_pipeline (0.94) and testing (0.88), which are well-specified synthetic pipelines and test-writing tasks. Several product/analytics categories show an exceptionally wide model spread (product_analytics ranges from 0.08 to 1.00 across models), a signature of tasks where the score turns on whether the model correctly reads the business intent rather than on whether its code runs.

**哪些 Code 类别最难。** Code 子集的按类别分解（对所有有效配置平均的均值奖励）在更细粒度上说明同一点。最难的两类是 bug_fix（均值 0.47）和 api_contract（均值 0.47）——真实仓库回归修复，以及精确、遵守契约的接口工作——最容易的是 feature_pipeline（0.94）和 testing（0.88），即规格明确的合成流水线与写测试任务。若干产品/分析类别显示出异常宽的模型分布（product_analytics 跨模型从 0.08 到 1.00），这是分数取决于模型是否正确读懂业务意图、而非代码能否运行的特征。

**Why bug_fix is the hardest category.** These tasks are real upstream regressions posed colloquially, with the root cause withheld. Solving one means locating an intermittent, context-dependent fault from a one-sentence symptom description – pure repository understanding with no algorithmic difficulty – and then patching it minimally without breaking the surrounding contract. The low mean (0.47) shows that current models still struggle at precisely this SWE-bench-style skill of grounding a vague report in the right lines of a large codebase.

**为何 bug_fix 是最难类别。** 这些任务是口语化提出的真实上游回归，根因被隐去。求解意味着从一句话的症状描述中定位间歇性、依赖上下文的故障——纯仓库理解，没有算法难度——然后最小限度地打补丁，且不破坏周围契约。低均值（0.47）表明，当前模型仍难以掌握这种 SWE-bench 风格的技能：把模糊报告锚定到大型代码库中正确的那些行。

¹Harness–model integration details also matter within a single harness: a diagnostic rerun of HY-3 on the Code subset with cross-turn reasoning passback enabled – thinking content passed back to the backend across turns – scored 66.72 under CodeBuddy Code (+3.82 over the leaderboard configuration) and 68.18 under Claude Code (+1.92), under the same three-run protocol. The leaderboard reports the standard configuration. A related, distinct failure is semantically correct but contract-mismatched code: the model implements the right behavior under the wrong function name, parameter shape, or output format, so a functional verifier still fails it. This is most acute on api_contract, where a task must preserve a precise set of fields under an existing contract and a single dropped field zeroes the checks that depend on it.

¹评测框架–模型集成细节在单一评测框架内部也很重要：对 HY-3 在 Code 子集上启用跨轮推理回传——将 thinking 内容跨轮回传给后端——的诊断重跑，在相同的三次运行协议下，CodeBuddy Code 得 66.72（比排行榜配置高 +3.82），Claude Code 得 68.18（+1.92）。排行榜报告的是标准配置。一种相关但不同的失败是语义正确但契约不匹配的代码：模型在错误的函数名、参数形态或输出格式下实现了正确行为，功能校验器仍判失败。这在 api_contract 上最为尖锐：任务必须在既有契约下保留精确的字段集合，丢掉一个字段就会使依赖它的检查全部归零。

**Two representative failure modes.** Two Code bad cases illustrate the dominant ways points are lost. In an OpenAPI contract task, a model produces behaviorally reasonable output but drops one or two required fields (for example deprecated or examples) or leaves a path parameter's required flag to its default; because the verifier runs a dozen per-field boolean checks, each omission zeroes the checks that depend on it and drags the overall score down sharply – the functionality is not wrong so much as the contract implied by the tests is not matched. In a product-analytics task, the colloquial ask is to compute per-group conversion and revenue while “not counting purchases that happen long afterward” – an implicit conversion-attribution window. High-scoring models filter the late purchases by that window; low-scoring ones ignore the constraint and count every purchase, over-estimating conversion, even though the code runs cleanly either way. The gap comes entirely from whether the business rule was understood, which is why the model spread on this category runs nearly the full range.

**两种代表性失败模式。** 两个 Code 反面案例说明失分的主要方式。在 OpenAPI 契约任务中，模型产出行为上合理的输出，但丢掉一两个必填字段（例如 deprecated 或 examples），或把路径参数的 required 标志留为默认值；因为校验器运行十多项逐字段布尔检查，每一处遗漏都会使依赖它的检查归零，从而急剧拉低总分——功能本身并不算错，而是测试所隐含的契约未被匹配。在产品分析任务中，口语化要求是计算分组转化与收入，同时“不把很久之后才发生的购买计算在内”——这是隐式的转化归因窗口。高分模型按该窗口过滤晚期购买；低分模型忽略该约束并计入每一笔购买，从而高估转化，尽管代码两种写法都能干净运行。差距完全来自是否理解了业务规则，因此该类别上的模型分布几乎拉满全区间。

**Web capability slices.** Web slice results point to a consistent pattern: visual design and analytical reporting are the strongest categories, with code testing and page implementation next, while page interaction and data-visualization semantics expose the most failures. The interaction/state axis tells a complementary story: noninteractive and lightly interactive artifacts score well above stateful ones – single-flow state changes, multi-step workflows, and persistence, offline, and cross-state behavior are the hardest slices in the subset.

**Web 能力切片。** Web 切片结果指向一致模式：视觉设计与分析报告是最强类别，其次是代码测试与页面实现，而页面交互与数据可视化语义暴露出最多失败。交互/状态轴讲述互补故事：非交互与轻度交互产物的分数远高于有状态产物——单流状态变化、多步工作流，以及持久化、离线与跨状态行为，是该子集中最难的切片。

The failure pattern is less about rendering a visible page than about closing a front-end engineering loop. Models often produce a plausible UI but lose consistency among state source, display, persistence, and final payload – the interactive and stateful slices are precisely where scores are lowest – or produce charts and data-visualization outputs without a clear source-to-output evidence trail. By evaluation signal, LLM/VLM items account for most checks and most failed items; rule failures mostly reflect delivery, precheck, format, or executable-test contracts, while agent-judge failures correspond to workflow or state breakage in the running artifact.

失败模式与其说是渲染出可见页面，不如说是未能闭合前端工程闭环。模型常常产出看似合理的 UI，却在状态源、展示、持久化与最终载荷之间失去一致性——交互与有状态切片恰恰是分数最低之处——或产出图表与数据可视化输出，却没有清晰的源到输出证据链。按评测信号看，LLM/VLM 项占大多数检查和大多数失败项；规则失败主要反映交付、预检、格式或可执行测试契约，而 agent-judge 失败对应运行产物中的工作流或状态断裂。

**Office performance by difficulty and task type.** Figure 9 shows how Office performance varies by difficulty and by seven diagnostic task types. Within each harness, cross-model mean scores decline from easy to medium to hard tasks (84.6/80.3/73.1 under cbc and 83.9/78.9/72.0 under cc). Model strengths also differ by task type: Claude Opus 4.8 leads multi-source merge and reconciliation under both harnesses, whereas GPT-5.5 leads five of the seven types shown under cc, including aggregation and metric reasoning, complex rule execution, and structured extraction. This view also reveals differences hidden by aggregate scores: GLM-5.2 is nearly unchanged overall across harnesses (79.60 vs. 79.57), yet its multi-file extraction score falls from 87.7 to 70.5 while complex rule execution remains nearly unchanged (83.1 vs. 83.3).

**按难度与任务类型看 Office 表现。** 图 9 显示 Office 表现如何随难度以及七种诊断性任务类型变化。在每种评测框架内，跨模型均值分数从易到中到难下降（cbc 下为 84.6/80.3/73.1，cc 下为 83.9/78.9/72.0）。模型优势也因任务类型而异：Claude Opus 4.8 在两种评测框架下都领先多源合并与对账，而 GPT-5.5 在 cc 下领先所示七种类型中的五种，包括聚合与指标推理、复杂规则执行和结构化抽取。这一视角也揭示了汇总分数所掩盖的差异：GLM-5.2 跨评测框架总体几乎不变（79.60 对 79.57），但其多文件抽取分数从 87.7 降至 70.5，而复杂规则执行几乎不变（83.1 对 83.3）。

**Common failure patterns in reviewed Office submissions.** We inspected the deliverables and Rule/Judge evidence for selected low-scoring tasks. The same problems recurred: related deliverables were inconsistent, records were not clearly tied to their source or current state, structured files could not be parsed, or agents submitted artifacts without validating them. Because the Office verifier checks files, cross-file relations, state, output contracts, and evidence-grounded semantic requirements, these incomplete workflows lose points even when one deliverable looks plausible.

**已审阅 Office 提交中的常见失败模式。** 我们检查了若干低分任务的交付物与 Rule/Judge（规则检查/评判）证据。同样的问题反复出现：相关交付物不一致，记录未清晰绑定到其来源或当前状态，结构化文件无法解析，或智能体提交产物却未加以验证。因为 Office 校验器检查文件、跨文件关系、状态、输出契约以及证据锚定的语义要求，这些不完整工作流即使某一份交付物看起来合理，仍会失分。

### 5.1 Token and Turn Efficiency / Token 与轮次效率

Figure 9. Office results by difficulty and task type. (a) Mean Office score by calibrated difficulty within each harness, averaged over all models with scored runs in that panel. (b) Equal-weight task average for the seven diagnostic task types represented by at least four tasks, shown for the three models discussed in the text. Scores use a 0–100 scale. Bold marks the best score in the full model set for each task type and harness, so a displayed three-model group may contain no bold value. HY-3's per-task slices in this figure predate its updated Office run, so its contribution to the panel means reflects the earlier scoring.

图 9. 按难度与任务类型划分的 Office 结果。(a) 各评测框架内按校准难度的 Office 均值分数，对该面板中有计分运行的全部模型取平均。(b) 至少由四个任务代表的七种诊断性任务类型的等权任务平均，展示正文讨论的三个模型。分数采用 0–100 标尺。加粗标出完整模型集合中各任务类型与评测框架的最佳分数，因此所展示的三模型组可能不含加粗值。本图中 HY-3 的任务切片早于其更新后的 Office 运行，因此它对面板均值的贡献反映的是较早计分。

![Figure 9](images/fig09.png)

Table 7 reports per-run averages of assistant turns, output tokens, and input tokens on the Code subset. Turns are counted as unique assistant messages, including subagent activity alongside the main agent. Output tokens are comparable across the two harnesses; input tokens are reported cache-inclusive – they count cached context reads as well as fresh input – and are not comparable across harnesses, because the two harnesses manage context and caching under different conventions, so input figures should only be read within a harness column. Output-token counts should also not be read as a cross-model efficiency metric: different models use different tokenizers, so a token is not a constant unit of work across models, and the comparisons below are illustrative rather than a rigorous cross-model efficiency ranking.

表 7 报告 Code 子集上助手轮次、输出 token 与输入 token 的每次运行平均值。轮次按唯一助手消息计数，包括主智能体之外的子智能体活动。输出 token 在两种评测框架之间可比较；输入 token 按含缓存报告——既计入缓存上下文读取，也计入新输入——且在评测框架之间不可比较，因为两种评测框架按不同惯例管理上下文与缓存，因此输入数字只应在同一评测框架列内阅读。输出 token 计数也不应被读作跨模型效率指标：不同模型使用不同分词器，因此一个 token 并不是跨模型恒定的工作单位，下文比较是示意性的，而非严格的跨模型效率排名。

| Model<br>模型 | CodeBuddy Code (cbc) | | | Claude Code (cc) | | |
| --- | --- | --- | --- | --- | --- | --- |
| | Avg turns<br>平均轮次 | Output (k)<br>输出 (k) | Input (k)<br>输入 (k) | Avg turns<br>平均轮次 | Output (k)<br>输出 (k) | Input (k)<br>输入 (k) |
| Claude Opus 4.8 | 29.51 | 22.3 | 928.7 | 13.2^‡ | 4.7^‡ | 646.5^‡ |
| GPT-5.5 | 26.92 | 6.9 | 753.2 | 30.44 | 8.7 | 696.5 |
| GLM-5.2 | 33.06 | 12.3 | 861.4 | 33.73 | 22.0 | 1243.3 |
| HY-3 | 26.02 | 9.3 | 586.8 | 18.07 | 13.9 | 659.2 |
| MiniMax-M3 | 28.89 | 8.5 | 1021.4 | 33.90 | 10.6 | 1308.3 |
| DeepSeek-V4-Pro | 44.01 | 10.2 | 800.0 | 24.20 | 23.7 | 642.3 |
| DeepSeek-V4-Flash | 40.30 | 9.8 | 700.5 | 23.12 | 28.6 | 771.4 |

Table 7. Per-run averages on the Code subset, by harness: turns (unique assistant messages, including subagent activity), output tokens, and cache-inclusive input tokens, in thousands. Output tokens are comparable across harnesses; input tokens are not, because the two harnesses manage context and caching under different conventions. ‡Claude Opus 4.8's Claude Code figures come from the modified-instruction run described in Table 6.

表 7. Code 子集按评测框架的每次运行平均值：轮次（唯一助手消息，含子智能体活动）、输出 token，以及含缓存的输入 token，单位为千。输出 token 在评测框架之间可比较；输入 token 不可比较，因为两种评测框架按不同惯例管理上下文与缓存。‡Claude Opus 4.8 的 Claude Code 数字来自表 6 所述的修改指令运行。

Three observations. First, GPT-5.5 posts top-tier scores on a minimal output budget: its 6.9k tokens per run under cbc is the lowest output budget on that harness, and its 8.7k under cc is the lowest among the standard-protocol runs – against a field that mostly spends 8–29k; the smallest cc output overall belongs to Claude Opus 4.8's modified-instruction run (4.7k). Second, spend and rank are not aligned: DeepSeek-V4-Flash emits roughly 3.3× GPT-5.5's output under cc (28.6k vs. 8.7k) while scoring 14.74 points lower (61.89 vs. 76.63), and GLM-5.2's 77.06 under cc costs 22.0k output tokens against GPT-5.5's 8.7k for a 0.43-point margin – while Claude Opus 4.8 pairs the highest cbc output (22.3k) with the cbc lead. Third, among standard-protocol runs turn counts vary roughly 2.4× across configurations (18.07 to 44.01 per run), and neither extreme aligns with score: the leanest standard configuration is HY-3 under cc at 18.07 turns for a mid-board 66.26, while the two largest turn counts (DeepSeek-V4-Pro at 44.01 and DeepSeek-V4-Flash at 40.30, both under cbc) belong to the two lowest-scoring cbc configurations. Claude Opus 4.8's modified-instruction cc run sits below the standard range at 13.2 turns and 4.7k output tokens per run.

三点观察。第一，GPT-5.5 以极小的输出预算拿到顶级分数：其在 cbc 下每次运行 6.9k token 是该评测框架上最低的输出预算，cc 下的 8.7k 是标准协议运行中最低的——对照大多消耗 8–29k 的一组模型；cc 上整体最小输出属于 Claude Opus 4.8 的修改指令运行（4.7k）。第二，花费与名次并不对齐：DeepSeek-V4-Flash 在 cc 下大约产出 GPT-5.5 的 3.3× 输出（28.6k 对 8.7k），分数却低 14.74 分（61.89 对 76.63）；GLM-5.2 在 cc 下 77.06 花费 22.0k 输出 token，对 GPT-5.5 的 8.7k 仅有 0.43 分优势——而 Claude Opus 4.8 以最高的 cbc 输出（22.3k）搭配 cbc 领先。第三，在标准协议运行中，轮次大约在各配置间相差 2.4×（每次运行 18.07 到 44.01），两端都不与分数对齐：最精简的标准配置是 cc 下的 HY-3，18.07 轮拿到中游的 66.26；最大的两个轮次数（cbc 下 DeepSeek-V4-Pro 的 44.01 与 DeepSeek-V4-Flash 的 40.30）属于 cbc 上得分最低的两个配置。Claude Opus 4.8 的修改指令 cc 运行低于标准区间，为每次运行 13.2 轮与 4.7k 输出 token。

Across subsets. The Code budget profile is not universal. Office runs are the leanest – 16–42 turns and 10–30k output tokens per run across models and harnesses – and Web sits in the middle (13–39 turns), while Security is the heaviest track by a wide margin, at 30–89 turns per run. ^{2} The Security extreme is stark: MiniMax-M3 under cbc averages 88.8 turns and roughly 11.1M cache-inclusive input tokens per run for its 74.14. Across all four tracks, GPT-5.5 is consistently the leanest high scorer: under cbc it posts the smallest output budget of any model on every track – 6.9k output tokens per run on Code, 13.5k on Web, 10.2k on Office, and 7.5k on Security.

跨子集。Code 的预算画像并不普适。Office 运行最精简——跨模型与评测框架为每次运行 16–42 轮、10–30k 输出 token——Web 居中（13–39 轮），而 Security 以很大差距成为最重的赛道，每次运行 30–89 轮。^{2} Security 的极端很鲜明：MiniMax-M3 在 cbc 下平均 88.8 轮，每次运行为其 74.14 分消耗大约 11.1M 含缓存输入 token。在全部四条赛道上，GPT-5.5 始终是最精简的高分者：cbc 下它在每条赛道都交出所有模型中最小的输出预算——Code 每次运行 6.9k 输出 token，Web 13.5k，Office 10.2k，Security 7.5k。
