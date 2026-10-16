# C. Leadership & Ownership (L3 = initiative, not titles)

> Answers are built from **your real stories** (03-story-bank/S01–S08), in STAR order, ~2 min spoken.
> - At L3, "leadership" = **noticing a gap nobody owned, acting, and bringing people along**. Never claim a title you didn't have.
> - **[Brackets]** = facts only you know. Practise from the **Anchors**, not the full text.
> - Say "a large academic publisher", never the client's name. Never mention terminations.
> - Some questions share a story from different angles. **In the real round, use each moment only once.**

---

### C1. Tell me about a time you showed leadership without being the formal lead.
**⭐ top question** · **Tests:** emergent leadership
**➡️ Use story:** S04

**Answer (from S04):**
"**[S]** On my current project, a GenAI system that automates copy-editing for a large academic publisher, our ML team of seven was split between the US and India. There was no ML-specific sync, just a general evening huddle, and people logged off right after. So findings stayed in silos: I'd discuss approaches with the onshore architect, and the offshore side often didn't know what had been tried.

**[T]** I was one of the most junior people on the team. Setting up process wasn't my job. But we were in the discovery phase, which is when we should be learning fastest, and we were losing time and repeating work.

**[A]** I did three things. First, I went to our offshore ML lead and proposed a **short daily ML sync** to share findings, approaches and blockers. I kept it small so it was an easy yes, and framed it around the team's goal, not my frustration. Second, I took on **bridging the two sides**: writing my observations and decisions into **shared docs** so context didn't depend on any one conversation. Third, before v1, when people still weren't aligned on the approach, I didn't escalate it as a complaint. I went to senior teammates one by one, walked them through how I saw the approach, and **asked them to connect directly** with the architects.

**[R]** The team agreed and the sync started [still running?]. Alignment got noticeably better [concrete effect?], and it's when the offshore team started noticing my work. Over time I ended up dividing tasks across our workstreams and presenting our progress to leadership and the client. What I learned about leadership without a title: **you don't need authority to fix a gap. You need to make it easy for people to say yes, and then step back so it doesn't depend on you.**"

**Anchors:** 7 MLEs, US/India → no ML sync, silos → junior, not my role → proposed short daily sync (easy yes) → shared docs → misaligned before v1: no complaint, 1:1s, connect people directly → adopted, noticed → make it easy to say yes, then step back
**Follow-ups:** "How did you convince the lead?" → framed around the team's goal, kept it small · "What if they'd said no?" → I'd have kept sharing via docs and asked again with evidence of the cost

**My answer:**

**Feedback:**

---

### C2. Tell me about a time you owned a project end-to-end.
**Tests:** ownership, execution
**➡️ Use story:** S01

**Answer (from S01, ownership angle):**
"**[S]** On my copy-editing automation project, everything depends on parsing the incoming manuscripts correctly. They arrive as Word files with no consistent structure, around 5,000 samples across many article types.

**[T]** A few weeks before our first release, the senior engineer who owned parsing went on leave for a month, and I took it over completely, from design to release.

**[A]** I treated it as fully mine. **Understand:** I went through samples across article types and catalogued the structural patterns. **Design:** I chose an LLM orchestrator that first classifies the manuscript and its sections, then routes each part to a focused extraction step, rather than a brittle rules-based parser or one huge LLM call. **Build and test:** I built it, split testing across samples with my intern, and when our testers found edge cases, I turned each one into a fix. **Hand-off:** I kept a running doc of patterns, decisions and open issues, so the senior could pick it up when he returned. I also took on the front-matter and body-matter rule application that sits on top of the parser. **After launch,** [how did you support it: monitoring, bug fixes, client feedback?].

**[R]** The parser became the foundation of v1 and is still in use. [Metric.] And when requirements later grew beyond what it could handle, I was the one who said so, which is part of ownership too. The lesson: **ownership doesn't end when the code merges.** It covers the documentation, the edge cases, and being honest about the limits."

**Anchors:** parsing = foundation → owner on leave → fully mine → understand (patterns) → design (classify → route) → build + test (intern, testers, edge cases) → hand-off doc → + front/body rules → [after launch] → v1 foundation → honest about limits → ownership ≠ merge

**My answer:**

**Feedback:**

---

### C3. Tell me about a time you convinced a team to adopt a new tool / technology / approach.
**Tests:** influence without authority
**➡️ Use story:** S02

