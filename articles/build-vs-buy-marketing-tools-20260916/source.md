# Build vs. buy: Marketing tools in the vibe code era

*Matt (Sentry) and Sarah (Railway) share their takes on when to build something yourself, when to reach for engineering, and when to buy software in the age where anyone can cook*

> 作者: Matt Henderson | 日期: 2026-09-02T23:55:50+08:00

> 原文链接: https://hendersonmatthew.substack.com/p/build-vs-buy-marketing-tools

---

The exponential number of new vendors popping up on the annual marketing technology landscape map is getting out of hand:


![](images/img_01_4db2fb65.png)

And yet, we’re all shipping internal tooling in parallel*.* AI adoption was likely a top-down priority from the CEO, Founder, or CMO this year, but how do we ensure we don’t create a tech debt problem, spend tokens/time on vibe coded tools only one team member uses, and also keep the productivity bar high?

Experimenting and solving your most annoying problems with AI is always a good thing. And getting the whole team AI-pilled through this method is great, but there’s so many instances where a project simply shouldn’t be reached for bc it’d be better driven with an engineer or outsourced and bought.

> *At Sentry, everyone in marketing is operating with their own skills, their own tools, their own hosted projects. A handful of these skills and tools are duplicative of what other people have or software that already exists in the stack. We’re now starting to converge on what should be shared, how it should be, and what we’re going to keep within our existing SaaS contracts. - Matt*

We are going to walk through our takes on what should be built vs. bought and to start, we created a framework for deciding **who** should build internal tooling. Then, we’ll list out common categories of marketing technology and share each of our POVs on whether it’s worth building or buying.


## Framework for who should build

Creating an internal system for building can help drastically improve likelihood that tool will be maintained and used widely.

> *At Railway, we have an internal MCP that’s borderline god within the organization. It holds a shared set of skills, tools, guardrails, and the like so anyone using it can create internal tooling safely. Beyond safety, it holds guidelines for things like brand design and architecture specs so our internal tooling is pleasant to look at. This setup is possible because: we have a highly technical team; we spend a lot of effort perfecting our tooling; we’re still under 50 employees. - Sarah*

But knowing when to reach for eng help and knowing when to DIY could save you many hours and wasted resources/tokens. So we came up with a general framework:


![](images/img_02_7f69cf94.png)

Occasionally a customer-facing vibe-coded tool could be *fine*. Maybe it’s a survey tool or template creator that lives on your website. but customer facing tools always need more scrutiny.

Ok with that out of the way, let’s get into each decision on whether to build or buy a tool for marketing. We both went through 8 scenarios and separately flagged if we’d build or buy that marketing software or system.


## Build vs. Buy: marketing decisions

1. CRM

  1. Sarah - **buy.** an automation-forward CRM (like Attio) so you can use it as a datastore and build reporting on top of it. Salesforce may be a necessary evil at scale, as much as I hate to admit it.
  2. Matt - **buy.** Salesforce, HubSpot, etc. They have so many integrations that make life easier and the customer data becomes actionable. Google ads conversion passthrough, sales tools like Gong integrate, ops workflows are automated, reporting on opportunities is out of the box, etc. Don’t build this.
