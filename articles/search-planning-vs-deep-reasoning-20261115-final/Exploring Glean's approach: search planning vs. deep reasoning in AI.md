## Key Takeaways / 核心洞察

> 阅读笔记（凡哥）：以下 4 点为归档时补充的解读与引申，非原文内容；原文全文与逐段中英对照见下文。

### 1. How Waldo works / Waldo 智能体搜索模型的工作原理

**原文明确写出**：Waldo 是一个只做一件事的专用智能体搜索模型 —— 决定*搜什么、去哪搜、何时停*。底模是紧凑的开放模型 NVIDIA Nemotron 3 Nano，用 DPO（直接偏好优化）+ 强化学习两阶段后训练，专攻企业检索的工具使用规划；训练数据是 Glean 既有智能体系统在生产环境的**匿名行为轨迹**，只记录查了哪些连接器、顺序、需要几轮迭代，不含任何企业内容，因此「学的是检索策略，不是专有信息」。生产环境中它跑在查询流水线最前面：跨三个检索面迭代 —— 内部搜索（文档、消息、知识库）、员工搜索（人员目录与组织图，经 Enterprise Graph）、网页搜索 —— 并用证据阈值判断结果是否够用。关键能力是**检索压缩**：通过后训练学到「一次搜索就能找到通用模型要几轮才找到的内容」，识别哪些连接器组合对特定查询类型足以凑齐证据，从而减少检索轮次而不牺牲召回。交接点很明确：证据足够时，把带**来源归因和权限元数据**的上下文打包交给前沿模型；前沿模型从不规划搜索，只做推理、综合与带引用的回答。因为职责边界窄，Waldo 可独立于推理模型更新、监控和约束，比前沿模型的开放式生成更易审计。

### 2. The Agentic Engine handoff / 与 Glean Agentic Engine 的关系

**原文明确写出**（与你的表述几乎逐字一致）：`Glean's Agentic Engine coordinates this handoff: the specialized model handles query decomposition, connector selection, and evidence gathering, then passes compressed, permission-filtered context to the frontier model for synthesis and cited response generation.` —— Agentic Engine 协调这次交接：专用模型负责查询分解、连接器选择和证据收集，再把压缩、按权限过滤的上下文交给前沿模型，由其综合并生成带引用的回答。补充两点上下文：Agentic Engine 用这种分离架构把前沿模型容量**留给真正需要大模型的环节**（多步推断、矛盾消解、引用生成）；搜索规划模型每次调用延迟约为前沿模型的十二分之一，只消耗一小部分 token 且回答质量不回退。FAQ 里还明确否定了「这套架构是否取代前沿模型」——答案是 No，两者是按任务分工。文章把检索与推理称为「两个不同学科，而不是一个 prompt」。

### 3. Enterprise Graph & Personal Graph / 与企业图谱、个人图谱的关系

**原文明确写出**：搜索规划层并不孤立运行，它会查询 **Enterprise Graph**（人、内容、关系、互动的组织级结构化地图）来判断某个问题该去哪些来源找；**Personal Graph** 则提供个体上下文：角色、团队归属、近期活动、文档互动和访问权限。最直观的例子就是同一个查询 `"Q1 revenue"`：销售代表提问时，规划模型优先路由到 CRM 仪表盘、近期交易摘要和团队共享预测；财务分析师提同样的问题时，则路由到 ERP 导出、董事会级财务报告和会计系统数据。原文原句是 `The query is identical. The search plan is entirely different.`（查询相同，搜索计划完全不同）。这正是企业检索与「同一查询所有人看到相同结果」的网页级搜索的区别。
**一处校准**：原文说的是**搜索计划／路由的数据源不同**（因而回答自然不同），并未直接表述「两人会获得不同的回答」；另外图谱在这里承担两件事 —— 既指引检索计划（角色、团队、活动），也支撑上游权限过滤（未授权文档根本不进上下文窗口，前沿模型无法引用、转述或推断）。把它概括成「不仅是文档权限」是对的，但更精确的说法是「图谱同时驱动计划与治理，权限执行发生在前沿模型之前」。

### 4. Value = broader access, not just savings / 价值：从高价值用例走向更广覆盖

**原文明确写出**（这一条不是推断）：规划阶段约 **50% 延迟下降、25% token 减少**；单次调用约 250 ms 对比前沿推理模型约 3 秒，约 10 倍快、约十二分之一延迟。更重要的是文章把它推到了部署经济学：`Lower latency and lower cost per query also change who gets access to AI assistants. When every query runs through a frontier model end to end, the economics limit deployment to high-value use cases — analysts, executives, specialized knowledge workers.` 当每次查询端到端都跑前沿模型时，成本把部署限制在分析师、高管、专业知识工作者这类高价值用例；而检索交给小而快的模型、只有推理阶段用前沿算力后，单次成本降到足以服务**更广泛的人群**，支撑组织级铺开（organization-wide deployment）。文章还给了规模算账：1 万名知识工作者、每人每天 20 次智能体查询，就是每天 20 万次检索循环，若每轮 3–5 次前沿模型规划迭代，延迟与 token 开销会从「舍入误差」变成一项正式成本。
**一处校准**：原文说的是「覆盖更广泛的用户群体／全员部署」（broader populations），你表述的「覆盖更加丰富的场景」是合理延伸；原文的直接论证是**成本与延迟决定了谁能用上**，而不是场景种类本身变多。

