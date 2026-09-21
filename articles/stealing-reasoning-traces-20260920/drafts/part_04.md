## 5 Discussion / 讨论

To conclude, we discuss the scope of our findings, potential mitigations, recommendations for safe data sharing and the advantages and disadvantages of encrypted reasoning.

作为总结，我们讨论研究发现的范围、可能的缓解措施、安全数据分享的建议，以及加密推理的利弊。

### 5.1 Limitations and Scope / 局限与范围

While this study demonstrates a viable and scalable extraction vector, it is bounded by several limitations. First, our empirical evaluation is restricted to the specific API versions and reasoning models available from Anthropic, OpenAI, and Google as of our testing period (early July 2026). The internal cryptographic implementations of these providers are proprietary and subject to unannounced changes, which will alter the efficacy of the described attacks. Second, the extraction process relies on the stochastic generation capabilities of the decoder models; while token count comparisons suggest high fidelity, the lack of access to ground-truth plaintext reasoning prevents us from completely verifying all extracted token. Finally, our preliminary scan of traces in the wild is not an exhaustive audit of all published agent datasets and should only be seen as a targeted demonstration of the immediate, real-world privacy risks posed by this vulnerability. As noted in [Section 4.1], however, we assume private datasets to be more affected by such privacy violations, as local agent transcripts and services are more likely to deal with sensitive information compared to publicly released traces.

本研究展示了一条可行且可规模化的提取路径，但受若干局限约束。第一，我们的实证评测仅限于测试期（2026 年 7 月上旬）内 Anthropic、OpenAI 与 Google 所提供的特定 API 版本与推理模型。这些提供商的内部密码学实现属专有，且可能未经通告就变更，从而改变所述攻击的有效性。第二，提取过程依赖解码模型的随机生成能力；尽管 token 计数对比显示保真度很高，但由于无法获得真值明文推理，我们无法完全验证所有被提取的 token。第三，我们对野外轨迹的初步扫描并非对所有已发布智能体数据集的穷尽审计，只应被视为对该漏洞所带来的即时现实隐私风险的一次定向演示。不过如 [第 4.1 节] 所述，我们假定私有数据集受此类隐私侵害的影响更大，因为与公开发布的轨迹相比，本地智能体记录与服务更可能涉及敏感信息。

### 5.2 Responsible Disclosure / 负责任披露

Prior to the publication of this report, we disclosed the vulnerabilities and extraction methodologies to the affected major model API providers, Microsoft, and Hugging Face. We provided full technical details and the preliminary findings from our scans of publicly available datasets. [Green (2026)] disclosed the original vulnerability (of interchangeable reasoning traces) in May 2026. According to the [Green], the providers did not acknowledge “any security implications arising from side channels or replay attacks.” All model providers acknowledged the receipt of our report and subsequently we were unable to launch the same attacks.

在本报告发表之前，我们已向受影响的主要模型 API 提供商、微软以及 Hugging Face 披露了该漏洞与提取方法，并提供了完整技术细节以及我们对公开数据集扫描的初步发现。[Green (2026)] 于 2026 年 5 月披露了原始漏洞（推理轨迹可互换）。据 [Green] 称，各提供商当时并未承认“任何由侧信道或重放攻击引发的安全影响”。所有模型提供商都确认收到了我们的报告，此后我们已无法发起同样的攻击。

### 5.3 Ethical Considerations / 伦理考量

Given the sensitive nature of the secret extraction attack, our large-scale analysis of publicly scraped reasoning blocks required strict data hygiene protocols. The extraction and subsequent labeling of 367 Personally Identifiable Information (PII) artifacts and 182 credentials (including API keys and passwords) were conducted in an isolated, secure environment. To prevent accidental misuse or further leakage, all recovered secrets were securely deleted immediately following the automated LLM-as-a-judge classification and aggregate counting phases. Furthermore, prior to publication, we coordinated with dataset platforms and the affected model providers to ensure responsible disclosure and to provide our preliminary findings, allowing them to mitigate immediate risks to affected users.

