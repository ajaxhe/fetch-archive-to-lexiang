# How to build an AI assistant for the enterprise

*See how Glean works.*

*看看 Glean 是如何工作的。*

> 作者: Chau Tran

Engineering | 日期: Jul 09, 2023

> 原文链接: https://www.glean.com/blog/how-to-build-an-ai-assistant-for-the-enterprise

9minutes read[Chau Tran

Engineering](/authors/chau-tran)[Mrinal Mohit

Engineering](/authors/mrinal-mohit)[Arvind Jain

CEO](/authors/arvind-jain)

![How to build an AI assistant for the enterprise](images/img_04_9a1806ca.jpg)

### Table of contents

[The challenges of fine-tuning LLMs on enterprise data](#the-challenges-of-fine-tuning-llms-on-enterprise-data)[Retrieval Augmented Generation: Vector search is not enough](#retrieval-augmented-generation-vector-search-is-not-enough)[Data: Scalable permission-aware indexing](#data-scalable-permission-aware-indexing)[Topical relevance: Hybrid search with reranking](#topical-relevance-hybrid-search-with-reranking)[Personalization: Extensive knowledge graph](#personalization-extensive-knowledge-graph)[Integrating LLMs: Enhancing search itself](#integrating-llms-enhancing-search-itself)[Unlock the full value of generative AI today – not tomorrow](#unlock-the-full-value-of-generative-ai-today-not-tomorrow)[Have questions or want a demo?

We're here to help! Click the button below and we'll be in touch.

Get a Demo](/get-a-demo)Share this article:

Large Language Models (LLMs) like GPT-4 and PALM are powerful reasoning engines that form the foundation of most text-based generative AI experiences seen today. Ask the LLM a question, and it usually provides an intelligent answer. They are able to reach into the depths of knowledge provided by the data they were trained on – or what we call "world knowledge".

像 GPT-4 和 PALM 这样的大语言模型（LLM）是强大的推理引擎，构成了当今大多数基于文本的生成式 AI 体验的基础。向 LLM 提问，它通常会给出智能的回答。它们能够深入挖掘训练数据所提供的知识——也就是我们所说的"世界知识"。

But what about data that is proprietary – say, information restricted to your company's employees? If you ask a generic LLM a question about the status of your latest customer deal, it will likely tell you that it doesn't have enough context to answer. Worse yet, it might hallucinate and fabricate an incorrect reply, resulting in the spread of misinformation and potentially serious workflow consequences.

那专有数据呢——比如仅限于公司内部员工访问的信息？如果你向一个通用的 LLM 询问最新客户交易的进展，它很可能会告诉你它没有足够的上下文来回答。更糟的是，它可能会产生幻觉并编造错误的回复，从而导致错误信息传播，并可能引发严重的工作流后果。

Applying generative AI technologies like ChatGPT to enterprise data is challenging given the complexity of handling security permissions, scaling infrastructure, and establishing a broad, high-quality knowledge graph. In this blog post, we'll walk through some approaches to make ChatGPT work on enterprise data, their pitfalls, and how Glean solves for them through [Glean Chat](https://glean.com/blog/glean-chat-launch-announcement).