> 作者: The Glean Team | 页面日期: Jun 04, 2026（Last updated） | 阅读时长: 11 分钟

> 原文链接: https://www.glean.com/perspectives/exploring-gleans-approach-search-planning-vs-deep-reasoning-in-ai

![Exploring Glean's approach: search planning vs. deep reasoning in AI](images/img_01_18d5ccbc.png)

Glean separates search planning from deep reasoning by assigning retrieval orchestration to a purpose-trained model and reserving frontier-model compute for synthesis and response generation. These two operations — deciding where to look and actually thinking through what you find — demand fundamentally different resources, yet most systems today treat them as one job.

Glean 把搜索规划与深度推理拆开：检索编排交给专门训练的模型，前沿模型算力留给综合与回答生成。这两件事 —— 决定去哪找，以及真正想清楚找到的东西 —— 需要的资源根本不同，但如今多数系统把它们当成一份工作。

The distinction between retrieval planning and synthesis matters because [enterprise AI search](https://www.glean.com/blog/enterprise-ai-search-rag) spans dozens of data sources, each with its own permissions, schemas, and query patterns. When a single large language model handles both the mechanical work of routing queries and the intellectual work of synthesizing answers, organizations pay frontier-model prices for tasks that don't require frontier-model intelligence.

区分检索规划与综合很重要，因为[企业 AI 搜索](https://www.glean.com/blog/enterprise-ai-search-rag)横跨几十个数据源，每个都有自己的权限、结构和查询模式。当一个大语言模型同时承担「路由查询」这种机械活和「综合答案」这种智力活时，企业就是在为不需要前沿级智能的任务付前沿模型的价格。

Understanding how these functions differ — and why separating them changes the economics of [enterprise search](https://www.glean.com/blog/the-definitive-guide-to-ai-based-enterprise-search-for-2025) — is key to evaluating how AI retrieval architectures will evolve.

理解这两种职能的差异、以及为什么拆开会改变[企业搜索](https://www.glean.com/blog/the-definitive-guide-to-ai-based-enterprise-search-for-2025)的成本结构，是判断 AI 检索架构将如何演进的关键。

## What is the difference between search planning and deep reasoning in enterprise AI? / 企业 AI 中，搜索规划与深度推理有什么区别？

Search planning is the structured, mechanical process of deciding which data sources to query, what tool calls to make, and when enough evidence has been gathered. It follows predictable patterns: parse the user's question, identify relevant connectors, issue parallel queries, evaluate whether the retrieved documents are sufficient, and either refine the search or hand off results. The operations are iterative and latency-sensitive — each additional planning step adds wait time that the user feels directly.

搜索规划是一个结构化、机械化的过程：决定查哪些数据源、发起哪些工具调用、以及证据何时才算收齐。它有可预测的模式：解析用户问题、识别相关连接器、并行发起查询、评估检索到的文档是否充分，然后要么改写搜索、要么交接结果。这类操作是迭代的、对延迟敏感的 —— 每多一步规划，用户就直接多等一会儿。

[Deep reasoning](https://www.glean.com/product/agentic-engine) is what happens after retrieval. A model interprets the gathered context, draws inferences across multiple sources, resolves contradictions, and produces a grounded response with citations. This work demands high-parameter models optimized for nuance, abstraction, and multi-step logic — the kind of processing where a frontier model earns its cost.

[深度推理](https://www.glean.com/product/agentic-engine)发生在检索之后：模型解读收集到的上下文、跨多个来源做推断、消解矛盾，并产出有引用支撑的回答。这类工作要求为细腻度、抽象和多步逻辑优化过的高参数模型 —— 也正是在这类处理上，前沿模型才值它的价钱。

The computational profiles are mismatched. A default reasoning model takes roughly three seconds per call, while a purpose-trained search planning model can execute the same retrieval step in about 250 milliseconds. Most enterprise AI systems today use a single frontier model for both jobs, which means organizations pay frontier-model prices and accept frontier-model latency for what is, during the retrieval phase, a mechanical task.

两者的计算画像并不匹配。默认推理模型每次调用约需 3 秒，而专门训练的搜索规划模型执行同一个检索步骤只需约 250 毫秒。如今多数企业 AI 系统用同一个前沿模型干这两件事，等于在检索阶段这个机械任务上，既付前沿模型的价格、又忍受前沿模型的延迟。

Glean's approach with Waldo — a search planning model built on NVIDIA Nemotron 3 Nano — splits these roles, achieving approximately 50% lower latency and 25% fewer tokens during the planning phase by assigning retrieval orchestration to a smaller, faster model trained specifically for that work.

Glean 用 Waldo（基于 NVIDIA Nemotron 3 Nano 的搜索规划模型）把两种角色拆开：把检索编排交给专为这份工作训练的更小、更快的模型，从而在规划阶段实现约 50% 的延迟下降与 25% 的 token 节省。

## Why separating search planning from deep reasoning improves enterprise AI efficiency / 为什么拆开能提升企业 AI 效率

The cost arithmetic changes when you look at scale. An organization with 10,000 knowledge workers generating even modest query volume — say 20 agentic queries per person per day — runs 200,000 retrieval loops daily. If each loop requires three to five search-planning iterations through a frontier model at roughly three seconds per call, the cumulative latency and token spend become a line item, not a rounding error.

放到规模上看，成本算法就变了。一个拥有 1 万名知识工作者的组织，哪怕查询量很温和 —— 假设每人每天 20 次智能体查询 —— 每天也有 20 万次检索循环。若每次循环都要通过前沿模型做 3 到 5 轮搜索规划、每轮约 3 秒，累计延迟与 token 开销就成了一项正式成本，而不是舍入误差。

A specialized smaller model post-trained for tool-use decisions breaks this pattern. Instead of routing every retrieval step through the same high-parameter model that handles synthesis, the search-planning model runs the retrieval loop independently — an approach consistent with how [agentic RAG](https://www.glean.com/blog/agentic-rag-explained) enhances traditional retrieval by letting intelligent agents adapt in real time. It decides which corpora to query — internal documents, people directories, web sources — evaluates whether enough evidence exists, and assembles grounded context before a frontier model ever sees the request.

为工具使用决策做过后训练的小型专用模型打破了这个模式：不再把每一步检索都路由给负责综合的同一个高参数模型，而是由搜索规划模型独立跑检索循环 —— 这与[智能体 RAG](https://www.glean.com/blog/agentic-rag-explained)让智能体实时自适应、从而增强传统检索的思路一致。它决定查哪些语料（内部文档、人员目录、网络来源）、判断证据是否充分，并在前沿模型看到请求之前就把有据可依的上下文组装好。

The result is a system where token budgets go where they matter. Glean's Agentic Engine uses this split architecture to reserve frontier-model capacity for reasoning — the multi-step inference, contradiction resolution, and citation generation that actually requires a large model's capabilities. The [search planning](https://www.glean.com/blog/agentic-reasoning-future-ai) phase, handled by a purpose-trained model running at roughly one-twelfth the latency per call, consumes a fraction of the tokens without regression in answer quality.

结果是 token 预算被花在真正要紧的地方。Glean 的 Agentic Engine 用这套分离架构，把前沿模型容量留给推理 —— 多步推断、矛盾消解、引用生成，这些才真正需要大模型能力。[搜索规划](https://www.glean.com/blog/agentic-reasoning-future-ai)阶段交给专用模型，每次调用延迟约为十二分之一，只消耗一小部分 token，而回答质量不回退。

This architecture is not about replacing frontier models or treating them as overhead. Frontier models are essential for the reasoning step.

这套架构不是要替换前沿模型、也不是把它们当累赘。前沿模型在推理环节不可或缺。

The waste comes from feeding them tasks they're overqualified for — parsing connector schemas, deciding whether to query Confluence or Slack first, determining that three retrieved documents aren't sufficient and a fourth search is needed. A 2026 analysis by Clarifai found that small language models can deliver [10–30x cheaper inference](https://www.clarifai.com/blog/top-cost-efficient-small-models) than large models, with enterprises using smaller models for 80% of their API calls and cutting compute costs by up to 70%. A compact model post-trained on those exact decision patterns handles them with equivalent accuracy at a fraction of the compute.

浪费来自把「大材小用」的任务喂给它们 —— 解析连接器结构、决定先查 Confluence 还是 Slack、判断三份文档不够还要再搜第四次。Clarifai 2026 年的一项分析发现，小语言模型的[推理成本可以低 10–30 倍](https://www.clarifai.com/blog/top-cost-efficient-small-models)；企业把 80% 的 API 调用交给小模型，可削减最多 70% 的算力成本。一个针对这些决策模式做过后训练的紧凑模型，能以一小部分算力达到同等准确度。

For enterprise teams evaluating AI infrastructure costs, the implication is straightforward: every token spent on search planning through a frontier model is a token that could have been spent on deeper, more accurate reasoning.

对评估 AI 基础设施成本的企业团队来说，结论很直接：花在「用前沿模型做搜索规划」上的每一个 token，本可以用于更深、更准确的推理。

## How the Waldo agentic search model works / Waldo 智能体搜索模型如何工作

Waldo is a purpose-built agentic search model designed to handle one job well: deciding what to search, where to search, and when to stop searching. Built on a compact open foundation model (NVIDIA Nemotron 3 Nano), Waldo was post-trained using two techniques — [direct preference optimization](https://arxiv.org/abs/2305.18290) (DPO) and reinforcement learning — to specialize in tool-use planning for enterprise retrieval.

Waldo 是专门构建的智能体搜索模型，只把一件事做好：决定搜什么、去哪搜、何时停。它建立在紧凑的开放基础模型（NVIDIA Nemotron 3 Nano）之上，用两种技术做后训练 —— [直接偏好优化](https://arxiv.org/abs/2305.18290)（DPO）与强化学习 —— 专攻企业检索中的工具使用规划。

The training data came from anonymized behavioral traces of how Glean's existing agentic system planned searches across production environments. These traces captured the decision patterns — which connectors were queried, in what order, how many iterations were needed — without exposing any enterprise content. The model learned retrieval strategies, not proprietary information.

训练数据来自 Glean 既有智能体系统在生产环境中规划搜索的匿名行为轨迹。这些轨迹只记录决策模式 —— 查了哪些连接器、顺序如何、需要几轮迭代 —— 不暴露任何企业内容。模型学到的是检索策略，不是专有信息。

In production, Waldo runs first in the query pipeline. When a user asks a question through Glean Assistant, Waldo evaluates the query and plans tool use across three retrieval surfaces: internal search (documents, messages, knowledge bases), employee search (people directories and org charts via the Enterprise Graph), and web search. It iterates across these surfaces, evaluating retrieved results against an evidence threshold before passing the assembled context forward.

在生产环境中，Waldo 跑在查询流水线最前面。用户通过 Glean Assistant 提问时，Waldo 评估查询，并在三个检索面上规划工具使用：内部搜索（文档、消息、知识库）、员工搜索（经由 Enterprise Graph 的人员目录与组织图）和网页搜索。它跨这些面迭代，按证据阈值评估检索结果，再把组装好的上下文向后传递。

A key capability is retrieval compression. Through its post-training on effective search patterns, Waldo learned to find in a single search iteration what previously required several iterations from a general-purpose model. It recognizes which connector combinations tend to produce sufficient evidence for specific query types and routes accordingly, cutting retrieval cycles without sacrificing recall.

一项关键能力是检索压缩。通过对高效搜索模式的后训练，Waldo 学会了一次搜索迭代就找到通用模型过去要几轮才能找到的内容。它能识别哪些连接器组合对特定查询类型通常足以凑齐证据，并据此路由，从而减少检索轮次而不牺牲召回。

The handoff point is explicit. Once Waldo determines that enough grounded evidence exists, it packages the retrieved context — with source attribution and permission metadata intact — and passes it to the frontier model.

交接点非常明确。一旦 Waldo 判定已有足够的有据可依的证据，它就把检索到的上下文打包 —— 来源归因与权限元数据完整保留 —— 交给前沿模型。

The frontier model never plans a search. It receives pre-assembled, permission-aware context and focuses entirely on reasoning, synthesis, and generating cited responses.

前沿模型从不规划搜索。它收到的是预先组装好、带权限感知的上下文，于是可以全力做推理、综合与生成带引用的回答。

Because Waldo's scope is limited to tool-use planning, it can be updated, monitored, and constrained independently from the reasoning model — a narrower decision boundary that's easier to audit than a frontier model's open-ended generation.

由于 Waldo 的职责仅限于工具使用规划，它可以独立于推理模型被更新、监控和约束 —— 决策边界更窄，比前沿模型的开放式生成更易审计。

## What challenges does this architecture address in enterprise workflows? / 这套架构解决企业工作流中的哪些问题

Separated search planning addresses four compounding problems that erode enterprise AI adoption: latency, cost, accuracy, and governance. Understanding the full scope of [agentic reasoning](https://www.glean.com/blog/a-complete-guide-to-agentic-reasoning) helps contextualize why each of these challenges worsens at scale — and why they interact, as slow responses drive workarounds, workarounds reduce data quality, and reduced data quality undermines trust in the system.

把搜索规划拆开，解决的是四个相互叠加、共同侵蚀企业 AI 落地的问题：延迟、成本、准确性和治理。理解[智能体推理](https://www.glean.com/blog/a-complete-guide-to-agentic-reasoning)的全貌，有助于看清为什么这些问题在规模化时都会恶化、以及它们如何互相作用：响应慢会催生绕开系统的土办法，土办法降低数据质量，数据质量下降又削弱对系统的信任。

**Latency compounds with every retrieval step.** Knowledge workers expect near-instant responses from search tools. When an agentic system loops a frontier model through multiple retrieval iterations — each taking roughly three seconds — a query that requires four search steps introduces 12 seconds of wait time before reasoning even begins.

延迟随每一步检索叠加。 知识工作者期待搜索工具近乎即时响应。当智能体系统让前沿模型跑多轮检索迭代、每轮约 3 秒时，一个需要四步搜索的查询，在推理还没开始之前就产生了 12 秒等待。

That delay drives users back to manual search or tribal knowledge, which defeats the purpose of deploying an AI system.

这种延迟会把用户推回手工搜索或「问老同事」，也就违背了部署 AI 系统的初衷。

Glean's architecture runs these retrieval iterations through Waldo at sub-second speeds, keeping total response times within the window where users stay engaged.

Glean 的架构让这些检索迭代由 Waldo 以亚秒级速度完成，把总响应时间控制在用户仍愿意等待的区间内。

**Token costs scale linearly with query volume.** Every token sent to a frontier model during the search-planning phase represents compute spent on a task that doesn't require frontier-level intelligence. Across thousands of daily queries in a large organization, those planning tokens accumulate into meaningful infrastructure cost — without generating any reasoning value.

Token 成本随查询量线性增长。 搜索规划阶段送往前沿模型的每一个 token，都是花在「并不需要前沿级智能」的任务上的算力。在大型组织每天数千次查询的规模下，这些规划 token 会累积成可观的基础设施成本，却不产生任何推理价值。

Redirecting planning work to a compact model reclaims that budget for the synthesis step, where frontier-model quality directly affects answer accuracy.

把规划工作转给紧凑模型，等于把这份预算收回来用在综合环节 —— 在那里，前沿模型的质量才直接影响回答准确性。

**Simultaneous planning and reasoning degrades retrieval quality.** When a single model handles both search planning and answer generation, it can begin synthesizing responses before sufficient evidence is retrieved. The model generates plausible-sounding answers grounded in partial context rather than waiting for complete evidence.

规划与推理混在一起会降低检索质量。 当同一个模型既做搜索规划又生成回答时，它可能在证据还没收齐就开始综合，基于不完整的上下文生成「听起来很像样」的答案，而不是等待完整证据。

Separating the roles enforces a clear evidence threshold — Waldo must determine that enough grounded context exists before the reasoning model receives any input.

拆开角色会强制形成清晰的证据阈值 —— 必须是 Waldo 判定有足够的有据上下文，推理模型才会收到任何输入。

This boundary prevents premature synthesis.

这条边界杜绝了过早综合。

**A narrower model is easier to govern.** A purpose-trained search-planning model has a constrained scope: it decides what to query and when to stop. That narrow function makes its decisions more auditable than a frontier model's, because there's less ambiguity about what it should and shouldn't do. Enterprise teams can monitor Waldo's retrieval patterns, flag anomalies in connector usage, and adjust its behavior without touching the reasoning layer — a governance advantage that matters in regulated industries.

更窄的模型更容易治理。 专门训练的搜索规划模型职责受限：只决定查什么、何时停。这个窄函数让它的决策比前沿模型更可审计，因为「该做什么、不该做什么」更少歧义。企业团队可以监控 Waldo 的检索模式、标记连接器使用异常、并在不触碰推理层的前提下调整行为 —— 这对受监管行业是实打实的治理优势。

## How specialized AI retrieval models differ from general-purpose frontier models / 专用检索模型与通用前沿模型有何不同

Specialized retrieval models and general-purpose frontier models solve different problems, and treating them as interchangeable drives up cost and latency in enterprise deployments. The distinction comes down to architecture, training objectives, and where each model type delivers the most value per compute dollar.

专用检索模型与通用前沿模型解决的是不同问题，把它们当成可互换的组件，会推高企业部署的成本与延迟。区别落在架构、训练目标，以及每一类模型在「每美元算力产出」上最值钱的位置。

### Architecture and training / 架构与训练

Specialized retrieval models are compact by design. They're built on [efficient base architectures](https://www.nvidia.com/en-us/ai-data-science/products/nemo/) — Waldo, for example, uses NVIDIA Nemotron 3 Nano — and post-trained narrowly on three specific capabilities: tool-use planning, source selection, and evidence-sufficiency judgment. The training data consists of anonymized query-response traces from real enterprise search sessions, refined through direct preference optimization and reinforcement learning.

专用检索模型在设计上就是紧凑的。它们建立在[高效基础架构](https://www.nvidia.com/en-us/ai-data-science/products/nemo/)之上（例如 Waldo 使用 NVIDIA Nemotron 3 Nano），并围绕三项具体能力做窄域后训练：工具使用规划、来源选择、证据充分性判断。训练数据来自真实企业搜索会话的匿名「查询—响应」轨迹，再经直接偏好优化与强化学习打磨。

The result is a model trained for one job and nothing else.

结果是得到一个只为一份工作而训练、别无他用的模型。

Frontier models follow a different path. They're trained on broad corpora spanning general reasoning, creative generation, code synthesis, and multi-domain knowledge. That breadth makes them effective at synthesizing complex answers, but wasteful during mechanical retrieval — the model carries capabilities it never uses when the task is simply deciding which of 100+ data connectors to query.

前沿模型走的是另一条路：在覆盖通用推理、创意生成、代码合成与多领域知识的广泛语料上训练。这种广度让它们擅长综合复杂回答，但在机械式检索环节很浪费 —— 当任务只是「从 100 多个数据连接器里决定查哪个」时，模型带着一身用不上的能力。

### Performance tradeoffs / 性能取舍

The speed difference is significant: a specialized retrieval model completes search-planning tasks roughly 10 times faster per call than a frontier reasoning model. But that speed comes with intentional limitations. A retrieval model isn't designed to synthesize, interpret, or generate final responses — it identifies sources, issues queries, and compresses results.

速度差异很显著：专用检索模型完成搜索规划任务，每次调用大约比前沿推理模型快 10 倍。但这种速度伴随着刻意设下的限制：检索模型不是为综合、解读或生成最终回答而设计的 —— 它只识别来源、发起查询、压缩结果。

| Capability<br>能力 | Specialized retrieval model<br>专用检索模型 | Frontier reasoning model<br>前沿推理模型 |
| --- | --- | --- |
| Search-plan generation<br>搜索计划生成 | Optimized (approximately 250 ms per call)<br>已优化（每次调用约 250 ms） | Functional but slow (approximately three seconds per call)<br>能用但慢（每次调用约 3 秒） |
| Source selection and tool use<br>来源选择与工具调用 | Primary training objective<br>主要训练目标 | Incidental capability<br>附带能力 |
| Evidence synthesis and response generation<br>证据综合与回答生成 | Not designed for this task<br>并非为此设计 | Primary strength<br>主要强项 |
| Token cost per retrieval step<br>每步检索的 token 成本 | Lower (smaller model, fewer parameters)<br>更低（模型更小、参数更少） | Higher (full-parameter inference)<br>更高（全参数推理） |
| Multi-step reasoning and abstraction<br>多步推理与抽象 | Not applicable<br>不适用 | Core capability<br>核心能力 |

In enterprise settings, retrieval planning is the highest-frequency operation in agentic workflows. Every user query triggers at least one search plan, and complex requests trigger several. Shifting that volume to a smaller, faster model produces measurable savings without reducing answer quality.

在企业场景里，检索规划是智能体工作流中频率最高的操作。每次用户查询至少触发一个搜索计划，复杂请求会触发多个。把这部分量迁到更小更快的模型上，能带来可量化的节省，且不降低回答质量。

### The system-of-models approach / 模型体系（system-of-models）思路

Rather than asking one large model to do everything, a system-of-models architecture assigns each model to the task it was trained for. The retrieval model runs the search loop and the frontier model reasons over the results. Each component iterates independently — a search-planning improvement ships without retraining the reasoning model, and vice versa.

与其让一个大模型包办一切，模型体系架构把每个模型分配到它被训练的那项任务上：检索模型跑搜索循环，前沿模型对结果做推理。各组件独立迭代 —— 搜索规划的改进上线不需要重训推理模型，反之亦然。

Organizations with data spread across dozens of applications need retrieval that understands source authority, permission boundaries, and content freshness. Glean's Agentic Engine coordinates this handoff: the specialized model handles query decomposition, connector selection, and evidence gathering, then passes compressed, permission-filtered context to the frontier model for synthesis and cited response generation. The architecture treats retrieval and reasoning as separate disciplines, not a single prompt.

数据分散在几十个应用里的组织，需要能理解来源权威性、权限边界和内容新鲜度的检索。Glean 的 Agentic Engine 协调这次交接：专用模型负责查询分解、连接器选择和证据收集，然后把压缩、按权限过滤的上下文交给前沿模型，由其综合并生成带引用的回答。这套架构把检索与推理当作两个不同学科，而不是一个 prompt。

## How search planning integrates with enterprise knowledge graphs and permissions / 搜索规划如何与企业知识图谱、权限结合

The search-planning layer doesn't operate in isolation — it queries the Enterprise Graph, a structured map of people, content, relationships, and interactions across the organization, to decide which sources are most relevant for a given question. Understanding [how knowledge graphs work](https://www.glean.com/blog/knowledge-graph-agentic-engine) is key to understanding what separates enterprise retrieval from web-scale search, where every user gets the same results for the same query.

搜索规划层并不孤立运行 —— 它会查询 Enterprise Graph（一张覆盖组织内人员、内容、关系与互动的结构化地图），以判断某个问题最该去哪些来源找。理解[知识图谱如何工作](https://www.glean.com/blog/knowledge-graph-agentic-engine)，是理解「企业检索」与「网页级搜索」差别的关键：后者对同一个查询，每个用户拿到的结果都一样。

Personal context shapes every search plan. The Personal Graph captures an individual's role, team membership, recent activity, document interactions, and access rights. When a sales rep asks about "Q1 revenue," the search-planning model prioritizes CRM dashboards, recent deal summaries, and team-shared forecasts.

个人上下文塑造了每一份搜索计划。Personal Graph 记录个体的角色、团队归属、近期活动、文档互动与访问权限。当销售代表问起「Q1 revenue」时，搜索规划模型优先选择 CRM 仪表盘、近期交易摘要和团队共享预测。

When a finance analyst asks the same question, the model routes to ERP exports, board-ready financial reports, and accounting system data. The query is identical. The search plan is entirely different.

当财务分析师问同一个问题时，模型转而路由到 ERP 导出、董事会级财务报告和会计系统数据。查询一模一样，搜索计划完全不同。

Permission enforcement happens upstream of the frontier model. Before any retrieved document reaches the reasoning step, the search-planning layer filters results by the user's access rights. If a user doesn't have permission to view a document in its source application — Salesforce, Google Drive, Confluence, or any of the 100+ natively connected systems — that document never enters the context window.

权限执行发生在前沿模型**上游**。在任何检索到的文档进入推理环节之前，搜索规划层就按用户访问权限过滤了结果。如果用户在源应用（Salesforce、Google Drive、Confluence，或 100 多个原生连接系统中的任意一个）里无权查看某篇文档，这篇文档根本不会进入上下文窗口。

The frontier model cannot reference, quote, or infer from content the user isn't authorized to see.

前沿模型无法引用、转述或推断用户无权看到的内容。

Upstream filtering also reduces token consumption. Enterprise knowledge bases contain massive volumes of content, and most of it is irrelevant to any specific query. By excluding impermissible and low-relevance documents before they reach the reasoning model, the search-planning layer keeps the context window focused on high-value evidence.

上游过滤还顺带减少 token 消耗。企业知识库体量巨大，其中绝大多数内容与某个具体查询无关。在文档抵达推理模型之前就排除无权访问的和低相关度的，搜索规划层让上下文窗口聚焦在高价值证据上。

Fewer tokens in means lower cost per query and faster time to response.

进来的 token 更少，意味着每次查询成本更低、响应更快。

Glean Search applies this pattern at every query. The Enterprise Graph provides the organizational map, the Personal Graph supplies individual context, and the search-planning model uses both to construct a permission-aware retrieval plan — all before the frontier model begins reasoning. The result is a system where data governance isn't a filter applied after the fact — it's built into the retrieval architecture itself.

Glean Search 在每次查询上都应用这一模式：Enterprise Graph 提供组织地图，Personal Graph 提供个体上下文，搜索规划模型用两者构造一份带权限感知的检索计划 —— 全部发生在前沿模型开始推理之前。结果是，数据治理不再是事后加上的过滤器，而是内建在检索架构里。

## What this means for the future of enterprise AI search and agentic systems / 对企业 AI 搜索与智能体系统意味着什么

The separation of search planning from deep reasoning signals a broader shift in how organizations deploy AI — away from monolithic frontier-model architectures and toward orchestrated systems of purpose-trained models. That shift has practical consequences for cost, speed, and how quickly enterprises can improve their AI capabilities.

把搜索规划与深度推理拆开，标志着组织部署 AI 的方式正在发生更广泛的转变 —— 从单体式前沿模型架构，走向由专用模型编排而成的体系。这一转变对成本、速度，以及企业改进 AI 能力的节奏都有实际影响。

Independent iteration is one of the most immediate benefits. When search planning and reasoning are separate models, each can be retrained, fine-tuned, and updated without touching the other. A retrieval-planning improvement based on new query patterns ships in weeks, not months, and teams working on answer quality operate on release cycles independent from those working on retrieval speed.

独立迭代是最直接的收益之一。搜索规划与推理分成两个模型后，各自可以重训、微调、更新而互不影响。基于新查询模式的检索规划改进以周为单位上线、而不是按月；负责回答质量的团队，与负责检索速度的团队可以按各自节奏发版。

Lower latency and lower cost per query also change who gets access to AI assistants. When every query runs through a frontier model end to end, the economics limit deployment to high-value use cases — analysts, executives, specialized knowledge workers. When the retrieval phase runs on a smaller, faster model and only the reasoning phase uses frontier-model compute, the per-query cost drops enough to serve broader populations.

更低的延迟与单次查询成本，还改变了「谁用得上 AI 助手」。当每次查询端到端都跑前沿模型时，经济性把部署限制在高价值用例上 —— 分析师、高管、专业知识工作者。当检索阶段由更小更快的模型承担、只有推理阶段使用前沿算力时，单次成本降到足以服务更广泛的人群。

[AI agents](https://www.glean.com/blog/ai-agents-enterprise) built on this architecture handle multi-step workflows — planning retrieval across data sources, gathering evidence, and handing structured context to the reasoning model — at a cost structure that supports organization-wide deployment.

建立在这套架构上的 [AI 智能体](https://www.glean.com/blog/ai-agents-enterprise)能处理多步工作流 —— 跨数据源规划检索、收集证据、把结构化上下文交给推理模型 —— 而其成本结构足以支撑组织级铺开。

The maturity path for enterprise AI follows a clear sequence: unified search across siloed applications, then conversational assistants that synthesize answers from retrieved context, then autonomous agents that plan, retrieve, reason, and act across systems. Each stage benefits from separating retrieval from reasoning.

企业 AI 的成熟路径有清晰次序：先是跨孤岛应用的统一搜索，然后是从检索到的上下文综合答案的对话式助手，最后是能跨系统规划、检索、推理并采取行动的自助智能体。每一阶段都受益于把检索与推理拆开。

Unified search needs fast, permission-aware query planning. Conversational assistants need grounded reasoning over retrieved evidence. Autonomous agents need both — plus the ability to execute actions and reflect on outcomes.

统一搜索需要快速、带权限感知的查询规划；对话式助手需要基于检索证据的有据推理；自主智能体两者都要，还要能执行动作并对结果做反思。

Gartner projects that by 2028, 33% of enterprise software applications will include agentic AI, up from less than 1% in 2024. That trajectory aligns with [McKinsey's 2025 survey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai), which found that 62% of organizations are already experimenting with AI agents and 23% are scaling agentic systems. That growth depends on architectures that scale retrieval independently of reasoning — because the retrieval layer is what connects AI to the messy reality of enterprise data, permissions, and organizational structure.

Gartner 预计到 2028 年，33% 的企业软件应用将包含智能体 AI，而 2024 年这一比例还不到 1%。这一轨迹与 [麦肯锡 2025 年调研](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)相互印证：62% 的组织已在试验 AI 智能体，23% 正在规模化智能体系统。这种增长依赖「检索可独立于推理扩展」的架构 —— 因为检索层才是把 AI 连到企业数据、权限与组织结构这堆 messy reality 上的那一层。

## Frequently asked questions / 常见问题

### What are the benefits of separating search planning from deep reasoning? / 拆开搜索规划与深度推理有什么好处？

Separating these functions reduces latency by roughly 50% and token consumption by approximately 25% during the retrieval phase. It also allows each model to be updated independently, so improvements to search quality don't require retraining the reasoning model.

拆开这两种职能，在检索阶段可降低约 50% 延迟、约 25% 的 token 消耗。它还允许两个模型各自独立更新，因此搜索质量的改进不需要重训推理模型。

### What is the Waldo agentic search model? / 什么是 Waldo 智能体搜索模型？

Waldo is a purpose-trained search planning model built on NVIDIA Nemotron 3 Nano. It handles query decomposition, source selection, and evidence-sufficiency judgment, trained through direct preference optimization and reinforcement learning on anonymized enterprise search traces.

Waldo 是基于 NVIDIA Nemotron 3 Nano 的专用搜索规划模型，负责查询分解、来源选择和证据充分性判断；它用匿名化的企业搜索轨迹，经直接偏好优化与强化学习训练而成。

### How does this separation affect enterprise workflows? / 这种分离对企业工作流有什么影响？

It makes AI assistants and agents faster and cheaper to run per query, which lets organizations deploy them to broader user populations. Complex multi-step workflows — like gathering data from several systems to answer a cross-functional question — complete in less time because the retrieval phase runs on an optimized model rather than a general-purpose one.

它让 AI 助手与智能体每次查询跑得更快、更便宜，使组织能把它们部署给更广泛的用户群体。复杂的多步工作流 —— 例如从多个系统收集数据来回答跨职能问题 —— 完成得更快，因为检索阶段由优化过的模型而非通用模型承担。

### Does this approach replace frontier models? / 这套方案会取代前沿模型吗？

No. Frontier models handle the reasoning, synthesis, and response generation that specialized retrieval models are not designed for. The architecture assigns each model to the task it does best — retrieval planning to a compact, fast model and deep reasoning to a high-parameter frontier model.

不会。推理、综合与回答生成仍由前沿模型承担，这些本就不是专用检索模型被设计来做的事。这套架构只是把每个模型分配到它最擅长的任务上 —— 检索规划交给紧凑快速的模型，深度推理交给高参数前沿模型。

### How does this architecture handle permissions and data governance? / 这套架构如何处理权限与数据治理？

Permission enforcement happens at the search-planning layer, before any content reaches the frontier reasoning model. Glean's Enterprise Graph and Personal Graph verify access rights against the user's permissions in each source application, so the reasoning model never sees documents the user isn't authorized to access.

权限执行发生在搜索规划层，在任何内容抵达前沿推理模型之前。Glean 的 Enterprise Graph 与 Personal Graph 会按用户在各源应用中的权限核验访问权，因此推理模型永远不会看到用户无权访问的文档。

The separation of search planning from deep reasoning is an architectural decision that determines how fast, accurate, and cost-effective your enterprise AI system performs at scale. As retrieval and reasoning workloads grow, the organizations that assign each task to the right model will see compounding advantages in speed, accuracy, and adoption.

把搜索规划与深度推理拆开，是一个决定企业 AI 系统在规模化时有多快、多准、多省钱的架构决策。随着检索与推理负载增长，能把每项任务分配给合适模型的组织，将在速度、准确性和采纳率上获得叠加优势。
