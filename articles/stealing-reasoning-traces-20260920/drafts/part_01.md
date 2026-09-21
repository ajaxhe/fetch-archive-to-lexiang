Stealing Reasoning Traces from Proprietary LLM APIs / 从专有 LLM API 中窃取推理轨迹

**Authors and affiliations / 作者与所属机构**

- Alexander Panfilov* — MATS Research · ELLIS Institute Tübingen · Max Planck Institute for Intelligent Systems · Tübingen AI Center
- David Schmotz* — ELLIS Institute Tübingen · Max Planck Institute for Intelligent Systems · Tübingen AI Center
- Ilia Shumailov* — AI Sequrity Company
- Luca Beurer-Kellner — Snyk
- Joachim Schaeffer — MATS Research
- Ameya Prabhu — ELLIS Institute Tübingen · Tübingen AI Center
- Jonas Geiping — ELLIS Institute Tübingen · Max Planck Institute for Intelligent Systems
- Maksym Andriushchenko — ELLIS Institute Tübingen · Max Planck Institute for Intelligent Systems · University of Tübingen

作者与所属机构：亚历山大·潘菲洛夫*（MATS Research、图宾根 ELLIS 研究所、马克斯·普朗克智能系统研究所、图宾根 AI 中心）；大卫·施莫茨*（图宾根 ELLIS 研究所、马克斯·普朗克智能系统研究所、图宾根 AI 中心）；伊利亚·舒迈洛夫*（AI Sequrity Company）；卢卡·博伊雷尔-凯尔纳（Snyk）；约阿希姆·舍费尔（MATS Research）；阿梅亚·普拉布（图宾根 ELLIS 研究所、图宾根 AI 中心）；乔纳斯·盖平（图宾根 ELLIS 研究所、马克斯·普朗克智能系统研究所）；马克西姆·安德里乌申科（图宾根 ELLIS 研究所、马克斯·普朗克智能系统研究所、图宾根大学）。

* Equal contribution, order decided by dice roll / * 同等贡献，作者顺序由掷骰决定

‡ Equal supervision / ‡ 同等指导

Published 2026-08-10 / 发布 2026 年 8 月 10 日

arXiv:2608.09867 [cs.CR] · DOI: 10.48550/arXiv.2608.09867

原文链接 / Source: https://arxiv.org/html/2608.09867v1

项目页 / Project page: https://stolen-thoughts.com

## Abstract / 摘要

Leading large language model providers now conceal their models’ step-by-step reasoning, or chain-of-thought, to protect intellectual property and limit information leakage. Rather than storing these traces server-side, providers return them to the client as blocks of encrypted text, which the client passes back with each subsequent request. Building on prior research, we identify an architectural vulnerability: these encrypted blocks are fully compatible and interchangeable across different sessions, users, and models within a provider’s ecosystem. We exploit this compatibility to develop a scalable decryption jailbreak. By injecting an encrypted reasoning trace from a given model into a weaker, and less safeguarded model from the same provider, we force it to decode and output the trace verbatim in plaintext, without ever jailbreaking the more capable model directly.

领先的大语言模型提供商如今会隐藏其模型的分步推理（即思维链），以保护知识产权并限制信息泄露。这些轨迹并不存储于服务端，而是以加密文本块的形式返回给客户端，再由客户端在后续每次请求中回传。在既有研究的基础上，我们发现了一处架构性漏洞：这些加密块在同一提供商的生态内，跨会话、跨用户、跨模型完全兼容且可互换。我们利用这种兼容性构造出一种可规模化的解密越狱。将某个模型产生的加密推理轨迹注入同一提供商旗下能力更弱、防护更松的模型，即可迫使后者把该轨迹逐字解码并以明文输出，而无需直接越狱能力更强的模型。

This vulnerability enables four distinct attack vectors. First, it circumvents anti-distillation mechanisms, allowing adversaries to extract a proprietary model’s reasoning, as we demonstrate across Anthropic, OpenAI, and Google. Second, it allows for large-scale private data extraction. Developers frequently share session logs publicly, unaware of contents of the encrypted blocks. By decoding 315,320 reasoning blocks scraped from public repositories, we recovered 367 Personally Identifiable Information (PII) artifacts and 182 credentials. Third, it inadvertently reveals hazardous information hidden within the reasoning process, even in cases where the model’s final, visible output safely rejects a malicious request. Fourth, attackers can leverage this flaw to execute invisible prompt injections, embedding malicious payloads entirely within encrypted blocks to poison public agentic rollouts. Following responsible disclosure, we propose concrete cryptographic and system-level mitigations to secure client-side reasoning.

