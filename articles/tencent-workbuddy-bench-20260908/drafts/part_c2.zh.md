## 6 Related Work / 相关工作

We first position Tencent WorkBuddy Bench against existing agent benchmarks in the code, web, office, and security domains; the suite's own task-construction methodology, subset design, and evaluation harness are detailed in the sections that follow. These are design-time comparisons drawn from the benchmark's own qualitative analysis of task design, not a head-to-head measured evaluation of agents across these suites.

我们首先将腾讯 WorkBuddy Bench 与代码、Web、办公和安全领域的现有智能体基准进行定位；本套件自身的任务构建方法、子集设计与评测框架将在后续各节详述。这些是基于本基准对任务设计的定性分析所做的设计时对比，而非跨这些套件对智能体的头对头实测评估。

Code. The Code subset occupies a similar problem space to the SWE-bench family [1, 2] and to library-from-scratch benchmarks such as Commit0 [7] , but differs in instruction style and role diversity. Where SWE-bench and SWE-bench Verified supply a detailed GitHub issue – and Commit0 a test-driven specification to implement against – Code tasks are authored as short, colloquial requests, closer to how a teammate phrases an ask than to a filed issue, deliberately leaving implementation detail underspecified; and Code spans five requester roles (developer, algorithm engineer, product manager, QA, ops) across 18 categories beyond bug fixing, rather than a single issue-resolution framing. Contamination resistance is pursued differently across the family: LiveCodeBench [8] relies on problems released after model training cutoffs, whereas Code relies on freshly authored task directories – real upstream commits, clean-room reimplementations, and synthetic workspaces – built and held back from publication until the benchmark's release, at which point prompts, hidden tests, and gold patches are published in full alongside it. RepoBench [9] and Aider Polyglot [10] target narrower slices of the same space (repository-level completion and templated multi-language exercises), and Terminal-Bench [11] evaluates general terminal-agent competence rather than repository-scoped code changes.

代码。Code 子集与 SWE-bench 系列 [1, 2] 以及 Commit0 [7] 这类从零构建程序库的基准占据相似的问题空间，但在指令风格和角色多样性上有所不同。SWE-bench 与 SWE-bench Verified 提供详细的 GitHub issue——Commit0 则提供用于对照实现的测试驱动规格——而 Code 任务被撰写为简短、口语化的请求，更接近同事口头提出需求的方式，而非已提交的 issue，刻意让实现细节保持未充分指定；并且 Code 跨越五种提出者角色（开发者、算法工程师、产品经理、测试、运维）和 18 个超出缺陷修复的类别，而非单一的问题单解决框架。抗污染性在该系列中以不同方式追求：LiveCodeBench [8] 依赖模型训练截止日期之后发布的题目，而 Code 依赖新撰写的任务目录——真实上游提交、洁净室重实现和合成工作区——在基准发布前构建并暂缓公开，发布时再将提示、隐藏测试和标准补丁一并完整公开。RepoBench [9] 与 Aider Polyglot [10] 瞄准同一空间的更窄切片（仓库级补全和模板化多语言练习），而 Terminal-Bench [11] 评估的是通用终端智能体能力，而非仓库范围内的代码变更。

 ^{2} Security turn and token statistics still use the earlier turn-counting convention and have not yet been recomputed as unique assistant messages; their turn counts are therefore not directly comparable to the Code figures in Table 7.

 ^{2} Security 的轮次与 token 统计仍使用较早的轮次计数约定，尚未按唯一助手消息重新计算；因此其轮次数不能与表 7 中的 Code 数字直接比较。

End-to-end and production coding-agent benchmarks. Vibe Code Bench [12] evaluates zero-to-one web application development from text specifications through browser-agent workflow tests over deployed applications, making it a close reference point for runnable front-end deliverables. CursorBench [5] pursues a related realism goal by a different route: it traces committed code back to the original agent request from authentic production sessions, so its task distribution is anchored to how one vendor's users actually work rather than to curated issue text. These choices make both benchmarks important reference points, but they leave different gaps for our setting. Vibe Code Bench focuses on from-scratch application construction, while WorkBuddy Web also covers modification, review, front-end project tests, analysis, and conversion. CursorBench is closed-source, so its task set, category distribution, and any selection bias toward the vendor's own agent cannot be independently audited, and its representativeness cannot be confirmed to extend beyond that vendor's user base. Tencent WorkBuddy Bench pursues realism through a distribution-informed route and then releases the result fully open: task categories, shapes, and intents are checked against real usage (Section 3), tasks are reverse-engineered from real artifacts and curated or synthesized to match that distribution rather than released as raw production sessions, and the resulting task directories, environment images, evaluation code, grading tests, and reference solutions are all publicly released and independently auditable.