鉴于处理安全权限、扩展基础设施以及建立广泛且高质量的知识图谱的复杂性，将 ChatGPT 这类生成式 AI 技术应用于企业数据极具挑战性。在这篇博文中，我们将梳理一些让 ChatGPT 在企业数据上发挥作用的方法、它们的坑，以及 Glean 如何通过 [Glean Chat](https://glean.com/blog/glean-chat-launch-announcement) 来解决这些问题。

## The challenges of fine-tuning LLMs on enterprise data / 在企业数据上微调大语言模型的挑战

In the previous generation of natural-language-processing models (e.g. BERT, RoBERTa, and others), one popular paradigm was "fine-tuning" – where one would start with the weights of a foundational model, and then train them to better fit the needs of their specific tasks and domain.

在上一代自然语言处理模型（例如 BERT、RoBERTa 等）中，一种流行的范式是"微调（fine-tuning）"——即从一个基础模型的权重出发，再对其进行训练，使其更好地适配特定任务和领域的需求。

However, how has the fine-tuning paradigm fared in today's era of LLMs? Let's start with how a modern LLM like ChatGPT is trained:

然而，微调范式在如今的 LLM 时代表现如何？让我们从现代 LLM（如 ChatGPT）的训练方式说起：

1. First, a "foundational model" is trained on massive amounts of data (trillions of tokens), which requires immense compute power (costing millions of dollars). This is what it costs to build the impressive reasoning and generation abilities you've seen from ChatGPT. / 首先，一个"基础模型"在海量数据（数万亿 token）上训练，这需要巨大的算力（耗资数百万美元）。这正是打造你所见到的 ChatGPT 强大推理与生成能力所需的代价。
2. Then, the model enters a fine-tuning stage where it's trained to follow natural language instructions, and aligned to human values. This stage is critical to ensure the model behaves ethically by avoiding potential harms like toxicity, bias, and privacy violations. / 然后，模型进入微调阶段，在此阶段它被训练以遵循自然语言指令，并与人类价值观对齐。这一阶段对于确保模型行为合乎伦理、避免毒性、偏见和隐私侵犯等潜在危害至关重要。

![Product Illustration](images/img_05_00a04e09.png)

A seemingly natural way to infuse proprietary knowledge into an LLM is at the fine-tuning stage. However, the fine-tuning stage is meant to improve task-specific performance, not to teach the model about new knowledge. When an LLM is fine-tuned on unfamiliar knowledge, it actually [increases hallucinations](https://www.youtube.com/live/hhiLw5Q_UFg?feature=share). This is because we're essentially teaching the model to generate responses for topics it does not have a strong, factual understanding of. It's why we agree with [OpenAI](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb) that "fine-tuning is better suited to teaching specialized tasks or styles, and is less reliable for factual recall."

一个看似自然地将专有知识注入 LLM 的方式是在微调阶段进行。然而，微调阶段的本意是提升特定任务的表现，而非向模型传授新知识。当 LLM 在不熟悉的知识上微调时，它实际上会[加剧幻觉](https://www.youtube.com/live/hhiLw5Q_UFg?feature=share)。这是因为我们本质上是在教模型为它并不具备扎实事实理解的 topic 生成回复。这也是我们认同 [OpenAI](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb) 的观点——"微调更适合教授专门的任务或风格，而在事实召回方面并不可靠"的原因。

Alternatively, one could try including company private data at the foundational pretraining stage through domain adaptation (similar to [BloombergGPT](https://www.bloomberg.com/company/press/bloomberggpt-50-billion-parameter-llm-tuned-finance/), or [MedPALM](https://sites.research.google/med-palm/)). While this approach is effective for adapting LLMs for broad domains, it has several fundamental limitations when building an [enterprise AI](https://www.glean.com/blog/enterprise-ai-search-rag)copilot:

另一种做法是尝试在基础预训练阶段通过领域适配纳入公司私有数据（类似于 [BloombergGPT](https://www.bloomberg.com/company/press/bloomberggpt-50-billion-parameter-llm-tuned-finance/) 或 [MedPALM](https://sites.research.google/med-palm/)）。虽然这种方法在将 LLM 适配到广泛领域时很有效，但在构建[企业 AI](https://www.glean.com/blog/enterprise-ai-search-rag)副驾驶（copilot）时存在几个根本性局限：

1. **Freshness** – One could fine-tune models on a snapshot of their company's data, but what happens when that changes on an hourly basis? Users are interested in having the most recent and relevant data, but continually training the model to provide that is expensive and difficult to maintain. / **新鲜度（Freshness）** – 人们可以在公司数据的某个快照上微调模型，但当数据每小时都在变化时会发生什么？用户希望获得最新、最相关的数据，但持续训练模型以提供这些数据既昂贵又难以维护。
2. **Permissions** – Not every employee has access to see all of the data within their company. Sensitive conversations might happen between the CEO and the CFO, performance reviews might be restricted to managers, and engineers might not have access to Salesforce. Throwing "all" data into a LLM results in generated answers leaking sensitive details. / **权限（Permissions）** – 并非每位员工都能访问公司内的所有数据。CEO 与 CFO 之间可能发生敏感对话，绩效评估可能仅限经理查看，工程师可能无法访问 Salesforce。把"所有"数据一股脑塞进 LLM 会导致生成的回答泄露敏感细节。
3. **Explainability** – When your employees are relying on an assistant to help them with their job, you want the answers to not just be correct, but verifiable. If a support agent recommends a fix for a ticket using an assistant, they should be able to verify what document was the source of the recommended fix. Does a source document even exist? Did the model hallucinate one? Is the document canonical, or was last updated 10 years ago? Is there any additional context in the document they should know about? All of this is impossible to process if you trust LLM generations blindly. / **可解释性（Explainability）** – 当员工依赖助手来辅助工作时，你不仅希望答案正确，还希望可验证。如果客服坐席借助助手为某个工单推荐修复方案，他们应当能够核实该推荐方案的依据文档是什么。源文档真的存在吗？是模型编造的吗？文档是权威版本，还是十年前更新的？文档中还有哪些他们应当了解的背景信息？如果盲目相信 LLM 的生成结果，这一切都无从验证。
4. **Catastrophic forgetting** – The amount of proprietary data in your company is several orders of magnitude smaller than the vast amount of data used to train a base LLM. As a result, fine-tuning the model risks it either forgetting much of the broad, general world knowledge it had originally gained, or failing to learn the nuances of your proprietary data. / **灾难性遗忘（Catastrophic forgetting）** – 公司内的专有数据量比训练基础 LLM 所用的海量数据小了好几个数量级。因此，微调模型可能导致它遗忘原本获得的广泛通用世界知识，或者无法学会你专有数据的细微差别。

In conclusion, while fine-tuning/training LLMs is appealing for improving task-specific performance, there are too many limitations and risks with this approach for [workplace AI assistants](https://www.glean.com/product/workplace-search-ai).

总之，尽管微调/训练 LLM 对提升特定任务表现很有吸引力，但这种方式对[职场 AI 助手](https://www.glean.com/product/workplace-search-ai)而言存在太多局限和风险。

## Retrieval Augmented Generation: Vector search is not enough / 检索增强生成：向量搜索还不够

To separate the ability of LLMs to generate coherent, well-reasoned responses from their (in)ability to reliably retrieve factual knowledge, the system can be designed as a pipeline. We first retrieve knowledge through a separate search system, and *then* give it to the LLM to read in order to ground its reasoning and synthesis. This is widely known as [Retrieval Augmented Generation (RAG)](https://www.glean.com/blog/how-to-build-an-ai-assistant-for-the-enterprise).

为了将 LLM 生成连贯、推理合理回复的能力，与其（不可）靠地检索事实性知识的能力分离开来，系统可以被设计成一条流水线。我们先通过一个独立的搜索系统检索知识，*然后*将其交给 LLM 阅读，以支撑其推理与综合。这就是广为人知的[检索增强生成（RAG）](https://www.glean.com/blog/how-to-build-an-ai-assistant-for-the-enterprise)。

- Knowledge is always as recent and relevant as possible, since the regularly updated search index is inserted into the LLM at query-time. / 知识始终保持尽可能新且相关，因为定期更新的搜索索引会在查询时注入 LLM。
- The LLM will never access something a user doesn't have access to. / LLM 永远不会访问用户无权访问的内容。
- Users can look at the subset of documents which were fed into the LLM and to verify that the generated response is grounded in truthful information. / 用户可以查看被输入 LLM 的文档子集，并核实生成的回复是有真实信息支撑的。
- Catastrophic forgetting doesn't happen, as it retrieves relevant knowledge at query-time rather than trying to retain all knowledge within the model. / 不会发生灾难性遗忘，因为它在查询时检索相关知识，而非试图把全部知识都保留在模型内部。

At the heart of RAG is the retrieval component – underpinning the security of your company's data and the relevance of the generated responses your workers need to succeed. We'll go through why this is essentially a search problem, along with some of the technical requirements of implementing this in the enterprise setting.

RAG 的核心在于检索组件——它支撑着公司数据的安全性，以及员工成功所需生成回复的相关性。我们将解释为什么这本质上是一个搜索问题，以及在企业环境中实现它的一些技术要求。

### Data: Scalable permission-aware indexing / 数据层：可扩展的权限感知索引

When building the data layer for an [enterprise search solution](https://www.glean.com/blog/top-enterprise-search-software), there are a couple approaches to consider.

在构建[企业搜索方案](https://www.glean.com/blog/top-enterprise-search-software)的数据层时，有几种方法值得考虑。

Federated search across individual app APIs is one approach, but it comes with major downsides. Each app's search API has its own nuances, requirements, and rate limiting, making it largely unscalable. Federated search also results in suboptimal ranking algorithms (since they only understand data within that single app, and search features in SaaS are usually underinvested), ultimately providing a poor search experience.

跨各个应用 API 的联邦搜索是一种方法，但它存在重大缺陷。每个应用的搜索 API 都有其自身的细微差别、要求和速率限制，使其在很大程度上难以扩展。联邦搜索还会导致次优的排序算法（因为它们只理解单个应用内的数据，而 SaaS 中的搜索功能通常投入不足），最终提供糟糕的搜索体验。

A better solution is to build a centralized index by crawling and indexing data from all sources. However, building a scalable, permission-aware crawler and search platform is an engineering challenge that can take years of work – from scaling to corpuses billions of documents in size, to creating a unified document model that's capable of handling a wide variety of different data sources.

更好的方案是通过爬取和索引所有来源的数据来构建集中式索引。然而，构建一个可扩展、权限感知的爬虫与搜索平台是一项可能需要数年工作的工程挑战——从扩展到数十亿文档规模的语料库，到创建能够处理各种不同数据源的统一文档模型。

Glean provides over [100 pre-built connectors](https://www.glean.com/connectors) that hook into apps like Google Drive, Slack, Jira, Salesforce, and more – helping users start indexing data quickly and skip years of development. For enterprise customers with hundreds of thousands of employees, billions of documents, and hundreds of terabytes of data, Glean's infrastructure (built over a period of nearly five years) handles data at this scale wonderfully.

Glean 提供超过 [100 个预构建连接器](https://www.glean.com/connectors)，可接入 Google Drive、Slack、Jira、Salesforce 等应用——帮助用户快速开始索引数据，跳过数年的开发。对于企业客户（拥有数十万名员工、数十亿文档和数百 TB 数据），Glean 的基础设施（在将近五年内构建）能够出色地处理这种规模的数据。

By indexing data from all sources into a single platform, Glean is able to build a **cross-app knowledge graph** that thoroughly understands all the content, context, and collaborators across the organization. By then applying advanced ranking algorithms to surface the most relevant results, Glean delivers a vastly improved search experience over systems that use individual app APIs.

通过将所有来源的数据索引到统一平台，Glean 能够构建一张**跨应用知识图谱**，全面理解整个组织的内容、上下文和协作者。进而应用先进的排序算法来呈现最相关的结果，Glean 由此带来了比使用单个应用 API 的系统好得多的搜索体验。

For any company looking to unlock the value of their data, a scalable indexing platform with pre-built connectors is the way to go over federated search. Glean provides turnkey access to [enterprise search](https://www.glean.com/blog/what-is-enterprise-search) with an indexing solution built for the modern SaaS-powered workplace.

对于任何希望释放数据价值的公司，带有预构建连接器的可扩展索引平台是优于联邦搜索的选择。Glean 以专为现代 SaaS 驱动的工作场所打造的索引方案，提供[企业搜索](https://www.glean.com/blog/what-is-enterprise-search)的即开即用能力。

### Topical relevance: Hybrid search with reranking / 主题相关性：混合检索与重排序

With a scalable indexed corpus, the next challenge is retrieving the most relevant knowledge for a given query. Among the billions of documents in your company's corpus, how do you find the ones that contain the most useful, accurate, and up-to-date information?

有了可扩展的索引语料库，下一个挑战就是为给定查询检索最相关的知识。在公司语料库数十亿文档中，你如何找到那些包含最有用、最准确、最新信息的文档？

To fetch these "relevant" documents to feed into the LLM, vector search has emerged as a prime candidate. The system "embeds" each piece of text into a vector of numbers, and stores that in a vector database. When a query comes, it's similarly embedded into the database. The closest file to the query in the vector space is then sourced as the most relevant piece of information.

为了获取这些"相关"文档以输入 LLM，向量搜索已成为首选方案。系统将每段文本"嵌入（embed）"为一个数字向量，并存入向量数据库。当查询到来时，它同样被嵌入到数据库中。然后在向量空间里离查询最近的文档就被提取为最相关的信息。

Database providers such as Pinecone or Weaviate have been getting a lot of attention lately. What isn't discussed enough, however, is that the *quality* of the vector embeddings is usually a bigger bottleneck than having a database to host those embeddings.

Pinecone 或 Weaviate 等数据库提供商近来备受关注。然而，讨论得不够充分的是：向量嵌入的*质量*通常比承载这些嵌入的数据库本身更大的瓶颈。

We've shown [previously](https://www.glean.com/blog/unlocking-the-power-of-vector-search-in-enterprise) that if you **fine-tune embedding encoders** on company-specific data, you can get far better matching quality than most "generic" embedding models, open-source (MPNet, E5, Instructor) or close-source (OpenAI, Cohere). This of course requires expertise in training these models, along with the infrastructure to do so continuously. Glean has been steadily building and refining this over the past years.

我们[此前](https://www.glean.com/blog/unlocking-the-power-of-vector-search-in-enterprise)已经证明，如果在公司特定数据上**微调嵌入编码器**，可以获得比大多数"通用"嵌入模型（开源的 MPNet、E5、Instructor，或闭源的 OpenAI、Cohere）好得多的匹配质量。这当然需要训练这些模型的专长，以及持续训练所需的基础设施。Glean 在过去几年里一直在稳步构建并打磨这一能力。

![Product Illustration](images/img_06_613e1bd3.gif)

But even though embeddings are powerful, traditional keyword-based methods are far from being obviated. In fact, what works well in practice are "hybrid" methods, which take the best of classical information retrieval techniques and modern neural-network based semantic embedders ([Thakur et al. (2021)](https://arxiv.org/abs/2104.08663)). Tuning a **hybrid retrieval and reranking** system is an extremely complicated task – it requires training models to combine dozens different ranking signals (including semantic similarity, keyword match, document freshness, personalization features, and more) in order to produce a final relevance score. Our search models are continuously learning and improving from every query to provide the most relevant results for each employee.

但尽管嵌入非常强大，传统的基于关键词的方法远未被淘汰。事实上，在实践中行之有效的是"混合"方法，它兼取经典信息检索技术与现代基于神经网络的语义嵌入器之长（[Thakur et al. (2021)](https://arxiv.org/abs/2104.08663)）。调优一个**混合检索与重排序**系统是一项极其复杂的任务——它需要训练模型，将数十种不同的排序信号（包括语义相似性、关键词匹配度、文档新鲜度、个性化特征等）结合起来，以产生最终的相关性评分。我们的搜索模型从每一次查询中持续学习并改进，为每位员工提供最相关的结果。

![Enterprise search buyer's guide](images/img_10_b1854826.png)

## Enterprise search buyer's guide / 企业搜索采购指南

Enterprise search solutions have become essential to ensuring employee satisfaction, workflow efficiency, and business success. Discover what features and capabilities to look for when considering the best search solution for you.

企业搜索方案对于确保员工满意度、工作流效率和业务成功已变得不可或缺。在考虑最适合你的搜索方案时，了解应关注哪些功能与能力。

[Get The Resource](/resources/guides/enterprise-search-buyers-guide)
### Personalization: Extensive knowledge graph / 个性化：庞大的知识图谱

Even with a perfect textual search system, documents that are textually related to the search query may not always contain the right information to answer a user's question. For example, an engineer may ask where the latest design specs are kept. However, the search results may contain hundreds of documents/pull requests/messages about the topic. This scenario is also why we believe that using a much larger context window (up to 1 million tokens) would not eliminate the need for search relevancy, since providing wrong and outdated information would cause the language model to give an incorrect answer.

即便拥有完美的文本搜索系统，与搜索查询在文本上相关的文档也不总包含回答用户问题的正确信息。例如，一名工程师可能会问最新的设计规格保存在哪里。然而，搜索结果可能包含数百个关于该主题的文档/拉取请求/消息。这也是为什么我们相信，使用更大的上下文窗口（多达 100 万 token）并不能消除对搜索相关性的需求——因为提供错误和过时的信息会导致语言模型给出不正确的答案。

Dense vector methods are specifically designed to handle text, whereas in reality, there are more data mediums at play. To make search personalized to each individual user, Glean continually builds a **knowledge graph of all information** being created within your company. The nodes in this knowledge graph include:

稠密向量方法专门用于处理文本，而现实中还有更多的数据媒介在起作用。为了让搜索对每个用户实现个性化，Glean 持续构建一张涵盖公司内所有正在生成信息的**知识图谱**。这张知识图谱的节点包括：

- **Contents** – Individual documents, messages, tickets, entities, etc. / **内容（Contents）** – 单个文档、消息、工单、实体等。
- **People** – Identities and roles, teams, departments, groups, etc. / **人员（People）** – 身份与角色、团队、部门、群组等。
- **Activity** – Critical signals and user behavior, sharing and usage patterns / **活动（Activity）** – 关键信号与用户行为、共享与使用模式。

![Product Illustration](images/img_08_84552519.png)

The edges in the graph are how all these entities interact with each other:

图谱中的边表示所有这些实体如何相互作用：

- **Document linkage** – Documents that are linked from other documents, or mentioned by other users are more likely to be relevant ([PageRank - the paper that started Google](https://blogs.cornell.edu/info2040/2019/10/28/the-academic-paper-that-started-google/)) / **文档关联（Document linkage）** – 被其他文档链接或提及其他用户的文档更可能相关（[PageRank——开启 Google 的那篇论文](https://blogs.cornell.edu/info2040/2019/10/28/the-academic-paper-that-started-google/)）。
- **User-User interactions** – Documents from authors who are on the same team, who I have interacted with in the past, whom I have an upcoming meeting with, … are more likely to be relevant to me. / **用户-用户交互（User-User interactions）** – 来自同团队成员、我过去交互过的人、或即将与我开会的人所撰写的文档，更可能对我相关。
- **User-Document interactions** – Documents that I (or someone from my team) created/edited/shared/commented/… are all more likely to be relevant to me / **用户-文档交互（User-Document interactions）** – 我（或团队中的某人）创建/编辑/共享/评论过的文档，都更可能对我相关。

### Integrating LLMs: Enhancing search itself / 集成大语言模型：增强搜索本身

LLMs are not only useful for summarizing and synthesizing search results – they can also enhance the overall search experience. For example, LLMs enable the enterprise AI copilot to do **advanced** **query planning**, allowing systems to interpret natural language commands and translate them into a set of search queries that yield the intended results. A command like:

LLM 不仅有助于总结和综合搜索结果——它们还能增强整体搜索体验。例如，LLM 让企业 AI 副驾驶能够进行**高级的****查询规划（query planning）**，使系统能够解读自然语言指令，并将其转化为一组能产生预期结果的搜索查询。像这样的指令：

> "*Read through our Glean Chat code changes in the last month. Give me a list of enhancements we are making to the feature. You can also check our #project-glean-chat channel for more discussion.*"

> 「阅读我们上个月 Glean Chat 的代码变更。给我一份我们正在为该功能所做的增强列表。你也可以查看我们的 #project-glean-chat 频道获取更多讨论。」

…could be translated into two search queries, and synthesize results from them:

……可以被转化为两个搜索查询，并将它们的合成结果：

- Github pull requests in the last month that mentions "Glean Chat" / 上个月提及 "Glean Chat" 的 Github 拉取请求
- Messages from the #project-glean-chat Slack channel that talks about project progress / 来自 #project-glean-chat Slack 频道、谈论项目进展的消息

LLMs can also help bootstrap domain-specific encoders for new customers by **augmenting sparse real-world data** with machine-generated examples ([Promptagator](https://arxiv.org/abs/2209.11755), [InPars](https://arxiv.org/abs/2202.05144)). Since each customer's data is used exclusively to train their own encoders, synthetic data helps compensate for the lack of large in-domain datasets while retaining the customer's unique language and terminology. This results in enterprise-adapted encoders that are customized for and generalize better to each customer's data.

LLM 还可以通过用机器生成的样本**增强稀疏的真实世界数据**（[Promptagator](https://arxiv.org/abs/2209.11755)、[InPars](https://arxiv.org/abs/2202.05144)），来帮助为新客户引导出特定领域的编码器。由于每位客户的数据仅用于训练他们自己的编码器，合成数据有助于弥补大规模领域内数据集的缺失，同时保留客户独特的语言和术语。这就产生了为每个客户数据定制、且泛化能力更好的企业适配编码器。

![Product Illustration](images/img_09_e46ec1c2.png)

## Unlock the full value of generative AI today – not tomorrow / 今日解锁生成式 AI 的全部价值——而非明日

Building an enterprise-ready ChatGPT system is no small feat. There are significant requirements around freshness, permissions, explainability, and catastrophic forgetting that come with applying LLMs to company data. While vector search and embeddings have received a lot of recent interest, developing high-quality embeddings and the infrastructure to support them at scale is an engineering challenge of its own. For most companies, developing an in-house solution for unlocking the power of LLMs in their workplace data will require years of work and expertise across machine learning, search, and scalable data infrastructure.

构建一个企业级可用的 ChatGPT 系统绝非易事。将 LLM 应用于公司数据会带来关于新鲜度、权限、可解释性和灾难性遗忘的重大要求。尽管向量搜索和嵌入近来备受关注，但开发高质量的嵌入以及在大规模下支撑它们的基础设施本身就是一项工程挑战。对大多数公司而言，开发内部方案来释放 LLM 在工作场所数据中的力量，将需要多年的工作，以及横跨机器学习、搜索和可扩展数据基础设施的专业知识。

Rather than building from scratch, Glean provides an out-of-the-box solution for enterprise search and knowledge management powered by the latest generative AI technologies. Glean's underlying platform also enables you to easily build custom point solutions through our APIs for numerous enterprise workflows. The end result is an enterprise implementation that harvests the benefits of generative AI at a fraction of the cost and complexity of an in-house solution.

与其从零开始构建，Glean 提供了一套由最新生成式 AI 技术驱动、开箱即用的企业搜索与知识管理方案。Glean 的底层平台还能让你通过我们的 API 轻松构建自定义的点状解决方案，以适配众多企业工作流。最终成果是一个企业级实现，它能以内部方案零头般的成本和复杂度，收获生成式 AI 的红利。

With Glean, companies can stay focused on higher-level goals like driving new business and innovation, while fast-tracking to success through the latest innovations in generative AI without having to wait. To see how Glean helps leading companies unlock the value of their data, [request a demo today](https://www.glean.com/get-a-demo). You'll be on your way to transforming how your organization leverages knowledge through market-leading enterprise search and [AI-powered chat assistance](https://www.glean.com/product/assistant) – without any of the hassle of building it yourself.

借助 Glean，公司可以专注于更高层次的目标，例如推动新业务和创新，同时通过生成式 AI 的最新创新快速走向成功，而无需等待。要了解 Glean 如何帮助领先企业释放其数据价值，[立即申请演示](https://www.glean.com/get-a-demo)。你将踏上一条通过市场领先的企业搜索和[AI 驱动的聊天助手](https://www.glean.com/product/assistant)来改变组织利用知识方式的路径——而无需自己构建的任何麻烦。

[Back to all stories](/blog)
![Enterprise search buyer's guide](images/img_10_b1854826.png)

[Get The Resource](#)Work AI for all.[Get a Demo](/get-a-demo)
![CTA Section Background Shape](images/img_11_1a9fe696.png)

## Work AI that works. / 真正好用的 Work AI

[Get a demo](/get-a-demo)

![Work AI that works](images/img_13_daf5c826.png)

![Work AI that works](images/img_13_daf5c826.png)

![CTA Background Gradient 3](images/img_15_436da666.png)

![CTA Background Gradient 3](images/img_15_436da666.png)

![CTA Background Mobile](images/img_16_5043a133.png)