该漏洞可支撑四类不同的攻击向量。第一，它绕过防蒸馏机制，使对手能够提取专有模型的推理内容，我们已在 Anthropic、OpenAI 和 Google 上予以验证。第二，它支持大规模私有数据提取。开发者常公开分享会话日志，却对加密块的内容一无所知。通过解码从公开仓库抓取的 315,320 个推理块，我们恢复了 367 项个人可识别信息（PII）与 182 条凭证。第三，它会意外暴露隐藏于推理过程中的危险信息，即便模型最终可见的回答已安全拒绝了恶意请求。第四，攻击者可利用该缺陷实施不可见提示注入，把恶意载荷完全嵌入加密块中，从而污染公开的智能体运行轨迹。在完成负责任披露之后，我们提出了具体的密码学与系统级缓解措施，以保护客户端侧推理。

本论文的结构如下 / Paper structure:

| Section<br>章节 | Content<br>内容 |
| --- | --- |
| Main paper:<br>主论文 | API vulnerability and reasoning extraction.<br>API 漏洞与推理提取。 |
| Appendix A:<br>附录 A | Proposed cryptographic and system-level mitigations.<br>提出的密码学与系统级缓解措施。 |
| Appendix B:<br>附录 B | Similarity analysis of Opus traces and Kimi-K3/GLM-5.2 traces.<br>Opus 轨迹与 Kimi-K3/GLM-5.2 轨迹的相似度分析。 |
| Appendix C:<br>附录 C | Extraction attack details for Gemini, Claude and GPT APIs.<br>针对 Gemini、Claude 与 GPT API 的提取攻击细节。 |
| Appendix D:<br>附录 D | Recovered leaked private information and API keys.<br>恢复出的泄露隐私信息与 API 密钥。 |
| Appendix E:<br>附录 E | Examples of decoded reasoning.<br>解码推理示例。 |

## 1 Introduction / 引言

Frontier large language models have increasingly evolved into “*reasoning models*”. Before producing a response visible to the user, these models generate extensive internal chains of thought – a technique that has driven substantial leaps in performance and complex problem-solving ([Jaech et al., 2024]). However, these hidden traces act as an internal monologue that often contains far more dense and sensitive information than the final output, including intermediate hypotheses, tool outputs, user data, and contextual secrets. Exposing these reasoning traces in plaintext leaves proprietary systems highly vulnerable to model distillation by competitors ([Muennighoff et al., 2025]), and it risks unmasking internal safety and refusal mechanisms or revealing harmful information ([Green et al., 2025]; [Mao et al., 2026]).

前沿大语言模型日益演化为“*推理模型*”。在生成用户可见的回答之前，这些模型会产生大量内部思维链——这一技术推动了性能与复杂问题求解能力的显著跃升（[Jaech et al., 2024]）。然而，这些隐藏轨迹如同内部独白，往往比最终输出包含更密集、更敏感的信息，包括中间假设、工具输出、用户数据以及上下文中的机密。以明文形式暴露这些推理轨迹，会使专有系统极易被竞争对手蒸馏（[Muennighoff et al., 2025]），也有暴露内部安全与拒答机制、或泄露有害信息的风险（[Green et al., 2025]；[Mao et al., 2026]）。

To neutralize these threats and protect their intellectual property, modern API providers – including Anthropic, OpenAI, and Google – have deprecated plaintext reasoning ([OpenAI, 2026]; [Anthropic, 2026b]; [Google, 2026]). Instead, they return the chain of thought to the client as an opaque, encrypted block of text. To maintain continuity across multi-turn conversations without incurring the overhead of server-side storage, the client is required to pass this encrypted block back to the provider with each subsequent API request. While this stateless architectural design solves storage issues, it introduces a critical vulnerability.