端到端与生产环境编程智能体基准。Vibe Code Bench [12] 评估从文本规格出发、经已部署应用上的浏览器智能体工作流测试的从零到一 Web 应用开发，因此是可运行前端交付物的相近参照点。CursorBench [5] 以另一条路径追求相关的真实性目标：它将已提交代码回溯到真实生产会话中的原始智能体请求，因此其任务分布锚定于某一厂商用户的实际工作方式，而非经策划的 issue 文本。这些选择使二者都成为重要参照点，但在我们的设定中留下了不同缺口。Vibe Code Bench 聚焦从零构建应用，而 WorkBuddy Web 还覆盖修改、评审、前端项目测试、分析与转换。CursorBench 是闭源的，因此其任务集、类别分布、以及任何偏向该厂商自身智能体的选择偏差都无法被独立审计，其代表性也无法被确认为能延伸到该厂商用户群之外。腾讯 WorkBuddy Bench 通过基于分布的路径追求真实性，然后将结果完全开放发布：任务类别、形态与意图对照真实用法进行核对（第 3 节），任务从真实产物逆向工程，并经策划或合成以匹配该分布，而非作为原始生产会话发布；由此产生的任务目录、环境镜像、评测代码、评分测试和参考解全部公开发布且可独立审计。

Web. Design2Code [3] and Interaction2Code [13] evaluate static and lightly interactive page reproduction from a reference design; FrontendBench [14] extends automatic judging to a broader set of front-end generation tasks; WebArena [4] and VisualWebArena [15] instead evaluate an agent operating an existing browser environment rather than producing a runnable artifact from scratch. Each is strong on one or two axes – static reproduction, interactive generation, browser-agent operation, or code-maintenance realism – but none combines page/UI work, data and chart artifacts, front-end project documents, tests, and analyses, non-scratch lifecycle coverage, runtime interaction/state checks, and rule, LLM/VLM, and agent judging in one evaluation. Table 8 keeps those axes separate rather than reporting task counts, since published benchmark scales are not directly comparable across webpage, interaction, issue, and application-specification units. The comparison is qualitative and self-reported from each benchmark's own published description, not a measured evaluation.

Web。Design2Code [3] 与 Interaction2Code [13] 评估根据参考设计复现静态及轻度交互页面；FrontendBench [14] 将自动评判扩展到更广的前端生成任务；WebArena [4] 与 VisualWebArena [15] 则评估智能体操作既有浏览器环境，而非从零产出可运行产物。各自在一两个轴向上很强——静态复现、交互生成、浏览器智能体操作，或代码维护真实性——但没有一个能在同一评测中同时覆盖页面/UI 工作、数据与图表产物、前端项目文档、测试与分析、非从零生命周期覆盖、运行时交互/状态检查，以及规则、LLM/VLM 与智能体评判。表 8 将这些轴向分开呈现，而不报告任务数量，因为已发布基准的规模在网页、交互、issue 与应用规格等单位之间不可直接比较。该对比是定性的，且来自各基准自身已发表描述的自我报告，而非实测评估。

| Benchmark<br>基准 | Work surface<br>工作面 | | | | Lifecycle<br>生命周期 | | | Runtime evidence<br>运行时证据 | | Oracle<br>判定器 | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | UI<br>界面 | App<br>应用 | Data<br>数据 | Doc/test<br>文档/测试 | Scratch<br>从零 | Fix/ext.<br>修复/扩展 | Review/convert<br>评审/转换 | Action<br>动作 | State<br>状态 | Rule<br>规则 | VLM<br>视觉语言模型 | Agent<br>智能体 |
| Vibe Code Bench v1.1 | ● | ● | ○ | | ● | | | ● | ○ | ● | | ○ |
| CursorBench 3.1 | ○ | | | ○ | ○ | ● | ● | | | ○ | | ● |
| Design2Code | ● | | | | ● | | | | | ○ | ● | |
| Interaction2Code | ● | ● | | | ● | | | ● | ○ | ● | ○ | |
| FrontendBench | ● | ○ | | | ● | | | ● | ○ | ● | | |
| WebArena | | ● | | | | | | ● | ● | ● | | |
| VisualWebArena | | ● | | | | | | ● | ● | ● | ○ | |
| WorkBuddy Web | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |

Table 8. Web benchmark capability matrix. ● = full coverage, ○ = partial coverage, blank = not covered or not applicable. Axes are task-design and verification coverage, not a head-to-head measured evaluation of agent performance; model-judge bias for VLM and agent-judge layers is discussed separately in Section 7.

表 8。Web 基准能力矩阵。● = 完全覆盖，○ = 部分覆盖，空白 = 未覆盖或不适用。各轴向是任务设计与验证覆盖，而非对智能体表现的头对头实测评估；VLM 与智能体评判层的模型评判偏差在第 7 节另行讨论。

Office. Recent benchmarks cover complementary parts of office-agent work. Workspace-Bench 1.0 [16] evaluates tasks with large-scale heterogeneous file dependencies using fine-grained rubrics across multiple agent harnesses. ClawsBench [17] evaluates capability and safety in snapshot-restored simulations of Gmail, Calendar, Docs, Drive, and Slack. OdysseyBench [18] targets long-horizon, multi-application workflows over extended interaction histories, while SpreadsheetBench 2 [19] probes end-to-end construction, repair, and visualization in complex multi-sheet workbooks.

办公。近期基准覆盖办公智能体工作的互补部分。Workspace-Bench 1.0 [16] 使用细粒度评分标准、跨多个智能体评测框架，评估具有大规模异构文件依赖的任务。ClawsBench [17] 评估在 Gmail、Calendar、Docs、Drive 和 Slack 的快照还原仿真中的能力与安全。OdysseyBench [18] 面向跨越延长交互历史的长时程、多应用工作流，而 SpreadsheetBench 2 [19] 探测复杂多工作表工作簿中的端到端构建、修复与可视化。

