# Exploring Glean's approach: search planning vs. deep reasoning in AI

> 作者: The Glean Team | 页面日期: Jun 04, 2026（Last updated） | 阅读时长: 11 分钟

> 原文链接: https://www.glean.com/perspectives/exploring-gleans-approach-search-planning-vs-deep-reasoning-in-ai

![Exploring Glean's approach: search planning vs. deep reasoning in AI](images/img_01_18d5ccbc.png)

Glean separates search planning from deep reasoning by assigning retrieval orchestration to a purpose-trained model and reserving frontier-model compute for synthesis and response generation. These two operations — deciding where to look and actually thinking through what you find — demand fundamentally different resources, yet most systems today treat them as one job.

The distinction between retrieval planning and synthesis matters because [enterprise AI search](https://www.glean.com/blog/enterprise-ai-search-rag) spans dozens of data sources, each with its own permissions, schemas, and query patterns. When a single large language model handles both the mechanical work of routing queries and the intellectual work of synthesizing answers, organizations pay frontier-model prices for tasks that don't require frontier-model intelligence.

Understanding how these functions differ — and why separating them changes the economics of [enterprise search](https://www.glean.com/blog/the-definitive-guide-to-ai-based-enterprise-search-for-2025) — is key to evaluating how AI retrieval architectures will evolve.

## What is the difference between search planning and deep reasoning in enterprise AI?

Search planning is the structured, mechanical process of deciding which data sources to query, what tool calls to make, and when enough evidence has been gathered. It follows predictable patterns: parse the user's question, identify relevant connectors, issue parallel queries, evaluate whether the retrieved documents are sufficient, and either refine the search or hand off results. The operations are iterative and latency-sensitive — each additional planning step adds wait time that the user feels directly.

[Deep reasoning](https://www.glean.com/product/agentic-engine) is what happens after retrieval. A model interprets the gathered context, draws inferences across multiple sources, resolves contradictions, and produces a grounded response with citations. This work demands high-parameter models optimized for nuance, abstraction, and multi-step logic — the kind of processing where a frontier model earns its cost.

The computational profiles are mismatched. A default reasoning model takes roughly three seconds per call, while a purpose-trained search planning model can execute the same retrieval step in about 250 milliseconds. Most enterprise AI systems today use a single frontier model for both jobs, which means organizations pay frontier-model prices and accept frontier-model latency for what is, during the retrieval phase, a mechanical task.

Glean's approach with Waldo — a search planning model built on NVIDIA Nemotron 3 Nano — splits these roles, achieving approximately 50% lower latency and 25% fewer tokens during the planning phase by assigning retrieval orchestration to a smaller, faster model trained specifically for that work.

## Why separating search planning from deep reasoning improves enterprise AI efficiency

The cost arithmetic changes when you look at scale. An organization with 10,000 knowledge workers generating even modest query volume — say 20 agentic queries per person per day — runs 200,000 retrieval loops daily. If each loop requires three to five search-planning iterations through a frontier model at roughly three seconds per call, the cumulative latency and token spend become a line item, not a rounding error.

A specialized smaller model post-trained for tool-use decisions breaks this pattern. Instead of routing every retrieval step through the same high-parameter model that handles synthesis, the search-planning model runs the retrieval loop independently — an approach consistent with how [agentic RAG](https://www.glean.com/blog/agentic-rag-explained) enhances traditional retrieval by letting intelligent agents adapt in real time. It decides which corpora to query — internal documents, people directories, web sources — evaluates whether enough evidence exists, and assembles grounded context before a frontier model ever sees the request.

The result is a system where token budgets go where they matter. Glean's Agentic Engine uses this split architecture to reserve frontier-model capacity for reasoning — the multi-step inference, contradiction resolution, and citation generation that actually requires a large model's capabilities. The [search planning](https://www.glean.com/blog/agentic-reasoning-future-ai) phase, handled by a purpose-trained model running at roughly one-twelfth the latency per call, consumes a fraction of the tokens without regression in answer quality.

This architecture is not about replacing frontier models or treating them as overhead. Frontier models are essential for the reasoning step.

The waste comes from feeding them tasks they're overqualified for — parsing connector schemas, deciding whether to query Confluence or Slack first, determining that three retrieved documents aren't sufficient and a fourth search is needed. A 2026 analysis by Clarifai found that small language models can deliver [10–30x cheaper inference](https://www.clarifai.com/blog/top-cost-efficient-small-models) than large models, with enterprises using smaller models for 80% of their API calls and cutting compute costs by up to 70%. A compact model post-trained on those exact decision patterns handles them with equivalent accuracy at a fraction of the compute.

For enterprise teams evaluating AI infrastructure costs, the implication is straightforward: every token spent on search planning through a frontier model is a token that could have been spent on deeper, more accurate reasoning.

## How the Waldo agentic search model works

Waldo is a purpose-built agentic search model designed to handle one job well: deciding what to search, where to search, and when to stop searching. Built on a compact open foundation model (NVIDIA Nemotron 3 Nano), Waldo was post-trained using two techniques — [direct preference optimization](https://arxiv.org/abs/2305.18290) (DPO) and reinforcement learning — to specialize in tool-use planning for enterprise retrieval.

The training data came from anonymized behavioral traces of how Glean's existing agentic system planned searches across production environments. These traces captured the decision patterns — which connectors were queried, in what order, how many iterations were needed — without exposing any enterprise content. The model learned retrieval strategies, not proprietary information.

In production, Waldo runs first in the query pipeline. When a user asks a question through Glean Assistant, Waldo evaluates the query and plans tool use across three retrieval surfaces: internal search (documents, messages, knowledge bases), employee search (people directories and org charts via the Enterprise Graph), and web search. It iterates across these surfaces, evaluating retrieved results against an evidence threshold before passing the assembled context forward.

A key capability is retrieval compression. Through its post-training on effective search patterns, Waldo learned to find in a single search iteration what previously required several iterations from a general-purpose model. It recognizes which connector combinations tend to produce sufficient evidence for specific query types and routes accordingly, cutting retrieval cycles without sacrificing recall.

The handoff point is explicit. Once Waldo determines that enough grounded evidence exists, it packages the retrieved context — with source attribution and permission metadata intact — and passes it to the frontier model.

The frontier model never plans a search. It receives pre-assembled, permission-aware context and focuses entirely on reasoning, synthesis, and generating cited responses.

Because Waldo's scope is limited to tool-use planning, it can be updated, monitored, and constrained independently from the reasoning model — a narrower decision boundary that's easier to audit than a frontier model's open-ended generation.

## What challenges does this architecture address in enterprise workflows?

Separated search planning addresses four compounding problems that erode enterprise AI adoption: latency, cost, accuracy, and governance. Understanding the full scope of [agentic reasoning](https://www.glean.com/blog/a-complete-guide-to-agentic-reasoning) helps contextualize why each of these challenges worsens at scale — and why they interact, as slow responses drive workarounds, workarounds reduce data quality, and reduced data quality undermines trust in the system.

**Latency compounds with every retrieval step.** Knowledge workers expect near-instant responses from search tools. When an agentic system loops a frontier model through multiple retrieval iterations — each taking roughly three seconds — a query that requires four search steps introduces 12 seconds of wait time before reasoning even begins.

That delay drives users back to manual search or tribal knowledge, which defeats the purpose of deploying an AI system.

Glean's architecture runs these retrieval iterations through Waldo at sub-second speeds, keeping total response times within the window where users stay engaged.

**Token costs scale linearly with query volume.** Every token sent to a frontier model during the search-planning phase represents compute spent on a task that doesn't require frontier-level intelligence. Across thousands of daily queries in a large organization, those planning tokens accumulate into meaningful infrastructure cost — without generating any reasoning value.

Redirecting planning work to a compact model reclaims that budget for the synthesis step, where frontier-model quality directly affects answer accuracy.

**Simultaneous planning and reasoning degrades retrieval quality.** When a single model handles both search planning and answer generation, it can begin synthesizing responses before sufficient evidence is retrieved. The model generates plausible-sounding answers grounded in partial context rather than waiting for complete evidence.

Separating the roles enforces a clear evidence threshold — Waldo must determine that enough grounded context exists before the reasoning model receives any input.

This boundary prevents premature synthesis.

**A narrower model is easier to govern.** A purpose-trained search-planning model has a constrained scope: it decides what to query and when to stop. That narrow function makes its decisions more auditable than a frontier model's, because there's less ambiguity about what it should and shouldn't do. Enterprise teams can monitor Waldo's retrieval patterns, flag anomalies in connector usage, and adjust its behavior without touching the reasoning layer — a governance advantage that matters in regulated industries.

## How specialized AI retrieval models differ from general-purpose frontier models

Specialized retrieval models and general-purpose frontier models solve different problems, and treating them as interchangeable drives up cost and latency in enterprise deployments. The distinction comes down to architecture, training objectives, and where each model type delivers the most value per compute dollar.

### Architecture and training

Specialized retrieval models are compact by design. They're built on [efficient base architectures](https://www.nvidia.com/en-us/ai-data-science/products/nemo/) — Waldo, for example, uses NVIDIA Nemotron 3 Nano — and post-trained narrowly on three specific capabilities: tool-use planning, source selection, and evidence-sufficiency judgment. The training data consists of anonymized query-response traces from real enterprise search sessions, refined through direct preference optimization and reinforcement learning.

The result is a model trained for one job and nothing else.

Frontier models follow a different path. They're trained on broad corpora spanning general reasoning, creative generation, code synthesis, and multi-domain knowledge. That breadth makes them effective at synthesizing complex answers, but wasteful during mechanical retrieval — the model carries capabilities it never uses when the task is simply deciding which of 100+ data connectors to query.

### Performance tradeoffs

The speed difference is significant: a specialized retrieval model completes search-planning tasks roughly 10 times faster per call than a frontier reasoning model. But that speed comes with intentional limitations. A retrieval model isn't designed to synthesize, interpret, or generate final responses — it identifies sources, issues queries, and compresses results.

| Capability | Specialized retrieval model | Frontier reasoning model |
| --- | --- | --- |
| Search-plan generation | Optimized (approximately 250 ms per call) | Functional but slow (approximately three seconds per call) |
| Source selection and tool use | Primary training objective | Incidental capability |
| Evidence synthesis and response generation | Not designed for this task | Primary strength |
| Token cost per retrieval step | Lower (smaller model, fewer parameters) | Higher (full-parameter inference) |
| Multi-step reasoning and abstraction | Not applicable | Core capability |

In enterprise settings, retrieval planning is the highest-frequency operation in agentic workflows. Every user query triggers at least one search plan, and complex requests trigger several. Shifting that volume to a smaller, faster model produces measurable savings without reducing answer quality.

### The system-of-models approach

Rather than asking one large model to do everything, a system-of-models architecture assigns each model to the task it was trained for. The retrieval model runs the search loop and the frontier model reasons over the results. Each component iterates independently — a search-planning improvement ships without retraining the reasoning model, and vice versa.

Organizations with data spread across dozens of applications need retrieval that understands source authority, permission boundaries, and content freshness. Glean's Agentic Engine coordinates this handoff: the specialized model handles query decomposition, connector selection, and evidence gathering, then passes compressed, permission-filtered context to the frontier model for synthesis and cited response generation. The architecture treats retrieval and reasoning as separate disciplines, not a single prompt.

## How search planning integrates with enterprise knowledge graphs and permissions

The search-planning layer doesn't operate in isolation — it queries the Enterprise Graph, a structured map of people, content, relationships, and interactions across the organization, to decide which sources are most relevant for a given question. Understanding [how knowledge graphs work](https://www.glean.com/blog/knowledge-graph-agentic-engine) is key to understanding what separates enterprise retrieval from web-scale search, where every user gets the same results for the same query.

Personal context shapes every search plan. The Personal Graph captures an individual's role, team membership, recent activity, document interactions, and access rights. When a sales rep asks about "Q1 revenue," the search-planning model prioritizes CRM dashboards, recent deal summaries, and team-shared forecasts.

When a finance analyst asks the same question, the model routes to ERP exports, board-ready financial reports, and accounting system data. The query is identical. The search plan is entirely different.

Permission enforcement happens upstream of the frontier model. Before any retrieved document reaches the reasoning step, the search-planning layer filters results by the user's access rights. If a user doesn't have permission to view a document in its source application — Salesforce, Google Drive, Confluence, or any of the 100+ natively connected systems — that document never enters the context window.

The frontier model cannot reference, quote, or infer from content the user isn't authorized to see.

Upstream filtering also reduces token consumption. Enterprise knowledge bases contain massive volumes of content, and most of it is irrelevant to any specific query. By excluding impermissible and low-relevance documents before they reach the reasoning model, the search-planning layer keeps the context window focused on high-value evidence.

Fewer tokens in means lower cost per query and faster time to response.

Glean Search applies this pattern at every query. The Enterprise Graph provides the organizational map, the Personal Graph supplies individual context, and the search-planning model uses both to construct a permission-aware retrieval plan — all before the frontier model begins reasoning. The result is a system where data governance isn't a filter applied after the fact — it's built into the retrieval architecture itself.

## What this means for the future of enterprise AI search and agentic systems

The separation of search planning from deep reasoning signals a broader shift in how organizations deploy AI — away from monolithic frontier-model architectures and toward orchestrated systems of purpose-trained models. That shift has practical consequences for cost, speed, and how quickly enterprises can improve their AI capabilities.

Independent iteration is one of the most immediate benefits. When search planning and reasoning are separate models, each can be retrained, fine-tuned, and updated without touching the other. A retrieval-planning improvement based on new query patterns ships in weeks, not months, and teams working on answer quality operate on release cycles independent from those working on retrieval speed.

Lower latency and lower cost per query also change who gets access to AI assistants. When every query runs through a frontier model end to end, the economics limit deployment to high-value use cases — analysts, executives, specialized knowledge workers. When the retrieval phase runs on a smaller, faster model and only the reasoning phase uses frontier-model compute, the per-query cost drops enough to serve broader populations.

[AI agents](https://www.glean.com/blog/ai-agents-enterprise) built on this architecture handle multi-step workflows — planning retrieval across data sources, gathering evidence, and handing structured context to the reasoning model — at a cost structure that supports organization-wide deployment.

The maturity path for enterprise AI follows a clear sequence: unified search across siloed applications, then conversational assistants that synthesize answers from retrieved context, then autonomous agents that plan, retrieve, reason, and act across systems. Each stage benefits from separating retrieval from reasoning.

Unified search needs fast, permission-aware query planning. Conversational assistants need grounded reasoning over retrieved evidence. Autonomous agents need both — plus the ability to execute actions and reflect on outcomes.

Gartner projects that by 2028, 33% of enterprise software applications will include agentic AI, up from less than 1% in 2024. That trajectory aligns with [McKinsey's 2025 survey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai), which found that 62% of organizations are already experimenting with AI agents and 23% are scaling agentic systems. That growth depends on architectures that scale retrieval independently of reasoning — because the retrieval layer is what connects AI to the messy reality of enterprise data, permissions, and organizational structure.

## Frequently asked questions

### What are the benefits of separating search planning from deep reasoning?

Separating these functions reduces latency by roughly 50% and token consumption by approximately 25% during the retrieval phase. It also allows each model to be updated independently, so improvements to search quality don't require retraining the reasoning model.

### What is the Waldo agentic search model?

Waldo is a purpose-trained search planning model built on NVIDIA Nemotron 3 Nano. It handles query decomposition, source selection, and evidence-sufficiency judgment, trained through direct preference optimization and reinforcement learning on anonymized enterprise search traces.

### How does this separation affect enterprise workflows?

It makes AI assistants and agents faster and cheaper to run per query, which lets organizations deploy them to broader user populations. Complex multi-step workflows — like gathering data from several systems to answer a cross-functional question — complete in less time because the retrieval phase runs on an optimized model rather than a general-purpose one.

### Does this approach replace frontier models?

No. Frontier models handle the reasoning, synthesis, and response generation that specialized retrieval models are not designed for. The architecture assigns each model to the task it does best — retrieval planning to a compact, fast model and deep reasoning to a high-parameter frontier model.

### How does this architecture handle permissions and data governance?

Permission enforcement happens at the search-planning layer, before any content reaches the frontier reasoning model. Glean's Enterprise Graph and Personal Graph verify access rights against the user's permissions in each source application, so the reasoning model never sees documents the user isn't authorized to access.

The separation of search planning from deep reasoning is an architectural decision that determines how fast, accurate, and cost-effective your enterprise AI system performs at scale. As retrieval and reasoning workloads grow, the organizations that assign each task to the right model will see compounding advantages in speed, accuracy, and adoption.