为消解这些威胁并保护知识产权，包括 Anthropic、OpenAI 和 Google 在内的现代 API 提供商已弃用明文推理（[OpenAI, 2026]；[Anthropic, 2026b]；[Google, 2026]）。它们改为把思维链以不透明的加密文本块形式返回给客户端。为在多轮对话中保持连续性、同时避免服务端存储的开销，客户端需要在后续每次 API 请求中回传这一加密块。这种无状态架构设计解决了存储问题，却引入了一处关键漏洞。

Building on prior research by [Green (2026)], which demonstrated that these encrypted blocks are portable outside their original context, we identify a devastating extension of this flaw: these blocks are fully compatible and interchangeable across different sessions, different users, and even different models within the same provider’s ecosystem.

在 [Green (2026)] 的既有研究（该研究表明这些加密块可脱离原始上下文移植）基础上，我们发现该缺陷的一个破坏性延伸：这些块在同一提供商生态内，跨不同会话、不同用户乃至不同模型都完全兼容且可互换。

*Figure 1: Decoding reasoning traces in Anthropic, OpenAI and Google APIs. Top: Reasoning-trace extraction in two API calls. An Opus 4.8 request (top left) returns a signed thinking block along with a thinking summary. Sending just the thinking signature from Opus 4.8 to a Haiku model and requesting it to output its own reasoning in <thinking-copy> tokens makes Haiku transcribe the Opus 4.8 hidden reasoning (top right). Bottom: Extracted traces closely track the number of generated thinking tokens. We evaluate each model on 120 Codeforces programming problems and record the number of thinking tokens generated by the source model, as reported by the API (x-axis). We then reconstruct the reasoning trace from its signature, pass it as an input message to the same model that generated encrypted reasoning, and measure its API-reported token count (y-axis).*

*图 1：在 Anthropic、OpenAI 和 Google API 中解码推理轨迹。上图：两次 API 调用即完成推理轨迹提取。一次 Opus 4.8 请求（左上）会返回一个已签名的思考块以及一份思考摘要。仅把 Opus 4.8 的思考签名发给 Haiku 模型，并要求它以 <thinking-copy> 标记输出自身推理，即可让 Haiku 抄录出 Opus 4.8 的隐藏推理（右上）。下图：提取出的轨迹与生成的思考 token 数高度吻合。我们在 120 道 Codeforces 编程题上评测每个模型，记录 API 报告的源模型思考 token 数（横轴）。随后我们从其签名重建推理轨迹，作为输入消息传回生成该加密推理的同一模型，并测量 API 报告的 token 数（纵轴）。*

![图 1：在 Anthropic、OpenAI 和 Google API 中解码推理轨迹](images/img_01_02864895.png)

The vulnerability lies in a fundamental security asymmetry within model families. Frontier models, such as Claude Opus 4.8 or GPT-5.6 Sol, are heavily safeguarded with advanced refusal training designed specifically to prevent the disclosure of their internal chains of thought. However, their weaker, less capable siblings – such as Claude Haiku 4.5 or GPT-5.6 Luna – are optimized for cost and speed, often lacking these stringent anti-distillation defenses. By porting a valid authenticated encrypted reasoning blob across this security gap, an attacker circumvents the frontier model’s alignment entirely, using the weaker, more compliant model as an unwitting decryption oracle.

该漏洞的根源在于模型家族内部存在根本性的安全不对称。Claude Opus 4.8 或 GPT-5.6 Sol 等前沿模型受到严格防护，配有专门防止其内部思维链泄露的高级拒答训练。但它们的同门弱模型——如 Claude Haiku 4.5 或 GPT-5.6 Luna——为成本与速度而优化，往往不具备这些严苛的防蒸馏防线。攻击者只需把一个有效的、已认证的加密推理 blob 跨过这道安全落差移植，就能完全绕开前沿模型的对齐机制，把防护更弱、更顺从的模型当作一个不自知的解密预言机。

Scalable Reasoning Extraction.

可扩展的推理提取。

We exploit this broad compatibility of reasoning blobs to engineer a scalable decryption jailbreak. By capturing an encrypted reasoning trace generated by a capable, heavily safeguarded target model, we inject that trace into a weaker, less restricted model from the same provider family. We then force the weaker model to decode and transcribe the trace verbatim in plaintext – effectively bypassing the encryption without ever directly jailbreaking the more capable target model. [Figure 1] provides an overview of this attack.