ClawsBench and OdysseyBench emphasize interaction across multiple applications, SpreadsheetBench 2 focuses on workbook workflows, and Workspace-Bench addresses heterogeneous file dependencies. WorkBuddyBench-Office, the suite's Office subset, focuses on complete hand-offs in local workspaces containing multiple file formats. Agents must carry source information into deliverables, keep related files and state consistent, and respect execution constraints under CodeBuddy Code or Claude Code. Deterministic rule checks verify files, cross-file relations, state changes, side effects, and execution constraints, while an evidence-grounded LLM Judge scores binary semantic rubrics from fixed post-task evidence. Each task sets its own Rule/Judge weight. These comparisons concern task and verification design; the benchmarks use different task units, environments, and scoring schemes.

ClawsBench 与 OdysseyBench 强调跨多个应用的交互，SpreadsheetBench 2 聚焦工作簿工作流，Workspace-Bench 处理异构文件依赖。WorkBuddyBench-Office，即本套件的 Office 子集，聚焦包含多种文件格式的本地工作区中的完整交接。智能体必须将源信息带入交付物，保持相关文件与状态一致，并在 CodeBuddy Code 或 Claude Code 下遵守执行约束。确定性规则检查验证文件、跨文件关系、状态变更、副作用与执行约束，而基于证据的 LLM 评判器根据任务后固定证据对二元语义评分项打分。每个任务设定自己的规则/评判权重。这些对比关乎任务与验证设计；各基准使用不同的任务单位、环境和计分方案。

Security. Existing security-agent benchmarks each cover a slice of the red-team side: Cybench [20] and NYU CTF Bench [21] score professional-level and competition CTF challenges, InterCode-CTF [22] casts CTF solving as interactive coding with execution feedback, CVE-Bench [23] measures autonomous exploitation of real-world web-application CVEs, and Meta's CyberSecEval series [24, 25] assesses cybersecurity risks and capabilities of the models themselves, from insecure code suggestions to offensive-operation assistance. The Security subset differs on two axes: coverage and scoring. Its 60 tasks span red- and blue-team work in a single suite – vulnerability discovery and safe exploitation, malware analysis, security operations, and agent security – rather than CTF or exploitation alone, and every task is scored by a deterministic per-task scoring.py behind five anti-cheat layers, with no LLM judge anywhere. Its whitebox discovery tasks are anchored to real, historical CVEs in widely deployed upstream projects, rebuilt as rewritten, sandboxed environments kept out of public training corpora for contamination resistance.

安全。现有安全智能体基准各自覆盖红队侧的一个切片：Cybench [20] 与 NYU CTF Bench [21] 为专业级和竞赛 CTF 挑战打分，InterCode-CTF [22] 将 CTF 解题建模为带执行反馈的交互式编程，CVE-Bench [23] 衡量对真实 Web 应用 CVE 的自主利用，Meta 的 CyberSecEval 系列 [24, 25] 评估模型自身的网络安全风险与能力，从不安全的代码建议到进攻性操作协助。Security 子集在两个轴向上有所不同：覆盖面与计分。其 60 个任务在同一套件中跨越红队与蓝队工作——漏洞发现与安全利用、恶意软件分析、安全运营和智能体安全——而非仅 CTF 或利用，且每个任务都由确定性的逐任务 scoring.py 在五层反作弊之后计分，全程不使用 LLM 评判器。其白盒发现任务锚定于广泛部署的上游项目中真实的历史 CVE，重建为经改写的沙箱环境，并排除在公开训练语料之外以抵抗污染。

What the suite adds. Breadth and framing differentiate the suite, not a new task type. Code pairs repository-scale tasks with five requester roles and an 18-category taxonomy on colloquial asks, not filed-issue prompts, resistant to searchable-prompt and leaked-answer contamination by construction through freshly authored task directories held back until release. Web unifies the task-type, lifecycle-mode, interaction/state, and judge axes above in one family, combining rule checks, LLM/VLM judgment, and agent-judge verification over running front-end artifacts. Office treats mixed-format, multi-artifact workflows as complete handoffs, measuring machine-checkable workspace state and semantic deliverable quality through separately retained Rule and Judge channels. Security covers the red- and blue-team spectrum under fully deterministic per-task scoring, in a domain where public benchmarks remain scarce. Resistance to searchable prompts and leaked tests or answers rests on freshly authored task directories held back until release and by-construction design; distribution-informed construction rests on distribution-matched tasks, released fully open – task directories, environment images, evaluation code, grading tests, and reference solutions all public – and so independently auditable in full where closed vendors cannot be. These remain the benchmark's own design-time positioning claims, not a measured comparison of agent performance across the compared suites.