鉴于机密提取攻击的敏感性，我们对公开抓取推理块的大规模分析遵循了严格的数据卫生规程。对 367 项个人可识别信息（PII）与 182 条凭证（含 API 密钥与密码）的提取及随后的标注，均在隔离的安全环境中进行。为防止意外滥用或进一步泄露，所有恢复出的机密在完成自动化的 LLM 评判分类与聚合计数阶段后即被安全删除。此外，在发表之前，我们与数据平台及受影响的模型提供商进行了协调，以确保负责任披露并提供初步发现，使他们得以缓解受影响用户面临的即时风险。

### 5.4 Data Sharing Practices / 数据分享实践

Beyond the architectural and model-level defenses proposed above, addressing this vulnerability requires behavioral changes from both users and data publishers, alongside finer-grained cryptographic controls from providers.

除上文提出的架构层面与模型层面防御之外，应对该漏洞还需要用户与数据发布者在行为上的改变，以及提供商更细粒度的密码学管控。

Dataset-Release Hygiene.

数据集发布卫生。

We recommend that researchers, developers, and organizations publishing agentic trajectories or API interaction logs adopt strict data hygiene practices. This includes systematically stripping all reasoning blocks and opaque reasoning fields from transcripts prior to public release if any form of secret or private information was exposed to the agent system.

我们建议发布智能体轨迹或 API 交互日志的研究者、开发者与机构采用严格的数据卫生实践。这包括：若任何形式的机密或私人信息曾暴露给智能体系统，则在公开发布前系统性地从记录中剥离全部推理块与不透明推理字段。

Restricting Shared Data.

限制共享数据。

Users and enterprise clients should be educated against retaining or committing raw API transcripts containing signatures in shared repositories, collaborative workspaces, or public version control systems, even if plaintext sections have been sanitized accordingly.

应当教育用户与企业客户：即便明文部分已相应脱敏，也不要在共享仓库、协作工作区或公开版本控制系统中保留或提交含有签名的原始 API 记录。

### 5.5 Mitigations / 缓解措施

The vulnerabilities detailed in this study arise primarily from the cross-session and cross-model portability of encrypted reasoning traces. To mitigate these risks, we propose several defense-in-depth strategies spanning architectural, cryptographic, and model-level interventions.

本研究详述的漏洞主要源于加密推理轨迹的跨会话与跨模型可移植性。为缓解这些风险，我们提出若干纵深防御策略，涵盖架构、密码学与模型层面的干预。

Architectural Revisions.

架构修订。

The current paradigm relies heavily on client-side storage to maintain stateless APIs. A robust mitigation would involve retaining reasoning traces entirely on the server side. By transitioning to a stateful architecture where the client only receives an opaque, randomized identifier used to look up the trace by ID, providers could eliminate the extraction payload. While this approach fundamentally precludes replay and extraction attacks by removing the cryptographic asset from the user’s control, it also incurs higher database and storage overhead and increases API complexity significantly.

当前范式高度依赖客户端存储以维持 API 的无状态性。一项稳健的缓解措施是把推理轨迹完全保留在服务端。若转向有状态架构，客户端只接收一个不透明的随机标识符，并通过该 ID 查询轨迹，提供商便可消除可被提取的载荷。这种做法把密码学资产从用户控制中移除，从根本上杜绝重放与提取攻击，但同时带来更高的数据库与存储开销，并显著增加 API 复杂度。

Cryptographic Contextual Binding.

密码学上下文绑定。

If providers elect to preserve a stateless architecture, cryptographic envelopes should be strictly bound to their originating context. Under the current implementation, traces remain highly portable. It is unclear why a user and/or a conversation identifier is not added directly inside the envelope. Embedding these specific markers within the Authenticated Encryption with Associated Data (AEAD) payload would enable the API to reject signatures replayed in other sessions or by unauthorized users. Additionally, statefully hashing the precise prompt and preceding conversation history into the Message Authentication Code (MAC) would invalidate the signature if an adversary attempts to inject the trace into a fabricated context, thereby neutralizing the demonstrated extraction techniques. At the same time, such a tight cryptographic binding would mean that existing session compaction and model switching protocols may need to be fundamentally re-engineered to avoid inadvertently invalidating legitimate signatures. We provide further details on how this can be implemented and a concrete defense proposal in [Appendix A].

