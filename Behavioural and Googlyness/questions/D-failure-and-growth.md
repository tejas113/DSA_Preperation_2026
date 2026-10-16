# D. Failure, Mistakes & Growth

> **Most important section for Googleyness.** "The most compelling candidates talk about a real failure clearly,
> without defensiveness, with genuine learnings." Formula: **own it → no excuses → what I did right after → what I changed permanently.**
> - Answers are built from **your real stories** (03-story-bank). **[Brackets]** = facts only you know.
> - D1, D2, D3, D7 are drafted **only from what you actually wrote**. ⚠️ Use them only if they're true; a *real* failure from you will beat them.
> - Practise from the **Anchors**, not the full text.

---

### D1. Tell me about a time you failed.
**⭐ top 5 question** · **Tests:** intellectual humility, growth mindset

**Draft A (from S04: you made yourself the bottleneck). ⚠️ Confirm the consequences in [brackets]:**
"**[S]** On my current project, our ML team was split between the US and India, and communication was weak. People logged off after the evening huddle, and findings stayed in silos.

**[T]** I stepped into the gap and became the bridge between the two sides. I was the one carrying context, relaying decisions and keeping both architects in sync.

**[A] (the failure)** The problem was that I did it by **making myself the single point of communication**. I worked late nights to overlap with both time zones, and a lot of context lived in my head and my chats rather than anywhere shared. I thought I was helping, but [honest consequence: e.g. 'decisions started waiting on me', 'when I was busy with parsing, the two sides drifted apart again', 'I was exhausted and my own work slowed down']. That's on me. I'd set up a system that only worked if I was always available, and it didn't scale.

**What I did to fix it:** I moved everything I knew into **shared docs**, proposed the **daily ML sync** so both sides heard things at the same time, and instead of relaying, I **asked senior teammates to talk directly** with the architects.

**[R]** Alignment actually got better once I stepped *out* of the middle, and I stopped needing late nights to keep things moving. The lasting change: **if something only works because I personally hold it together, it's broken**. Now I default to writing decisions down and connecting people directly. I learned a lot about this from our architect, who kept everything running calmly without anyone being a hero."

**Anchors:** comms gap US/India → I became the bridge → **failure: single point of communication, late nights, context in my head** → [consequence] → fix: shared docs + daily sync + connect people directly → better once I stepped out → "if it only works because of me, it's broken"

**Draft B (from S01/S08: you designed the parser only for the inputs you had). Use if Draft A doesn't feel right:**
"I built our manuscript parser for the documents we had then: journal articles and one style guide. I didn't stop to ask what the next version would need. When the client expanded to 600–1,000-page books and 20+ style guides, it couldn't handle the context, and we had to move to a different design. [Cost: rework? time?] I was the one who said it wouldn't scale, but honestly I should have asked those questions when I designed it. Now, before I design something, I ask 'what's the biggest input this will see in a year?'"

**⚠️ Strongest option: a real failure only you know.** Something where *you* were clearly at fault: a bug you shipped, a demo that broke, a wrong estimate, a wrong assumption about the data, an approach that wasted a week. Tell me it in rough words and I'll build it out.

**My answer:**

**Feedback:**

---

### D2. Tell me about a mistake you made that affected others.
**Tests:** accountability, transparency

**⚠️ Needs a real moment from you.** Your write-up doesn't contain one yet. Good places to look on your project:
- a parser change that broke something downstream for the rules-application or back-matter work?
- a wrong assumption about the manuscripts that the testers or your senior had to work around?
- something you told the client or team that turned out to be wrong?
- a task you gave your intern that was unclear, so he lost time?