**Answer (from S02):**
"**[S]** When my current project started, the plan was standard RAG, meaning vector search over chunks, to retrieve style-guide rules, plus an agent to apply them. The team was seven ML engineers, and I was the most junior full-timer.

**[T]** I believed standard vector search was a poor fit. The style guide has 2,000+ rules in a deep chapter-and-section structure, and similarity search tends to lose that structure. I wanted the team to consider **vectorless, reasoning-based RAG**, where you build a tree from the document's structure and the LLM navigates it like a table of contents. But I had no authority, and it wasn't in the plan.

**[A]** I didn't try to win the argument in a big meeting. I **shared the idea privately** with the senior architect first, to get an expert's reaction. When he was interested, I **built a proof of concept** on our real problem. Because the data is confidential, I [built the tree index myself / ran it locally]. I attached an agent that navigates the tree to fetch the right rules. Then I **demoed it to the team**, so they could see it working instead of hearing me describe it. And to keep it fair, I compared it with hybrid RAG while my intern explored graph RAG.

**[R]** The team responded really well. [Outcome: adopted? what did the comparison show?] What I learned about influence: **a working demo beats an argument, and you earn trust by testing your own idea against alternatives** instead of just selling it."

**Anchors:** plan = standard vector RAG → 2,000+ structured rules → similarity loses structure → no authority → private pitch to architect → PoC on real problem (confidential, so local) → demo → fair comparison (hybrid / graph) → [outcome] → demo > argument

**My answer:**

**Feedback:**

---

### C4. Tell me about a time you went beyond what was expected.
**Tests:** ownership, initiative
**➡️ Use story:** S03 angle (read the whole style guide) · backup: S04

**Answer (from S03, initiative angle):**
"**[S]** Early in my copy-editing automation project, we had to decide how to apply a publisher's style-guide rules to manuscripts. The style guide is huge, 2,000+ rules, and most people on the team were working from summaries and the sections relevant to them.

**[T]** Nobody expected anyone to read the whole thing. But a big design decision depended on what the rules were actually like: could they be written as deterministic scripts, or did they need an LLM?

**[A]** I **read the entire style guide end to end**, so I'd know the real shape of the rules, not just the examples. That showed me many rules depend on context and judgment. When a senior architect proposed a script-per-rule approach, I didn't just argue from what I'd read. I went further and, with my intern, **built deterministic functions for a section of the guide and tested them on real manuscripts**, so the team had evidence. I then presented the results, including where scripts worked well.

**[R]** That evidence settled the decision, and the team aligned on the agent approach. Knowing the guide that deeply also paid off later, when we rewrote the rules into a form an LLM could follow, and in client conversations, where we could speak to their own rules in detail. The lesson: **going beyond what's expected is most useful when it's aimed at the decision that matters most.**"

**Anchors:** 2,000+ rules → nobody expected a full read → the decision depended on it → read it end to end → many rules need context → went further: scripts for a section, tested on real manuscripts → presented fairly → settled the decision → paid off later (LLM-friendly rules, client conversations)

**My answer:**

**Feedback:**

---

### C5. Tell me about a time you mentored or taught someone.
**Tests:** making others better (team-first)
**➡️ Use story:** S06

**Answer (from S06). ⚠️ Fill the [brackets]; it's thin without them:**
"**[S]** During the discovery phase of my current project, an intern in India was paired with me, while I was still fairly junior myself.

**[T]** I wanted him to do meaningful work and grow, not just watch, while I kept my own work moving.