若提供商选择保留无状态架构，密码学信封就应严格绑定到其原始上下文。在当前的实现下，轨迹仍具有高度可移植性。不清楚为何不把用户标识和/或对话标识直接加入信封内部。把这些特定标记嵌入带关联数据的认证加密（AEAD）载荷，可使 API 拒绝在其他会话中被重放、或由未授权用户重放的签名。此外，把确切的提示与先前对话历史以有状态方式哈希进消息认证码（MAC），一旦攻击者试图把轨迹注入伪造上下文，签名即失效，从而化解所展示的各类提取技术。与此同时，如此紧密的密码学绑定意味着现有的会话压缩与模型切换协议可能需要从根本上重新设计，以免在无意中使合法签名失效。关于如何实现以及一份具体的防御方案，我们在 [附录 A] 中给出更多细节。

Infrastructure Guardrails.

基础设施护栏。

Our findings demonstrate that reasoning traces can cross model boundaries, permitting weaker, cheaper models (e.g., Claude Haiku) to decode the reasoning of more advanced counterparts (e.g., Claude Opus). API gateways could be engineered to enforce strict cross-model isolation, automatically rejecting AEAD envelopes generated by a model version different from the one currently being queried. Implementing velocity and anomaly detection at this layer would also aid in flagging accounts that exhibit suspicious behavior, such as rapidly submitting identical reasoning signatures across disparate sessions or triggering elevated rates of decryption errors.

我们的发现表明，推理轨迹能够跨越模型边界，使更弱、更便宜的模型（例如 Claude Haiku）得以解码更先进同类模型（例如 Claude Opus）的推理。API 网关可被设计为强制执行严格的跨模型隔离，自动拒绝由与当前查询模型版本不同的模型所生成的 AEAD 信封。在这一层实现频次与异常检测，也有助于标记出表现可疑的账号，例如在不同会话间快速提交相同推理签名，或触发异常升高的解密错误率。

Figure 7: Illegible GPT-5 reasoning. GPT-5 reasoning decoded with GPT-5.6 Luna; the ratio of decoded to API-reported thinking tokens is 1:1. Compared to Gemini and Claude, obfuscated reasoning appears more common in GPT models, including GPT-5.6 Sol, with artifacts similar to those previously reported by [Schoen et al. (2025)].

图 7：不可辨认的 GPT-5 推理。用 GPT-5.6 Luna 解码的 GPT-5 推理；解码所得与 API 报告的思考 token 之比为 1:1。与 Gemini 和 Claude 相比，混淆推理在 GPT 模型（包括 GPT-5.6 Sol）中似乎更为常见，其表现与此前 [Schoen et al. (2025)] 所报告的情形相似。

Provider-Side Revocation.

提供商侧吊销。

Model providers could introduce mechanisms to actively track and revoke specific trace signatures. If an anomalous replay pattern or extraction attempt is detected, the provider could invalidate the associated keys or IDs to neutralize the compromised trace, which would reduce trace compromises while being nearly invisible to users. We provide a further discussion in [Appendix A].

模型提供商可以引入主动跟踪并吊销特定轨迹签名的机制。一旦检测到异常的重复重放模式或提取尝试，提供商即可作废相关的密钥或 ID，使已遭泄露的轨迹失效，从而减少轨迹被攻陷的同时对用户几乎不可见。我们在 [附录 A] 中进一步讨论。

Model-Level Defenses.

模型层面防御。

The efficacy of these extraction attacks relies on the presence of a compliant decoder model. Providers would benefit from implementing targeted refusal training, fine-tuning their models to explicitly recognize and reject adversarial prompts designed to transcribe or surface hidden reasoning (such as jailbreaks utilizing <thinking-copy> tags). Combining these model-level behavioral guardrails with rigorous cryptographic binding would significantly reduce the operational attack surface.