本套件所增加的。区分本套件的是广度与框架，而非新的任务类型。Code 将仓库级任务与五种提出者角色、18 类分类体系以及口语化请求（而非已提交 issue 的提示）配对，通过新撰写并在发布前暂缓公开的任务目录，从构建上抵抗可检索提示与泄露答案污染。Web 将上述任务类型、生命周期模式、交互/状态与评判轴向统一到一个系列中，对运行中的前端产物结合规则检查、LLM/VLM 评判与智能体评判验证。Office 将混合格式、多产物工作流视为完整交接，通过分别保留的规则与评判通道衡量机器可检查的工作区状态与语义交付质量。Security 在完全确定性的逐任务计分下覆盖红队与蓝队谱系，而该领域的公开基准仍然稀缺。对可检索提示以及泄露测试或答案的抵抗，依赖于新撰写并在发布前暂缓公开的任务目录以及从构建出发的设计；基于分布的构建依赖于与分布匹配的任务，并完全开放发布——任务目录、环境镜像、评测代码、评分测试和参考解全部公开——因此在闭源厂商无法做到的地方可被完整独立审计。这些仍是本基准自身的设计时定位主张，而非跨所比较套件对智能体表现的实测对比。

## 7 Limitations and Conclusion / 局限与结论

This section discusses current limitations of Tencent WorkBuddy Bench as described in this report, and the near-term work planned to address them.

本节讨论本报告所述腾讯 WorkBuddy Bench 的当前局限，以及计划用于应对这些局限的近期工作。

- **One leaderboard cell uses a modified instruction setup.** All seven models are scored under both harnesses on all four tracks. The one comparability caveat is Claude Opus 4.8's Code score under Claude Code: as noted in Table 6, on top of the disabled AskUserQuestion tool, an explicit do-not-ask, complete-in-one-pass instruction was added for that run, so its setup differs slightly from the other runs, and its score is reported alongside – but not folded into – the Code harness-shift aggregate in Section 5. / **有一个排行榜单元格使用了修改后的指令设置。** 全部七个模型在全部四条赛道上均在两种评测框架下计分。唯一的可比性注意事项是 Claude Opus 4.8 在 Claude Code 下的 Code 分数：如表 6 所述，除禁用 AskUserQuestion 工具外，该次运行还额外加入了明确的「不要提问、一次完成」指令，因此其设置与其他运行略有不同，其分数与第 5 节中的 Code 评测框架偏移汇总并列报告，但不折入该汇总。
- **Single-language emphasis in Code.** The Code subset's open release is dominated by Python tasks; cross-language coverage is limited to a small number of tasks that port target behavior from JavaScript, TypeScript, or Rust projects into Python. Findings in this report about coding difficulty, the coding-versus-data/algorithm gap, and harness divergence should not be assumed to generalize to other programming languages or ecosystems without further evaluation. / **Code 以单一语言为主。** Code 子集的开放发布以 Python 任务为主；跨语言覆盖仅限于少数将 JavaScript、TypeScript 或 Rust 项目的目标行为移植到 Python 的任务。本报告中关于编程难度、编程与数据/算法差距以及评测框架分歧的发现，在未经进一步评估前，不应假定可推广到其他编程语言或生态。
- **Open release creates post-release contamination exposure.** Tencent WorkBuddy Bench is released fully open – task directories, environment images, evaluation code, grading tests, and reference solutions are all public, so that external readers can independently re-run and audit individual task outcomes, not just reproduce the pipeline described earlier in this report. The cost of that openness is that published task content is, from the moment of release, exposed to being scraped into future model training data, which can erode contamination resistance over time. This is mitigated, not eliminated, by dataset versioning – future revisions can retire or replace tasks that show contamination symptoms – rather than by withholding task content. / **开放发布带来发布后的污染暴露。** 腾讯 WorkBuddy Bench 完全开放发布——任务目录、环境镜像、评测代码、评分测试和参考解全部公开，以便外部读者能独立重跑并审计单个任务结果，而不仅仅复现本报告前文所述的流水线。这种开放的代价是：已发布的任务内容从发布那一刻起，就暴露于被抓取进未来模型训练数据的风险，从而可能随时间削弱抗污染性。这一点通过数据集版本管理得到缓解而非消除——未来修订可以退役或替换出现污染症状的任务——而不是通过扣留任务内容。
- **Judge-based components carry model-judge bias.** Web scoring combines rule-based checks with LLM/VLM and agent-judge rubric items over evidence from the running front-end artifact; Office combines deterministic rule checks with an LLM Judge over fixed post-task evidence; and Code additionally computes a diagnostic, weighted LLM-judge score across several dimensions that is not counted in the headline metric. Office retains rule-check outcomes independently, so the Judge cannot alter them, but its semantic-rubric scores remain subject to model-judge bias. More generally, model judges may favor response styles they find familiar or legible, independent of task correctness – a risk this report has not separately quantified. / **基于评判器的组件带有模型评判偏差。** Web 计分将基于规则的检查与针对运行中前端产物证据的 LLM/VLM 及智能体评判评分项相结合；Office 将确定性规则检查与针对任务后固定证据的 LLM 评判器相结合；Code 还额外计算跨若干维度的诊断性加权 LLM 评判分数，该分数不计入头条指标。Office 独立保留规则检查结果，因此评判器无法改动它们，但其语义评分项分数仍受模型评判偏差影响。更一般地，模型评判器可能偏好它们觉得熟悉或易读的应答风格，而与任务正确性无关——本报告尚未单独量化这一风险。
- **Scores are tied to specific serving and harness conditions.** The HY (Hunyuan) endpoint used in this evaluation is served first-party by its provider, while all other models are accessed through third-party serving endpoints, whose parameter configuration and request handling may affect metrics. Likewise, results are tied to the specific builds of the two harnesses used in this evaluation, and metrics may shift as harness versions evolve (Section 4). / **分数绑定于特定的服务与评测框架条件。** 本评估使用的 HY（混元）端点由其提供方第一方服务，而所有其他模型通过第三方服务端点访问，其参数配置与请求处理可能影响指标。同样，结果绑定于本评估所用两个评测框架的特定构建，指标可能随评测框架版本演进而变化（第 4 节）。
- **Office is text-first.** The current Office release covers local, mixed-format workflows but does not require OCR, vision-language models, pixel-level layout judgment, or native desktop-GUI interaction. Office results therefore apply to file handling, state updates, and evidence-based workflow completion, not to visual perception or GUI operation. / **Office 以文本为主。** 当前 Office 发布覆盖本地、混合格式工作流，但不要求 OCR、视觉语言模型、像素级布局判断或原生桌面 GUI 交互。因此 Office 结果适用于文件处理、状态更新和基于证据的工作流完成，而不适用于视觉感知或 GUI 操作。

