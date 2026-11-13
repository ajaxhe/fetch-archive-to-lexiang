> 主持人: Sonya Huang、Pat Grady | 嘉宾: Arvind Jain（Glean 联合创始人兼 CEO） | 来源: Sequoia Training Data 播客

> 原文链接: https://sequoiacap.com/podcast/training-data-arvind-jain

> 收听: https://playlist.megaphone.fm/?e=CPUAI7182880302

![](images/img_01_cca8a6d4.png)

Years before co-founding Glean, Arvind was an early Google employee who helped design the search algorithm. Today, Glean is building search and work assistants inside the enterprise, which is arguably an even harder problem. One of the reasons enterprise search is so difficult is that each individual at the company has different permissions and access to different documents and information, meaning that every search needs to be fully personalized. Solving this difficult ingestion and ranking problem also unlocks a key problem for AI: feeding the right context into LLMs to make them useful for your enterprise context. Arvind and his team are harnessing generative AI to synthesize, make connections, and turbo-change knowledge work. Hear Arvind’s vision for what kind of work we’ll do when work AI assistants reach their potential.

在联合创办 Glean 之前，Arvind 是 Google 的早期员工，参与设计了搜索算法。如今 Glean 在企业内部构建搜索与工作助手，这可以说是更难的问题。企业搜索之所以难，是因为公司里每个人的权限不同、能访问的文档与信息不同，每一次搜索都必须完全个性化。解决这一复杂的接入与排序问题，同时也打开了 AI 的一个关键命题：把正确的上下文喂给大语言模型，让它在你的企业语境里真正有用。Arvind 和团队正在用生成式 AI 做综合、建立关联，并彻底改变知识工作。来听听他对「当工作 AI 助手发挥全部潜力时，我们还做什么工作」的设想。

## SUMMARY / 摘要

Glean founder and CEO Arvind Jain spent over a decade as a distinguished engineer at Google leading Search, Maps and YouTube teams before co-founding Rubrik and then launching Glean in 2019. His insights stem from deep experience building both enterprise search and AI-powered applications. His insights focus on how to successfully integrate AI into enterprise environments while solving fundamental business problems.

Glean 创始人兼 CEO Arvind Jain 曾在 Google 做了十多年杰出工程师，带领过搜索、地图和 YouTube 团队，之后联合创办 Rubrik，并于 2019 年创办 Glean。他的判断来自同时构建企业搜索与 AI 应用的深厚经验，重点是如何把 AI 真正落进企业环境、同时解决根本性的业务问题。

**Knowledge Infrastructure Comes First: **Building effective AI applications requires a strong foundation of data infrastructure—including deep integrations with enterprise systems, robust security and permissions frameworks, and sophisticated knowledge graphs that understand relationships between people, content, and context. Without this foundation, AI applications will fail to deliver real value, regardless of model sophistication.

知识基础设施优先：有效的 AI 应用需要扎实的数据基础设施——与企业系统的深度集成、稳健的安全与权限框架，以及能理解人、内容与上下文之间关系的复杂知识图谱。没有这层底座，无论模型多先进，AI 应用都无法交付真实价值。

**Context is Critical for Enterprise AI:** Enterprise search and AI applications face unique challenges compared to consumer applications because company data is private, permissions-based, and deeply contextual. Success requires understanding not just content but also organizational structure, user roles, and access rights. Building this contextual understanding through techniques like knowledge graphs is essential for delivering relevant results.

上下文对企业 AI 至关重要：与消费级应用不同，企业搜索和 AI 应用面对的是私有、受权限控制且高度依赖上下文的公司数据。要成功，不只要理解内容，还要理解组织结构、用户角色和访问权。借助知识图谱等技术建立这种上下文理解，是给出相关结果的前提。

**Learn from Human Behavior: **The best AI systems learn continuously from how humans actually work—which documents they engage with, how they interact in communication tools, and what information they find valuable. Tracking these implicit signals creates a virtuous cycle where the system gets smarter over time about what's truly relevant and useful.

从人类行为中学习：最好的 AI 系统会持续从人们的真实工作方式中学习——他们看哪些文档、如何在沟通工具里互动、认为哪些信息有价值。捕捉这些隐性信号会形成正循环，让系统越来越懂什么才是真正相关和有用的。

**Start with Clear User Value:** Rather than building AI technology in search of a problem, focus first on delivering clear value to users through core functionality—like enterprise search—and then expand into more AI capabilities. This creates trust and provides the data foundation needed for advanced features.

从清晰的用户价值出发：不要拿着 AI 技术去找问题，而是先通过核心功能（比如企业搜索）交付明确价值，再扩展到更多 AI 能力。这样既建立信任，也为高级功能积累了所需的数据基础。

**The Future is Proactive:** While today's AI requires explicit user queries, the next evolution will be proactive AI assistants that understand your work context deeply enough to anticipate needs and guide you throughout your day—similar to an executive assistant but available to every knowledge worker. Building toward this vision requires excelling at both the foundational and advanced aspects of enterprise AI.

未来是主动式的：今天的 AI 需要用户明确提问，下一阶段则是主动式助手——它足够理解你的工作上下文，可以预判需求、贯穿全天引导你，类似高管助理，但每位知识工作者都能拥有。走向这一愿景，需要同时把基础层和高级能力都做到极致。

## TRANSCRIPT / 逐字稿

Chapters / 章节