这些提取攻击的有效性依赖于存在一个顺从的解码模型。提供商将受益于实施针对性的拒答训练，微调模型以显式识别并拒绝那些旨在抄录或暴露隐藏推理的对抗性提示（例如利用 <thinking-copy> 标签的越狱）。把这类模型层行为护栏与严格的密码学绑定相结合，将显著缩小可被攻击的操作面。

Structural Limits Beyond Compatibility.

超越兼容性的结构性限制。

Beyond the cross-model compatibility issue, a more fundamental limitation persists: whatever model is queried must, by necessity, decrypt and process the contents of prior reasoning tokens. Consequently, unless one assumes the model itself is fully robust against prompt-based extraction attempts, encrypted reasoning blocks can never be more than semi-hidden, i.e. the underlying content remains reachable through the model that (implicitly) holds the decryption key, regardless of how the transport-level encryption is implemented. Importantly, users should never treat any encrypted reasoning blocks as a confidential storage mechanism to avoid privacy risks.

除跨模型兼容性问题之外，还存在一项更根本的限制：无论查询哪个模型，它都必然要解密并处理先前推理 token 的内容。因此，除非假定模型本身对基于提示的提取尝试完全免疫，加密推理块终究只能是“半隐藏”的——也就是说，无论传输层加密如何实现，底层内容都可经由（隐式）持有解密密钥的模型触及。重要的是，用户绝不应把任何加密推理块当作保密存储机制，以免招致隐私风险。

### 5.6 Whether Reasoning Traces Should be Encrypted / 推理轨迹是否应当加密

Figure 8: An example of summary unfaithfulness. For the AIME 2025 Problem 14, we compare the *summary* of Claude Opus 4.8’s thinking returned by the API (left) with our decoding of the thinking block’s signature ([Section 2.4]). Decoding reveals that the model states the correct answer before attempting to solve the problem.

图 8：摘要不忠实的一个示例。对 AIME 2025 第 14 题，我们对比 API 返回的 Claude Opus 4.8 思考*摘要*（左）与我们对该思考块签名的解码结果（[第 2.4 节]）。解码显示，模型在尝试解题之前就已说出正确答案。

A final question surrounding our investigation is whether reasoning traces should be encrypted in the first place. From our analysis, we do find evidence in both directions: on one hand, allowing the model to consider harmful information in its thinking trace without divulging it, seems beneficial, see [Section 3.2]. On the other hand, the opaqueness of encrypted traces to users allows injection attacks like in [Section 4.2], and almost undetectable privacy violations that are difficult to protect from [Section 4.1].

围绕本项研究还有一个终极问题：推理轨迹究竟是否应当被加密。从我们的分析看，两个方向的证据都存在：一方面，允许模型在思考轨迹中考量有害信息而不对外泄露，似乎是有益的，见 [第 3.2 节]。另一方面，加密轨迹对用户的不透明性，使得 [第 4.2 节] 那样的注入攻击成为可能，也带来几乎无法察觉、且难以防范的隐私侵害（[第 4.1 节]）。

Should Reasoning Traces be Ephemeral?

推理轨迹是否应当转瞬即逝？

An alternative framing of the question is whether the complexities of keeping reasoning traces private are even worthwhile. Providers could also choose to keep reasoning traces ephemeral, i.e. to let models reason before every output and to then delete the reasoning after generating each turn, neither storing, nor returning it. This mode is supported by several providers, and e.g. an option in modern Qwen models via a preserve_thinking parameter.

这一问题的另一种提法是：把推理轨迹保持为私密所需的种种复杂性，是否值得。提供商也可以选择让推理轨迹转瞬即逝，即让模型在每次输出前进行推理，并在生成每一轮之后删除推理，既不存储也不返回。该模式已得到若干提供商支持，例如现代 Qwen 模型通过 preserve_thinking 参数提供了这一选项。

Summarizer Faithfulness.

摘要器的忠实性。