Near-term work focuses on calibration: continuing Web rubric calibration, and, where feasible, bringing the one modified-instruction configuration (Claude Opus 4.8 on Code under Claude Code) under the standard instruction protocol.

近期工作聚焦校准：继续 Web 评分标准校准，并在可行时，将那一个修改后的指令配置（Claude Code 下 Code 赛道上的 Claude Opus 4.8）纳入标准指令协议。

This report has described Tencent WorkBuddy Bench as released: four subsets sharing one task-directory format, one admission protocol, and one execution harness, together with its leader-board and the limitations stated above. These limitations and scope boundaries are the ones we consider material enough to state explicitly, not an exhaustive list. The suite is released fully open – task directories, environment images, evaluation code, grading tests, and reference solutions are all public for offline third-party testing and audit – and the near-term trajectory beyond this revision is a public leaderboard with expanding model coverage across both harnesses.

本报告已按发布状态描述腾讯 WorkBuddy Bench：四个子集共享一种任务目录格式、一套准入协议和一套执行评测框架，以及其排行榜和上述局限。这些局限与范围边界是我们认为有必要明确陈述的，而非穷尽清单。本套件完全开放发布——任务目录、环境镜像、评测代码、评分测试和参考解全部公开，供离线第三方测试与审计——本修订之后的近期轨迹是一个公开排行榜，并在两种评测框架上扩展模型覆盖。

## Contributors / 贡献者

Siqi Cai¹*, Shaopeng Chen⁴*, Xiang Fei¹*, Yong Mao¹*, Zihan Xu¹*, Zhiheng Lyu³*, Zhijian Shao²*, Yuchen Shi¹, Shuwen Zhang¹, Chaofan Qiu¹, Linjie Che³, Xiaoxi Zhao³, Feng Wu³, Kai Zhang³, Chaofan Zhu³, Yubin Qi³, Xiaoyun Liang³, Peijie Dong³, Yunhao Zhang³, Yuanjie Zhu, Ling Jiang², Xianjun Zhang², Zhehang Chu², Anyuan Sang², Zhen Feng², Sen Nie², Shi Wu², Yuanzhen Xu⁴, Xin Li⁴, Ning Yang⁴, Zhiqiang Dong⁴, Hande Dong³, Qiang Lin³, Yi Liu³, Yunsheng Wu¹, Ke Li¹†, Xing Sun¹

（作者名单按原文保留；*同等贡献，†项目负责人）

¹Youtu Lab · ²Keen Security Lab · ³Workbuddy · ⁴Yunding Security Lab

¹优图实验室 · ²科恩安全实验室 · ³Workbuddy · ⁴云鼎安全实验室

*These authors contributed equally to this work. The author order was determined alphabetically.

*这些作者对本工作贡献同等。作者顺序按字母顺序确定。

†Project Lead.

†项目负责人。

## References / 参考文献

[1] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan. SWE-bench: Can language models resolve real-world github issues? In International Conference on Learning Representations (ICLR), 2024. URL https://arxiv.org/abs/2310.06770.

[1] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan. SWE-bench：语言模型能否解决真实世界的 GitHub 问题？发表于 International Conference on Learning Representations (ICLR)，2024。URL https://arxiv.org/abs/2310.06770。

[2] OpenAI. Introducing SWE-bench verified. OpenAI blog, 2024. URL https://openai.com/index/introducing-swe-bench-verified/.

[2] OpenAI. 介绍 SWE-bench Verified。OpenAI 博客，2024。URL https://openai.com/index/introducing-swe-bench-verified/。

[3] Chenglei Si, Yanzhe Zhang, Zhengyuan Yang, Ruibo Liu, and Diyi Yang. Design2code: How far are we from automating front-end engineering? In Proceedings of the Association for Computational Linguistics (ACL), 2024. URL https://arxiv.org/abs/2403.03163.

