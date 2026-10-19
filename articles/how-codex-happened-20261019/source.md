# How Codex Happened

> 作者: Dan Shipper | 日期: 2026-10-15

> 原文链接: https://every.to/p/how-codex-happened

---


![](images/img_01_461ebf6f.webp)


![](images/img_02_9ecb3796.png)

Inside OpenAI’s comeback in coding, from a failed launch to the app that took over ChatGPT

By Dan Shipper

I can remember exactly when I began to think that OpenAI would lose the mandate of heaven—the seemingly insurmountable lead they had built in AI coding since ChatGPT originally took off. I was in their Mission Bay office, in the summer of 2025, the night before the launch of [GPT-5](https://every.to/vibe-check/gpt-5?utm_cta_source=p_how_codex_happened_before_launch_gpt_5_1).


There was a certain buzz to the building. The overhead lights burned like stage lights, and people seemed to walk the warm rusts and browns of its halls just a little faster than usual. Even the gravity felt heavier—as if the sheer size of the following day’s launch had drawn the rest of the world into its orbit.


[This made what I had come to say a little awkward.](/p/how-codex-happened/interviews/alex/?cite=awkward-revisit&utm_cta_source=p_how_codex_happened_before_launch_cite_awkward_revisit#final-20261015-0003)


Every, the company I run, had begun to build a reputation for testing new AI models on real work and explaining what they could—and couldn’t—do. OpenAI had given us access to GPT-5 about a month before launch so we could help them understand the model’s strengths and weaknesses and publish our Vibe Check—a detailed review—on launch day.


Ten of us had spent a week in a house in upstate New York for a team retreat, eating and working together at one long wooden table and gathering on a couch in front of a big screen to test the long-awaited model. We were especially excited to try it for coding, where AI was advancing fastest. But while we liked it for everyday use, our reaction to it in Codex was muted.


Today, Codex is the centerpiece of OpenAI’s comeback—the product that has swallowed ChatGPT from the inside and become the foundation for everything the company is building next. But that summer it was still a scrappy effort to build an AI software engineer. A [version launched in the cloud](https://every.to/vibe-check/vibe-check-codex-openai-s-new-coding-agent?utm_cta_source=p_how_codex_happened_before_launch_version_launched_in_the_cloud_1) a few months earlier hadn’t found product-market fit, and the team was mid-pivot to a new version that ran on a developer’s computer in their terminal and in their code editor.


In Codex, GPT-5 was fast, and it seemed smart. One of our most technical engineers, [Naveen Naidu](https://every.to/@naveen_6804?utm_cta_source=p_how_codex_happened_before_launch_naveen_naidu_1), had used it to track down a mysterious freeze in his voice dictation app [Monologue](https://monologue.to/) that had stumped him for days. But it also seemed to stop too early, as if it were overly wary of stepping outside the bounds of what it was allowed to do. It felt designed to be used as a pair programmer.


As a team, we were moving beyond step-by-step collaboration with AI models. Using Anthropic’s terminal agent, Claude Code, a group of us led by [Kieran Klaassen](https://every.to/@kieran_1355?utm_cta_source=p_how_codex_happened_before_launch_kieran_klaassen_1) had started handing entire tasks to Opus 4 and walking away until a finished feature—or sometimes an entire app—came back. With minimal help from an engineer, staff writer [Katie Parrott](https://every.to/@katie.parrott12?utm_cta_source=p_how_codex_happened_before_launch_katie_parrott_1) built and deployed her own AI content management system in a few days. It had some bugs, but building it would previously have been out of reach.


Next to Opus 4 inside Claude Code, GPT-5 inside Codex felt boxed in.


Sharing what we’d found in our testing had brought me to a conference room in OpenAI’s office with **Lindsay McCallum** from the communications team and **Alexander Embiricos** from the Codex team. I sensed that McCallum, who has a keen radar for vibe shifts in the market, had set up the conversation so I could explain to Embiricos why I suddenly wouldn’t shut up about this new way of working.


McCallum was typing with intense focus on her laptop across the conference table from me. Embiricos sat beside me, coding while he talked, which I took as a good sign. He was rushing to finish a GPT-5 release feature that would let the agent pause and ask a human for permission to access files or run commands outside its sandbox.


“With Claude Code, you just let it rip,” I told Embiricos. “GPT-5 feels a little timid—like it’s held back by the sandbox and it seems afraid to use its own power.”


The tapping of McCallum’s keys slowed. “Tell Alexander about this new engineering workflow you have,” I remember her saying without looking up from her laptop.


Embiricos swiveled his chair to focus fully on me.


“We don’t even really look at the code anymore,” I began. But I blushed as I said it. I felt ridiculous explaining agentic delegation to Embiricos, of all people—building an autonomous coding agent was his job. I also wasn’t sure, at the time, that our engineering approach would work beyond our tiny team.


A Slack ping lit up Embiricos’s screen and broke the sudden quiet of the conference room. He muted his computer and pushed its lid three-quarters shut—just enough to keep his Codex agent thinking.


---


Leaving Mission Bay that night, I wondered if OpenAI was building the perfect tool for a dying workflow. Burned once by its failed cloud agent, the company looked like it was retreating to the code editor, where AI helped programmers work step by step. Meanwhile, Claude Code was taking off among people handing over entire tasks and walking away.


There were good reasons to stay in the editor. After GPT-5 launched, the Codex team shipped an extension that tucked Codex into the sidebar of code editors like Microsoft’s Visual Studio Code (VS Code)—where programmers write, run, and debug code—and Cursor. Usage grew more than 10-fold by last October, and the editor extension quickly overtook the terminal to become Codex’s most-used surface.[[1]](/p/how-codex-happened/interviews/alex/?cite=ide-most-used-surface&utm_cta_source=p_how_codex_happened_before_launch_cite_ide_most_used_surface#final-20261015-0153)


In most companies, that would have been the business to double down on. But Embiricos and a small group of engineers, designers, and researchers inside OpenAI had bigger ambitions.


In the months that followed, the Codex team trained and rapidly improved a dedicated line of coding models, separate from those powering ChatGPT, and built a desktop app for managing multiple agents at once. By June 2026, Codex had more than 5 million weekly active users and was spreading beyond programming into other kinds of knowledge work.


By July 2026, Codex had merged into the flagship ChatGPT desktop app. Its leader, **Thibault Sottiaux**, had been elevated to head all of OpenAI’s core products and platforms, including ChatGPT, Codex, and the API. Today, Codex and ChatGPT for Work combined have 40 million weekly active users.


In less than a year, the Codex team went from a failed cloud launch to becoming the foundation for OpenAI’s flagship product—and in doing so, they helped remake the company.


This is the story of how Codex happened.


---


![](images/img_03_508bb6ac.png)

> *Thinking…*Thinking...


> *Something is off. The lead I had a year ago isn’t showing up in the results…*


> *It looks like the problem starts earlier than I assumed…*


> *Going back to the beginning…*


> *Thinking…*Thinking...


> *Something is off. The lead I had a year ago isn’t showing up in the results…*


> *It looks like the problem starts earlier than I assumed…*


> *Going back to the beginning…*


---


OpenAI’s comeback begins with a simple line: “Thinking....”


In 2026, any time you interact with an AI model on any kind of complex request, you’ll see that word—*thinking*—shimmering in the place where your response will appear.


It might seem like a throwaway: a one-word replacement for the spinning beach ball on macOS or the circling blue ring Windows displays beside its cursor, each a sign that the computer is too busy to respond.


But “Thinking,” in this context, denotes a new style of computing without which Codex would never have happened.


The first generation of large language models were external processors. They had no shimmering status label for their internal reasoning; instead, they did their thinking directly by responding to you. Whether you asked them to write an email or a line of code, they had to work out their answer [one word at a time](https://every.to/chain-of-thought/how-language-models-work?utm_cta_source=p_how_codex_happened_thinking_one_word_at_a_time_1), with no opportunity to plan ahead or revise afterward.


In that way, early chat models were like improv actors given a prompt by the audience as the basis for a scene invented on the spot. As these tools composed on the run, their results could be impressive—and sometimes unintentionally funny. (They would insist [“strawberry”](https://every.to/chain-of-thought/openai-s-new-model-strawberry-explained?utm_cta_source=p_how_codex_happened_thinking_strawberry_1) had two r’s, spell it out to prove it, and congratulate themselves at the end.)


Early users of these models noticed that if you asked the model to write out its reasoning step by step before answering, it would often arrive at a better answer. This technique, the same advice as a grade school math teacher would give a student, was called [chain-of-thought prompting](https://every.to/also-true-for-humans/7-22?utm_cta_source=p_how_codex_happened_thinking_chain_of_thought_prompting_1).


Chain-of-thought prompting led to the second generation of AI models and the shimmering “Thinking” user interface. Rather than requiring the user to ask the model to work through a problem step by step, OpenAI trained that behavior into the model itself. Before responding, a reasoning model works in a scratch pad, called a reasoning trace, where it can attack a problem from different angles, backtrack out of a blind alley, and pick a path more likely to succeed. It responds only when it has settled on an answer.


OpenAI called its first model of this kind [o1](https://every.to/chain-of-thought/openai-s-o1-model-explained?utm_cta_source=p_how_codex_happened_thinking_o1_1) and released a preview of it in September 2024. Until then, progress had depended mainly on training larger models for longer. With o1, OpenAI found that the same model could improve its answers on a difficult problem simply by spending more time on it.


One kind of work stood to gain more from this than any other: programming. Programming is uniquely suited to reasoning models because it offers a closed loop: A model can edit code, run it, and see within seconds whether the change worked, allowing it to test and revise fixes on its own without needing a person to check.


Left to think for long enough, theoretically, a reasoning model could do any programming task by itself.


---


![](images/img_11_dee0f9eb.webp)

Building an AI programmer has been a goal at OpenAI for so long that Codex has had many beginnings—starting with its name.[[2]](/p/how-codex-happened/interviews/tibo/?cite=many-codex-beginnings&utm_cta_source=p_how_codex_happened_many_beginnings_cite_many_codex_beginnings#final-20261015-0010)


The first Codex, released in 2021, was a version of [GPT-3](https://every.to/chain-of-thought/gpt-3-is-the-best-journal-you-ve-ever-used?utm_cta_source=p_how_codex_happened_many_beginnings_gpt_3_1) fine-tuned on public code that powered the original [GitHub Copilot](https://every.to/chain-of-thought/i-spent-24-hours-with-github-copilot-workspaces?utm_cta_source=danshipper_main_a_22). Three years later, in the weeks after o1’s preview showed what reasoning models could do, a prompt from leadership set several groups across OpenAI chasing the dream again from different directions.


One of those beginnings came from Embiricos in late 2024.


“The first real, massive ‘feel-the-AGI’ moment for me was [when] I saw someone running a reasoning model that was connected to a terminal,”[[3]](/p/how-codex-happened/interviews/alex/?cite=the-terminal&utm_cta_source=p_how_codex_happened_many_beginnings_cite_the_terminal#final-20261015-0034) he told me, referring to when an AI stops feeling like a tool and starts feeling like a machine that can think and act like a human. “I know [it’s] not exciting now,” but watching it read files, run commands, and work through errors on its own “was fucking cool.”


Embiricos, the product lead I’d met on the eve of GPT-5, had come to OpenAI earlier that year when it acquired Multi, a multiplayer screen-sharing tool for programmers he’d cofounded. At OpenAI he’d pursued a related idea: letting humans and agents work together inside the apps they used. He chased that vision first on the ChatGPT desktop app and then on [Atlas](https://every.to/vibe-check/vibe-check-openai-s-new-ai-browser-atlas?utm_cta_source=p_how_codex_happened_many_beginnings_atlas_1), an AI-powered browser,[[4]](/p/how-codex-happened/interviews/alex/?cite=desktop-before-atlas&utm_cta_source=p_how_codex_happened_many_beginnings_cite_desktop_before_atlas#final-20261015-0028) but [the models at the time were too slow and clumsy at reading a user’s screen](/p/how-codex-happened/interviews/alex/?cite=multimodal-bet&utm_cta_source=p_how_codex_happened_many_beginnings_cite_multimodal_bet#final-20261015-0010) to be useful.


In the terminal, though, the models didn’t have to read a screen—they could work directly in text and code. Seeing an early reasoning model in the terminal convinced Embiricos that they could power a real coding product. Coding wasn’t yet his full-time job, but he immediately started sketching one. For it to work, he believed, users would need to see what the model was doing every 30 seconds, or at most every minute.


Speed was the problem again. Most AI coding products at the time grew around VS Code. GitHub Copilot added AI autocomplete through an extension; Cursor and Windsurf built their own editors on VS Code’s open-source code, adding AI chat alongside the programmer’s work.


These tools depended on a tight feedback loop. Copilot completed the line you were typing; Cursor and Windsurf answered questions within seconds. None asked the model to work on its own for long, because the models couldn’t. OpenAI’s early reasoning models were the reverse: slow and weak when their thinking time was cut short.


Could he turn their flaw—the time it took to get a response—into an advantage?


---


Meanwhile, in another part of OpenAI, Sottiaux, who goes by Tibo, was trying to turn reasoning models back on themselves: using their powers to help researchers build the next generation of models.


“I got involved with coding agents around December 2024,”[[5]](/p/how-codex-happened/interviews/tibo/?cite=research-start-december&utm_cta_source=p_how_codex_happened_building_the_builders_cite_research_start_december#final-20261015-0012) he told me. We were sitting in the OpenAI cafeteria. His glossy brown hair fell to one side, and he wore thin wire glasses that caught the afternoon light. If above the nose he looked like an architect, below he was all programmer: A beard of brown stubble paired with a dark brown hoodie printed with “Research and Deployment Co,” and a slice of pepperoni pizza in hand.


The goal, he told me between bites of pizza, “was to help us write infrastructure and do research faster.”[[6]](/p/how-codex-happened/interviews/tibo/?cite=research-infrastructure-purpose&utm_cta_source=p_how_codex_happened_building_the_builders_cite_research_infrastructure_purpose#final-20261015-0030)


Sottiaux had spent much of his career building infrastructure for researchers, first at DeepMind and then at OpenAI. Research infrastructure—the shared code that AI researchers rely on to run, evaluate, reproduce, and deploy experiments—might seem like an odd origin story for the person who would eventually lead Codex. When you think of infrastructure, you might think of servers and undersea cables, the tech world’s equivalent of plumbing: necessary, but invisible until a pipe springs a leak.


In the AI world, though, infrastructure—and particularly research infrastructure—is where much of the action happens. If you can cut the time it takes to run an experiment, you can run more experiments and get a better model sooner.


“At what point did you split out the model line?” I asked. “How did you decide?” I wanted to fast-forward to the action. Having its own model line felt core to Codex’s magic, and I pictured a meeting inside OpenAI where Sottiaux, president and cofounder **Greg Brockman**, or CEO **Sam Altman** made the farsighted choice to separate Codex from the rest of ChatGPT—giving the team the freedom to ship quickly and upend the company from within.


“[There was no decision to split off the model line](/p/how-codex-happened/interviews/tibo/?cite=no-model-split-decision&utm_cta_source=p_how_codex_happened_building_the_builders_cite_no_model_split_decision#final-20261015-0028),” Sottiaux said matter-of-factly. At the start, he said, “this was a research exploration and an optimization of our velocity.”


Rather than building a model for public consumption, Sottiaux’s group trained internal coding agents on OpenAI’s monorepo,[[7]](/p/how-codex-happened/interviews/tibo/?cite=monorepo-training&utm_cta_source=p_how_codex_happened_building_the_builders_cite_monorepo_training#final-20261015-0012) the single repository where all of the organization’s code lives. The agents wrote the Python code OpenAI’s researchers needed to run and improve the systems that built new models. Those researchers used the agents every day, giving the team a tight feedback loop.


“We were seeing rapid gains on coding,” Sottiaux said. His team was training models frequently, using techniques that differed from—and for a while, were hard to reconcile with—how the larger organization trained models for the public.


Sottiaux, like everyone else at the AI labs, is tight-lipped about those training techniques. But it became clear they were working: His group had successfully turned the models back on the research process that created them, and researchers were using those models to make the next generation.[[8]](/p/how-codex-happened/interviews/tibo/?cite=recursive-improvement&utm_cta_source=p_how_codex_happened_building_the_builders_cite_recursive_improvement#final-20261015-0030)


Engineers call this bootstrapping. Make a model that’s good at helping researchers run experiments, and the researchers can use it to build a more powerful one, which runs better experiments, which leads to a better model, and so on.


This effort supplied one half of what became Codex: agents that could improve the [infrastructure](https://every.to/p/openai-infrastructure?utm_cta_source=p_how_codex_happened_building_the_builders_infrastructure_1) for building new models. To become a product that the rest of the company could use—and that would eventually make its way beyond the confines of OpenAI—it needed the other half: Embiricos’s thesis about how people should work with those agents.


---


> *Thinking…*Thinking...


> *Three approaches so far…*


> *Two of them overlap…*


> *I’ll merge those and continue with what works…*


> *Thinking…*Thinking...


> *Three approaches so far…*


> *Two of them overlap…*


> *I’ll merge those and continue with what works…*


---


After exploration comes convergence.


We can picture OpenAI from above in the last months of 2024 and early 2025. After coding became a top-level company goal,[[9]](/p/how-codex-happened/interviews/greg/?cite=coding-company-goal&utm_cta_source=p_how_codex_happened_convergence_cite_coding_company_goal#final-20261015-0002) several teams of individuals including Sottiaux and Embiricos had started working at oblique angles on the same question.


The open question, Brockman told me, was the right “form factor”:[[10]](/p/how-codex-happened/interviews/greg/?cite=form-factor-search&utm_cta_source=p_how_codex_happened_convergence_cite_form_factor_search#final-20261015-0006) whether the agent belonged in a terminal where developers execute commands, in an editor where they write code, or in the cloud working on its own computer. Some of these paths were blind alleys, but at the time nobody knew which.


“There’s some sense in which OpenAI is betting on a series of startups, but they’re all internal,” Altman said in [an interview with](https://stratechery.com/2025/an-interview-with-openai-ceo-sam-altman-about-devday-and-the-ai-buildout/#the-investor-mindset) **Ben Thompson** [in 2025](https://stratechery.com/2025/an-interview-with-openai-ceo-sam-altman-about-devday-and-the-ai-buildout/#the-investor-mindset). This spirit of parallel inquiry inside of the company [sometimes feels chaotic and wasteful](/p/how-codex-happened/interviews/andrew/?cite=startup-chaos&utm_cta_source=p_how_codex_happened_convergence_cite_startup_chaos#final-20261015-0049) to a few insiders I spoke to. [Who wants to work on the team that built the third-best agent product inside of OpenAI?](/p/how-codex-happened/interviews/greg/?cite=unglamorous-work&utm_cta_source=p_how_codex_happened_convergence_cite_unglamorous_work#final-20261015-0018) Having run a similar strategy at my own company, I know that there’s a thin line between creating space to explore and creating an utter mess.


But in watching OpenAI—and despite the internal grumbling I’ve heard—I have also come to see it as necessary when the frontier keeps moving. In AI, fast [“sustaining”](https://www.christenseninstitute.org/graphic/disruptive-vs-sustaining-innovations/) progress at the model level—to use the late Harvard professor **Clayton Christensen**’s term—makes new kinds of apps possible, constantly disrupting the ones that came before.


A model that can finish a line of code works well as an autocomplete tool; a model that can think for 30 seconds can answer questions in a chat sidebar; a model that can work for an hour wants to be something else entirely. Building a successful product around the previous model doesn’t mean you know what’s next. You need several teams trying different ideas, then bringing their work together once you see what’s useful.


By early 2025 OpenAI was ready to do just that. “Eventually, we thought we should combine forces with another effort, which was called Scientist Assistant,”[[11]](/p/how-codex-happened/interviews/tibo/?cite=scientific-assistant-merge&utm_cta_source=p_how_codex_happened_convergence_cite_scientific_assistant_merge#final-20261015-0020) Sottiaux told me—a merger that brought him together with Embiricos. Across the various internal coding efforts, Brockman said, “We ended up merging two of them. And then merging another two of them.”[[12]](/p/how-codex-happened/interviews/greg/?cite=efforts-converge&utm_cta_source=p_how_codex_happened_convergence_cite_efforts_converge#final-20261015-0006) The combined team was a small multidisciplinary crew of technical product thinkers like Embiricos, infrastructure and engineering wizards like Sottiaux, and researchers like **Mia Glaese**.


Glaese came to OpenAI from DeepMind, where she worked on Gemini and model alignment. At OpenAI, she was responsible for the data used for model training and alignment,[[13]](/p/how-codex-happened/interviews/mia/?cite=glaese-data-alignment&utm_cta_source=p_how_codex_happened_convergence_cite_glaese_data_alignment#final-20261015-0008) meaning she specialized in getting and using data that would shape the specific behaviors of the models.


On one level, she is the ultimate unsentimental empiricist. In our interview, she was unapologetically quantitative: “Just trusting vibes is not that useful in research,” she said. Yet when she talks about the process of making a model, she is quick to laugh at how much of it is a leap into the unknown.


“Every time we train a model, we go on this magical adventure where we’re like, ‘How are we gonna do that?’” she said.


This sort of multidisciplinary team, with product people and researchers working side by side, is somewhat unusual in AI. AI has historically been a research-driven field with the best researchers fetching multimillion-dollar **LeBron James**–sized contracts for their services while everyone else is paid industry-standard engineering salaries. (AI labs have long tried to counter the exalted superstar dynamic by giving most technical employees, whether they are researchers or not, the job title “Member of Technical Staff.”)


Working alongside the product team gave Glaese and the other researchers a chance to see how their models were being used—and hear what people wanted them to do next. Product people could ask, “[Wouldn’t it be amazing if the model could do this thing?](/p/how-codex-happened/interviews/mia/?cite=research-product-together&utm_cta_source=p_how_codex_happened_convergence_cite_research_product_together#final-20261015-0077)” Then researchers could bring it to life. It was Sottiaux’s bootstrapping loop again, this time running between a model and the product built on it.


OpenAI finally had its Codex team—product, design, and research—all working together. Now they just had to decide what to build.


---


![](images/img_12_80e79b3a.webp)

> *Thinking...
> I could try the terminal, the editor, or the cloud…*


> *Which approach fits the models I have?*


> *Our researchers work in the cloud. Could other developers work there, too?*


> *Thinking…Thinking...I could try the terminal, the editor, or the cloud…*


> *Which approach fits the models I have?*


> *Our researchers work in the cloud. Could other developers work there, too?*


---


At Anthropic, a promising approach had already begun to take off.


On February 24, 2025, the company released [Claude 3.7 Sonnet](https://www.anthropic.com/news/claude-3-7-sonnet) and, with it, a [research preview of Claude Code](https://every.to/vibe-check/vibe-check-claude-3-7-sonnet-and-claude-code?utm_cta_source=p_how_codex_happened_the_cloud_research_preview_of_claude_code_1). Unlike Cursor and similar tools, Claude Code had no built-in code editor. It ran in the terminal and worked directly on the files on your own computer: You told it what you wanted, and it read the code, made the changes, and ran them.


Because it ran on your own computer, its work landed in the same files you were already working in, with the same tools you already had installed, and with the context of everything you’d done together so far. You could interrupt it mid-task. You could also bring lessons learned from one session into the next so that your system improved and compounded over time—something that Codex Cloud, with its ephemeral cloud computers, didn’t allow for.


Developers took to Claude Code quickly. At Every, for example, **Edmar Ferreira** wrote in a March 2025 [Vibe Check](https://every.to/vibe-check/vibe-check-claude-3-7-sonnet-and-claude-code?utm_cta_source=p_how_codex_happened_the_cloud_vibe_check_1) that “Claude Code is better than anything that I have used on the agent front.” The rest of the team had begun to agree.


By the spring of 2025, the merged Codex team—Embiricos, Sottiaux, Glaese, and a handful of others—set its sights on a different vision for the future of software engineering: Codex Cloud. They envisioned an agent in the cloud, with access to its own computer, designed for asynchronous work that would allow users to delegate coding tasks from their computer or their phone. They gave themselves roughly seven weeks to build and launch it.[[14]](/p/how-codex-happened/interviews/tibo/?cite=seven-week-cloud-sprint&utm_cta_source=p_how_codex_happened_the_cloud_cite_seven_week_cloud_sprint#final-20261015-0020)


You could click Codex in ChatGPT’s sidebar and open a workspace where you could describe a task and hit “Code.” The assignment peeled off into a queue, clearing the prompt box for the next one. Codex copied your codebase into an isolated cloud machine, edited files, and ran tests and linters—tools that scan code for common mistakes. It returned a summary, a diff of the changes, and a button to open a pull request.


Codex Cloud launched on May 16, 2025, nearly three months before the night I met with McCallum and Embiricos in Mission Bay. It was “very successful internally,”[[15]](/p/how-codex-happened/interviews/tibo/?cite=cloud-internal-success&utm_cta_source=p_how_codex_happened_the_cloud_cite_cloud_internal_success#final-20261015-0024) Sottiaux told me. Outside OpenAI, its launch drew interest but little sustained use.[[16]](/p/how-codex-happened/interviews/alex/?cite=cloud-usage-limits&utm_cta_source=p_how_codex_happened_the_cloud_cite_cloud_usage_limits#final-20261015-0108)


To get it working, developers had to recreate their laptop’s software, permissions, and settings in the cloud[[17]](/p/how-codex-happened/interviews/tibo/?cite=cloud-friction-evidence&utm_cta_source=p_how_codex_happened_the_cloud_cite_cloud_friction_evidence#final-20261015-0024)—a process that could take hours, as you needed to copy over credentials and install critical software packages. Once set up, it could deliver on a well-specified task. But you couldn’t interrupt it to correct its course, and even a follow-up prompt started a fresh cloud computer.


“It’s a tool you’ll reach for if you’re a tech lead adding features or fixing bugs on an existing codebase. If you’re trying to vibe code a new one-person billion-dollar SaaS company, look elsewhere,” I wrote in our launch-day [Vibe Check](https://every.to/vibe-check/vibe-check-codex-openai-s-new-coding-agent?utm_cta_source=p_how_codex_happened_the_cloud_vibe_check_2).


Inside OpenAI, standardized development environments had made setup automatic, and the researchers had clearly defined work to hand off. The team’s own working environment had hidden how much they were asking of everyone else.


The product wasn’t the only thing holding Codex Cloud back. “It was too early because the models weren’t smart enough,”[[18]](/p/how-codex-happened/interviews/alex/?cite=cloud-model-limits&utm_cta_source=p_how_codex_happened_the_cloud_cite_cloud_model_limits#final-20261015-0052) Embiricos said.


“[We were kind of approaching it with this more future vision](/p/how-codex-happened/interviews/mia/?cite=meet-users-on-laptops&utm_cta_source=p_how_codex_happened_the_cloud_cite_meet_users_on_laptops#final-20261015-0040),” Glaese told me. “We didn’t do this like, ‘Let’s go to the people where they are,’” which was “on their laptop.”


Why then did OpenAI [skip the terminal form factor](/p/how-codex-happened/asides/codex-cli/?utm_cta_source=p_how_codex_happened_the_cloud_skip_the_terminal_form_factor_1) that began to work for Anthropic?


“We didn’t skip it,” Sottiaux told me in our cafeteria conversation, referring to an unreleased internal prototype. “[We built a version of that and then discarded it after a month to go for the full cloud version](/p/how-codex-happened/interviews/tibo/?cite=discarded-internal-cli&utm_cta_source=p_how_codex_happened_the_cloud_cite_discarded_internal_cli#final-20261015-0022).”


“Why?” I asked. I knew somewhere out the large floor-to-ceiling windows on all sides of me, if I really looked, I could probably find Anthropic’s office on the horizon. I could certainly walk there without much trouble. San Francisco is a small town.


“Because we were optimizing for what we thought we would benefit from the most if we were willing to invest a lot in the setup,”[[19]](/p/how-codex-happened/interviews/tibo/?cite=internal-cloud-optimization&utm_cta_source=p_how_codex_happened_the_cloud_cite_internal_cloud_optimization#final-20261015-0024) he said.


Behind that answer was a belief I’d heard over and over from people inside of OpenAI. To them, the ideal form of an AI agent has always been one that works autonomously for you in the cloud, that doesn’t stop responding when you shut your laptop lid. Brockman had said the same thing in our interview: “If you project into the future, the right form factor is an AI in the cloud that has its own laptop. And so we actually built that.”[[20]](/p/how-codex-happened/interviews/greg/?cite=cloud-agent-ambition&utm_cta_source=p_how_codex_happened_the_cloud_cite_cloud_agent_ambition#final-20261015-0006)


That choice was also a truce with model limits. The team built the first Cloud product around models that could spend longer working on a task,[[21]](/p/how-codex-happened/interviews/alex/?cite=async-product-choice&utm_cta_source=p_how_codex_happened_the_cloud_cite_async_product_choice#final-20261015-0047) rather than respond to a programmer moment by moment.


OpenAI did, in fact, release a small, [open-source Codex command-line interface](/p/how-codex-happened/interviews/tibo/?cite=open-source-reasons&utm_cta_source=p_how_codex_happened_the_cloud_cite_open_source_reasons#final-20261015-0036) (CLI) reminiscent of Claude Code on April 16, exactly one month before Codex Cloud. It was one more of Codex’s many beginnings.


Embiricos described that public CLI as a separate side project built “heroically by, like, two people.”[[41]](/p/how-codex-happened/interviews/alex/?cite=two-person-cli&utm_cta_source=p_how_codex_happened_the_cloud_cite_two_person_cli#final-20261015-0126) But this CLI was not where OpenAI had placed most of its resources—or the specialized model it was training for Codex Cloud. “You couldn’t even use the Codex model in the CLI,” he said.


Running an agent on a user’s computer also raised safety questions. A coding agent could do more than suggest code: It could edit files and run commands on the user’s computer. “As a company, we have a very conservative safety stance,”[[42]](/p/how-codex-happened/interviews/alex/?cite=cli-safety-constraint&utm_cta_source=p_how_codex_happened_the_cloud_cite_cli_safety_constraint#final-20261015-0130) Embiricos said. “We actually had to do a lot of work to figure out how to get comfortable deploying that level of capability.” Early users instead had to run the CLI with a general-purpose model—[o4-mini](https://every.to/vibe-check/vibe-check-openai-s-o3-gpt-4-1-and-o4-mini?utm_cta_source=p_how_codex_happened_the_cloud_o4_mini_1) by default—that hadn’t been built to work as a coding agent. The CLI existed, but the attention of the team—and its best model—was on Cloud.


The problem was it didn’t work. The Cloud product failed to find product-market fit. The team’s engineering manager left for Cursor, the front-runner in AI coding with a valuation of $9 billion. Around this time, OpenAI reportedly [reached a $3 billion agreement](https://www.bloomberg.com/news/articles/2025-05-06/openai-reaches-agreement-to-buy-startup-windsurf-for-3-billion) to acquire Windsurf, Cursor’s closest competitor. That deal would fall apart [in July](https://techcrunch.com/2025/07/11/windsurfs-ceo-goes-to-google-openais-acquisition-falls-apart).


“The most challenging time was when we felt like we didn’t know what to do. Or we knew what to do, but it was really hard to see that [progress] actually happening,” Embiricos told me.


For the first time, the Codex team—and to an extent OpenAI’s larger coding ambitions—were lost in the wilderness.


---


![](images/img_13_28e4750c.webp)

> *Thinking…*Thinking...


> *Hmm, this worked in our environment. Why isn’t it working for users?…*


> *Maybe I’m trying to fix the wrong thing…*


> *Going back to the local approach I set aside…*


> *There’s something here. But I’ll need to rebuild it…*


> *Thinking…*Thinking...


> *Hmm, this worked in our environment. Why isn’t it working for users?…*


> *Maybe I’m trying to fix the wrong thing…*


> *Going back to the local approach I set aside…*


> *There’s something here. But I’ll need to rebuild it…*


---


What makes a reasoning model powerful is its ability to backtrack. If it believes a bug lives in a particular part of the code and rewrites it, only to find the bug is still there, it does not typically continue marching confidently in the wrong direction. It can reconsider its assumptions, broaden its search for solutions, and decide on a new, more promising path based on what it’s learned.


This ability to use mistakes to course-correct is what allows reasoning models to find answers that were not obvious at the start.


In the aftermath of the Cloud launch, in the late spring and summer of 2025, the Codex team was ready to try another path. At the time, the project occupied what designer **Ed Bayes**—who had recently joined the team—recalled as “the backwaters” of OpenAI. “If you wanted to be the sexy designer,” he told me, “you work[ed] on ChatGPT.”


Here, into this neglected outpost, Sottiaux ascended as the team’s engineering manager. “I took over the team, and then I changed the direction quite a bit,”[[22]](/p/how-codex-happened/interviews/tibo/?cite=tibo-takes-over&utm_cta_source=p_how_codex_happened_backtracking_cite_tibo_takes_over#final-20261015-0030) he told me. “We pivoted to local.”


“Local” meant running the agent on the developer’s own computer, the way Claude Code did, instead of in the cloud. They started with [the local Codex CLI](/p/how-codex-happened/asides/codex-cli/?utm_cta_source=p_how_codex_happened_backtracking_the_local_codex_cli_1) that, as Embiricos mentioned, had been “heroically” built as a two-person side project. Rather than start adding features to it immediately, which would quickly generate momentum, Sottiaux took a different tack. He decided to rewrite the agent.[[23]](/p/how-codex-happened/interviews/tibo/?cite=agent-rewrite-bet&utm_cta_source=p_how_codex_happened_backtracking_cite_agent_rewrite_bet#final-20261015-0032)


“We were kind of slow to have really good CLI features,”[[24]](/p/how-codex-happened/interviews/tibo/?cite=cli-feature-delay&utm_cta_source=p_how_codex_happened_backtracking_cite_cli_feature_delay#final-20261015-0032) he told me, “because we were so busy developing the agent.”


The CLI was the interface users interacted with, but Sottiaux’s priority was the machinery underneath: the agent that read files, ran commands, and more. He wanted to improve it and separate it from the terminal interface so it could live anywhere—inside a code editor, a desktop or mobile app, the cloud, or ChatGPT itself.


The team rebuilt the agent in Rust,[[25]](/p/how-codex-happened/interviews/tibo/?cite=shared-agent-infrastructure&utm_cta_source=p_how_codex_happened_backtracking_cite_shared_agent_infrastructure#final-20261015-0032) a language designed for systems where speed and safety matter. The same machinery could then power both the terminal CLI and, later, the editor extension.


What they still lacked, though, was a model good enough to drive it.


While the Codex team was rebuilding its agent under Sottiaux’s leadership, **Michelle Pokrass** was working to make GPT-5 better at real-world programming.


Pokrass, who had led research on [GPT-4.1](https://every.to/vibe-check/vibe-check-openai-s-o3-gpt-4-1-and-o4-mini?utm_cta_source=p_how_codex_happened_backtracking_gpt_4_1_1), led post-training—refining an already trained model’s behavior so it could handle real programming work—with a focus on customers who had asked for better interactive coding.[[26]](/p/how-codex-happened/interviews/alex/?cite=interactive-coding-customers&utm_cta_source=p_how_codex_happened_backtracking_cite_interactive_coding_customers#final-20261015-0157)


A coding model can be like a student with a perfect SAT score who has never held a job. OpenAI’s models had excelled at coding competitions, but those results hadn’t carried over to everyday engineering. “[They never had seen a messy codebase or how a programmer might interrupt it halfway through](/p/how-codex-happened/interviews/greg/?cite=messy-codebases&utm_cta_source=p_how_codex_happened_backtracking_cite_messy_codebases#final-20261015-0002),” Brockman told me.


To give the book-smart models real-world experience, Pokrass and her team sat with programmers and watched them work to see where the models broke down and turned those failures into repeatable training tasks.


That was how OpenAI arrived at the model—and the moment—that had brought me to that conference room in Mission Bay in August 2025.


Seen from inside the Codex team’s tumultuous summer, the caution I had felt in GPT-5 that night made sense. Burned by trying to leap straight to full autonomy with Codex Cloud and guided by customers asking for a better interactive collaborator, OpenAI had built a model that excelled at working *with* a human programmer step by step. It could understand how the pieces of a messy codebase fit together, explain its plan, investigate a bug, and pause to ask before stepping out of line.


Compared with Claude Code, GPT-5 in the Codex CLI still felt behind to us at Every. Kieran wrote in our [launch-day Vibe Check](https://every.to/vibe-check/gpt-5?utm_cta_source=p_how_codex_happened_backtracking_launch_day_vibe_check_1), “GPT-5 is a Sonnet 3.5 killer, not a leap into the future.” But for the vast majority of software engineers at the time, a careful collaborator was what they wanted. Delegating production code to autonomous agents was still commonly snorted at by programmers used to writing every line by hand.


“[I don’t let it drive my code](/p/how-codex-happened/asides/dhh-later/?utm_cta_source=p_how_codex_happened_backtracking_i_don_t_let_it_drive_my_code_1),” **David Heinemeier Hansson**, the creator of Ruby on Rails and an influential voice in the engineering community, said [around the time of the GPT-5 launch](https://lexfridman.com/dhh-david-heinemeier-hansson-transcript/). “The joy of a programmer, of me as a programmer, is to type the code myself.” Besides, when the agent drove, he said, “I can literally feel competence draining out of my fingers.” (By January 2026 he would [write that AI agents](https://world.hey.com/dhh/promoting-ai-agents-3ee04945) were “fully capable of producing production-grade contributions to real-life code bases,” and at [Rails World](https://devops.com/dhh-declares-end-of-hand-writing-code-at-rails-world-2026/) in September he declared the end of writing code by hand at his company.)


When the Codex team followed up the GPT-5 launch in late August with an extension for VS Code and Cursor, those developers flocked to it. Their enthusiasm gave OpenAI every reason to keep improving the extension. Each new user and feature request pulled the team toward helping programmers work step by step and away from building agents that could take on whole tasks.


For Embiricos, though, the same launch meant the team could pursue their larger ambitions. After months in the wilderness, the rebuilt local agent finally had a model capable of driving it.


Once they shipped GPT-5 with the revamped CLI, he told me, “it created this self-fulfilling flywheel.”


He remembered thinking, “Finally we can fight now.”


---


> *Thinking…*
> Thinking...
> *The CLI and editor extension are finally taking off…*


> *Customers love the sidebar, and Claude Code is the product to beat in the terminal…*


> *Let’s double down on the editor extension and catch up in the terminal…*


> *Interrupted by Tibo*


> *Thinking…*
> Thinking...
> *The CLI and editor extension are finally taking off…*


> *Customers love the sidebar, and Claude Code is the product to beat in the terminal…*


> *Let’s double down on the editor extension and catch up in the terminal…*


> *[Interrupted by Tibo]Interrupted by Tibo*


---


With the Codex CLI and VS Code extension exploding in popularity, the logical choice would be to continue to invest in both of them.


Instead, the Codex team did something unexpected.


“[We decided we should continue maintaining the CLI, but the next biggest immediate investment should be a native desktop app](/p/how-codex-happened/interviews/tibo/?cite=desktop-investment&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_desktop_investment#final-20261015-0038),” Sottiaux told me.


Inside OpenAI, he could see the models completing longer tasks and drawing on information from outside the codebase, with voice and images on the way. People would soon be running several agents at once and spending their whole day with them. “It has to be this very rich interface if you’re gonna spend all your time in it,” he said. Trying to juggle half a dozen agents communicating in text, images, voice, and video inside of a text-only window built in the 1970s seemed silly to him.


For Embiricos, a local desktop app also pointed toward the workflow that had eluded them with Codex Cloud, where users could not interrupt the agent mid-task. With an app on their own computer, he thought, people could start by working closely with the agent and then, like onboarding a teammate, learn which tasks they could leave to it.[[27]](/p/how-codex-happened/interviews/alex/?cite=interactive-teammate&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_interactive_teammate#final-20261015-0122) The same interface could eventually take Codex beyond developers to people who would never open a terminal.


To help design and build it, Sottiaux brought in **Andrew Ambrosino**, a designer, programmer, and former startup founder.


![A team stands before a transparent app-window outline. Four people examine the app window they have built. A person steps inside the app window while others stand nearby. A group gathers inside the app window. Stylized illustration; the figures are not portraits or a literal record of the room.](images/img_14_800b62e3.png)
*A team stands before a transparent app-window outline. Four people examine the app window they have built. A person steps inside the app window while others stand nearby. A group gathers inside the app window. Stylized illustration; the figures are not portraits or a literal record of the room.*

Ambrosino reminds me of B.J. Novak’s character in *The Office*: dark hair, thick eyebrows, and a small, tight-lipped smile. In person and online, he gives the sense of [perpetually being inwardly amused](/p/how-codex-happened/interviews/andrew/?cite=pets-shareholders&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_pets_shareholders#final-20261015-0063); whether or not anyone else joins him in the joke is a consideration but often appears to be somewhat secondary.


Anyone following him for insights into the future of artificial intelligence might scroll his feed and find a post with 617 likes consisting entirely of a single word: “ai.” Another post is, mysteriously, [“tibo”](/p/how-codex-happened/asides/tibo/?utm_cta_source=p_how_codex_happened_the_desktop_bet_tibo_1) (1,000-plus likes).


(If you’re wondering what he meant by “tibo,” I can report that Sottiaux seems to be consistently on his mind. When I asked him whose comedy he admires, he replied, “Tibo is my comedy idol.” I leave it to the reader to decide how much this clarifies.)


When Ambrosino joined the small group working on the app, they knew they wanted to make a desktop app, but not what it would look like.[[28]](/p/how-codex-happened/interviews/andrew/?cite=app-starting-uncertainty&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_app_starting_uncertainty#final-20261015-0022) All the team knew was that they wanted to make something they would use themselves.


Their first mandate, Ambrosino told me, was to make the app their main tool for everyday work.[[29]](/p/how-codex-happened/interviews/andrew/?cite=daily-driver-mandate&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_daily_driver_mandate#final-20261015-0031) “We knew we wanted a surface that could be a daily driver, but [one] that was more lightweight than an IDE,” he said.


As Claude Code took off, a handful of apps had begun experimenting with what a home for coding agents might look like outside the terminal. Conductor, a Mac app for running coding agents, had a sidebar of tasks, each with its own agent and chat where you could give instructions and follow the work. ChatGPT supplied another reference point: a list of conversations down the side and a single thread in the middle. The Codex app took “more inspiration from chat than it does VS Code,”[[30]](/p/how-codex-happened/interviews/andrew/?cite=chat-design-inspiration&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_chat_design_inspiration#final-20261015-0091) Ambrosino said of their design process. Anthropic, too, by that point, had a Claude desktop app.


The team worked quickly, answering the basic questions like how users would keep track of their work (each task had its own conversation with an agent), [how the sidebar should be organized](/p/how-codex-happened/interviews/ed/?cite=basic-interface-questions&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_basic_interface_questions#final-20261015-0009) (conversations grouped by project), and how the basic interface should be laid out (a sidebar of tasks beside the selected conversation).


Then came a harder question: When an agent got something wrong, could you fix the code yourself by hand inside of Codex? The team decided on a risky answer: No built-in code editor. If you wanted to make any changes to your code, you *had* to ask the agent.


“We specifically wanted it to be a different thing [from a code editor],” Ambrosino told me. Let developers type code in the app, and they’d expect everything else their editor did—undo, search, keyboard shortcuts—and thereby notice what Codex lacked. Meeting, let alone exceeding, these expectations would have required a massive effort from their team of four.


Codex couldn’t win by being a bad code editor. Coding with agents had to be so good that developers wouldn’t miss the editor.


The only problem was that they were still building a replacement for VS Code *with* VS Code.


“Every day Alexander would come in and be like, ‘Let’s go around the table. Are you maining this app? Are you maining this app?’”[[31]](/p/how-codex-happened/interviews/andrew/?cite=maining-the-app&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_maining_the_app#final-20261015-0031) said Ambrosino.


At first the answers were all “no”—none of them was using Codex as their main coding tool. Without a code editor, even a small correction required a conversation with an agent. **Dominik Kundel**, who works in developer experience, wrote in an early Slack message that “it feels cumbersome to have to prompt Codex” just to replace a sentence.


Even Ambrosino had doubts: “I think ‘no file editing’ is the launch scope I’m most skeptical about,” he wrote in November to the team.


The outside market made the decision to leave out a code editor look even riskier. In November of 2025, Google [released Antigravity](https://codelabs.developers.google.com/next26/kcc-ops-skill-antigravity), another coding tool [built on VS Code](/p/how-codex-happened/asides/forking/?utm_cta_source=p_how_codex_happened_the_desktop_bet_built_on_vs_code_1), combining AI agents with a full editor.


“We just kinda looked at each other,” Ambrosino recalled. “[Did we make a huge mistake by not forking VS Code?](/p/how-codex-happened/interviews/andrew/?cite=forking-vscode-doubt&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_forking_vscode_doubt#final-20261015-0024) We felt very conflicted on this, and I don’t think the team even agreed with each other.”


The models powering the app were a problem, too. OpenAI had launched its dedicated Codex model line in September, but by November it still wasn’t good enough for the desktop product they were building. Even a fully featured app would have been “unreleasable because of the quality of the models at that point,”[[32]](/p/how-codex-happened/interviews/andrew/?cite=unreleasable-models&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_unreleasable_models#final-20261015-0018) Ambrosino told me.


Over the next several weeks, that began to change. On November 19, OpenAI released GPT-5.1 Codex Max, which could code for hours at a time. [GPT-5.2 Codex](https://every.to/vibe-check/vibe-check-gpt-5-2-is-an-incremental-upgrade?utm_cta_source=p_how_codex_happened_the_desktop_bet_gpt_5_2_codex_1) followed on December 18, bringing further improvements in making changes across large codebases.


Glaese worked directly with the rest of the Codex team to further shorten the feedback loop between developer feedback and model improvements. Crucially, [they focused on making Codex work better for the people using it](/p/how-codex-happened/interviews/mia/?cite=prioritize-real-workflows&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_prioritize_real_workflows#final-20261015-0091), rather than just raising the models’ scores on popular benchmarks. And because the Codex model line was separate from the main ChatGPT model, they could move more quickly without worrying about how those changes would affect the 800 million people using ChatGPT.


By December, more of the team was using the Codex app over their code editors. “I was originally craving a code editor,” Kundel wrote in Slack. “Now most of my changes I just leave inline comments and it’s rapid fast.” Ambrosino found that he still had to steer the model, but he no longer needed to edit its code by hand.[[33]](/p/how-codex-happened/interviews/andrew/?cite=no-longer-hand-editing&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_no_longer_hand_editing#final-20261015-0041) Glaese, too, became aware that the sentiment had changed internally. “5.2 was a turning point where I was like, ‘Wow, I’m very excited about what this can do[[34]](/p/how-codex-happened/interviews/mia/?cite=glaese-five-two-threshold&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_glaese_five_two_threshold#final-20261015-0048) for me,’” she said.


Across the industry, the holidays became an [inflection point](https://every.to/context-window/claude-code-in-a-trenchcoat?utm_cta_source=context_window_main_claude_code_in_a_trenchcoat_plus_personal_projects_took_over_the_holiday_break_1), as developers spent Christmas break building entire apps end to end with Anthropic’s [Opus 4.5](https://every.to/vibe-check/vibe-check-opus-4-5-is-the-coding-model-we-ve-been-waiting-for?utm_cta_source=p_how_codex_happened_the_desktop_bet_opus_4_5_1) and OpenAI’s GPT-5.2 without touching a line of code.


By early January the whole team was using the Codex app. Now they needed to find out whether the rest of OpenAI would use it, too. If not, Ambrosino said, it was “back to the drawing board.”[[35]](/p/how-codex-happened/interviews/andrew/?cite=internal-pmf-release-gate&utm_cta_source=p_how_codex_happened_the_desktop_bet_cite_internal_pmf_release_gate#final-20261015-0034)


By February the Codex desktop app was gaining wide adoption on the engineering and research teams. OpenAI researcher **Noam Brown** said he had “fully switched” to it, and Brockman, a devoted user of the terminal and the Emacs editor, had, too. He said returning to his old workflow “felt like going back in time.” Altman would [describe](https://venturebeat.com/orchestration/openai-launches-a-codex-desktop-app-for-macos-to-run-multiple-ai-coding) it later as “the most loved internal product we’ve ever had.”


The Codex team had built something that developers inside of OpenAI loved. But Codex Cloud had also been embraced inside OpenAI and flopped once it was launched. Would this time be different?


---


![](images/img_15_3989533a.webp)

> *Thinking…*Thinking...


> *A lot of people here are using it…*


> *But I’ve mistaken that for success before…*


> *This time it works where the user already works…*


> *Time to test it outside…*


> *Thinking…*


> **


> **


> **


> **


---


The Codex macOS desktop app was released to the public on February 2, 2026. It looked more like a chat app than a code editor: A sidebar held ongoing and historical tasks, and clicking one showed what the agent had done and let you send it further instructions.


You could ask one agent to fix a bug, send another off to build a feature, and move between them to answer questions or review their changes. Each could work on its own copy of the code without overwriting the others’ work. You could stay close and steer, or leave several assignments running and come back when they needed you.


At the time, none of this was especially groundbreaking. The Claude desktop app, for example, had allowed technical and nontechnical users to do the same for months. But the Claude desktop app had been built step by step, starting with Chat, then adding Code, and then adding [Cowork](https://every.to/vibe-check/vibe-check-claude-cowork-is-claude-code-for-the-rest-of-us?utm_cta_source=p_how_codex_happened_the_codex_app_cowork_1)—which made its interface feel confusing and tacked together. It was hard to figure out which tab to use for which task and what set of features or permissions would be available in each.


The Codex app bore [none of these scars](/p/how-codex-happened/asides/late-comer/?utm_cta_source=p_how_codex_happened_the_codex_app_none_of_these_scars_1). When I used it for the first time—alongside the new Codex model released a few days later, [GPT-5.3 Codex](https://every.to/vibe-check/gpt-5-3-codex?utm_cta_source=p_how_codex_happened_the_codex_app_gpt_5_3_codex_1)—it was fast, simple, and totally [agent-native](https://every.to/guides/agent-native?utm_cta_source=p_how_codex_happened_the_codex_app_agent_native_1). There was a fluidity to the experience, a feeling you get when all of the details of a product are right. Because of the team’s early insistence on excluding a code editor, they made sure that the Codex agent could do almost anything inside of the app that a user could do. That meant you didn’t have to dig through settings to, for example, connect a new tool. [Instead, you could just ask the agent.](/p/how-codex-happened/interviews/andrew/?cite=nontechnical-worlds&utm_cta_source=p_how_codex_happened_the_codex_app_cite_nontechnical_worlds#final-20261015-0074)


Partly, this was a latecomer advantage. Because the OpenAI team had started its desktop app after the Claude desktop app added tabs for both Claude Code and Claude Cowork, the Codex team could see a validated trajectory for their app.


GPT-5.3 Codex was also a turning point in OpenAI’s model capabilities. According to Glaese, it was the first time they had started to branch out from programming-specific training for the Codex line. They still named it Codex, and she wasn’t claiming it was better at everything. But [the team had begun asking what else a coding agent needed to know to be useful for all kinds of knowledge work](/p/how-codex-happened/interviews/mia/?cite=beyond-coding&utm_cta_source=p_how_codex_happened_the_codex_app_cite_beyond_coding#final-20261015-0024).


The impact on my workflow was immediate: I switched from using Claude almost exclusively to [using Codex](https://every.to/vibe-check/gpt-5-3-codex?utm_cta_source=p_how_codex_happened_the_codex_app_using_codex_1) for large portions of my work. On [Proof](https://proofeditor.ai/), a document editor I was building, I watched Codex fix [complex bugs](https://every.to/chain-of-thought/when-your-vibe-coded-app-goes-viral-and-then-goes-down?utm_cta_source=p_how_codex_happened_the_codex_app_complex_bugs_1) autonomously without much intervention. Soon I was leaving it working overnight on difficult problems, and anytime I was faced with a particularly gnarly task, I went to Codex first.


[GPT-5.4](https://every.to/vibe-check/gpt-5-4-openai-is-back?utm_cta_source=p_how_codex_happened_the_codex_app_gpt_5_4_1)’s arrival in early March cemented Codex as my daily driver. It was still an expert coder, but now it explained itself clearly and better understood what I wanted. And because the Codex app had a clean and fast interface, I started to do all of my work inside of it.


By then many people at Every were using OpenAI’s tools and models every day too—a reversal from just a few months earlier, when Claude was far and away the dominant choice. As we put it in our [GPT-5.4 Vibe Check](https://every.to/vibe-check/gpt-5-4-openai-is-back?utm_cta_source=p_how_codex_happened_the_codex_app_gpt_5_4_vibe_check_1): OpenAI was back.


The same thing was happening far beyond Every. By March 19, OpenAI said Codex had passed [2 million weekly users](https://openai.com/index/openai-to-acquire-astral/), while overall usage had grown fivefold since the start of the year. In April, OpenAI added an in-app browser, so the agent could look things up and check its work on a live web page. It could also work across other Mac apps and show previews of documents, slides, and spreadsheets. Even someone who had never written code could ask for a presentation or a budget report and see the result without leaving the app.


  
  
  CHAT
  
  
  
  CODEX
 
  
  
  CHAT
  
  
  
  CODEX
 By June, Codex had more than 5 million weekly users, and roughly [one in five was a knowledge worker](https://openai.com/index/codex-for-knowledge-work/). On July 9, OpenAI made the Codex desktop app [the new ChatGPT desktop app](https://every.to/context-window/the-urge-to-merge-chatgpt-and-codex?utm_cta_source=p_how_codex_happened_the_codex_app_the_new_chatgpt_desktop_app_1), with chat inside it.[[36]](/p/how-codex-happened/interviews/tibo/?cite=merge-desktop-identity&utm_cta_source=p_how_codex_happened_the_codex_app_cite_merge_desktop_identity#final-20261015-0122) Under the hood, the new ChatGPT still tells your Mac its name is com.openai.codex.


Codex Cloud had shipped as a tab inside ChatGPT. Now ChatGPT runs on Codex.


Ed Bayes remembers walking out of the all-hands where the merge was announced, thinking about how far the team had come. What had started as “a few people in the corner” had now become “[the future of ChatGPT](/p/how-codex-happened/interviews/ed/?cite=future-of-chatgpt&utm_cta_source=p_how_codex_happened_the_codex_app_cite_future_of_chatgpt#final-20261015-0001).”


“This is like a piece of American corporate history,” he told me.


---


![](images/img_16_0ab53ff2.webp)

Ten months after the GPT-5 launch, I was back in a conference room with Alexander Embiricos.


“I’m just going full honesty here, right?” Embiricos asked.


“Please do,” I said.


It was early June, a month before the now red-hot Codex was to merge into ChatGPT, and we sat in OpenAI’s downtown Manhattan office. He wore a gray zip-up with the sleeves pushed up. His role had recently changed from product lead for the Codex agent to OpenAI’s head of enterprise product. Behind him was a whiteboard.


I had come to ask Embiricos how his team went on from Codex Cloud’s failure to building what would become the foundation of ChatGPT—and how they had avoided getting stuck in the pair-programming trap I’d worried about in Mission Bay. Most teams build on what’s working. The Codex team hadn’t. What had allowed them to keep moving?


Embiricos picked up a black marker and sketched Codex’s growth on the whiteboard. He started with a short upward curve for Codex Cloud. It was a nice spike, but it flattened out quickly.[[37]](/p/how-codex-happened/interviews/alex/?cite=cloud-growth-curve&utm_cta_source=p_how_codex_happened_the_next_curve_cite_cloud_growth_curve#final-20261015-0108)


Then he drew a steeper, bigger curve for the CLI after GPT-5; another, higher still, for the editor extension. Last came 5.3 Codex and the desktop app, a curve that dwarfed the others.[[38]](/p/how-codex-happened/interviews/alex/?cite=successive-growth-curves&utm_cta_source=p_how_codex_happened_the_next_curve_cite_successive_growth_curves#final-20261015-0116) The first mark now looked like a scratch near the bottom of the board.


The curves he drew on the whiteboard looked like a diagram from Christensen’s *The Innovator’s Dilemma*.


Four product curvesEditorial reconstruction of four qualitative product curves described in the article: Codex Cloud, CLI after GPT-5, IDE extension, and the desktop app with 5.3-Codex. Coordinates, spacing and scale are illustrative, not measured data or a tracing of the two-curve photograph.CodexCloudCLI &GPT-5IDEextensionDesktop app& 5.3-CodexChristensen famously traced how steady advances in hard drives and processors drove the shift from mainframes to minicomputers to desktop PCs, laptops, and eventually phones—each leap in the underlying hardware enabling a simpler form factor that unlocked a larger, less technical market and overtook the last.


A pattern that took half a century inside of a succession of new companies in traditional computing had played out in miniature inside OpenAI in 10 months with a team of just a handful of people. Relentless leaps in the models kept outgrowing the interfaces built around them—forcing the Codex team to move from a code-editor sidebar, to a terminal, to a lightweight desktop app that stripped out the code editor entirely.


In Christensen’s book, the team riding a winning curve almost never rides the next one; the success of the existing product suffocates whatever comes after it. The Codex team avoided that fate partly because OpenAI’s executives had grown up in the startup world studying that exact trap. The company was structured to behave like a portfolio of parallel bets, and the Codex team was given space to iterate on its own product and model line outside of the strictures of ChatGPT’s mammoth scale and user base.


Using AI to build AI also changed the physics of product development. In a traditional company, starting a new product requires months of meetings to win budget and engineers—debates where the booming existing product almost always wins. At OpenAI, because the team was using Codex to build Codex, a handful of people could spin up a new surface in weeks.[[39]](/p/how-codex-happened/interviews/tibo/?cite=agents-compress-months&utm_cta_source=p_how_codex_happened_the_next_curve_cite_agents_compress_months#final-20261015-0046)


“It takes way less talking now to convince people,”[[40]](/p/how-codex-happened/interviews/tibo/?cite=less-talking-more-showing&utm_cta_source=p_how_codex_happened_the_next_curve_cite_less_talking_more_showing#final-20261015-0048) Sottiaux had told me.


Looking at the whiteboard, Embiricos had one more new curve to draw. Now that millions of people trusted the agent on their computers, the next step was to return to the vision that had failed the previous spring—an agent that kept working long after you walked away.


“We’re gonna move to asynchronous,” he said, “which means we’re gonna have to rehoist to the cloud.”


This time, I couldn’t help but notice his laptop sitting on the conference table, its lid firmly closed.


[Dan Shipper](https://every.to/@danshipper?utm_cta_source=post_4512_post_body_dan_shipper_1) is the cofounder and CEO of Every, where he writes the [Chain of Thought](https://every.to/chain-of-thought?utm_cta_source=post_4512_post_body_chain_of_thought_1) column and co-hosts [The Every Podcast](https://every.to/podcast?utm_cta_source=post_4512_post_body_the_every_podcast_1).