**Skeleton:** what I did wrong → who it affected and how → **I told people quickly** (didn't hide it) → I fixed the impact → I changed something so it can't happen again.
*(Draft A of D1 can also work here if the "decisions waited on me" consequence is true.)*

**My answer:**

**Feedback:**

---

### D3. Tell me about a time you were wrong / changed your mind.
**Tests:** intellectual humility

**⚠️ Best candidate from your write-up: the new architect.** You wrote that she *"went into the detail as a real developer"* and that you'd *"found someone who can actually disagree on my approach."* That's exactly this question. Tell me **one specific time she challenged your approach and she was right**.

**Skeleton once you have it:**
"I was confident about [X: e.g. part of the parser design / how rules should be applied]. When [the architect] reviewed it, she pushed back on [specific point]. My first reaction was [honest]. But when I looked at [evidence / her test cases], she was right because [reason]. I changed [what], and [result]. Since then I [lasting habit: e.g. ask for a detailed review before I'm attached to a design]."

**Alternative (only if true):** if **vectorless RAG was NOT what the team finally used**, that's a great answer here: "I was convinced vectorless was the right retrieval approach. When we compared it with [X], [evidence] showed [X] was better for [reason], so I changed my mind and backed it."

**My answer:**

**Feedback:**

---

### D4. Tell me about a time you had to learn something new quickly.
**Tests:** GCA, learning ability
**➡️ Use story:** S02 (learned vectorless RAG on my own) or S01

**Answer (from S02 + S01: going from fine-tuning to production RAG/agents):**
"**[S]** Before my current project, I'd worked on only one project, focused on fine-tuning. I'd never built production RAG or agent systems, which was exactly what this new project needed: a system that reads manuscripts and applies a publisher's style-guide rules automatically.

**[T]** I had to get productive fast, and within weeks I was also handed manuscript parsing when the engineer who owned it went on leave.

**[A]** I learned by **building**, not just reading. Even before the project needed it, I'd been studying vectorless, reasoning-based RAG on my own, and I turned that into a **proof of concept** on the real problem within [timeframe], which taught me more than any tutorial. For parsing, I started from the **real data**: I went through samples across article types to understand the patterns before designing anything. And I learned a lot from people, asking the senior architect questions, getting his feedback on my approach, and later learning from our new architect's very detailed reviews.

**[R]** Within [a few months], I went from no production RAG experience to building the manuscript parser that our v1 release is built on, and now I own two components of our agent-based redesign. My learning approach since: **build a small real thing early, start from the data, and find the person who knows more than you.**"

**Anchors:** before: only fine-tuning → project needed RAG + agents → handed parsing too → learn by building: vectorless PoC → start from real data (samples, patterns) → learn from architects → [timeframe] → parser = v1 foundation → own 2 agent components → build small, data first, find the expert

**My answer:**

**Feedback:**

---

### D5. Tell me about a time you had to adapt to a big change.
**Tests:** adaptability
**➡️ Use story:** S08 (or S05)

**Answer (from S08):**
"**[S]** After we released v1 of our copy-editing automation system, the client's requirements changed dramatically. Instead of one style guide, they wanted to onboard 20+. Instead of articles, they wanted books of 600 to 1,000 pages. And they wanted a feedback loop, where a user can reject a suggested edit and the rule gets updated.

**[T]** It went from one style guide and many manuscripts to **many-to-many**, on a tight timeline. And the parser I'd built for v1, something I'd put months into, wasn't going to handle it.

**[A]** I adapted in three ways. First, **I let go of my own solution**: I told the team plainly that my parser wouldn't scale, instead of trying to stretch it. Second, I helped move us to an **agent-harness design**, where agents plan and act instead of following a fixed pipeline. That was new for the whole team, including me, so I had to learn it as we built. Third, to handle the uncertainty, we adopted **spec-driven development**: PRDs, then architecture, then stories, then code, with reviews at each stage. I took ownership of two of the five components: the **style-guide onboarding agent**, which turns each guide into chapter-wise skill files, and the **text-extraction harness**. And I carried over everything we'd learned in v1 about messy manuscripts.

**[R]** [Current status.] The lesson: **adapting isn't just accepting the change, it's being willing to drop your own work**, and carry forward the learnings rather than the code."

**Anchors:** v1 shipped → 20+ guides, 600–1,000-page books, feedback loop → many-to-many, tight timeline → let go of my parser → agent harness (new to everyone) → spec-driven (PRD → arch → stories → code) → own C1 + C2 → v1 learnings carried over → drop the code, keep the learnings

**My answer:**

**Feedback:**

---

### D6. Tell me about a project that didn't go as planned.
**Tests:** resilience, judgment
**➡️ Use story:** S05

**Answer (from S05):**
"**[S]** On my current project, the plan for our first release assumed a team of seven ML engineers across the US and India. About [a month] before v1, that plan fell apart. Within a few weeks, architects rolled off, our interns finished, and my intern moved to another company. **We were down to three.** We also still had a fairly brute-force prototype for applying the rules, so a lot was unproven.

**[T]** We still had to deliver v1. I owned manuscript parsing and the front-matter and body-matter rule application; my senior took back matter, reference validation and deployment.

**[A]** We re-planned around what three people could actually do. A new architect joined and brought in testers to check manuscripts rigorously, which surfaced many more patterns, and I turned each edge case into a fix in the parser. As a team, we rewrote the style-guide rules into a form an LLM could follow reliably, instead of patching the brute-force approach. [What *you* cut or deferred for v1.] Clear ownership between the three of us meant nobody was waiting on anyone.

**[R]** In about [a month] we delivered v1: parse the manuscript, apply the rules, output JSON, and show the suggested edits in the UI. **Looking back, one early signal we missed** was [honest: e.g. 'how much knowledge sat with individual people; when they left, it left with them']. Now I write things down as I go, so the project doesn't depend on any one person, including me."

**Anchors:** plan = 7 people → weeks before v1: 7 → 3 → brute-force prototype, a lot unproven → re-plan for 3 → testers → edge cases → parser fixes → rules rewritten LLM-friendly → [cut] → clear ownership → v1 delivered → missed signal: knowledge in people's heads → write things down
**⚠️ Never** mention terminations or management issues.

**My answer:**

**Feedback:**

---

### D7. Tell me about a goal you set and didn't achieve.
**Tests:** honesty, reflection

**⚠️ Needs a real one.** Possible sources (tell me which is true):
- **If vectorless RAG wasn't adopted:** "My goal was to get vectorless retrieval into the solution. It didn't make it because [reason]. What I learned: [e.g. I fell in love with the technique before proving it on the full problem / I should have measured X earlier]."
- **A personal or career goal**, e.g. a certification, a side project, a target you set for yourself that you missed.
- **A v1 scope goal** you personally committed to that got cut.

**Skeleton:** the goal and why it mattered to me → what I did → why it fell short (own your part) → what I learned → how I set goals differently now.

**My answer:**

**Feedback:**

---

### D8. Tell me about a time you were under a lot of pressure or stress. How did you handle it?
**Tests:** resilience, self-management
**➡️ Use story:** S05

**Answer (from S01 + S05):**
"**[S]** The most pressure I've felt was in the weeks before our first release on my current project. The engineer who owned manuscript parsing went on leave for a family emergency, and I took over parsing **on top of** the rule-application work I already owned. At the same time, the team shrank from seven ML engineers to three.

**[T]** I had to keep my areas on track for v1 without burning out, and honestly I was close to it. I'd been working late nights, partly to bridge the US and India time zones.

**[A]** A few things helped. First, **I broke it down**: I listed everything and put parsing first, because every downstream rule depended on it. Second, **I stopped holding everything in my head**: I moved my notes and decisions into shared docs, which reduced the load and meant others weren't waiting on me. Third, I **asked for help instead of quietly struggling**, from my intern, the testers and my senior. And I learned a lot from our new architect: she never got angry or rattled, even when things weren't going well. I actually asked her how she managed the work and her personal life, and I started following some of her habits: [e.g. protecting time off, fixed working hours, planning the day].

**[R]** We delivered v1, and I came out of it with a much more sustainable way of working. The lesson: **under pressure, structure and asking for help beat working longer hours.**"

**Anchors:** pre-v1: parsing handed to me + my rules work + team 7 → 3 → late nights, near burnout → break it down, parsing first → move it out of my head into docs → ask for help → learn from architect's calm + habits [which ones] → v1 delivered → structure > hours

**My answer:**

**Feedback:**

---

### D9. Tell me about a time you decided to stop or drop something you'd invested in.
**Tests:** humility, avoiding sunk-cost thinking
**➡️ Use story:** S08 (let go of my own parser)

**Answer (from S08):**
"**[S]** For our first release, I built the manuscript parser: an LLM orchestrator that classifies a manuscript and its sections and routes each part to focused extraction. It took a lot of effort over [months], and it became the foundation of v1. I was proud of it.

**[T]** After v1, the client's requirements expanded: 20+ style guides instead of one, and books of 600 to 1,000 pages instead of articles. I had to be honest about whether my parser could handle that.

**[A]** It couldn't. It wasn't designed for that much context, and stretching it would have meant patch after patch. So **I said that openly to the team**, even though it was my own work, rather than defending it. We moved to an agent-harness design instead. What I did keep was **everything I'd learned building it**: the structural patterns across manuscript types, the edge cases the testers found, how to make rules LLM-friendly. All of that went straight into the new components I now own, the text-extraction harness and the style-guide onboarding agent.

**[R]** [Current status.] It was genuinely hard to let go of something I'd built, but it was the right call. The lesson I took: **the value is in what you learned, not in the code.** And the earlier you say 'this won't scale', the cheaper the change is."

**Anchors:** built the v1 parser (months, proud) → requirements: 20+ guides, 600–1,000-page books → honest check → won't scale → **said so openly** → agent harness → kept the learnings (patterns, edge cases, LLM-friendly rules) → now in C1/C2 → value is in the learning, not the code
**Note:** D9 and D1-Draft-B use the same moment from different angles. **Use only one of them** in the real round.

**My answer:**

**Feedback:**