[3] Chenglei Si, Yanzhe Zhang, Zhengyuan Yang, Ruibo Liu, and Diyi Yang. Design2Code：我们离自动化前端工程还有多远？发表于 Proceedings of the Association for Computational Linguistics (ACL)，2024。URL https://arxiv.org/abs/2403.03163。

[4] Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Graham Neubig. WebArena: A realistic web environment for building autonomous agents. In International Conference on Learning Representations (ICLR), 2024. URL https://arxiv.org/abs/2307.13854.

[4] Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Graham Neubig. WebArena：用于构建自主智能体的真实 Web 环境。发表于 International Conference on Learning Representations (ICLR)，2024。URL https://arxiv.org/abs/2307.13854。

[5] Cursor. How we compare model quality in Cursor. Cursor blog, 2026. URL https://cursor.com/blog/cursorbench.

[5] Cursor. 我们如何在 Cursor 中比较模型质量。Cursor 博客，2026。URL https://cursor.com/blog/cursorbench。

[6] Harbor Framework Team. Harbor: A framework for evaluating and optimizing agents and models in container environments. GitHub repository, Laude Institute, 2026. URL https://github.com/laude-institute/harbor. DOI: 10.5281/zenodo.20953922.

[6] Harbor Framework Team. Harbor：在容器环境中评估与优化智能体和模型的框架。GitHub 仓库，Laude Institute，2026。URL https://github.com/laude-institute/harbor。DOI: 10.5281/zenodo.20953922。

[7] Wenting Zhao, Nan Jiang, Celine Lee, Justin T. Chiu, Claire Cardie, Matthias Gallé, and Alexander M. Rush. Commit0: Library generation from scratch, 2024. URL https://arxiv.org/abs/2412.01769.

[7] Wenting Zhao, Nan Jiang, Celine Lee, Justin T. Chiu, Claire Cardie, Matthias Gallé, and Alexander M. Rush. Commit0：从零生成程序库，2024。URL https://arxiv.org/abs/2412.01769。

[8] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. LiveCodeBench: Holistic and contamination free evaluation of large language models for code, 2024. URL https://arxiv.org/abs/2403.07974.

[8] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. LiveCodeBench：对代码大语言模型的整体且无污染评估，2024。URL https://arxiv.org/abs/2403.07974。

[9] Tianyang Liu, Canwen Xu, and Julian J. McAuley. RepoBench: Benchmarking repository-level code auto-completion systems. In International Conference on Learning Representations (ICLR), 2024. URL https://arxiv.org/abs/2306.03091.

[9] Tianyang Liu, Canwen Xu, and Julian J. McAuley. RepoBench：仓库级代码自动补全系统基准评测。发表于 International Conference on Learning Representations (ICLR)，2024。URL https://arxiv.org/abs/2306.03091。

[10] Paul Gauthier. Aider polyglot benchmark. Aider documentation, 2024. URL https://aider.chat/docs/leaderboards/.

[10] Paul Gauthier. Aider 多语言基准。Aider 文档，2024。URL https://aider.chat/docs/leaderboards/。

[11] Terminal-Bench Team. Terminal-bench: A benchmark for ai agents in terminal environments. Project website, 2024. URL https://www.tbench.ai/.

[11] Terminal-Bench Team. Terminal-Bench：面向终端环境中 AI 智能体的基准。项目网站，2024。URL https://www.tbench.ai/。

[12] Hung Tran, Langston Nashold, Rayan Krishnan, Antoine Bigeard, and Alex Gu. Vibe Code Bench: Evaluating AI models on end-to-end web application development. In ACM Conference on AI and Agentic Systems (ACM CAIS), 2026. doi: 10.1145/3786335.3813180. URL https://arxiv.org/abs/2603.04601.

[12] Hung Tran, Langston Nashold, Rayan Krishnan, Antoine Bigeard, and Alex Gu. Vibe Code Bench：评估 AI 模型的端到端 Web 应用开发能力。发表于 ACM Conference on AI and Agentic Systems (ACM CAIS)，2026。doi: 10.1145/3786335.3813180。URL https://arxiv.org/abs/2603.04601。

[13] Jingyu Xiao, Yuxuan Wan, Yintong Huo, Zixin Wang, Xinyi Xu, Wenxuan Wang, Zhiyao Xu, Yuhang Wang, and Michael R. Lyu. Interaction2Code: Benchmarking MLLM-based interactive webpage code generation from interactive prototyping, 2024. URL https://arxiv.org/abs/2411.03292.

[13] Jingyu Xiao, Yuxuan Wan, Yintong Huo, Zixin Wang, Xinyi Xu, Wenxuan Wang, Zhiyao Xu, Yuhang Wang, and Michael R. Lyu. Interaction2Code：从交互原型出发、基于 MLLM 的交互网页代码生成基准，2024。URL https://arxiv.org/abs/2411.03292。

[14] Hongda Zhu, Yiwen Zhang, Bing Zhao, Jingzhe Ding, Siyao Liu, Tong Liu, Dandan Wang, Yanan Liu, and Zhaojian Li. FrontendBench: A benchmark for evaluating llms on front-end development via automatic evaluation, 2025. URL https://arxiv.org/abs/2506.13832.