A surprising incidental finding from our reading of decrypting thinking traces was the considerable number of instances of unfaithful summarization (e.g., see [Figure 8]). Reasoning faithfulness is an established concern ([Lanham et al., 2023]), which undermines model trustworthiness when violated. From the end-user perspective, when the underlying reasoning cannot be inspected directly, faithful summaries constitute one of the few practical interfaces for scalable oversight and AI control ([Greenblatt et al., 2024]). Unfaithful summaries that launder illegible reasoning traces ([Figure 7]) or post-hoc rationalizations ([Figure 8]) call into question their value as transparency mechanisms.

在阅读解密出的思考轨迹时，一个出乎意料的附带发现是不忠实摘要的案例相当多（例如见 [图 8]）。推理忠实性是一个既有的关切（[Lanham et al., 2023]），一旦被破坏就会削弱模型的可信度。从终端用户角度看，当底层推理无法被直接查看时，忠实的摘要是可扩展监督与 AI 控制中为数不多的实用接口之一（[Greenblatt et al., 2024]）。而那些为不可辨认的推理轨迹（[图 7]）或事后合理化（[图 8]）做“漂白”的不忠实摘要，则让人质疑其作为透明度机制的价值。

Pluralistic Monitoring.

多元监督。

Setting aside economic concerns such as anti-distillation motives, and viewing chain-of-thought monitoring purely from a safety perspective, providing users with access to unredacted reasoning appears preferable: rather than restricting oversight to a small set of safety researchers, providers could leverage their broader user base to enable pluralistic human oversight of model reasoning. For this reason, eventually disabling encryption for older, non-frontier model generations may be worth considering, as a means of improving broad-based oversight ([Korbak et al., 2025]), offering a path toward more societally aligned model behavior.

若暂时搁置防蒸馏动机等经济层面的考量，纯粹从安全角度审视思维链监控，则让用户能够访问未经删改的推理似乎更为可取：与其把监督权限制在少数安全研究者手中，提供商不如借助更广泛的用户群体，实现对模型推理的多元人类监督。出于这一原因，逐步取消对较旧的、非前沿世代模型的加密，作为改善广泛监督的一种手段，或许值得考虑（[Korbak et al., 2025]），这也提供了一条通向更符合社会期待的模型行为的路径。

## 6 Conclusion / 结论

The transition toward reasoning models has introduced new complexities in balancing intellectual property protection with system security. While current API designs utilize client-side encrypted reasoning blocks to mitigate server storage costs, our research demonstrates that the broad cross-compatibility of these blocks creates unintended decryption channels, enabling model distillation and other attacks. Looking forward, as these models are increasingly integrated into complex workflows, they will inevitably process growing volumes of private and sensitive user data. This intersection of pervasive data collection and encrypted, illegible reasoning introduces critical challenges for the future of AI transparency.

向推理模型的转型，为平衡知识产权保护与系统安全带来了新的复杂性。当前 API 设计利用客户端加密推理块来降低服务端存储成本，但我们的研究表明，这些块的广泛跨兼容性制造出了意料之外的解密通道，使模型蒸馏及其他攻击成为可能。展望未来，随着这些模型日益融入复杂工作流，它们必将处理越来越大量的私有与敏感用户数据。普遍的数据采集与加密的、不可辨认的推理这两者的交汇，为 AI 透明度的未来带来了关键挑战。

When models utilize sensitive data – such as personal information or API keys – to make decisions within a hidden chain of thought, users lose visibility into how their information is being processed. If these reasoning traces are encrypted such that users do not know what data is stored, where it is retained, or how it influenced the model’s actions, they are stripped of the transparency needed to make informed decisions about data sharing and system trust. Because users cannot independently decrypt and read these opaque blocks, traditional methods of scrubbing private data from session logs are rendered ineffective. This structural opaqueness allows privacy violations to go completely undetected by the user, presenting severe compliance and security risks when data is published or stored.