- [Introduction](https://sequoiacap.com/podcast/training-data-arvind-jain#header-0) / 引言
- [Search rankings](https://sequoiacap.com/podcast/training-data-arvind-jain#header-1) / 搜索排序
- [Retrieval-augmented generation](https://sequoiacap.com/podcast/training-data-arvind-jain#header-2) / 检索增强生成
- [Where enterprise search meets rag](https://sequoiacap.com/podcast/training-data-arvind-jain#header-3) / 企业搜索与 RAG 的交汇
- [How is glean changing work?](https://sequoiacap.com/podcast/training-data-arvind-jain#header-4) / Glean 如何改变工作
- [Agentic reasoning](https://sequoiacap.com/podcast/training-data-arvind-jain#header-5) / 智能体推理
- [Act 2: application platform](https://sequoiacap.com/podcast/training-data-arvind-jain#header-6) / 第二幕：应用平台
- [Developers building on glean](https://sequoiacap.com/podcast/training-data-arvind-jain#header-7) / 在 Glean 上开发的开发者
- [5 years in the future](https://sequoiacap.com/podcast/training-data-arvind-jain#header-8) / 五年之后
- [Advice for founders](https://sequoiacap.com/podcast/training-data-arvind-jain#header-9) / 给创业者的建议

*Arvind Jain:* *The majority of the work that we do today is not going to be done by us anymore in five years from now. And that applies to me, that applies to you. Like, you know, we both do very different things, but still, like, I think we are knowledge workers and I think a lot of our work is actually going to be done by these amazing AI assistants that are actually in many ways more powerful than us. Like, you know, they have access to all of our company’s data, our knowledge. They have all the context from all the past conversations and meetings. They don’t forget anything. And they can really sort of—and they have the—you know, on top of that, they have the reasoning capabilities, you know, that allow them to be super helpful to you in, like, any tasks that you do. So that’s sort of our core belief, like, you know, that the majority of our work is actually going to be done by these AI companions or assistants. And we want Glean to be that assistant in the workplace.*

我们今天所做的大部分工作，五年后不会再由我们自己完成。这适用于我，也适用于你。我们做的工作很不一样，但都是知识工作者，而很多工作会由这些在很多方面比我们更强大的 AI 助手完成：它们能访问公司全部数据和知识，掌握过去所有对话与会议的上下文，从不遗忘，还具备推理能力，因而能在你做的任何任务上帮上大忙。这就是我们的核心信念：未来大部分工作会由这些 AI 伙伴或助手完成，而我们希望 Glean 成为工作场景里的那个助手。

#### INTRODUCTION / 引言

**Sonya Huang:** Joining us today is Arvind Jain, co-founder and CEO of Glean. Earlier in his career Arvind was instrumental in building Google search and was co-founder and CTO of Rubrik. Glean began life as an enterprise search company and today has evolved to a general purpose work assistant. Bringing AI into an enterprise context is notoriously difficult because of the integrations, the permissions, the ranking, the parsing–all of the other magic that needs to happen to make AI work on your company data. Arvind joins us today to share how Glean is solving this problem where other companies have failed and what he’s learned as one of the first successful AI-native application companies.

今天加入我们的是 Glean 联合创始人兼 CEO Arvind Jain。他早年参与构建 Google 搜索，也是 Rubrik 的联合创始人兼 CTO。Glean 起初是一家企业搜索公司，如今已演化为通用的工作助手。把 AI 带进企业出了名地难：集成、权限、排序、解析，以及让 AI 能在公司数据上跑起来所需的各种「魔法」。今天我们请 Arvind 分享，Glean 如何解决这个别人没做成的问题，以及作为最早成功的 AI 原生应用公司之一，他学到了什么。

Arvind, thank you so much for joining us. We have a lot of questions about RAG and agents and knowledge graphs and all of that, but before we do that, can you give us one or two minutes on what is Glean and what are you building?

Arvind，非常感谢你加入。我们有一堆关于 RAG、智能体和知识图谱的问题，但在此之前，能不能用一两分钟讲讲 Glean 是什么、你们在构建什么？

**Arvind Jain:** Yeah. First of all, thank you for having me. Glean, think of it as the Google or ChatGPT, but inside your enterprise. It’s a place where your employees go and ask questions and Glean answers all of those questions using your company knowledge, regardless of where that knowledge is, brings it all back to you. So that’s what Glean does. Glean is also an AI platform. So if you want to actually build AI applications inside your company, you can use the Glean RAG platform to build those applications quickly.

首先谢谢邀请。把 Glean 想成企业内部的 Google 或 ChatGPT：员工来提问，Glean 用公司的知识回答，不管这些知识散落在哪里，都给你汇总回来。这是 Glean 做的事。Glean 同时也是一个 AI 平台——如果你想在公司内部构建 AI 应用，可以用 Glean 的 RAG 平台快速搭出来。

**Sonya Huang:** Wonderful. And since you make the analogy of a Google for work, Google for work, I think, is something that every CIO has described as their holy grail. And we have two decades of failed attempts at building it. You were actually a star search engineer at Google before, and even Google never managed to crack this category before. Maybe can you just say a word on why is this such a hard problem and how did you do it?

很好。你打了「工作版 Google」这个比方，而它大概是每位 CIO 心中的圣杯，过去二十年里失败尝试不断。你之前是 Google 的明星搜索工程师，连 Google 都没能攻下这个品类。能不能说说为什么这么难，你们又是怎么做到的？

**Arvind Jain:** Well, I mean, search is hard because it’s actually magic in some sense. Like, you can come and ask any question that you have, and you expect the system to actually give you back the right answer. So expectations are always high. And it’s a difficult problem, especially in the enterprises, because there’s so much information inside the enterprises spread across so many different systems, it’s both hard to actually even get hold of that information, but then even harder to actually make sense of what information is actually good, what has become out of date. So there is lots and lots of challenges around building that system.

搜索难，在某种意义上它就像魔法：你可以问任何问题，并期待系统给出正确答案，期望值天生就很高。在企业里尤其难，因为信息量巨大又分散在很多不同系统里，光是把信息拿全就很难，判断哪些信息是好的、哪些已经过时更难。构建这套系统处处是挑战。

And in the past, I would say that there were no good attempts made because the problem was so—it was so hard, it requires so much R&D, so much investment. Like, you know, it is not really startup friendly in many ways. And you also, like, couldn’t even—you know, in the pre-SaaS world, you couldn’t even build a product because you know, just getting connecting with all of your enterprise data meant that you just spent a year sitting with an enterprise trying to actually bring the data into your search system and then actually, you know, solve the real problem, which is like, you know, make that information searchable.

过去我认为甚至没有过像样的尝试，因为问题太难，需要海量研发和投入，对创业公司很不友好。而且在 pre-SaaS 时代你根本做不出产品：光是连上企业数据，就得花一年时间陪着一家企业把数据接进搜索系统，然后才开始解决真正的问题——让这些信息可检索。

**Pat Grady:** Arvind, one of the things that I think is so interesting about Glean is you are probably one of the first and best examples of what an enterprise AI application company can or should look like. And we’re going to focus most of this conversation on the AI aspects of Glean, however, I know there are a lot of layers to your stack. You’ve got the infrastructure, you’ve got the connectors, you’ve got the governance engine, you’ve got the knowledge graph. Can you say a couple words about all the stuff you had to build before you even got to the AI part to make the AI work?

Arvind，Glean 很有意思的一点是，你大概是企业 AI 应用公司最早也最好的样板之一。今天我们会把重点放在 Glean 的 AI 部分，但我知道你的技术栈有很多层：基础设施、连接器、治理引擎、知识图谱。能不能讲讲，在还没轮到 AI 之前，你们为了让 AI 能工作，先得把哪些东西建出来？

**Arvind Jain:** Absolutely. So as you said, like, you know, search starts first with the data and the knowledge that you need to actually make searchable. So the first part of the Glean tech stack is these deep integrations that we built with most common enterprise systems. So think of systems like Salesforce or Confluence, Jira, Google Drive, SharePoint, ServiceNow. Like, your enterprise data typically lives in all of these different systems, and you bring it all together in one place. So that’s the first part of our technology stack is these integrations.

当然。正如你所说，搜索首先得有要被检索的数据和知识。Glean 技术栈的第一层，是我们与常见企业系统做的深度集成：Salesforce、Confluence、Jira、Google Drive、SharePoint、ServiceNow 等等。企业数据通常散落在这些系统里，我们把它们汇到一处，这就是第一层——集成。

But then if you think about enterprise data, and this is one of the most unique things about enterprise search versus if you think about Google search on the web, is most of your enterprise information is actually private in nature. When you author a document in Google Drive, this document may actually be private to you or you may share it with a few other people, and so you can’t build a search engine in which you just dump all the company knowledge and make it accessible to everyone. You have to actually understand the permissions of each content. So when you go and search, the system should understand who you are and only retrieve information that you actually have access to. So that’s our governance layer. Understanding governance across all of these hundreds of different systems, which is quite complicated.

第二层和网页搜索最大的不同在于，企业信息大多是私有的。你在 Google Drive 写一份文档，它可能只对你可见，或只分享给少数几个人，所以不能把全公司知识一股脑倒进索引、让所有人都能搜到。系统必须理解每份内容的权限：用户搜索时，要识别他是谁，只取回他有权访问的信息。这就是我们的治理层，而要在几百个不同系统里统一理解权限，相当复杂。

And then the third part, and this is where really most products have failed in the past, is search is not about just putting like a whole bunch of documents in an index and then, like, you know, when somebody comes and asks a question, take those words or take that question and just match it up semantically or with keywords, you know, with the right content. You got to actually also understand who’s the person who’s asking a question. You know, I can come in and ask for an onboarding guide because I’m new, I’m a new employee. But then which onboarding guide should be actually, you know, given to me? Like, it depends on like, you know, whether I’m in the marketing team or I’m in the engineering team. So sort of understanding people and understanding knowledge and relationships between them, you know, that’s a big part of actually making a search or a question answering service work inside an enterprise. So we do that. So we actually build a deep knowledge graph, you know, where we look at all the employees, understand what roles do they play in the company, look at all the documents, and then we sort of try to understand what documents are meant for what departments, what documents actually are popular. Like, what are the relationships between a particular individual and a particular document? And that is what we used as a core foundation that sort of then governs like when somebody comes and asks a question, what are the most relevant pieces of knowledge for them.

第三层，也是过去大多数产品折戟的地方：搜索不是把一堆文档丢进索引，等用户提问时把关键词或语义跟内容匹配上就完了。你还得理解提问的人是谁。比如新员工来要一份入职指南，但该给他哪一份？取决于他在市场部还是工程部。理解人、理解知识、理解两者之间的关系，才是企业内搜索或问答能跑通的大头。所以我们构建了一张深度知识图谱：看清所有员工及其角色，看清所有文档，弄明白哪些文档面向哪些部门、哪些文档真正被高频使用、某个具体的人和某份具体文档是什么关系。这张图是基础，决定了用户提问时，哪些知识对他最相关。

So we have to do all of that work. And actually like, interestingly you mentioned like what came, you know, before AI even became relevant. You know, for us, the AI was actually part of the core search technology from day one. We were actually working with LLMs in 2019, or I mean, at least language models like, you know, these were, you know, BERT-based language models that you could use. And so when Glean …

这些工作都得先做完。有意思的是，你提到 AI 变得重要之前的事：对我们来说，AI 从第一天起就是核心搜索技术的一部分。2019 年我们就在用语言模型了，至少是当时可用的 BERT 类模型，所以当 Glean……

**Sonya Huang:** MLMs.

你是说 MLM（掩码语言模型）吧。

**Arvind Jain:** That’s right. Is that the name for them now? But yeah, you know, in the search engineering sort of community, like, we just called them language models at the time. And so the language models were actually part of the core search experience from day one because it really allowed us to understand content at a semantic level. So that we sort of already baked in, like, in our core search experience on day one when we were actually trying to look at a question from a user. We were never sort of limited by the actual exact keywords that users use. We were able to actually understand the meaning behind the question and actually match it up with the right documents. But still that’s sort of all the work that you have to do before you can actually even do anything with LLMs.

对，现在叫这个了？在搜索工程圈子里，当时我们就叫它语言模型。语言模型从第一天起就在核心搜索体验里，因为它让我们能在语义层面理解内容。所以从第一天看用户提问时，我们就不受用户用的确切关键词限制，而是理解问题背后的意思，再匹配到正确的文档。但这些依然只是你真正用上大语言模型之前，必须先做完的功课。

#### SEARCH RANKINGS / 搜索排序

**Sonya Huang:** Can you say a word about rankings? Like, I think part of what makes Google work so well is I always get the answer I want at the top of the page. In the case of the public internet, you have so much web data and links and all that to make the rankings really work. To what extent is that part of the magic for Glean and how do you guys do it?

能讲讲排序吗？Google 好用的一大原因是，我想要的答案总在页面最上面。在公开互联网上，有海量网页数据和链接把排序做得很好。这套「魔法」在 Glean 里占多大分量？你们是怎么做的？

**Arvind Jain:** Yeah, so that’s of course the core of the product is all the effort that we put in to actually build a really good ranking system for our search. I’ll give you some examples of the kind of things that go into determining what documents are the best ones to rank for a given question. So of course, if you imagine that there’s a document that people in the company are constantly looking at, so that gives you obviously a signal that there must be something about it. It’s actually important, people like to spend time on it. If there’s a document that was actually written in the last one or two weeks and there’s some engagement around it, you know that this again is information that people care about. It’s not actually become obsolete yet. Then if you think about the particular document that we see is not popular, like, when you look at a company level, but you look at one individual team inside the company, we see there’s heavy usage for that document inside that particular team. So that sort of tells us more about that, hey, this document may actually be relevant for this particular set of people.

排序系统当然是产品的核心，我们投入了大量精力。举几个决定某个问题该把哪些文档排在前面的信号：如果公司里的人一直在看某份文档，这显然说明它重要、大家愿意花时间；如果一份文档是最近一两周写的、并且有互动，说明信息仍被关心、还没过时；再比如某份文档在公司层面不热门，但在某个团队内部被重度使用，那就说明它对这一小群人特别相关。

Or the last thing, the last example, imagine that somebody had a question and they’re not bothering to a search, they go in Slack and ask a question, and then somebody else posts a link to a document as a response to that, and the person who asked the question gave a thumbs up to it. Just imagine this interaction, like what it means. It actually means that particular document was actually a really good answer for that question that the user had asked. And so if you keep that association in mind, like, it’s going to help you later when somebody else came and asked a similar question.

最后一个例子：有人遇到问题懒得去搜，直接在 Slack 里问，另一个人贴了一份文档作回答，提问者点了个赞。想象一下这个互动的含义——那份文档确实很好地回答了那个问题。把这种关联记下来，等以后别人问类似问题时就能派上用场。

So those are some of the signals. You have to sort of constantly look for all these signals, you know, they have to collect them differently in the enterprise setting. Then, you know, on the web, Google only has to look at all the activity that’s happening right on Google itself because that’s the gateway to any sort of knowledge quest. But if you look at in the enterprise, you know, not all the things are happening, you know, through the search paradigm. So you have to sort of go and look at all the activity around all the knowledge in different systems, like, you know, your communication systems, your document systems, and just try to learn from that human behavior. Because ultimately that’s how you learn. You learn from what people are doing inside the company. The more you can actually collect, you know, that information, the better your ranking systems are going to be.

这只是部分信号。你得持续捕捉这些信号，而且在企业环境里，采集方式和网页不同：Google 只需看发生在 Google 自己身上的行为，因为它是一切知识检索的入口；企业里并非所有事都通过搜索发生，你得去各系统里看围绕知识产生的全部活动——沟通系统、文档系统——并从人类行为中学习。说到底学习就是这么来的：看公司里的人实际在做什么。这类信息收集得越多，排序系统就越好。

#### RETRIEVAL-AUGMENTED GENERATION / 检索增强生成

**Sonya Huang:** Totally. Can we spend a minute on RAG? As Pat mentioned, you were kind of in the right place at the right time. You had put together all the hard stuff so that when the LLMs got really good, you kind of had all the infrastructure in place. And I think you’ve been one of the experts in using RAG to make these LLMs actually useful on your corporate content. Can you explain RAG to me like I’m five years old, and, like, what are the secrets to making it work? What are the things that people don’t talk about? You know, what are examples of things that you can do thanks to RAG that you can’t in a generic chat interface?

完全同意。能花一分钟讲 RAG 吗？正如 Pat 说的，你们恰好处在对的时间点上：把硬骨头都啃完了，等大模型变强时基础设施已经就位。你也是用 RAG 让大模型在公司内容上真正有用的专家之一。能不能把我当五岁小孩解释一下 RAG？做好它的诀窍是什么、大家不太谈的东西是什么？还有，有了 RAG 能做哪些在通用聊天界面里做不到的事？

**Arvind Jain:** Yeah, well, so first of all, I think since you were talking about a five year old, let’s first talk about what RAG is.

好，既然你提到五岁小孩，那我们先说说 RAG 是什么。

**Sonya Huang:** Okay. 10 year old. 10 year old.

好，那就十岁吧，十岁。

**Arvind Jain:** So yeah.

嗯，好。

**Pat Grady:** I need five. Let’s start with five.

我要五岁版的，还是从五岁开始吧。

**Arvind Jain:** Let’s start with five. Yeah. So I mean, like, if you think about all these amazing models, you know, GPT and Gemini and Claude, these models are all trained on the world’s public knowledge and data. And so if you were to actually go in ChatGPT and ask a question like, “Hey, how many days do I get off with my PTO policy?” it has no idea. Like, it can’t answer that question because that’s my company’s private knowledge. The answer is somewhere there and the model is not trained on it.

就从五岁开始。你看 GPT、Gemini、Claude 这些很棒的模型，都是用全世界的公开知识训练的。所以你去 ChatGPT 问「我的带薪休假政策有几天？」，它根本不知道——那是我公司的私有知识，答案就在某处，但模型没学过。

So how do you bring your private enterprise data to these models so that you can actually have AI create that magic for you? That’s what a RAG-based AI application architecture allows you to do. So the way it works is that you come and ask a question, and you have a search engine or a retrieval engine, whatever you want to call it. And given the question, this retrieval engine, you know, finds potentially relevant documents, you know, that could actually answer your question. And then you’re going to take those documents or those sort of content fragments and make the model work on it. You’ll tell the model like GPT that “Hey, I have this question and I have this company knowledge that I think is relevant, you know, in terms of answering that question. Now you answer that question using this knowledge.”

那怎么把企业私有数据带给模型，让 AI 为你创造这种魔法？这正是基于 RAG 的 AI 应用架构要做的事。流程是：你提一个问题，有一个搜索引擎或检索引擎，它根据问题找出可能相关的文档；然后你把这些文档或内容片段交给模型，告诉它「我有这个问题，也有这些我认为相关的公司知识，请用这些知识回答」。

So this is how, like, most AI applications today are being built in the enterprise. The only way to actually connect, you know, your private enterprise data to the power of these language models is basically a search engine that’s sort of sitting, you know, in the middle. So we—like in our given—you know, at Glean also, like, you know, we of course built a search engine for all of our enterprise content in the last five years. It actually allowed us to actually become one of the best RAG systems that allows you now—not only of course we deliver our own end user application, which is a Glean assistant, using this RAG-based application architecture, but we’re also allowing companies to actually build more and more applications using RAG.

今天企业里大多数 AI 应用就是这么搭的。把私有企业数据与语言模型能力连起来的唯一方式，基本就是中间放一个搜索引擎。Glean 过去五年为企业全部内容建了搜索引擎，这让我们成为最好的 RAG 系统之一：不仅用这套架构交付自己的终端应用 Glean 助手，也让越来越多企业基于 RAG 构建自己的应用。

Now I think in terms of—while this is the architecture that is emerging as a canonical architecture for building AI applications, I think it is still full of challenges. It’s actually really hard to build great AI applications using RAG because one of the things that, you know, how models themselves are sort of while very powerful, they’re also still an emerging technology. Like, models hallucinate, they make things up. And what you’re doing now is you’re actually adding one more complex layer of technology in this application architecture. So think of it like you’re chaining two things which are both not perfect.

不过，虽然这正在成为构建 AI 应用的典范架构，它依然满是挑战。用 RAG 做出优秀 AI 应用其实很难：模型本身虽然强大，却仍是新兴技术，会幻觉、会编造；而现在你又往架构里加了一层复杂技术，等于把两个都不完美的东西串在一起。

So oftentimes you will see a RAG-based AI application not perform well because you asked a question and the failure actually happens at the RAG stage, at the retrieval stage where you didn’t even actually—you know, weren’t able to find the right pieces of knowledge or maybe you found like, you know, stale information that then you’re actually giving to the LLM to work on. And then of course it’s going to give you bad results. So it actually—you know, while it’s the only way to sort of bring knowledge together, it creates these interesting challenges for you as well.

所以你常会看到 RAG 应用表现不佳：问了个问题，失败其实发生在 RAG 的检索阶段——压根没找到正确的知识，或者找到的是过期信息，再喂给大模型，结果自然很差。所以，尽管这是把知识汇聚起来的唯一办法，它同时也带来了这些有趣的挑战。

#### WHERE ENTERPRISE SEARCH MEETS RAG / 企业搜索与 RAG 的交汇

**Pat Grady:** Let me ask you a question—and just to paraphrase a bit what you were saying at the start of this conversation, act one: enterprise search; act two: application platform. For that, act on, which is enterprise search, how do the concepts of enterprise search and RAG relate? Is one a superset or a subset of the other? Are they similar but distinct? Are they the same thing? How does enterprise search and RAG—how do those concepts relate?

我问个问题，顺带复述一下你开场说的：第一幕是企业搜索，第二幕是应用平台。就第一幕而言，企业搜索和 RAG 这两个概念是什么关系？一个是另一个的超集或子集？相似但不同？还是同一回事？

**Arvind Jain:** So I think, like, you know, I think of search and RAG as being in some sense, you know, they’re one and the same thing. The real core technology is taking all of your knowledge, enterprise knowledge, and putting them into this search system where now you can actually ask questions, and the system is able to actually give you relevant pieces of information back. So that’s sort of the core technology. Now you can actually use this technology either as a standalone product, so that’s what the Glean search product is, for example, where people come in, they ask questions and we can give them the relevant documents that potentially are useful to them based on that question. Or you could actually use this as an API layer in your overall AI application. So where the search system, the search module now is only one component of your overall AI application architecture. And so I think in that sense it’s sort of similar.

我认为搜索和 RAG 在某种意义上是同一件事。真正的核心技术是：把全部企业知识放进一个搜索系统，让你可以提问，系统能返回相关的信息片段。这项技术既可以做成独立产品——比如 Glean 搜索，用户来提问，我们基于问题给出可能有用的文档；也可以作为整个 AI 应用架构里的 API 层，这时搜索模块只是其中一个组件。从这个角度看，两者是相通的。

But the industry on the other hand, like, I think what we’ve seen most of these RAG-based applications in the enterprise today, they actually use a much more simpler version of a retrieval system in their RAG application, typically like a vector search-based system which doesn’t really have full enterprise context. And so I would say, that’s the key difference. So for us, our approach always has been to really think about how to build a standalone search system, something that is as good, that you can actually put them in front of the users as a standalone product. That’s really the real test for how good the search is. And that then actually when you put it behind the scenes in a RAG-based application, it’s actually going to actually create better AI experiences.

但行业里我看到的是，今天企业中的大多数 RAG 应用用的是简化得多的检索系统，典型的就是向量搜索，它并没有完整的企业上下文。我认为这才是关键差别。我们的思路一直是：先做一个能单独摆到用户面前、足够好的独立搜索系统——这是检验搜索好不好最真实的标准；然后把它放到 RAG 应用背后，才会带来更好的 AI 体验。

**Sonya Huang:** So is it fair to say that kind of the magic that you’ve done in terms of getting a good ranking of search results, that is exactly—like, you’ve made that ranking good for people. It turns out making that ranking good for people is also what you need to make the ranking good for machines in order to get the best possible results. And that’s why, you know, what you’ve built is very different from somebody that’s just DIYing a data pipeline and their own little retrieval system.

所以可以这么说吗：你们把搜索结果排序做好的那套「魔法」，本来是为人做的；结果发现，让人觉得排得好的能力，恰好也是让机器得到最好结果所需要的排序能力。这正是你们和那些自己 DIY 数据管道、搭个小检索系统的人的根本区别。

**Arvind Jain:** Yeah. Yeah, that’s correct. I mean, I think it’s really hard to build these systems, you know, like yourself and build them in a matter of weeks. Like, I think you can build a great AI demo, you know, in one day, maybe like in two hours now. But I think, like, to actually build, you know, where it’s sort of like, you know, it’s robust, it’s stable, it actually adds value to your—within your enterprise, you know, like, you know, it’s a hard problem.

对，没错。自己几周内把这类系统搭好非常难。做出一个漂亮的 AI demo，现在也许一天、甚至两小时就够了；但要做得稳健、稳定、能在企业里真正产生价值，那是很难的问题。

#### HOW IS GLEAN CHANGING WORK? / Glean 如何改变工作

**Pat Grady:** So we’ve talked a little bit about how you’ve built what you’ve built and we know that it’s working. We know that the company is quadrupling year over year. And we use it here internally, and there are a lot of happy people out there who are customers of yours. The real measure of success in some ways is how your product is changing the lives of its customers. And so I’m curious to hear from you, when you look at your customers and sort of how they operate day to day pre-Glean versus post-Glean, what are some of the changes you notice? How does this help people do their jobs?

我们已经聊了一些你们怎么把东西建出来，也知道它跑得通：公司年同比增长四倍，我们自己内部也在用，外面很多客户用得很开心。某种意义上，真正的成功标准是产品怎样改变了客户的日常。所以我很好奇：你观察客户在「用 Glean 之前」和「之后」的运作方式，看到了哪些变化？它到底怎么帮人把工作做好？

**Arvind Jain:** So Glean is actually a product that is used quite heavily by people. Like, there’s many, many different types of things. We’re often surprised by what people are using Glean for, but I would give you a few examples. So for engineering teams, you know, they find Glean super useful, like, in terms of troubleshooting. Whenever you run into any kind of a roadblock or an issue, like, sometimes an error like, you know, your programs are not working properly, and so Glean serves as a really good troubleshooting tool for them. Like, you know, it’s a place where you go and debug because you post the issue. More often than not, you’re not the first one who’s going to experience an issue. Like, somebody else has experienced those issues before. So just getting the context from all of those, you know, like, all the other people and how they solved that problem before, like, you know, that sort of helps you move, solve that issue for yourself.

Glean 是个被用得很重的产品，用途非常多样，连我们都常常惊讶于人们拿它做什么。举几个例子：工程团队觉得它在排查问题上特别有用。遇到任何卡点或故障，比如程序跑不对，Glean 就是很好的排障工具——你把问题贴进去调试，而多数情况下你不是第一个遇到这个坑的人，别人早就碰到过、也解决过。把那些上下文和别人的解法拿过来，就能帮自己把问题解决掉。

So that’s—you know, that’s a big use case for engineering. For some roles, like for support, you know, their life day in, day out is about resolving, you know, answering people’s questions. And I think a tool like Glean actually fundamentally just changes how they work now because by default now they don’t think about giving a question, like trying to go and look for answers in different knowledge bases and whatnot. Instead the first reaction that they have now is that there’s a question that’s coming in from a customer, and then Glean on the side is actually already answering those questions for them. So their sort of model of working changes from trying to find things to actually trying to validate what AI is telling them is the right answer, and then just share that back with users.

这是工程侧的大场景。对支持岗位来说，日常工作就是回答别人的问题，Glean 从根本上改变了他们的工作方式：现在默认动作不再是去各个知识库里翻答案，而是客户问题进来时，旁边的 Glean 已经把答案给出来了。他们的工作模式从「找东西」变成「验证 AI 给的答案对不对」，然后回复用户。

Some teams have actually really changed their behavior. Like salespeople, for example, they use Glean as a way to prep for meetings. So before, like, a customer call is coming up, they will just ask Glean. Like, you know, they can be lazy. They can ask Glean, like, you know, help me prep for this meeting. And Glean is actually going to bring that 360 view of all of the data from that customer, like what happened in the last meeting, who’s—you know, like what opportunities are open with them and things like that. So it sort of really helps them prep for a meeting, then actually run a meeting well, because customers always have lots of questions. And so the salespeople feel more confident, you know, like, running that meeting. Because if somebody throws a curveball at them, you know, they can just ask clean, like, right in the meeting, you know, get the answer and quickly sort of, you know, get the responses back.

有些团队的行为真的变了。比如销售用 Glean 准备会议：客户电话前直接问一句「帮我准备这次会议」，Glean 就会把该客户的 360 度视图端出来——上次会议发生了什么、有哪些在谈的机会等等。这帮他们把会前准备做好，会上也更从容，因为客户总会问各种问题；万一被问个措手不及，他们可以在会议中直接问 Glean 拿到答案，快速给出回应。

So in fact, like, you know, in our company, we don’t allow salespeople to actually bring in sales engineers in the call. Like, they have to answer those questions themselves. So that’s like, you know, one change in behavior that we drive, like in the first few calls. Yeah, those are some of the things. But overall, the use cases are unbounded. Like, the one that I think is the one that’s universal across everybody inside the company is finding other people who can help you. That is one of the things that Glean makes it really easy for people. We help you connect with the right subject matter experts based on what questions you have. So that’s one thing that we see everybody in the company make use of a lot.

事实上在我们公司，销售不允许把售前工程师拉进客户电话，必须自己回答这些问题。这是我们在头几次通话里就推动的行为改变。总体来说用例是无穷的，但我觉得全公司最通用的一个是：找到能帮到你的人。Glean 让这件事变得很容易，根据你的问题把你接到合适的领域专家，这点几乎公司里每个人都在大量使用。

**Sonya Huang:** Is there a North Star metric you track? Like, these are wonderful kind of stories of customer impact. I guess, how do you benchmark yourselves objectively?

你们有北极星指标吗？这些客户影响的故事很棒，但你们怎么客观地给自己打分？

**Arvind Jain:** Yeah, so our key metric is how many questions people ask on a daily basis and actually get successful—like, you know, we were successful in answering those questions correctly for them.

我们的关键指标是：人们每天问了多少问题，并且其中有多少被我们正确回答了。

**Sonya Huang:** Hmm. So similar to, like, Google’s Search SAT metric then.

嗯，有点像 Google 的搜索满意度指标。

**Arvind Jain:** Okay. Can you share anything about those numbers, or do you prefer to keep it private?

这个数字能分享一点吗，还是你更愿意保密？

**Arvind Jain:** Well, we have—so yeah, so we have this technical metric. I don’t know how much sense it’s going to make, but we tend to actually keep that number at 80 percent. So I think it’s a proxy for that 80 percent of the sessions, you know, that users had with us, they were actually successful in getting what they needed.

我们确实有这个技术指标，我不知道说出来好不好理解：我们一般把它维持在 80%。它大致是个代理指标，意思是约 80% 的用户会话里，用户拿到了他需要的东西。

**Pat Grady:** And is that—do you measure that success, is that explicitly they thumbs up, this was good. Or is that implicitly they take action on the basis of the results that you served, and you can see that action taking—how do you actually measure the success?

这个成功是显式衡量的吗——比如用户点个赞说「很好」？还是隐式地看他们是否基于结果采取了行动，你们能看到这个动作？到底怎么测？

**Arvind Jain:** It’s actually implicit. So we will track their actions. For example, in search, when you come and ask a question, and then you click on one of the top two or three results and go to the destination and then stay there for a long time, so that sort of gives us an indication that you were happy. You didn’t come back and ask another question quickly or refine your search. So that’s sort of how we track, like, whether somebody’s successful or not.

是隐式的，我们跟踪行为。比如搜索时你问了个问题，点了前两三条结果里的某一条、跳到目标页面并停留很久，这就说明你比较满意；你没有马上回来再问一次或改写查询。我们大致用这类信号判断一次搜索是否成功。

**Pat Grady:** Got it. What are some of the top things that are not in the product yet that you think will make people more successful?

明白。那现在产品里还没有、但你觉得最能让人更成功的，排在最前面的是哪些东西？

**Arvind Jain:** I think the—like, I referred to this, you know, when we started, that building a product like ChatGPT or Glean, it’s sort of like magic. Like, you know, the expectations are infinite. And because, you know, like, it’s supposed to basically not just answer any questions that people have, but also perform any task that they actually ask you to do. And so for us, it’s not so much about what features are missing. Like, you know, like, the big thing that we have to actually keep working on is actually be successful at this core feature, which is like, you know, answer people’s questions correctly, and answer questions of higher and higher complexity correctly for them over time.

我开头提过，做 ChatGPT 或 Glean 这类产品有点像变魔法，大家的期待是无限的：它不该只是回答任何问题，还得执行你交给它的任何任务。所以对我们来说，重点不是「缺哪些功能」，而是必须持续把核心那件事做成——把人们的问题答对，并且随时间推移能答对越来越复杂的问题。

So we feel like us or anybody else out there today, we’re all very far away from that true vision for our product, which is that we want Glean to be that AI assistant that can actually answer any questions that you have using your company knowledge, that can actually do half of your work for you in the future. And so I think, like, I would say, like, you know, we’re maybe two percent of the way there. Like, you know, AI, for all is said and done, you know, we’re still in very, very early stages of making that impact.

我觉得无论是我们还是外面任何人，今天离产品真正的愿景都还很远：我们希望 Glean 是那个能用公司知识回答你任何问题、未来能替你做掉一半工作的 AI 助手。所以我说，大概只走完了 2% 吧。AI 说得再多，我们对产生这种影响还处在非常非常早期的阶段。

#### AGENTIC REASONING / 智能体推理

**Sonya Huang:** So we’re only two percent of the way there. I’d love to ask you actually about agentic reasoning. It’s something that’s been on our mind a lot as a partnership at Sequoia, and I know it’s been on your mind as well as a founder. And one of the results that I was really impressed by in the coding space was that, you know, with RAG, I think these coding agents can get to three, four percent completion rates, but if you give them more agentic reasoning capabilities, they can get to 14, 15%. So like a multifold improvement. And, you know, it’s as simple as, you know, go reflect on what you just said or best event or, you know, whatever the techniques are. I’d love to understand how you guys are thinking about incorporating more agentic reasoning into your products, and anything else to kind of get from that two percent where you said we are today to what you hope to build one day.

才 2% 啊。那我很想问问智能体推理，这是红杉合伙层面最近想得很多的话题，我知道你作为创始人也在想。编码领域有个结果让我印象很深：用 RAG 时编码智能体的任务完成率大概只有 3%–4%，但加上更多智能体推理能力后能到 14%–15%，是数倍提升，而手段可能只是「反思一下你刚说的」或者 best-of-N 之类。我想了解你们打算怎么把更多智能体推理纳入产品，以及怎么从你说的 2% 走向你希望建成的样子。

**Arvind Jain:** Yeah. And I want to clarify the two percent is something that I was making up. Like, it’s not a measured number.

先澄清一下，那个 2% 是我随口编的，不是实测数字。

**Sonya Huang:** Yeah. Yeah.

嗯嗯，明白。

**Arvind Jain:** I just wanted to sort of, you know, express, like, how early things are today and how much amazing things we’re going to see in the future. Like, I was just basically trying to talk more about that. But in terms of agentic behavior, one of the things that we are doing on that front is first try to actually get a lot of input from our users. So we have a concept of building a workflow inside Glean to actually answer a complicated question. And today we actually seek a lot of help from our users in sort of completing that workflow. We’ll actually—like, say, for example, if you come and ask a question like, “Help me write a weekly status report of all the work that my team did.”

我只是想表达今天有多早期、未来会看到多少了不起的东西。回到智能体行为，我们做的一件事是先从用户那里拿到大量输入。Glean 里有个概念：为回答一个复杂问题构建一条工作流，而今天我们会在完成这条工作流时大量求助用户。比如你来问「帮我写一份团队本周所有工作的周报」。

So this is your question. Now if you think about this question, it’s complicated. There are a few things you need to do to actually go and really figure out the answer to it. The first thing is you have to actually understand what do you mean by ‘your team?’ Who’s your team? You have to maybe go in your HR system, try to figure out who are the people who report to you. Then we are talking about work. So where does work happen for each one of these team members? You sort of build an understanding of that, like, you know, and then go sort of pull a bunch of knowledge from all these different systems.

这就是你的问题。想想看，它很复杂：要真正回答，得先做几件事。第一，得弄明白「你的团队」指谁——可能要去 HR 系统查谁向你汇报；然后「工作」发生在哪里？得为每位成员建立起这个理解，再去各个系统里把相关知识拉出来。

So I think right now what we’re doing is we’re actually trying to get help from our users, and we will sort of create a plan for a complicated question, try to actually get the user to actually input and tell us, like, you know, are we getting it right? Sometimes, you know, users can actually explicitly, like, completely ignore what we do and just build a workflow on their own. And I think that’s going to be essential for us to build that fully agentic behavior for the future. I think you can build agentic behavior for a specific narrow set of problems, but in Glean, since our footprint is so wide, there is the range of questions that people can have, the range of tasks that they want to perform is so broad that we feel like first we have to learn. We have to learn from workflows that people are going to actually create manually, and then build these models which can then take complicated questions in the future and automatically build those, convert them into these agentic loops or a complicated workflow. So that’s the approach that we are taking on it.

所以我们现在的做法是请用户帮忙：为复杂问题生成一个计划，让用户确认我们理解得对不对；有时用户甚至可以完全忽略我们给的计划，自己搭一条工作流。我认为这对将来实现完整的智能体行为非常关键。针对一组很窄的问题，你可以做出智能体行为；但 Glean 覆盖面太宽，用户的问题和想做的任务范围太广，所以我们先得学习——从人们手动创建的工作流里学，再训练模型，让它们未来能把复杂问题自动转成智能体循环或复杂工作流。这是我们的路径。

**Sonya Huang:** I see. So you’re saying since you have such a broad surface area, you can’t build agentic reasoning for every single possible task, and so instead you’re exposing a workflow engine for your users to individually be able to build different automations and different agents.

明白了。你是说，因为覆盖面太宽，没法为每一种可能的任务都写一套智能体推理，所以干脆把工作流引擎开放给用户，让每个人自己搭不同的自动化和不同的智能体。

**Arvind Jain:** Yeah, and then you learn from it. And then you learn from it, so once you see people building these workflows, that sort of then fits and goes into a training data set to sort of allow you to actually automatically build, like, new workflows based on complicated questions that people have. So those agentic capabilities are coming, but again, I would say when it is hard for you to answer simple questions, then if you want to do complicated tasks, it’s equally hard because you’re going to make a mistake. Imagine an agent that actually breaks down a complex task into a series of 10 individual tasks, then your error rate is going to compound, like, if each step is 90 percent accurate. So there is like—it is incredible, but I think it is still something that we are—I feel like the human assist is actually critical in building these complicated workflows.

对，然后从中学。看到人们搭出这些工作流，它们就进入训练数据，让系统能基于新的复杂问题自动生成工作流。智能体能力会来，但我还是那句话：连简单问题都难答好的时候，做复杂任务一样难，因为错误会累积。想象一个智能体把复杂任务拆成 10 个子任务，就算每步 90% 准确，错误率也会复合放大。所以我认为，在构建这些复杂工作流时，人的协助仍然至关重要。

#### ACT 2: APPLICATION PLATFORM / 第二幕：应用平台

**Pat Grady:** It’s also—Arvind, it might be worth saying a word—maybe this is obvious to people who are listening, but just to state it explicitly, how act one, which is the enterprise search business, gives you the moral authority or the unfair advantage to get into act two, which is the application platform, or the platform for agentic behavior. It may not be totally obvious to people how act one leads to act two. Can you just say a couple words about that?

还有一点，Arvind，也许听众觉得显而易见，但值得明说：第一幕的企业搜索业务，凭什么给了你们进入第二幕——应用平台、或者说智能体行为平台——的「资格」或不公平优势？第一幕怎么通向第二幕，可能不是人人都看得明白，能讲两句吗？

**Arvind Jain:** By building the search product, which immediately adds value to our customers, to our users, we are able to actually solve a bunch of complicated problems that you will typically run into in an enterprise. The first part of that is security. So if you think about the Glean product, we are actually telling our customers that hey, give us all of your data and we’re going to hopefully do something useful for you after you give that data to us. And that’s a big demand. Like, it’s not easy for companies to actually trust, you know, a new product company, a startup with all of their data when they’re actually not getting any immediate value from it.

做出搜索产品，立刻给客户和用户带来价值，同时也让我们顺带解决了一批企业里必然会碰到的复杂问题。第一件是安全。你想，Glean 是在对客户说「把所有数据交给我们，我们拿去变点有用的东西出来」，这个要求很高。让一家企业把全部数据交给一家新产品公司、一家创业公司，而当下又拿不到即时价值，并不容易。

And so that is one of the things that we’ve seen to be super helpful to us, because we actually have this search product that people understand, that people want, and they want to deploy. So it’s already deployed now, and so Glean is running and it’s already connected with all of your enterprise data inside the company. And so then, like, you know, helping us going to our customers and then saying to them that, like, “Look, you know, use that as your core AI data platform,” is a much easier sell because we don’t actually have to convince them again to actually give all of their data to us. It’s already there.

这一点对我们帮助特别大：我们有一个大家看得懂、也想要、愿意部署的搜索产品。它一旦部署，Glean 就已经在公司里跑着、并且连上了全部企业数据。这时再去跟客户说「把它当作你的核心 AI 数据平台吧」，就好卖得多——因为不必再说服他们把数据给我们，数据本来就在那儿了。

**Pat Grady:** So this might not be a perfect analogy, but hopefully it’s not a terrible analogy that, you know, Tesla had an advantage in self driving because they’re already selling cars. You guys have an advantage in delivering AI agents because you’re already selling a data platform that organizes all the enterprise information, makes it accessible, makes it secure, kind of puts people in a position where they’re already asking questions of it, and it’s kind of a logical next step to ask it to start taking actions.

打个不太完美、但大概也不算太糟的比方：Tesla 在自动驾驶上有优势，是因为它本来就在卖车；你们在交付 AI 智能体上有优势，是因为你们本来就在卖一个把所有企业信息组织好、变得可访问又安全的数据平台，人们已经在上面提问了，那让它开始替你采取行动，就是很自然的下一步。

**Arvind Jain:** Absolutely.

完全正确。

#### DEVELOPERS BUILDING ON GLEAN / 在 Glean 上开发的开发者

**Sonya Huang:** I think you also announced a set of APIs that let developers build on Glean. Maybe say a word on that. Like, I think that was in response to customer demand. What makes developers want to build on Glean versus directly access their own data? I think it’s probably a similar effect to what you just talked about.

我记得你们还发布了一组 API，让开发者能在 Glean 上构建应用，能说说吗？我理解这是响应客户需求。开发者为什么愿意基于 Glean 开发，而不是直接读自己的数据？大概跟你刚讲的效应类似。

**Arvind Jain:** Yeah. So a lot of AI applications that our customers are wanting to build, they need to actually tap into data that lives in multiple different cloud-based SaaS systems. And I think it’s quite tedious for them to first go and actually bring that data in one place, build a search or retrieval layer using that. The integrations are hard, understanding permissions and governance is really, really hard on that. And I think when people—like, as these models actually became accessible and developers started to actually develop AI applications, they realized that—well, they were really excited about building these new cool AI apps, but basically they realized that building an app, 90 percent of the work was actually this boring infrastructure work that they didn’t want to do, like bringing data from all these different systems, running these ETL and data pipelines and then sort of building a good search over it. So you’ll spend so much time before you actually even get to play with AI.

是这样。客户想做的很多 AI 应用，都需要接进散落在多个云端 SaaS 系统里的数据。让他们先把数据汇到一处、再在上面搭搜索或检索层，非常繁琐：集成很难，理解权限和治理更是难上加难。等模型变得可用、开发者真开始做 AI 应用时，他们本来很兴奋要做新奇的 AI 应用，结果发现做一个应用有 90% 的工作量是这些他们不想干的枯燥基础设施活——从各系统搬数据、跑 ETL 和数据管道、再在上面做一套像样的搜索。光这些就花掉大把时间，还没轮到玩 AI。

And so that’s the thing that they find very useful with Glean because we’re actually solving all the problems around ETL, building a great search, properly obeying governance within your company. All of that stuff is done for you. You just have your search API, and you can focus all of your attention on the business problem that you’re working on and how AI can help you achieve that automation that you’re looking for.

这正是他们觉得 Glean 有用的地方：ETL、建好搜索、严格遵循公司内部的权限治理，这些问题我们都替他们解决了。你拿到的就是一个搜索 API，可以把全部注意力放在要解决的业务问题上，以及 AI 怎么帮你实现想要的自动化。

**Sonya Huang:** In some ways, all the hard work you’ve done to ETL and put all the data together with data governance reminds me a lot of Snowflake. And you’re really doing it with text data and unstructured data. But just that central data platform that companies can build around, build apps on top of reminds me a lot of the Snowflake story.

从某个角度看，你们在 ETL、把数据汇到一起、再配上数据治理上做的这些苦活，让我想到 Snowflake；只不过你们处理的是文本和非结构化数据。但「一个公司可以围着它建系统、在上面搭应用的中央数据平台」，确实很像 Snowflake 的故事。

#### 5 YEARS IN THE FUTURE / 五年之后

**Pat Grady:** Arvind, can we ask you a question about future state, if you allow us to dream for a few minutes? Five or ten years from now, how do you think Glean is showing up inside of a business? And maybe more importantly, if you’re the typical knowledge worker five or ten years from now and you are equipped with Glean, what is your life like then?

Arvind，能问一个关于未来状态的问题吗，允许我们畅想几分钟：五年或十年后，Glean 会以什么形态出现在一家企业里？也许更重要的是，五年或十年后一个配备了 Glean 的普通知识工作者，他的日子是什么样的？

**Arvind Jain:** That’s a great question. I think let’s keep it five years instead of ten. And I think the—well, I mean, one belief that I have is that the majority of the work that we do today is not going to be done by us anymore in five years from now. And that applies to me, that applies to you. Like, you know, we both do very different things, but still, like, I think, you know, we are knowledge workers, and I think a lot of our work is actually going to be done by these amazing AI assistants that are actually in many ways, you know, more powerful than us. Like, you know, they have access to all of our company’s data, our knowledge, they have all the context from all the past conversations and meetings. They don’t forget anything and they can really sort of—and on top of that, you know, they have the reasoning capabilities that allow them to be super helpful to you in any tasks that you do.

好问题。我想还是说五年吧，不说十年。我有一个信念：我们今天做的大部分工作，五年后不会再由我们自己完成。这适用于我，也适用于你。我们做的事很不同，但都是知识工作者，而其中很多工作会由这些在很多方面比我们更强大的 AI 助手完成。它们能访问公司全部数据和知识，记得过去所有对话与会议的上下文，从不遗忘，再加上推理能力，就能在你做的任何任务上帮上大忙。

So that’s sort of our core belief, like, that, like, the majority of our work is actually going to be done by these AI companions or assistants. And we want Glean to be, you know, that assistant in the workplace. We want Glean to be the place where most of your work happens.

这就是我们的核心信念：未来大部分工作会由这些 AI 伙伴或助手完成，而我们希望 Glean 就是工作场景里的那个助手，成为你大部分工作发生的地方。

One of the things that we also think is going to change is today a lot of AI is about you go and seek help from these AI agents. For example, you go and ask questions, you get answers back. But the future is sort of—the future is where this assistance is going to be proactive. It’s sort of like if you think about, like, if you have an executive assistant, they actually help you a lot. A lot of their help is when you go and ask them for help, but a lot of their help is actually proactive in nature. They tell you what to do next, they manage your day, they know everything about your work life, and they guide you to be effective throughout the day. And I think AI is going to actually allow that luxury regardless of who you are. And today, some executives in the company have that luxury, but in the future everybody’s going to have these really powerful AI-based assistants that are going to actually help them do their work. So we’re really excited about bringing that change to the workplace, and hope that, you know, Glean can be the world’s most successful AI assistant.

另一个会变的是：今天的 AI 大多是主动去找它帮忙——你去提问、拿回答案；未来的协助是主动式的。想想高管助理，很多帮助来自你开口求助，但同样多其实是主动的：告诉你接下来做什么、替你安排一天、了解你工作生活的一切，并引导你全天保持高效。我认为 AI 会让这种「奢侈品」不再挑人。今天公司里只有部分高管有这个待遇，未来每个人都会拥有这样强大的 AI 助手来帮自己干活。我们很兴奋能把这种变化带进职场，也希望 Glean 能成为世界上最成功的 AI 助手。

**Pat Grady:** Love it.

太好了。

#### ADVICE FOR FOUNDERS / 给创业者的建议

**Sonya Huang:** Arvind, can we change gears a little bit? And I’d love to step back and hear your advice for other founders. You are one of the most successful application-level AI companies—I think probably number two behind Copilot and Scale. And you did it as a startup, as an independent startup. I think you’ve also had to navigate some unique challenges, right? Like OpenAI, for example, is one of your providers and also one of your competitors, one of your top competitors. Maybe just tell us what that dynamic is like.

Arvind，我们换个话题，我想退一步听听你给其他创业者的建议。你们是最成功的应用层 AI 公司之一，我觉得大概排在 Copilot 和 Scale 之后，而且是以一家独立创业公司的身份做到的。你们还得应对一些独特挑战吧？比如 OpenAI 既是你们的供应商，又是你们的头部竞争者之一。能说说这种关系是什么感觉吗？

**Arvind Jain:** Well, I mean, first of all, from a point of view of, like, building a startup, in fact, like, you know, I’ve been actually quoting you guys in many places. Like, you know, Pat, I remember the slide where you talk about, like, the overall software market being $600 billion, but then AI sort of is, you know, expanding that market to $15 trillion or $12 trillion. Something massive.

先说做创业公司这件事，其实我在很多场合都引用过你们的内容。Pat，我记得你有页片子讲整体软件市场是 6000 亿美元，而 AI 会把它扩展到 15 万亿、12 万亿这样的量级，非常惊人。

**Pat Grady:** Yeah.

对。

**Arvind Jain:** And that’s actually like the reality of where we are today, which is that everything that we do is going to actually change, fundamentally change. AI is going to be a key component that’s going to drive that change. So first thing that I, as a founder, I don’t actually worry about what other people are actually working on, because even if all of us are working on a lot of great things, it will still not be enough. It will still not be enough to actually solve all the problems that need to get solved. And so that’s the first mindset.

这就是我们今天的现实：我们做的一切都会发生根本性改变，而 AI 是驱动这场变化的关键组成部分。所以作为创始人，我第一件事是不担心别人在做什么——因为就算所有人都在做很棒的东西，加起来仍然不够，仍不足以解决所有需要解决的问题。这是第一个心态。

So like, you know, I think for advice to other founders, that’s the thing I want to tell them, like, if you found a problem, you know, just go work on it and don’t worry about, like, if somebody else is solving it, because the chances are that other people are not and they won’t solve it the same way as you will. But for us, like, you know, and coming back to Glean specifically, the dynamics for us, you know, we felt the same way. For the first four years of our existence, we were working on a problem, you know, where we had no competition. You know, nobody was actually interested in solving the problem that we were solving because it was a dead market, and we had to create a category which would actually generate interest, you know, be evangelical. But we knew that we were working on an important problem.

所以我给其他创业者的建议就是这个：如果你发现了一个问题，就去做，别纠结是不是别人也在解；大概率别人没在做，而且就算做，解法也不会和你一样。回到 Glean，我们的体感也一样：头四年我们在做一个没有竞争的问题，没人有兴趣解它，因为那是个「死市场」，我们得创造出一个品类、去做布道。但我们知道自己在解一个重要的问题。

But then, you know, suddenly ChatGPT happened and search has become hot. And now, in fact, every company that you go and talk to wants to build a product like Glean. And so is that good news for us? Is that bad news for us? Like, how do you think about it? You know, from our perspective, like, it doesn’t matter. Like, you know, the way we feel is that it’s actually great news for us. Like, now everybody is interested, everybody wants to buy our product. And yes, we have to compete with many, many other vendors, but that’s the place where we think we’ll win, because we have the desire to actually solve this problem and stay focused on this problem, keep working on it. And there’s no reason for us to not do a better job than others.

后来 ChatGPT 突然出现，搜索变热了；现在你去聊的每家公司都想做一个像 Glean 的产品。这对我们是好消息还是坏消息？怎么想？从我们的角度看，无所谓，甚至觉得是大好消息：现在所有人都感兴趣、都想买我们的产品。没错，我们得和很多厂商竞争，但这恰恰是我们认为自己会赢的地方——因为我们有意愿解这个问题、愿意持续专注、一直做下去，没有理由做得比别人差。

**Pat Grady:** Part of what I heard in there was that building an AI company is just building a company: find an important problem and solve it in a compelling way. I’m curious, particularly because this is not your first rodeo. You know, Rubrik was obviously wildly successful, and of course, you were pretty core to some of the early days of Google. How much of building an AI company is just building a company, versus things that are AI specific in some way?

我听下来有一层意思是：做 AI 公司，说到底还是做公司——找到一个重要问题，用有说服力的方式解决它。我特别好奇，因为这不是你第一次创业：Rubrik 显然非常成功，你又亲历了 Google 早期。做一家 AI 公司，有多少成分就是「做公司」，又有多少是 AI 特有的？

**Arvind Jain:** It’s a great question. I think of AI mostly as a tool in your arsenal. And one of the tools. I don’t think you suddenly become a different company because you’re doing something with AI. In reality, I think there’s going to be no new company that is not going to use AI technologies in some shape or form. So my point of view is that look, you have to actually find a business problem that you’re planning to solve, and hopefully you can actually solve that problem in a much better way because of the technology that AI is actually providing to you now. So I don’t think it actually changes. I don’t think it actually feels different, like, you know, whether you are—like, we don’t think of ourselves as an AI company for that matter either.

好问题。我把 AI 主要看成你武器库里的工具之一，并不觉得因为用了 AI，你就突然变成了另一种公司。现实是，未来不会有哪一家新公司不以某种形式使用 AI 技术。所以我的看法是：你得找到一个打算解决的商业问题，然后最好能借 AI 现在提供的技术，把这个问题解得好得多。我不觉得这件事改变了什么，也没觉得有什么不同——顺带说，我们自己也不把自己当成一家 AI 公司。

**Sonya Huang:** Would you ever train your own models? I guess maybe more broadly, how do you think about where Glean’s core competencies start and stop? And, you know, if you have 100 R&D chips, where do you want to place them?

你们会训练自己的模型吗？或者更宽泛一点：你怎么划 Glean 核心能力的边界？如果有 100 个研发名额，你会押在哪里？

**Arvind Jain:** We don’t have plans to train super large models. But at the same time, you know, we do train models which are smaller in size. You know, for every individual customer of ours, these language models that we train for an individual customer, it sort of goes through all of their own enterprise corpus and sort of starts to understand, like, you know, sort of the lingo, the speak, you know, the acronyms, the code names, all of that stuff within their corpus. So model training is actually a core part of the clean core technology, but not in the sense of training a model like GPT-4. We don’t do that. We don’t have plans for it. We plan to partner with a lot of other great companies that build models of that scale.

我们没有训练超大模型的计划。但与此同时，我们确实会训练规模较小的模型：为每一位客户训练的语言模型，会通读该企业自己的语料，逐渐理解其中的行话、说法、缩写、代号等等。所以模型训练其实是 Glean 核心技术的一部分，但不是训练 GPT-4 那种模型——我们不做，也没这个计划，那个量级我们会和很多优秀的模型公司合作。

**Sonya Huang:** Wonderful. Arvind, thank you so much for joining us today. This was a wonderful conversation. We really appreciate it.

太好了。Arvind，非常感谢你今天加入，聊得非常愉快，真的很感谢。

**Arvind Jain:** Thank you for having me.

谢谢邀请。