[14] Hongda Zhu, Yiwen Zhang, Bing Zhao, Jingzhe Ding, Siyao Liu, Tong Liu, Dandan Wang, Yanan Liu, and Zhaojian Li. FrontendBench：通过自动评估衡量 LLM 前端开发能力的基准，2025。URL https://arxiv.org/abs/2506.13832。

[15] Jing Yu Koh, Robert Lo, Lawrence Jang, Vikram Duvvur, Ming Chong Lim, Po-Yu Huang, Graham Neubig, Shuyan Zhou, Ruslan Salakhutdinov, and Daniel Fried. VisualWebArena: Evaluating multimodal agents on realistic visual web tasks. In Proceedings of the Association for Computational Linguistics (ACL), 2024. URL https://arxiv.org/abs/2401.13649.

[15] Jing Yu Koh, Robert Lo, Lawrence Jang, Vikram Duvvur, Ming Chong Lim, Po-Yu Huang, Graham Neubig, Shuyan Zhou, Ruslan Salakhutdinov, and Daniel Fried. VisualWebArena：在真实视觉 Web 任务上评估多模态智能体。发表于 Proceedings of the Association for Computational Linguistics (ACL)，2024。URL https://arxiv.org/abs/2401.13649。

[16] Zirui Tang, Xuanhe Zhou, Yumou Liu, Linchun Li, Yukai Wu, Weizheng Wang, Hongzhang Huang, Wei Zhou, Jun Zhou, Jiachen Song, Shaoli Yu, Jinqi Wang, Zihang Zhou, Hongyi Zhou, Yuting Lv, Jinyang Li, Jiashuo Liu, Ruoyu Chen, Chunwei Liu, GuoLiang Li, Jihua Kang, and Fan Wu. Workspace-Bench 1.0: Benchmarking AI agents on workspace tasks with large-scale file dependencies, 2026. URL https://arxiv.org/abs/2605.03596.

[16] Zirui Tang, Xuanhe Zhou, Yumou Liu, Linchun Li, Yukai Wu, Weizheng Wang, Hongzhang Huang, Wei Zhou, Jun Zhou, Jiachen Song, Shaoli Yu, Jinqi Wang, Zihang Zhou, Hongyi Zhou, Yuting Lv, Jinyang Li, Jiashuo Liu, Ruoyu Chen, Chunwei Liu, GuoLiang Li, Jihua Kang, and Fan Wu. Workspace-Bench 1.0：针对具有大规模文件依赖的工作区任务评测 AI 智能体，2026。URL https://arxiv.org/abs/2605.03596。

[17] Xiangyi Li, Kyoung Whan Choe, Yimin Liu, Xiaokun Chen, Chujun Tao, Bingran You, Wenbo Chen, Zonglin Di, Jiankai Sun, Shenghan Zheng, Jiajun Bao, Yuanli Wang, Weixiang Yan, Yiyuan Li, and Han-chung Lee. ClawsBench: Evaluating capability and safety of LLM productivity agents in simulated workspaces, 2026. URL https://arxiv.org/abs/2604.05172.

[17] Xiangyi Li, Kyoung Whan Choe, Yimin Liu, Xiaokun Chen, Chujun Tao, Bingran You, Wenbo Chen, Zonglin Di, Jiankai Sun, Shenghan Zheng, Jiajun Bao, Yuanli Wang, Weixiang Yan, Yiyuan Li, and Han-chung Lee. ClawsBench：评估模拟工作区中 LLM 生产力智能体的能力与安全，2026。URL https://arxiv.org/abs/2604.05172。

[18] Weixuan Wang, Dongge Han, Daniel Madrigal Diaz, Jin Xu, Victor Rühle, and Saravan Rajmohan. OdysseyBench: Evaluating LLM agents on long-horizon complex office application workflows, 2025. URL https://arxiv.org/abs/2508.09124.

[18] Weixuan Wang, Dongge Han, Daniel Madrigal Diaz, Jin Xu, Victor Rühle, and Saravan Rajmohan. OdysseyBench：评估 LLM 智能体在长时程复杂办公应用工作流上的表现，2025。URL https://arxiv.org/abs/2508.09124。

[19] Jian Zhu, Yuzheng Zhang, Zeyao Ma, Bohan Zhang, Armin Schoepf, Daniel Woloch, Peter Yiliu Wang, Guangyu Robert Yang, Samuel Jacob, Siddharth Nagisetty, Abhiram Chundru, Jean Lin, Spencer Mateega, and Jing Zhang. SpreadsheetBench 2: Evaluating agents on end-to-end business spreadsheet workflows, 2026. URL https://arxiv.org/abs/2606.29955.

[19] Jian Zhu, Yuzheng Zhang, Zeyao Ma, Bohan Zhang, Armin Schoepf, Daniel Woloch, Peter Yiliu Wang, Guangyu Robert Yang, Samuel Jacob, Siddharth Nagisetty, Abhiram Chundru, Jean Lin, Spencer Mateega, and Jing Zhang. SpreadsheetBench 2：评估智能体在端到端商务电子表格工作流上的表现，2026。URL https://arxiv.org/abs/2606.29955。