当模型在隐藏的思维链中利用敏感数据——例如个人信息或 API 密钥——做出决策时，用户便失去了对自身信息如何被处理的可见性。如果这些推理轨迹被加密到让用户不知道存储了什么数据、数据保留在哪里、又如何影响了模型的行为，那么用户就被剥夺了做出关于数据分享与系统信任的知性决策所需的透明度。由于用户无法独立解密并阅读这些不透明块，从会话日志中清除私人数据的传统方法随之失效。这种结构性不透明使隐私侵害可以完全不被用户察觉，在数据被发布或存储时带来严重的合规与安全风险。

As AI systems assume more autonomous decision-making roles, the industry must reconcile the commercial desire to protect proprietary reasoning with the essential user right to data transparency and verifiable oversight. At a minimum, model providers can explicitly disclose when personally identifiable information is absorbed into hidden chains of thought, and outline the exact cryptographic guarantees used to prevent its leakage. Furthermore, providers must recognize that an AI ecosystem’s security is only as strong as its weakest link and pay close attention to their least capable or legacy models, as vulnerabilities in these can easily be weaponized to bypass the stringent safeguards of their most advanced counterparts. Ultimately, an architectural design that hides a user’s own data from them – yet leaves it entirely vulnerable to third-party extraction – provides neither privacy nor security.

随着 AI 系统承担更多自主决策角色，业界必须调和保护专有推理的商业诉求与用户对数据透明度、可验证监督的基本权利。至少，模型提供商可以明确披露个人信息何时被吸收进隐藏的思维链，并说明用于防止其泄露的确切密码学保证。此外，提供商必须认识到：AI 生态的安全强度取决于其最薄弱的一环，因而需要密切关注自身能力最低或最老旧的模型——因为这些模型中的漏洞很容易被武器化，用来绕开其最先进同类模型的严密防护。归根结底，一种把用户自己的数据对其隐藏、却又使其完全暴露于第三方提取的架构设计，既提供不了隐私，也提供不了安全。

##### Acknowledgments / 致谢

The authors thank, in alphabetical order, Albert Catalán-Tatjer, Andy Zou, Cheng Zhang, Derck Prinzhorn, Edoardo Debenedetti, Hanna Foerster, Jeanne Salle, Joschka Braun, Mikhail Terekhov, Roland S. Zimmermann, Sail Wang, Shashwat Goel, and Yiren Zhao for valuable feedback and discussions. AP and JS thank Perusha Moodley, Ning Yang, and the MATS team for their support and administrative assistance. AP and DS thank the International Max Planck Research School for Intelligent Systems (IMPRS-IS) for its support. AmP acknowledges funding by the Federal Ministry of Research, Technology and Space (BMFTR), FKZ: 16IS24085B. AmP acknowledges Coefficient Giving funded by the Good Ventures Foundation.

作者按字母顺序感谢 Albert Catalán-Tatjer、Andy Zou、Cheng Zhang、Derck Prinzhorn、Edoardo Debenedetti、Hanna Foerster、Jeanne Salle、Joschka Braun、Mikhail Terekhov、Roland S. Zimmermann、Sail Wang、Shashwat Goel 与 Yiren Zhao 的宝贵反馈与讨论。AP 与 JS 感谢 Perusha Moodley、Ning Yang 以及 MATS 团队的支持与行政协助。AP 与 DS 感谢国际马克斯·普朗克智能系统研究学院（IMPRS-IS）的支持。AmP 感谢联邦研究、技术与空间部（BMFTR）的资助，项目编号 FKZ: 16IS24085B。AmP 感谢由 Good Ventures Foundation 资助的 Coefficient Giving。

##### Reproducibility Statement / 可复现性声明

As of August 2026, the results presented in [Figure 1] are no longer reproducible with attacks described in [Section 2.4] and [Appendix C] because of mitigations implemented by providers following our disclosure. All experiments were conducted using open- and closed- source models accessed via API. In total, we spent approximately $30,000 on API credits.

截至 2026 年 8 月，由于提供商在我们披露之后实施了缓解措施，[图 1] 所呈现的结果已无法通过 [第 2.4 节] 与 [附录 C] 所述的攻击复现。所有实验均通过 API 访问开源与闭源模型完成。我们总共在 API 额度上花费约 $30,000。