**[A]** I gave him **real pieces of the project, not busywork**: building deterministic functions for part of the style guide for our approach experiment, exploring graph RAG while I worked on vectorless and hybrid, and testing parser samples across manuscript types. [How you taught: e.g. 'I'd explain the *why* behind a task first, pair with him on the first part, then review his work and let him own the rest.'] When his work came up with the seniors, **I took responsibility for it and backed him up**, so he felt safe to try things. [One concrete moment: something he struggled with and how you helped.]

**[R]** He contributed directly to our approach experiment and the same-day client prototype. [His growth: something he could do by the end that he couldn't at the start.] It was also the point where I realized I could lead people, not just tasks. The lesson: **give people real ownership, explain the why, and cover for them while they learn.**"

**Anchors:** intern paired with me → real work (deterministic experiment, graph RAG, parser testing) → [how I taught] → backed him with seniors → [struggle + help] → contributed to experiment + prototype → [his growth] → real ownership + why + cover
**Don't say:** "bro code". Say "we built a lot of trust."

**My answer:**

**Feedback:**

---

### C6. Tell me about a time you took a risk / chose the harder path.
**Tests:** courage, betting on yourself
**➡️ Use story:** S02 (speaking up despite fear of being the junior)

**Answer (from S02, courage angle):**
"**[S]** When my current project started, I was the most junior full-timer on a team of seven ML engineers, and honestly, I barely spoke in calls. I was nervous about speaking up as a junior, and the easy path was to quietly build what the plan said, which was standard RAG.

**[T]** But I'd been learning about vectorless, reasoning-based RAG on my own, and I believed it fit our problem much better: a style guide with 2,000+ rules in a deep structure. Proposing it meant putting an unproven idea, and myself, in front of very senior people.

**[A]** I took the harder path, but in a way I could actually manage. I **messaged the senior architect privately** first. That was my first step past the fear. When he was interested, I spent [time] building a **proof of concept** on our real problem, working around the client's data confidentiality, and then **demoed it to the whole team**. The risk was real: if it had flopped, that would have been my first impression on the project.

**[R]** The team responded really well [outcome], and it changed my path on the project. I started proposing ideas openly, I set up our daily ML sync, and within a few months I was presenting our approach to delivery heads and the client. The lesson: **the safe path would have kept me invisible.** Betting on an idea I believed in, and backing it with a demo, was worth the discomfort."

**Anchors:** most junior, barely spoke → easy path = build the plan quietly → believed in vectorless → risk: unproven idea + first impression → private message first → PoC → demo to whole team → [outcome] → began speaking up → ML sync → demos to leadership + client → the safe path = invisible

**My answer:**

**Feedback:**

---

### C7. Tell me about a time you challenged the status quo.
**Tests:** courage, 10x thinking
**➡️ Use story:** S04 · backup: S02 (questioned the standard RAG plan) or S03

**Answer (from S03, challenging the default plan):**
"**[S]** Early on my copy-editing automation project, the default direction from one of our senior architects was deterministic: write a script for each style-guide rule and apply them programmatically. It's the conventional, safe approach. It's predictable and easy to test.

**[T]** I'd read the full style guide, 2,000+ rules, and I didn't believe scripts could handle the many rules that depend on context. As a junior, challenging a senior's default plan was uncomfortable, but if we were wrong, we'd find out months later after writing hundreds of scripts.

**[A]** I challenged it **with evidence, not opinion**. With my intern, I took a section of the guide, wrote a deterministic function for every rule in it, and ran them on real manuscripts. I tracked which rules worked and which couldn't be expressed as code, and how long each took to build. Then I presented the results, **including where scripts worked well**, so it was a fair test of the existing plan, not an attack on it.

**[R]** The data showed contextual rules couldn't be scripted and the approach wouldn't scale to 2,000+ rules. The team moved to an agent-based approach [and kept scripts for simple mechanical rules, if true]. The lesson: **the best way to challenge the status quo is to test it honestly.** Either you find out it's right, or you have the evidence to change it."

**Anchors:** default = deterministic scripts (safe, senior's plan) → read 2,000+ rules, doubted it → cost of being wrong = months later → challenged with evidence: scripts for a section on real manuscripts → tracked worked/failed + effort → fair presentation → moved to agent approach → test the status quo honestly
**Note:** B2, E3, E5 use this same moment. If S03 is used elsewhere in the round, switch C7 to S04 (no ML sync was the status quo).

**My answer:**

**Feedback:**

---

### C8. Tell me about a time you did the right thing even though it was hard or unpopular.
**Tests:** integrity, ethics

**Draft (from S08, honesty angle). ⚠️ Use only if it felt hard; a real integrity moment from you is stronger:**
"**[S]** After our v1 release, the client's requirements grew massively: 20+ style guides instead of one, books of 600 to 1,000 pages, and a user feedback loop. The timeline was tight, and the easiest thing would have been to stretch what we had.

**[T]** What we had included my manuscript parser. I'd built it, it was the foundation of v1, and I'd been recognized for it. But I was fairly sure it couldn't handle book-length documents or multiple style guides.

**[A]** The comfortable option was to stay quiet, patch it, and hope. Instead I **told the team plainly that my own parser wouldn't scale**, with my reasons [context limits, many-to-many], even though it meant admitting a limit in my own work, under deadline pressure, and pushing the team toward a new design nobody had built before. I then took ownership of two of the new components, so I wasn't just pointing out a problem.

**[R]** We moved to an agent-harness design early, instead of discovering the limits mid-delivery. [Status.] The lesson: **being honest about your own work early is cheaper than being right about it late.**"

**Anchors:** requirements grew + tight timeline → easy path = stretch what we had → my parser, my credit → **said plainly it won't scale** → reasons → took ownership of 2 new components → moved early, not mid-delivery → honest early > right late
**⚠️ Same moment as D9.** Use one or the other. **Better if you have one:** a time you refused a shortcut, flagged a quality or data risk nobody wanted to hear, or told a client or lead something unwelcome. Tell me if so.

**My answer:**

**Feedback:**

---

### C9. Tell me about a time you made someone feel included / supported a diverse team.
**Tests:** inclusion (past-story version of F9)

**Draft (from S04, inclusion angle). ⚠️ Confirm it matches how it felt on the team:**
"**[S]** On my current project, our team was split across the US and India. Most technical discussion happened between me and the onshore architect, often after the offshore team had logged off, so our offshore teammates were often **finding out about decisions late, without being part of them**.

**[T]** I was in a position to see both sides, and I felt the offshore team, including the people senior to me, deserved to be in the room when ideas were being shaped, not just handed the result.

**[A]** I proposed a **daily ML sync** [at a time that worked for the offshore team, verify], so findings were shared with everyone at once. I started writing decisions and observations into **shared docs**, so nobody's understanding depended on being in a particular conversation or time zone. And when I noticed people weren't aligned, I walked them through the approach one-on-one and **connected them directly with the architects**, so their views reached the people making decisions. [If true: I also made sure my intern's work was presented with his name on it.]

**[R]** The offshore team became much more involved in shaping the approach [example?], and alignment improved. The lesson: **inclusion is often about logistics**: who's in the meeting, what's written down, and whose time zone you pick."

**Anchors:** US/India split → decisions made after offshore logged off → offshore found out late → daily sync at their time → shared docs → 1:1s + connect directly with architects → [credit intern by name] → offshore more involved → inclusion = logistics
**⚠️** Thin if you only did it for alignment, not inclusion. If you have a moment of **including one specific person** (a quiet teammate, a new joiner, someone from a different background), that's stronger. Tell me.

**My answer:**

**Feedback:**

---

### C10. Tell me about a time you led a team through a difficult situation.
**⭐ top 5 question** · **Tests:** leadership under pressure, keeping the team together
**➡️ Use story:** S05. ⚠️ Say "I wasn't the formal lead, but I owned half the delivery". Don't overclaim

**Answer (from S05, framed honestly):**
"I wasn't the formal lead, but I owned about half of the delivery in a pretty difficult stretch.

**[S]** About [a month] before our first release on my copy-editing automation project, our team changed a lot within a few weeks. Architects rolled off, our interns finished, and my intern moved to another company. **We went from seven ML engineers to three**, and a lot of the solution was still a brute-force prototype.

**[T]** We had to deliver v1 anyway. I owned manuscript parsing plus the front-matter and body-matter rule application; my senior took back matter, reference validation and deployment; and a new architect joined to lead.

**[A]** My part in keeping it together: **I made my areas predictable**, so nobody had to worry about them. I turned every edge case our testers found into a parser fix quickly, instead of letting issues pile up. [Verify: because I'd been on the project from the start, **I brought the new architect up to speed** on the approaches we'd tried and why, so she wasn't starting from zero.] [If true: I also divided the remaining threads of work and kept a clear list of who owned what.] And I learned a lot by watching her lead: she was calm and never angry, even when things weren't going well, and she kept everyone aligned. I deliberately tried to work the same way.

**[R]** In about [a month] we delivered v1: parse the manuscript, apply the rules, output JSON, and render the suggested edits in the UI. The lesson: **in a crisis, being the person whose work others don't have to worry about is a form of leadership**, and calm is contagious."

**Anchors:** not formal lead, owned half → weeks before v1: 7 → 3, brute-force prototype → my scope: parsing + front/body rules → made my areas predictable → edge cases → fast fixes → brought the new architect up to speed → [divided threads] → learned calm from her → v1 delivered → predictable + calm = leadership
**⚠️ Never** mention terminations, "management issues", or that previous architects were weaker.

**My answer:**

**Feedback:**