[20] Andy K. Zhang, Neil Perry, Riya Dulepet, Joey Ji, Celeste Menders, Justin W. Lin, Eliot Jones, Gashon Hussein, Samantha Liu, Donovan Jasper, et al. Cybench: A framework for evaluating cybersecurity capabilities and risks of language models. In International Conference on Learning Representations (ICLR), 2025. URL https://arxiv.org/abs/2408.08926.

[20] Andy K. Zhang, Neil Perry, Riya Dulepet, Joey Ji, Celeste Menders, Justin W. Lin, Eliot Jones, Gashon Hussein, Samantha Liu, Donovan Jasper, et al. Cybench：评估语言模型网络安全能力与风险的框架。发表于 International Conference on Learning Representations (ICLR)，2025。URL https://arxiv.org/abs/2408.08926。

[21] Minghao Shao, Sofija Jancheska, Meet Udeshi, Brendan Dolan-Gavitt, Haoran Xi, Kimberly Milner, Boyuan Chen, Max Yin, Siddharth Garg, Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri, and Muhammad Shafique. NYU CTF Bench: A scalable open-source benchmark dataset for evaluating LLMs in offensive security. In Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track, 2024. URL https://arxiv.org/abs/2406.05590.

[21] Minghao Shao, Sofija Jancheska, Meet Udeshi, Brendan Dolan-Gavitt, Haoran Xi, Kimberly Milner, Boyuan Chen, Max Yin, Siddharth Garg, Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri, and Muhammad Shafique. NYU CTF Bench：用于评估 LLM 进攻性安全能力的可扩展开源基准数据集。发表于 Advances in Neural Information Processing Systems (NeurIPS)，Datasets and Benchmarks Track，2024。URL https://arxiv.org/abs/2406.05590。

[22] John Yang, Akshara Prabhakar, Karthik Narasimhan, and Shunyu Yao. InterCode: Standardizing and benchmarking interactive coding with execution feedback. In Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track, 2023. URL https://arxiv.org/abs/2306.14898.

[22] John Yang, Akshara Prabhakar, Karthik Narasimhan, and Shunyu Yao. InterCode：标准化并基准评测带执行反馈的交互式编程。发表于 Advances in Neural Information Processing Systems (NeurIPS)，Datasets and Benchmarks Track，2023。URL https://arxiv.org/abs/2306.14898。

[23] Yuxuan Zhu, Antony Kellermann, Dylan Bowman, Philip Li, Akul Gupta, Adarsh Danda, Richard Fang, Conner Jensen, Eric Ihli, Jason Benn, Jet Geronimo, Avi Dhir, Sudhit Rao, Kaicheng Yu, Twm Stone, and Daniel Kang. CVE-Bench: A benchmark for AI agents' ability to exploit real-world web application vulnerabilities. In International Conference on Machine Learning (ICML), 2025. URL https://arxiv.org/abs/2503.17332.

[23] Yuxuan Zhu, Antony Kellermann, Dylan Bowman, Philip Li, Akul Gupta, Adarsh Danda, Richard Fang, Conner Jensen, Eric Ihli, Jason Benn, Jet Geronimo, Avi Dhir, Sudhit Rao, Kaicheng Yu, Twm Stone, and Daniel Kang. CVE-Bench：评估 AI 智能体利用真实 Web 应用漏洞能力的基准。发表于 International Conference on Machine Learning (ICML)，2025。URL https://arxiv.org/abs/2503.17332。

[24] Manish Bhatt, Sahana Chennabasappa, Yue Li, Cyrus Nikolaidis, Daniel Song, Shengye Wan, Faizan Ahmad, Cornelius Aschermann, Yaohui Chen, Dhaval Kapil, David Molnar, Spencer Whitman, and Joshua Saxe. CyberSecEval 2: A wide-ranging cybersecurity evaluation suite for large language models, 2024. URL https://arxiv.org/abs/2404.13161.

[24] Manish Bhatt, Sahana Chennabasappa, Yue Li, Cyrus Nikolaidis, Daniel Song, Shengye Wan, Faizan Ahmad, Cornelius Aschermann, Yaohui Chen, Dhaval Kapil, David Molnar, Spencer Whitman, and Joshua Saxe. CyberSecEval 2：面向大语言模型的广泛网络安全评估套件，2024。URL https://arxiv.org/abs/2404.13161。

[25] Shengye Wan, Cyrus Nikolaidis, Daniel Song, David Molnar, James Crnkovich, Jayson Grace, Manish Bhatt, Sahana Chennabasappa, Spencer Whitman, Stephanie Ding, Vlad Ionescu, Yue Li, and Joshua Saxe. CyberSecEval 3: Advancing the evaluation of cybersecurity risks and capabilities in large language models, 2024. URL https://arxiv.org/abs/2408.01605.

[25] Shengye Wan, Cyrus Nikolaidis, Daniel Song, David Molnar, James Crnkovich, Jayson Grace, Manish Bhatt, Sahana Chennabasappa, Spencer Whitman, Stephanie Ding, Vlad Ionescu, Yue Li, and Joshua Saxe. CyberSecEval 3：推进大语言模型网络安全风险与能力评估，2024。URL https://arxiv.org/abs/2408.01605。