2. CMS

  1. Matt - **build**. This is one marketing technology I see dying off over the next two years. Everyone wants to edit their website in code now that LLMs like Claude make this 10x easier to update pages, spin up new ones, utilize skills as templates, etc. One great engineer working to create guardrails, scalable systems, etc. will enable the rest of the team to build it all out and move faster. I wrote more on our website migration out of a CMS [here.](https://substack.com/home/post/p-199627523)
  2. Sarah - **build** but only if you have good design AI guardrails, are ready to vibe code your website, and have an eng-forward GTM/marketing team. Without those 3 things, your website is going to look like AI slop.
3. Audience data platform

  1. Sarah - **build** full stop. Any audience tool I’ve used is great at first, but hits a wall after a certain amount of customization. Your ICP is your company’s secret sauce and getting it right is a competitive advantage.
  2. Matt - **depends**. One of the tools I built in an afternoon allows you to define your ICP, then it will create thousands of youtube video URLs that you can use as targeting in google ads for youtube ads.  But tools like Clay (for B2B) exist to create ICP accounts, enrich, and find identities. So I’d build what you can, then use cheap, proven tools for the rest.
4. BI tools

  1. Sarah - **buy** because it’s a PITA to build. Just ask the Omni team how long it took them to implement all the quirks that come with editing charts, or the Hex team how long it took to get their AI query agent right. There is no competitive advantage to having your own BI tool, and the requirements are fairly standard across different organizations.
  2. Matt - **buy** because you need a data eng team to correctly make a scalable database and logic behind the scenes. The business will run on that, but build your own dashboards for blind spots like social listening data, or AI visibility data. Anytime you log into a separate tool for reporting, ask yourself if you could just build something to automate that.
5. Emailing system

  1. Sarah - **buy**. [Customer.io](http://customer.io) is the answer for any company pre-series C, and for most even after. Managing domain verification, email batch sends, DMARC policies, etc is also a PITA. Have a tool that manages the technicals, allows you to add your own design, and use it to your heart’s desire.
  2. Matt - **build**. I’m a big fan of what Resend is doing and if I had to start from scratch, I’d start there. I use it on my side projects and it works great for asking a coding agent “spin up a retention email sequence for once a customer hits 6 months of usage. Use my design system.” and it just works. Having your email templates and sequences all in code is a dream for updating. Sentry already has a well thought out and integrated system via Inflection, so I wouldn’t rip it out just to vibe code something.
6. AEO / SEO tracking

  1. Sarah - **buy** tools like Ahrefs and Gauge, which are built to run tests at scale and scrape tools via integrations. Both have the advantage of using aggregate data to make better suggestions, use it to your advantage.
  2. Matt - **buy**. Build your own tools/skills/dashboards/views based on the tools you buy. Ahrefs/Profound are what we use which help me automate AI visibility and SEO reporting as well as give context to my agents to update our site.

1. AB testing platform

  1. Sarah - **don’t do** except for when you reach a huge scale. Trust your convictions and run isolated tests on other platforms (like Google ads is a great place to test messaging).
  2. Matt - **build** a simple directional tool if you have your website in code (before/after analysis). Don’t buy until you reach a scale that matters. [Statistical significance calculators](https://abtestguide.com/calc/) exist so you could test the amount of sessions and conversions you get to see if a tool would even be able to make good decisions for you.
2. Attribution system

  1. Sarah - **build** - a [waterfall attribution algorithm](https://sarahsnewsletter.substack.com/p/marketing-attribution-a-guided-map) will get you really far. Sure, things like MMM exist, but unless you reach huge scale, you won’t have the numbers to make the investment worth it. Run timed tests, fail fast, and iterate.
  2. Matt - **build**. I worked with my BI team to write the SQL logic that we still use. I talk about ways to measure top of funnel [here](https://hendersonmatthew.substack.com/p/what-weve-learned-spending-70-of) based on how we spend 70% of our budget on awareness efforts.


## Navigating tool decisions

Interestingly enough, we both did this exercise separately and we disagreed on very little.

- Everywhere we said “build” was a category where the vendor is selling you a schema, a UI, and a set of integrations on top of data you already own: audience data, attribution, dashboards, the content layer of your site. You’re more buying someone else’s opinion about how your data should be shaped and how to automate on top of it, but now you can set up that system yourself.
- Everywhere we said “buy” -  it was a category where the vendor does something hard and boring on your behalf: deliverability, compliance, uptime, a crawler fleet, integrations that break every time a partner ships an API change.

When evaluating vendors for future decisions or renewals, we put together a few practical questions you can leverage:

- If you cancel tomorrow, what breaks, who notices, and how long would it take to replace it in-house? If few would notice and you can build, there’s your answer.
- Is what you like the product, or the data you’ve put in it? If it’s your data, find out today what it costs to get back out.
- Could you get an API/MCP version of the product that would enable you to build LLM workflows rather than log into a walled UI? If so consider tradeoffs (think [dataforSEO](https://dataforseo.com/) vs. a SEO platform).

You won’t win or lose based on the tools you choose. You will, however, win or lose based on the speed at which you can implement strategies you write down. Tools help you make good decisions, but your *internal* tools help you implement those decisions.

If you’ve replaced something on this list with an internal tool, or tried and rolled it back, we’d love to hear about it. Drop a note in the comments.