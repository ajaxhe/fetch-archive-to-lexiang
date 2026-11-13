## Reading Notes / 阅读笔记与延伸追问

> 阅读笔记（凡哥，2026-11-13）：以下是归档时附带的两个追问及核查结论，非原文内容。标注「原文事实」的可在本文正文核对；标注「外部来源」「推断」的不属于本文论述，链接已给出。

### 1. Does the article really detail embedding fine-tuning? / 文章是否详细讲了向量模型调优经验？

原文事实：是，方法论链条很完整。基座为 BERT 系模型，先在公司语料上做掩码语言建模（MLM）继续预训练；再用四类信号构造训练对——标题-正文对、文档引用与锚文本（借鉴 PageRank）、同一用户短时间窗内的共同访问、以及 MS MARCO 等公开数据集；Slack 消息聚成会话文档并用首条消息充当标题；语料小或新客户时用 LLM 生成合成问答对；最后接点击、赞踩、引用点击、emoji 等真实用户反馈。评测用能力级单元测试（含复述识别与实体解析）、会话满意度、LLM 评判做 A/B；工程上每月重训、更新时全量重建索引、ACL 在检索后过滤、传统信号仍解决 60-70% 的查询。

推断与边界：其一，本文没给超参、batch size、负采样策略，也没有点名损失函数或给出基准集上的量化提升；同一场讲座在 [ZenML 的整理](https://www.zenml.io/llmops-database/fine-tuning-custom-embedding-models-for-enterprise-search) 里补了对比学习与「6 个月搜索质量提升 20%」，但那是二手整理，不是本文内容。其二，本文 Advanced Topics 一节作者自述 combine direct statements from Manav Rathod with general industry practices，即掺入了行业通用实践，不全是 Glean 一手经验。准确说法是：工程方法论详细，可复现的实验参数与量化结果缺失。

### 2. What does this have to do with building a knowledge graph? / 这对构建图谱有什么作用？

原文事实：找不到这部分细节是对的。全文 knowledge graph、graph、triplet、provenance 均 0 次命中，entity 仅 1 次，出现在评测清单的一行 Entity resolution: Testing recognition of company-specific entities and terms，没有任何展开。全文唯一把结构当信号用的是 Anchor Data（文档引用链接）与 Co-Access Patterns，但方向是「用图状的关联信号训练 embedding」，与所问的「embedding 如何反过来帮助建图谱」正好相反。

外部来源：[Glean 官方讲图谱的文章](https://www.glean.com/blog/enterprise-ai-knowledge-graph) 把两者放进同一架构：图谱由 100 多个 connector 把内容、人、活动连起来，其中语义搜索系统 Scholastic 会针对每个客户的语料与点击微调语言模型，是图谱里的一路信号；官方还强调图谱的价值之一恰恰是 without requiring meticulous and time-consuming fine-tuning。按这个定位，微调服务于检索排序这一路，图谱负责融合结构化关系与各类信号，两者并列互补，而不是「微调产出图谱」。

推断（非本文、非 Glean 官方论述）：若问文本 embedding 对建图谱能起什么作用，业界常见做法是实体链接与候选召回、实体消歧与对齐、关系候选生成，用稠密向量做近邻检索再把候选交给结构化判定，参见 [MDPI 实体链接与图谱结构](https://www.mdpi.com/article/10.3390/app12052702) 与 [CEUR 图谱实体解析](https://ceur-ws.org/Vol-2873/paper8.pdf)。尤其要区分两类 embedding：本文是文档与查询的文本向量，图谱领域常说的 TransE、RotatE 是从三元组训练出的实体向量，训练目标与用途都不同，不能混为一谈。

可复用的关联线索（归档者归纳，原文并未这样连线）：Anchor Data 的引用链接对应图谱的边与 provenance；Co-Access Patterns 对应个人图谱的协作模式与活跃项目；Unified Data Model 对应跨源统一 schema；Authoritativeness 与 Document Supersession 对应文档节点更新与来源溯源；ACL 后过滤对应图谱的细粒度访问控制。这些连的是本目录上一篇 [Glean 知识图谱文章](https://www.glean.com/blog/knowledge-graph-agentic-engine) 的内容。

> 整理: Jason Liu（jxnl.co） | 内容来源: Manav Rathod（Glean 软件工程师）客座讲座 | 日期: 2025-03-06

> 原文链接: https://jxnl.co/writing/2025/03/06/fine-tuning-embedding-models-for-enterprise-rag-lessons-from-glean/

Systematically improving RAG systems / 系统化改进 RAG 系统

This transcript is based off of a guest lecture from my [Systematically Improving RAG Applications series](https://jxnl.co/writing/2025/09/11/rag-series-index/).

本文文字稿整理自我在系统化改进 RAG 应用系列中的一次客座讲座。

[Fine-Tuning Embedding Models for Enterprise RAG: Lessons from Glean](https://www.youtube.com/watch?v=jTBsWJ2TKy8) / 客座讲座视频（YouTube）

Retrieval-Augmented Generation (RAG) systems have become essential tools for enterprises looking to harness their vast repositories of internal knowledge. While the theoretical foundations of RAG are well-understood, implementing these systems effectively in enterprise environments presents unique challenges that aren't addressed in academic literature or consumer applications. This article delves into advanced techniques for fine-tuning embedding models in enterprise RAG systems, based on insights from Manav Rathod, a software engineer at Glean who specializes in semantic search and ML systems for search ranking and assistant quality.

检索增强生成（RAG）系统已经成为企业挖掘内部海量知识库的必备工具。RAG 的理论基础已被充分理解，但要在企业环境里真正落地，会遇到学术文献和消费级应用都没覆盖的独特挑战。本文深入探讨企业 RAG 系统中微调嵌入模型的高级技巧，素材来自 Glean 软件工程师 Manav Rathod，他专注语义搜索，以及服务于搜索排序与助手质量的机器学习系统。

The discussion focuses on a critical yet often overlooked component of RAG systems: custom-trained embedding models that understand company-specific language, terminology, and document relationships. As Jason Liu aptly noted during the session, "If you're not fine-tuning your embeddings, you're more like a Blockbuster than a Netflix." This perspective highlights how critical embedding fine-tuning has become for competitive enterprise AI systems.

讨论聚焦在 RAG 系统里一个关键却常被忽视的组件：能理解公司特有语言、术语和文档关系的定制训练嵌入模型。Jason Liu 在讲座中的一句话很到位：「如果你不微调自己的 embedding，你更像是 Blockbuster 而不是 Netflix。」这点出了嵌入微调对有竞争力的企业 AI 系统有多关键。

## The Enterprise RAG Challenge / 企业 RAG 的挑战

Enterprise data differs fundamentally from internet data in several key ways that affect how we build and fine-tune embedding models:

企业数据与互联网数据有根本差异，这些差异会影响我们如何构建和微调嵌入模型：

1. **Heterogeneous Data Sources**: Enterprise data spans numerous applications and formats—from Google Drive and Confluence documents to Slack messages, meeting transcripts, and GitHub pull requests. Each requires different handling strategies. / 数据源异构：企业数据横跨众多应用与格式——从 Google Drive、Confluence 文档到 Slack 消息、会议记录、GitHub pull request，每种都要不同的处理策略。
2. **Company-Specific Language**: Every organization develops its unique terminology, acronyms, project names, and language patterns that general-purpose embedding models won't understand without specific training. / 公司特有语言：每个组织都会长出自己的术语、缩写、项目名和语言习惯，通用嵌入模型不经过专门训练就看不懂。
3. **Evolving Knowledge**: Enterprise knowledge changes constantly. New projects emerge, old ones become obsolete, and terminology shifts. Embedding models must adapt to these changes. / 知识持续演化：企业知识一直在变，新项目出现、旧项目作废、术语更替，嵌入模型必须跟着适应。
4. **Security and Privacy Constraints**: Enterprise data is sensitive and often cannot be directly accessed for model training purposes, creating challenges for data preparation. / 安全与隐私约束：企业数据敏感，往往不能直接拿来训练模型，给数据准备带来挑战。
5. **Lack of Labeled Data**: Unlike consumer applications with abundant user interaction data, enterprise systems often start with little to no labeled data for training. / 缺少标注数据：消费级应用有丰富的用户交互数据，企业系统起步时常常几乎没有标注数据可用。

## When to Fine-Tune Embedding Models / 何时该微调嵌入模型

A key question practitioners face is determining when embedding fine-tuning is necessary versus using out-of-the-box models. According to Manav, fine-tuning becomes essential when:

实践者面临的一个关键问题是：什么时候必须微调嵌入模型，什么时候直接用现成模型就够了。按 Manav 的说法，以下情况微调变得不可或缺：

1. **Your users employ company-specific terminology** that general models won't understand / 用户使用公司特有术语，通用模型看不懂
2. **Search quality metrics plateau** despite improvements in other system components / 其他组件都在改进，但搜索质量指标已经见顶
3. **You have sufficient company-specific data** to make fine-tuning effective / 已有足够的公司专属数据支撑微调见效
4. **Different query patterns emerge** that standard models don't handle well / 出现了标准模型处理不好的新查询模式

While some scenarios can be addressed through retrieval strategies like query expansion or re-ranking, embedding fine-tuning becomes unavoidable when the semantic gap between general language and company-specific language is significant. As one attendee aptly phrased it, "look at your data!" — understanding your specific use case is crucial for determining when fine-tuning is necessary.

有些场景可以用查询扩展、重排这类检索策略解决，但当通用语言与公司内部语言之间的语义鸿沟足够大时，微调就无法回避。一位听众的说法很到位：「看你的数据！」——判断是否需要微调，前提是理解自己的具体用例。

## Glean's Approach to Embedding Fine-Tuning / Glean 的嵌入模型微调方法

Glean builds custom embedding models for each of their customers, recognizing that one-size-fits-all approaches don't work for enterprise search. Their process involves multiple stages:

Glean 为每一位客户构建定制嵌入模型，因为他们认定一刀切在企业搜索里行不通。整个流程分多个阶段：

### 1. Continued Pre-Training with Masked Language Modeling / 1. 用掩码语言建模做继续预训练

The foundation of Glean's approach begins with continued pre-training of base models (typically BERT-based) using masked language modeling (MLM) on company-specific corpora. This technique has been proven effective for domain adaptation for many years.

Glean 方法的起点，是在公司专属语料上用掩码语言建模（MLM）对基座模型（通常是 BERT 系）做继续预训练。这项技术用于领域适配的有效性早已被多年验证。

The process works by:

具体做法是：

- Taking sentences from the company's corpus / 从公司语料里取句子
- Blanking out certain words / 挖掉其中某些词
- Training the model to predict the masked words / 训练模型预测被掩掉的词

This forces the model to develop a nuanced understanding of both general English and company-specific language. The technique is especially effective when carefully selecting which words to mask, focusing on domain-specific terms.

这迫使模型同时建立对通用英语和公司特有语言的细腻理解。如果精心挑选被掩码的词、聚焦领域术语，效果尤其好。

MLM is particularly valuable in enterprise settings because:

MLM 在企业场景里特别有价值，原因在于：

- It can utilize all text data without requiring labels / 无需标注就能用上全部文本数据
- It works effectively regardless of corpus size / 不论语料规模大小都有效
- It adapts the model to understand company jargon, product names, and internal terminology / 让模型适配公司行话、产品名和内部术语
- It enables the model to incorporate new vocabulary specific to the business into the embedding space, integrating it with the dimensions of the pre-trained BERT model / 把业务特有的新词纳入向量空间，并与预训练 BERT 的维度融合

### 2. Converting Language Models to Embedding Models / 2. 把语言模型转成嵌入模型

While masked language modeling helps the model understand company language, it doesn't necessarily optimize embeddings for search tasks. To create effective search embeddings, Glean uses several techniques to generate training pairs:

MLM 能让模型理解公司语言，但并不必然让 embedding 适合搜索任务。为了得到好用的搜索向量，Glean 用几种方法生成训练对：

#### Title-Body Pairs / 标题-正文对

One effective approach is creating "title-body" pairs that map document titles to passages from the document body. This provides a weak but useful training signal since titles typically relate semantically to the content they describe.

一种有效做法是构造标题-正文对，把文档标题映射到正文里的段落。标题通常与它所描述的内容在语义上相关，因此这是一个偏弱但有用的训练信号。

#### Anchor Data / 锚文本数据

Drawing inspiration from Google's PageRank, Glean leverages document references as signals for relevance. When one document links to another, they likely share semantic relationships. These connections can be used to create pairs for training:

借鉴 Google PageRank 的思路，Glean 把文档之间的引用当作相关性信号：一篇文档链接到另一篇，两者很可能共享语义关系。这些连接可以用来构造训练对：

- Titles of documents that reference each other / 互相引用的文档标题
- Context around the anchor text paired with the referenced document / 锚文本周围的上下文，配上被引用的文档

#### Co-Access Patterns / 共同访问模式

When users research a topic, they often access multiple related documents in a short time window. This "co-access" pattern provides valuable signals about document relationships. Glean captures these patterns by creating positive pairs from documents accessed together by the same user within a time threshold.

用户研究某个主题时，常在短时间内访问多个相关文档。这种共同访问模式提供了关于文档关系的宝贵信号。Glean 把同一用户在时间阈值内一起访问的文档配成正样本。

#### Public Datasets / 公开数据集

While company-specific data is crucial, public datasets still provide value. Glean incorporates established datasets like MS MARCO to ensure models maintain general language understanding while adding company-specific knowledge.

公司专属数据固然关键，公开数据集依然有价值。Glean 会引入 MS MARCO 这类成熟数据集，让模型在补充公司知识的同时保持通用语言理解。

### 3. Handling Application-Specific Data / 3. 处理应用特定的数据

Different application data requires specialized processing to extract high-quality training pairs. For example, Slack messages present unique challenges:

不同应用的数据需要专门处理，才能抽出高质量训练对。以 Slack 消息为例，它有几个独特难题：

- Individual messages often lack context and are too short to be meaningful / 单条消息往往缺少上下文、太短而没有意义
- Messages don't have titles, making title-body pairing difficult / 消息没有标题，难以做标题-正文配对
- Not all channels contain equally valuable information / 并非所有频道的价值都一样

Glean addresses these challenges by:

Glean 的应对方式是：

- Creating "conversation documents" from message threads or time-based clusters / 把消息线程或按时间聚簇的消息做成会话文档
- Using the first message as a proxy for a title when needed / 需要时用第一条消息充当标题
- Filtering out low-value channels (e.g., "random" or "happy birthday" channels) / 过滤低价值频道（比如 random、生日祝福频道）
- Leveraging emoji reactions as relevance signals—messages with 👍 or similar positive reactions can be treated as "answers" or high-quality responses, creating additional training pairs / 把 emoji 反应当作相关性信号——带正面反应的消息可视为答案或高质量回复，从而生成额外训练对

Understanding these application-specific nuances is critical for creating high-quality training data. As emphasized in the discussion, there's no substitute for deeply examining your data and understanding user behaviors before designing training strategies.

理解这些应用层面的差异，是构造高质量训练数据的关键。讲座里反复强调：在设计训练策略之前，扎进去看自己的数据、理解用户行为，没有替代品。

### 4. Leveraging Synthetic Data / 4. 利用合成数据

For smaller corpora or when starting with new customers, Glean uses large language models (LLMs) to generate synthetic question-answer pairs:

语料较小或刚接入新客户时，Glean 用大语言模型生成合成的问答对：

- LLMs analyze documents and generate potential questions users might ask / 让 LLM 分析文档，生成用户可能会问的问题
- Careful prompt engineering ensures questions resemble actual user queries rather than just reformatting document text / 精心的提示工程确保问题像真实用户查询，而不是把文档文字换个说法
- Generation focuses on popular, high-value documents to maximize return on compute costs / 生成聚焦热门、高价值文档，让算力投入产出比最大

This approach provides "infinite" training data but requires careful implementation:

这条路相当于提供了无限训练数据，但落地要小心：

- Prompts must encourage variation in wording rather than exact matches / 提示词必须鼓励措辞变化，而不是与原文精确匹配
- Generated questions should account for how users actually phrase queries (using acronyms, omitting details, etc.) / 生成的问题要贴合用户真实的提问方式（用缩写、省略细节等）
- Questions should cover diverse query patterns, not just simple factoid questions / 问题要覆盖多样的查询模式，不能只出简单的事实型问题

### 5. Learning from User Feedback / 5. 从用户反馈中学习

The most valuable training signal comes from actual user interactions. Glean leverages several feedback mechanisms:

最有价值的训练信号来自真实的用户交互。Glean 用了几种反馈机制：

#### Search Interactions / 搜索交互

In their search product, click data provides direct relevance signals. When users search and click on results, these query-document pairs become valuable training data.

在搜索产品里，点击数据提供直接的相关性信号。用户搜索并点开结果时，这些查询-文档对就成了有价值的训练数据。

#### RAG Assistant Feedback / RAG 助手的反馈

For RAG-only scenarios (like their Glean Assistant), feedback collection is more challenging. Approaches include:

在纯 RAG 场景（比如 Glean Assistant）里，收集反馈更难。可用手段包括：

- Upvote/downvote systems (though engagement is typically sparse) / 赞/踩（不过参与度通常很稀疏）
- Citation clicks (when users click to read source documents) / 引用点击（用户点开原文阅读）
- Follow-up question patterns / 追问模式

These signals may be individually weak, but combined across many interactions, they provide valuable training data.

这些信号单看都很弱，但把大量交互叠在一起，就能形成有价值的训练数据。

#### Creative Feedback Collection / 有创意的反馈收集

Improving user engagement with feedback mechanisms remains an ongoing challenge. During the discussion, innovative approaches were suggested, such as gamifying the feedback experience: "Instead of passive thumbs up/down, a ball drops, and users steer it into 'good' or 'bad' buckets—actively engaging with feedback." Such creative approaches can increase the quantity of feedback signals available for model improvement.

如何提高用户在反馈机制上的参与度，仍是个持续性的难题。讨论中有人提出把反馈体验游戏化：与其被动点赞点踩，不如让一个小球落下、由用户把它拨进好或坏的桶里，让人主动参与反馈。这类巧思能增加可用于模型改进的信号量。

## Query Pattern Recognition / 查询模式识别

An important aspect of embedding fine-tuning involves recognizing different query patterns. As mentioned during the discussion, queries often fall into categories like:

嵌入微调还有一个重要方面，是识别不同的查询模式。讲座中提到，查询大致可分几类：

- **Factoid questions**: Seeking specific pieces of information / 事实型问题：找某条具体信息
- **Enumeration queries**: Requesting lists of items (e.g., "What are all the projects in the finance department?") / 枚举型查询：要一份清单（例如财务部门有哪些项目？）
- **Inventory queries**: Looking for assets like meetings, presentations, etc. / 盘点型查询：找会议、演示文稿这类资产
- **Navigational queries**: Trying to find specific documents / 导航型查询：想找到某份具体文档

Training embedding models to recognize these patterns and handle them accordingly leads to more effective retrieval. This often requires creating synthetic examples that represent each pattern and fine-tuning the model to recognize the underlying intent behind different query structures.

让嵌入模型学会识别这些模式并区别处理，检索会更有效。这往往需要为每种模式造合成样本，再微调模型去识别不同查询结构背后的意图。

## Evaluating Embedding Models / 评估嵌入模型

Evaluating embedding models in enterprise settings presents unique challenges, particularly when dealing with hundreds of customer-specific models and limited data access. Glean's approach emphasizes:

在企业环境里评估嵌入模型很特殊：面对的是几百个客户专属模型，而且数据访问受限。Glean 的做法强调：

### Focused Unit Testing / 聚焦式单元测试

Rather than relying solely on end-to-end evaluation, Glean builds targeted evaluations for specific capabilities:

Glean 不只看端到端评估，还会针对具体能力建定向评测：

- Paraphrase recognition: Testing whether models recognize different phrasings of the same question / 复述识别：测试模型能否认出同一问题的不同说法
- Entity resolution: Testing recognition of company-specific entities and terms / 实体解析：测试对公司特有实体与术语的识别
- Document relevance: Testing retrieval performance for key documents / 文档相关性：测试关键文档的检索表现

This "unit testing" approach helps identify specific weaknesses in models and provides clear targets for improvement.

这种单元测试式的做法能定位模型的具体短板，给出明确的改进目标。

### User Satisfaction Metrics / 用户满意度指标

Beyond technical evaluations, Glean tracks business outcomes:

技术评测之外，Glean 还跟踪业务结果：

- Session satisfaction: What percentage of search sessions end with users finding relevant documents? / 会话满意度：有多大比例的搜索会话以用户找到相关文档收尾？
- Usage metrics: Are users increasing their engagement with the system? / 使用指标：用户对系统的使用是否在增长？
- Explicit feedback: Upvote/downvote ratios and trends / 显式反馈：赞踩比例及其趋势

### LLM-Based Evaluation / 基于 LLM 的评估

For certain aspects of system performance, Glean employs LLM-based judges to evaluate response quality along dimensions like:

对系统表现的某些方面，Glean 用 LLM 作评判，按若干维度给回答质量打分：

- Factuality / 事实性
- Relevance / 相关性
- Context usage / 上下文使用
- Correctness / 正确性

These evaluations help identify improvements or regressions when making system changes.

这些评估能在系统改动后识别出改进或退化。

## Handling Enterprise-Specific Challenges / 处理企业特有的挑战

### Document Supersession / 文档被替代

One common challenge in enterprise settings is determining when documents have been superseded by newer information. Glean approaches this through a concept they call "authoritativeness," which considers:

企业里一个常见难题，是判断某份文档是否已被更新的信息取代。Glean 用他们称之为权威性（authoritativeness）的概念来处理，综合考虑：

- Recency: When was the document last updated? / 新近度：文档最后更新是什么时候？
- References: Do other documents link to this one as an authoritative source? / 被引用情况：其他文档是否把它当作权威来源来引用？
- User interactions: Do users still find and engage with this document? / 用户互动：用户是否还在找到并阅读这份文档？

Documents like WiFi passwords might be old but remain authoritative if they're still regularly accessed and referenced. This was highlighted as "one of the hardest aspects of enterprise RAG" during the discussion, requiring both algorithmic solutions and human judgment.

像 WiFi 密码这类文档可能很旧，但只要仍被经常访问和引用，就依然权威。讨论中把这一点列为企业 RAG 最难的方面之一，既需要算法方案，也离不开人的判断。

### Security and Privacy / 安全与隐私

Working with sensitive enterprise data requires strict security protocols. Glean emphasizes:

处理敏感企业数据要有严格的安全规范。Glean 强调：

- A unified data model that maintains security boundaries / 维持安全边界的统一数据模型
- Customer-specific models that don't share data between organizations / 客户专属模型，组织之间不共享数据
- Careful handling of permissions (ACLs) to ensure retrieved content respects access controls / 谨慎处理权限（ACL），确保召回内容遵守访问控制

Regarding ACL (Access Control List) handling, Manav clarified that access controls are applied post-retrieval rather than pre-filtering the corpus. This allows the system to consider all documents during retrieval and then filter results based on the user's permissions before presenting them, maintaining both relevance quality and security compliance. This approach requires careful integration with existing permission systems and strict security validation to ensure no unauthorized access occurs.

关于 ACL（访问控制列表），Manav 说明：访问控制是在检索之后施加，而不是预先过滤语料。这样检索阶段可以考虑全部文档，再在展示前按用户权限过滤，兼顾相关性与合规。这种做法要求与现有权限系统仔细集成，并做严格的安全校验，杜绝越权访问。

## Lessons Learned and Best Practices / 经验教训与最佳实践

From Glean's experience, several best practices emerge for fine-tuning embedding models in enterprise RAG systems:

从 Glean 的经验里，可以归纳出几条企业 RAG 嵌入模型微调的最佳实践：

1. **Unified Data Modeling is Critical**: Building a consistent schema across heterogeneous data sources enables systematic training and evaluation. / 统一数据建模至关重要：跨异构数据源建立一致 schema，才能系统化地训练和评估。
2. **Creative Data Generation Matters**: Finding ways to extract training signals from existing data is often more valuable than collecting new annotations. / 创造性地造数据：从既有数据里挖训练信号，往往比新收标注更有价值。
3. **User Feedback is Gold**: Even sparse signals from real users outperform synthetic data when available. / 用户反馈是金：哪怕稀疏，真实用户信号也胜过合成数据。
4. **Understand User Query Patterns**: Different types of queries require different optimization approaches; understanding these patterns enables targeted improvements. / 理解用户查询模式：不同查询需要不同的优化手段，看懂模式才能定向改进。
5. **Isolate Components for Improvement**: Rather than optimizing end-to-end performance, focus on improving specific components with clear metrics. / 拆开组件来改进：不要只盯端到端指标，聚焦有清晰度量的单个组件。
6. **Don't Overlook Traditional Search Techniques**: Basic signals like recency and exact matching still solve 60-70% of enterprise search queries; semantic search should complement, not replace these approaches. / 别忽视传统检索：新近度、精确匹配这类基础信号仍能解决 60-70% 的企业搜索查询，语义搜索应当补充而非取代它们。
7. **Continuous Learning is Essential**: Models should be regularly retrained (monthly for Glean) to adapt to evolving company knowledge and terminology. / 持续学习不可少：模型要定期重训（Glean 是每月一次），跟上公司知识与术语的演化。
8. **Look at Your Data**: This simple but powerful advice was emphasized repeatedly—there's no substitute for deeply understanding your specific data and use cases. / 看你的数据：这条朴素建议被反复强调——深入理解自己的数据和用例，无可替代。

## Conclusion / 结论

Fine-tuning embedding models for enterprise RAG represents a unique set of challenges distinct from both academic research and consumer applications. Glean's approach demonstrates that success requires a sophisticated multi-stage training process that combines continued pre-training, creative data pair generation, synthetic data, and user feedback signals.

在企业 RAG 里微调嵌入模型，面对的是一组既不同于学术研究、也不同于消费级应用的独特挑战。Glean 的做法说明，要成功就需要一条精密的多阶段训练流程：继续预训练、创造性地生成训练对、合成数据、用户反馈信号，缺一不可。

The most effective systems combine the strengths of traditional search techniques with the power of semantic search, rather than relying exclusively on embedding-based retrieval. As Manav Rathod noted, "Using traditional basic search techniques and using these traditional signals is super important, and it'll never be outdated. Any system that doesn't use that is a questionable search system."

最有效的系统会把传统检索技术的长处与语义搜索结合起来，而不是只依赖基于 embedding 的召回。正如 Manav Rathod 所说：「使用传统的基础搜索技术、使用这些传统信号非常重要，它永远不会过时。任何不用它们的系统都值得怀疑。」

For practitioners building enterprise RAG systems, this underscores the importance of a pragmatic approach: fine-tune embeddings to understand company-specific language, but don't abandon proven information retrieval techniques that continue to provide value.

对搭建企业 RAG 的实践者来说，这指向一种务实的态度：微调 embedding 让它听懂公司特有语言，但别丢掉那些仍在创造价值、久经检验的信息检索技术。

## Advanced Topics and Implementation Considerations / 进阶话题与实施考量

The following section explores advanced topics and practical implementation considerations for teams building enterprise RAG systems with fine-tuned embeddings. These insights combine direct statements from Manav Rathod with general industry practices.

下一节面向正在用微调嵌入模型搭建企业 RAG 的团队，探讨进阶话题与落地考量。这些内容把 Manav Rathod 的直接陈述与行业通用实践结合在了一起。

### Data Freshness vs. Model Stability / 数据新鲜度与模型稳定性

**Challenge**: Enterprises face a trade-off between keeping embedding models up-to-date with evolving terminology and the computational cost of re-indexing large document collections.

挑战：企业要在让嵌入模型跟上术语演化，与大规模文档重建索引的算力成本之间权衡。

**Manav's Approach**: Glean retrains their models on a monthly basis, which provides a good balance for most enterprise environments. As Manav explained:

Manav 的做法：Glean 每月重训一次模型，对多数企业环境是较好的平衡。他解释道：

> "We do things on a monthly basis. I think it does really just depend on the company whether or not that makes the most sense... because I think it's very rare where, like a brand new concept appears and become super important in the company, like over just the span of a week, or even a month, depending on the size of the company."

> 我们按月度来做。我觉得这是否最合适，真的取决于公司本身……因为很少会出现一个全新概念在一周、甚至一个月内就变得对公司极其重要的情况，具体还得看公司规模。

When models are updated, Glean completely re-indexes all content rather than attempting to maintain vector stability across versions. This ensures consistent quality but requires efficient infrastructure for regular re-indexing.

模型更新时，Glean 会把全部内容重新索引，而不是设法维持不同版本之间向量的稳定性。这样质量一致，但要求有能支撑定期全量重建的高效基础设施。

**Industry Practices**: Beyond what was explicitly discussed, many organizations implement:

行业实践：除了讲座明确谈到的做法，很多组织还会实现：

- Incremental embedding updates for new or changed documents / 对新增或改动的文档做增量 embedding 更新
- Importance-based prioritization focusing on frequently accessed content / 按重要性排优先级，优先处理高频访问内容
- Vector database partitioning to update segments independently / 把向量库分区，让各分片独立更新

### Evaluation at Scale / 规模化评估

**Challenge**: Evaluating embedding models in enterprise settings presents unique challenges, particularly when dealing with hundreds of customer-specific models and limited data access.

挑战：在企业环境里评估嵌入模型很特殊，尤其要面对几百个客户专属模型，而且数据访问受限。

**Manav's Approach**: Glean builds "unit tests" for their models to evaluate specific behaviors and capabilities:

Manav 的做法：Glean 给模型建单元测试，用来评估特定行为和能力：

> "We unit test our code. We also unit test our models in a lot of ways. An example of this is that you want to pick out behaviors of a model that you find desirable, and build an Eval set for them and make sure a model is kind of doing well on that particular type of query stream."

> 我们给代码写单元测试，也用很多方式给模型做单元测试。举个例子，你挑出希望模型具备的行为，为它们建一个评测集，然后确认模型在这类查询流上表现不错。

Manav emphasized testing specific capabilities like paraphrase understanding:

Manav 特别强调要测试复述理解这类具体能力：

> "A good semantic search model should be really good at paraphrasing. I understand that paraphrases of the same sentence or a particular query, are actually mean the exact same thing."

> 好的语义搜索模型应该非常擅长处理复述。我理解的是，同一个句子或某条查询的不同改写，其实表达的是完全相同的意思。

For generating evaluation data, Manav suggested using existing datasets or LLMs:

至于怎么造评估数据，Manav 建议用现成数据集或 LLM：

> "You can take examples of queries, or like existing data sets of like paraphrases of like sentences. Or you can use LMs to create more of them on your own."

> 你可以拿一些查询示例，或者现成的句子复述数据集；也可以让语言模型自己生成更多。

Glean also uses A/B testing with LLM judges to evaluate system improvements:

Glean 还会用带 LLM 评判的 A/B 测试来评估系统改进：

> "You can do a simple AB test like you ask hundreds of questions based on what users previously asked, and then with you using your old system and then on your new system, and you can use like a simple judge framework broken down, based on these different subcategories."

> 可以做个简单的 A/B 测试：拿用户以前问过的几百个问题，分别跑旧系统和新系统，再用一个按不同子类拆开的简单评判框架来打分。

**User Satisfaction Metrics**: Beyond technical evaluations, Glean tracks business outcomes:

用户满意度指标：技术评测之外，Glean 还跟踪业务结果：

> "For search, where the main thing we look at is like this notion of session satisfaction, like, essentially, when user ask a question or they start searching for something. What percent of the time do they find a relevant document based on their click patterns?"

> 在搜索上，我们主要看的是会话满意度这个概念——本质上就是，当用户提出问题、或开始搜某个东西时，根据他的点击模式，有多大比例的时候他找到了相关文档？

### Security and Privacy Considerations / 安全与隐私考量

**Challenge**: Working with sensitive enterprise data requires strict security protocols.

挑战：处理敏感企业数据要有严格的安全规范。

**Manav's Observations**: Manav highlighted the challenges of evaluating models when you can't directly access customer data:

Manav 的观察：他点出了无法直接访问客户数据时，模型评估有多难：

> "It becomes particularly challenging in the enterprise setting where you don't have access to your customer data, and you have enterprise, specific models for each of your customers."

> 在企业场景里这件事尤其有挑战，因为你拿不到客户数据，而且每个客户都有自己专属的企业模型。

For evaluation without accessing data directly, Manav mentioned using closed-loop environments with LLMs:

对于不直接接触数据的评估，Manav 提到可以用 LLM 搭闭环环境：

> "If within a closed loop environment where you use an LLM to judge the quality of your responses, you can get a lot of useful signal out of that for understanding if you're making improving things."

> 如果是在一个闭环环境里，用 LLM 来判断回答质量，你能拿到很多有用的信号，用来判断自己是不是真的在改进。

**ACL Handling**: Regarding access control, Manav clarified that security is applied post-retrieval rather than pre-filtering the corpus, allowing the system to consider all documents during retrieval and then filter results based on permissions.

ACL 处理：关于访问控制，Manav 说明安全措施是在检索之后施加，而不是预先过滤语料，因此检索时可以看全部文档，再按权限过滤结果。

### Application-Specific Data Processing / 应用特定的数据处理

**Challenge**: Different data sources require specialized processing to extract high-quality training pairs.

挑战：不同数据源需要专门处理，才能抽出高质量训练对。

**Manav's Approach**: For Slack messages, which present unique challenges, Manav suggested:

Manav 的做法：针对 Slack 消息的独特难题，他建议：

> "Instead of thinking about individual messages as documents, think about like threads as documents, or like a time span of messages as a document."

> 不要把单条消息当成文档，要把线程当成文档，或者把一段时间跨度内的消息当成一份文档。

As noted in the chat log, emoji reactions can provide valuable signals:

聊天记录里也提到，emoji 反应能提供有价值的信号：

> "Users emoji (thumbs up) responses that are 'answers' or high quality responses. Use that as signal for positive pairs."

> 用户用 emoji（点赞）回应的、属于答案或高质量回复的内容，可以拿来当正样本的信号。

For PDFs and other visual content, Manav mentioned:

关于 PDF 和其他视觉内容，Manav 提到：

> "PDFs are probably the main source of like images or image, like data that we have in the enterprise... There's a variety of different like, pretty powerful out of the box tools you have for, like PDF parsing, and we mainly leverage those. But we primarily work in the textual space because that's just kind of where most enterprise data lives."

> PDF 大概是企业里图片类数据的主要来源……现在有各种相当好用的开箱即用 PDF 解析工具，我们主要用那些。不过我们基本还是在做文本，因为企业数据绝大多数本来就在这个空间里。

### Document Supersession and Relevance / 文档替代与相关性

**Challenge**: One common challenge in enterprise settings is determining when documents have been superseded by newer information.

挑战：企业里一个常见难题，是判断某份文档是否已被更新的信息取代。

**Manav's Insights**: When asked about handling outdated documents, Manav explained:

Manav 的见解：被问到怎么处理过期文档时，他解释：

> "We have this notion of like authoritativeness... like, how authoritative is this document? And that's based on a lot of different signals. Like, how many people reference this document? How many people look at this document? How recent is this document?"

> 我们有一个叫权威性的概念……就是这份文档有多权威？它基于很多不同信号，比如有多少人引用这份文档、有多少人看过它、它有多新。

He provided a practical example:

他举了个实际例子：

> "A good example is like a WiFi password document. It might be really old, but it's still the WiFi password document. And so it's still authoritative, even if it's old."

> 一个很好的例子是 WiFi 密码文档。它可能真的很旧，但它仍然是那份 WiFi 密码文档，所以哪怕旧，它依然权威。

This was highlighted in the chat as "one of the hardest aspects of enterprise RAG."

聊天记录里把这一点列为企业 RAG 最难的方面之一。

### Balancing Traditional and Semantic Search / 平衡传统检索与语义搜索

**Challenge**: Development teams must decide how to balance embedding-based retrieval with traditional search techniques.

挑战：开发团队要决定如何在基于 embedding 的召回与传统检索技术之间取平衡。

**Manav's Perspective**: Manav emphasized the importance of isolating and improving individual components:

Manav 的观点：他强调拆开并逐个改进组件的重要性：

> "Isolating and improving individual components of your RAG system altogether is always going to be the best way to kind of move forward... if you want to really make good, tangible progress, like day by day, isolating and optimizing individual components, is always going to be like much more scalable than trying to improve everything altogether all at once."

> 把 RAG 系统的各个组件拆开来分别改进，永远是往前推进最好的方式……如果你想真正做出扎实、可感知的进展，日复一日地隔离并优化单个组件，永远比试图一次性把所有东西一起改好要可扩展得多。

In previous sections, he stressed that traditional search techniques remain essential and that "any system that doesn't use that is a questionable search system."

在前面几节他还强调，传统检索技术依然不可或缺，任何不用它们的系统都值得怀疑。

## Questions to Consider / 值得思考的问题

1. **When should you fine-tune embeddings vs. using out-of-the-box models?** / 什么时候该微调 embedding，而不是直接用现成模型？
2. Consider fine-tuning when your users employ company-specific terminology that general models won't understand / 当用户使用通用模型看不懂的公司特有术语时，考虑微调
3. Look for plateaus in search quality metrics despite improvements in other system components / 留意搜索质量指标是否在其他组件持续改进的情况下已经见顶
4. Ensure you have sufficient company-specific data to make fine-tuning effective / 确认已有足够的公司专属数据，让微调真正见效
5. As Manav emphasized: "Look at your data!" Understanding your specific use case is crucial / 正如 Manav 强调的：看你的数据！理解自己的具体用例至关重要
6. **How can you generate high-quality training data in enterprise settings?** / 在企业环境里，怎么造出高质量训练数据？
7. Leverage document structure (title-body pairs) / 利用文档结构（标题-正文对）
8. Analyze document references and links (anchor data) / 分析文档引用与链接（锚文本数据）
9. Study user behavior (co-access patterns) / 研究用户行为（共同访问模式）
10. Use synthetic data generation with LLMs / 用 LLM 生成合成数据
11. Collect and learn from user feedback / 收集用户反馈并从中学习
12. **What evaluation strategies work best for enterprise embedding models?** / 企业嵌入模型最有效的评估策略是什么？
13. Build targeted "unit tests" for specific model capabilities / 针对具体模型能力建定向的单元测试
14. Track user satisfaction and business outcomes / 跟踪用户满意度与业务结果
15. Use LLM-based judges for systematic evaluation / 用 LLM 评判做系统化评估
16. Compare model iterations rather than focusing on absolute metrics / 比较模型迭代之间的变化，而不是死盯绝对指标
17. **How frequently should embedding models be updated?** / 嵌入模型该多久更新一次？
18. Glean retrains on a monthly basis, which works well for most enterprises / Glean 每月重训一次，对多数企业都够用
19. Consider your company's pace of change and the emergence of new terminology / 结合公司自身的变化节奏与新术语出现的速度来定
20. Balance freshness with the computational cost of re-indexing / 在新鲜度与重建索引的算力成本之间取平衡
21. **How can you handle the challenge of document supersession?** / 怎么处理文档被替代这个难题？
22. Develop a notion of "authoritativeness" based on references, user engagement, and context / 基于引用、用户参与度和上下文建立权威性概念
23. Recognize that recency isn't always the best indicator of relevance / 要意识到新近度不一定是最好的相关性指标
24. Consider both algorithmic solutions and human judgment / 算法方案和人的判断都要考虑