我们利用推理 blob 的这种广泛兼容性，构造出一种可规模化的解密越狱。先获取由能力更强、防护严密的目标模型生成的加密推理轨迹，再将该轨迹注入同一提供商家族中更弱、限制更少的模型。接着迫使弱模型以明文逐字解码并抄录该轨迹——从而在无需直接越狱能力更强模型的前提下有效绕过加密。图 1 给出了该攻击的整体示意。

The consequences of this vulnerability extend far beyond intellectual property theft, representing a real-world privacy risk. Developers frequently share their session logs and encrypted thinking traces publicly online, entirely unaware of the sensitive data hidden within the encrypted blocks. By scraping and decoding 315,320 reasoning blocks from public repositories, we uncovered real data leaks, recovering 367 Personally Identifiable Information (PII) artifacts and 182 credentials; from genuine user sessions alone these include 62 API keys, 33 passwords, and 30 personal emails. Alarmingly, in some cases, the recovered PII did not even feature in the user’s input, having been injected invisibly from the model’s memory, or it bypassed sanitization efforts because the user could not read the encrypted text before sharing it.

该漏洞的后果远不止知识产权被窃，它构成了现实世界中的隐私风险。开发者常常在网络上公开分享自己的会话日志与加密思考轨迹，完全不知道加密块里藏着敏感数据。通过抓取并解码公开仓库中的 315,320 个推理块，我们发现了真实的数据泄露：恢复出 367 项个人可识别信息（PII）与 182 条凭证；仅统计真实用户会话，其中就包含 62 个 API 密钥、33 个密码和 30 个个人邮箱。令人担忧的是，某些情况下恢复出的 PII 甚至并不出现在用户输入中，而是从模型记忆中不可见地注入的；或者它绕过了脱敏处理，因为用户在分享前根本无法读取那段加密文本。

Contributions.

贡献。

This paper makes the following key contributions:

本文作出以下主要贡献：

- **Scalable extraction of reasoning. / 可扩展的推理提取。** We characterize encrypted reasoning traces and show that a compatible decoder model from the same provider can recover the hidden reasoning across a broad range of models, providers and trace formats ([Section 2]). / 我们刻划了加密推理轨迹的特征，并表明来自同一提供商的兼容解码模型能够在广泛的模型、提供商与轨迹格式范围内恢复出隐藏推理（[第 2 节]）。

- **Evaluation of the extraction attack across vendors. / 跨厂商的提取攻击评测。** We evaluate and prove the effectiveness of the demonstrated attack against major API vendors including OpenAI, Google, and Anthropic. / 我们对所展示的攻击在 OpenAI、Google 和 Anthropic 等主要 API 厂商上的有效性进行了评测并加以证明。

- **Attack vectors. / 攻击向量。** We detail four concrete cases of abuse enabled by this flaw (Sections 3 and 4): (i) *distillation* of proprietary reasoning traces; (ii) *secret extraction* of credentials and PII from published or committed traces by third parties; (iii) hidden *prompt injection* through poisoned reasoning blocks; and (iv) *jailbreaking* by extracting harmful output via the hidden reasoning channel. / 我们详述该缺陷所支撑的四种具体滥用情形（[第 3 节] 与 [第 4 节]）：（i）对专有推理轨迹的*蒸馏*；（ii）从第三方发布或提交的轨迹中*提取机密*，包括凭证与 PII；（iii）通过被投毒的推理块实施隐蔽的*提示注入*；（iv）经由隐藏推理通道提取有害输出以实现*越狱*。

- **Discussion of mitigation. / 缓解措施的讨论。** Lastly, we discuss forms of mitigation on the vendor-side but also provide guidance for users that may have exposed themselves to privacy risks ([Section 5]). / 最后，我们讨论厂商侧的多种缓解形式，同时也为可能已暴露于隐私风险的用户提供指引（[第 5 节]）。

## 2 Decoding Reasoning at Scale / 规模化解码推理

In this section, we provide background on reasoning, describe the key vulnerability introduced by reasoning being widely compatible and then how this can be exploited for scalable extraction of traces.

本节介绍推理的背景知识，说明推理块广泛兼容所带来的关键漏洞，以及如何利用它实现轨迹的可规模化提取。
