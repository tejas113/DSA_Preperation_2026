# B. Teamwork & Conflict

> Answers are built from **your real stories** (03-story-bank/S01–S08), in STAR order, ~2 min spoken.
> - Conflict stories score highest when you **look at your own part first**, try to **understand the other side**, and the relationship ends up **better**.
> - Never make anyone the villain. No names, and never mention terminations or "management issues".
> - **[Brackets]** = facts only you know. Practise from the **Anchors**, not the full text.
> - Several answers share a story. **In the real round, use each moment only once.**

---

### B1. Tell me about a time you had a conflict with a teammate.
**⭐ top 5 question** · **Tests:** collaboration, maturity, humility
**➡️ Use story:** S03 if you have no peer-only conflict. ⚠️ Better: a real disagreement with a peer (tell me one)

**Answer (from S03, conflict angle):**
"**[S]** Early in my current project, a GenAI system that automates copy-editing for a large academic publisher, one of the architects on my team and I disagreed on the core approach. He wanted to apply the publisher's style-guide rules with deterministic scripts, one per rule. I believed many rules needed an LLM, because they depend on context. It wasn't heated, but it was a real disagreement about the foundation of the system, and we were both fairly convinced.

**[T]** I needed to resolve it in a way that was good for the project and didn't damage the relationship, especially since he was more senior than me.

**[A]** First I tried to **understand why he preferred scripts**, and his reasons were good: they're predictable, cheap and easy to test, which matters a lot when you're editing someone's manuscript. So instead of arguing that he was wrong, I suggested we **test his approach properly**. With my intern, I took a section of the style guide, wrote a deterministic function for each rule, and ran them on real manuscripts. When I shared the results, I made sure to **show where scripts worked well**, not just where they failed, so it didn't feel like I was trying to beat him.

**[R]** The results showed contextual rules couldn't be scripted, and the effort per rule wouldn't scale to 2,000+ rules, so the team moved to an agent approach. [If true: we kept scripts for simple mechanical rules, which came from his idea.] [How was the relationship after? e.g. 'He appreciated that we'd given his idea a fair test.'] What I learned is that **most disagreements are about what each person is optimizing for**. Once I understood he cared about predictability, I could address that directly instead of just pushing my view."

**Anchors:** architect: scripts / me: LLM → real disagreement, he's senior → understood his reasons (predictable, cheap, testable) → test his idea fairly → scripts for a section on real manuscripts → showed where scripts worked → contextual ✗, doesn't scale → agent approach → [relationship] → understand what each side optimizes for
**⚠️ B2 uses the same moment.** If you can, give me a **peer** conflict (similar level: code review, design choice, task split, working style) for B1, and keep S03 for B2.

**My answer:**

**Feedback:**

---

### B2. Tell me about a time you disagreed with your manager / a senior person.
**Tests:** courage + respect, influence upward
**➡️ Use story:** S03

**Answer (from S03, upward angle):**
"**[S]** At the start of my current project, a senior architect proposed that we apply a publisher's style-guide rules with deterministic scripts, one per rule. I was the junior on the team.

**[T]** I'd read the entire style guide, 2,000+ rules, and I genuinely believed scripts couldn't handle the many rules that depend on context. But I was disagreeing with someone far more experienced, about the core architecture. I needed to raise it in a way that was respectful and useful, not just 'I think you're wrong.'

**[A]** I didn't debate it in a meeting. I **proposed a test**: with my intern, I took a section of the guide, wrote a deterministic function for every rule, and ran them on real manuscripts. I tracked which rules worked, which couldn't be expressed as code, and how long each function took. When I presented it, I was careful to show **where his approach worked well too**. I also went in genuinely open to being wrong: if the data had supported scripts, we'd have gone with scripts.

**[R]** The data showed contextual rules couldn't be scripted, and the effort wouldn't scale, so the team moved to an LLM/agent approach. [His reaction?] The lesson: **when you disagree with someone more senior, don't argue. Run the experiment, and give their idea a genuinely fair test.** The data makes the case without making it personal."

**Anchors:** senior architect: scripts → I'm junior, read all 2,000+ rules → disagreed → respectful + useful → proposed a test → scripts for a section, real manuscripts → tracked worked / failed / effort → showed where his approach worked → open to being wrong → team moved to agent approach → experiment > argument
**Follow-ups:** "What if the data had supported him?" → "Then we'd have used scripts. The goal was the right approach, not me being right."

**My answer:**

**Feedback:**

---

### B3. Tell me about a time you worked with a difficult person.
**⭐ top question** · **Tests:** empathy, professionalism

**Draft (from S04/S05, "team not communicating" angle). ⚠️ Confirm it's accurate. Never label anyone "difficult" in the answer:**
"**[S]** Before our first release, our team wasn't communicating well. Some senior teammates weren't aligned with the approach the architects and I were taking, and discussions kept going in circles. It was frustrating, because we were short on time.

**[T]** As the junior, I could have raised it as a complaint. But I didn't think that would help: it would make people defensive, and it wouldn't actually fix the alignment.

**[A]** I tried to understand **why** they weren't aligned. Mostly it was that they hadn't been part of the earlier discussions, many of which happened across time zones after they'd logged off. So it wasn't really about attitude, it was missing context. I went to each of them **one-on-one**, walked them through how I saw the approach and why, and listened to their concerns. [One concern they raised?] Then I **asked them to connect directly** with the architects, so they could shape the decision instead of receiving it secondhand.

**[R]** Alignment improved [concrete effect?], and we delivered v1. The lesson: **when someone seems 'difficult', it's usually missing context or different pressures.** A one-on-one conversation fixes more than a complaint does."

**Anchors:** team not aligned before v1 → frustrating, short on time → could complain, didn't → understood why: missing context (time zones, not in early discussions) → 1:1s, explained + listened → connected them directly with architects → aligned → v1 → "difficult" = missing context
**Better if you have it:** one specific person whose working style clashed with yours (no name), what made it hard, and how you adapted.

**My answer:**

**Feedback:**

---

### B4. Tell me about a time you received critical feedback.
**Tests:** intellectual humility, coachability

**⚠️ Needs your specific moment.** Best source from your write-up: **the new architect**, who reviewed your approach "in very detail, as a real developer," and who you said could genuinely disagree with you.

**Skeleton once you tell me the moment:**
"**[S]** When a new architect joined my project before v1, she reviewed everything we'd built in a lot of detail, including my manuscript parser.
**[T]** She pointed out [specific criticism: e.g. edge cases I hadn't handled, how I was testing, a design weakness].
**[A]** Honestly, my first reaction was [honest: a bit defensive / surprised], because I'd put a lot into it. But when I looked at [her examples / the test cases], she was right. I [what you changed], and I asked her [how she approaches reviews / what she looks for], so I could catch it myself next time.
**[R]** [Result: e.g. the parser handled more manuscripts correctly / fewer issues in testing.] Since then, I [lasting habit: ask for a detailed review early, before I'm attached to a design]."

**Tell me:** what did she actually criticize, how did you feel, and what did you change?

**My answer:**

**Feedback:**

---

### B5. Tell me about a time you gave difficult feedback to someone.
**Tests:** courage, kindness, directness

**⚠️ Needs a real moment.** Possible sources on your project (tell me which happened):
- **Your intern:** did his work ever need significant correction? How did you tell him?
- **Senior teammates before v1:** when you walked them through the approach one-on-one, did you have to tell them something they were missing or doing that was hurting alignment?
- **The team or client:** did you ever tell them an approach or timeline wasn't going to work?

**Skeleton:** what the issue was → why it mattered → said it **privately**, about the work not the person, with a specific example → listened to their side → agreed on a next step → followed up → the result.

**My answer:**

**Feedback:**

---

### B6. Tell me about a time you helped a teammate who was struggling.
**Tests:** team-first, empathy
**➡️ Use story:** S06

**Answer (from S06). ⚠️ Fill the [brackets]; it needs one concrete struggle:**
"**[S]** During the discovery phase of my current project, an intern was paired with me. He was new to production GenAI work, and honestly, so was I to a large extent.

**[T]** [The struggle: e.g. 'He got stuck on ___ / felt nervous presenting to the seniors / his first attempt at ___ didn't work.']

**[A]** [How you noticed, without being told.] I [what you did: e.g. sat with him and walked through it, broke the task into smaller pieces, explained the *why*]. I didn't just do it for him. I [how you let him finish it himself]. And when his work came up with the seniors, I **took responsibility for it and backed him up**, so he felt safe to keep trying.

**[R]** [Outcome: e.g. 'he went on to own the graph-RAG exploration and contributed to our same-day client prototype.'] We built a lot of trust, and I learned that helping someone isn't about taking over, it's about **removing what's blocking them and letting them own the result.**"

**Anchors:** intern paired with me → [struggle] → [noticed how] → [helped how] → didn't take over → backed him with seniors → [outcome] → unblock, don't take over

**My answer:**

**Feedback:**

---

### B7. Tell me about a time you worked with people from a different team or background (cross-functional).
**Tests:** communication across contexts
**➡️ Use story:** S04 (onshore/offshore bridge)

**Answer (from S04 + S05 + S07):**
"**[S]** My current project has involved a lot of different groups: ML engineers split between the US and India, architects with different technical views, testers checking manuscript output, our company's delivery heads, and the client, a large academic publisher whose copy editors would actually use the system.

**[T]** As one of the people who'd been on the project since the start, I ended up connecting a lot of these groups, and each needed something different from me.

**[A]** I **adapted how I communicated** to each group:
- **The US and India teams:** I wrote decisions and findings into shared docs, and proposed a daily ML sync so both sides heard things at the same time.
- **The testers:** I treated the edge cases they found as the most valuable input for the parser, and turned them into fixes quickly, so they could see their work mattered.
- **The delivery heads and the client:** in demos, I explained our approach in terms of *their* problem, how the system finds and applies their style rules, rather than in ML terms. [One example of how you explained something.]

**[R]** The team became much better aligned, the testers' findings directly improved the parser, and the demos went well enough that both leadership and the client were impressed by how well we understood their process. The lesson: **the same information needs a different shape for each audience.**"

**Anchors:** many groups: US/India MLEs, architects, testers, delivery heads, client → I connected them → adapted per group: docs + sync / testers' edge cases → fast fixes / demos in their terms → aligned, better parser, impressed client → different shape per audience

**My answer:**

**Feedback:**

---

### B8. Small team or large team: which do you prefer?
**Tests:** self-awareness, flexibility

**Answer (personalized with your real experience):**
"I've actually experienced both on the same project. It started as a team of seven ML engineers across the US and India, and before our first release it became a team of three.

The bigger team gave us more perspectives, more people to learn from, and more parallel exploration. But coordination was harder; across time zones, a lot of my effort went into keeping people aligned. The small team moved much faster. Ownership was crystal clear, and decisions happened in minutes, but everyone had to cover more ground, and there was less room for error.

So I don't have a strong preference for size. What matters more to me is that ownership is clear, decisions get written down, and people help each other. [If you have a real lean: 'If I had to pick, early in my career I'd lean toward ___, because ___.'] Either way, I adapt: in a bigger team I communicate more deliberately, and in a smaller one I'm comfortable wearing more hats."

**Anchors:** same project: 7 → 3 → big: more perspectives, harder coordination (time zones) → small: fast, clear ownership, more ground each → size matters less than clear ownership + written decisions + helping each other → I adapt

**My answer:**

**Feedback:**

---

### B9. Describe your ideal manager / work environment.
**Tests:** fit, maturity

**Answer (personalized with your real experience):**
"The best example I've had is the architect who joined my project before our first release. She reviewed everything in real detail, she was willing to disagree with my approach, and she never got angry, even when the project wasn't going well. She kept everyone aligned calmly. That's what I'd want in a manager: **clear expectations, honest and detailed feedback, and calm under pressure**, plus giving me ownership of real problems while being reachable when I'm stuck.

For the environment, I do best where it's safe to ask questions and disagree, where decisions get written down, and where people review each other's work seriously.

And I think the relationship is two-way. I try to make my manager's job easy: I share progress before I'm asked, flag risks early, and come with a proposed solution, not just a problem. If something isn't working between us, I'd rather raise it directly than let it build up."

**Anchors:** real example: new architect (detailed reviews, disagreed with me, calm, never angry) → clear expectations + honest feedback + calm + ownership + reachable → safe to disagree, written decisions, serious reviews → two-way: progress early, risks early, come with solutions

**My answer:**

**Feedback:**

---

### B10. Tell me about a time you explained something technical to a non-technical person.
**Tests:** communication, empathy

**Draft (from your demos to delivery heads and the client). ⚠️ Fill the [brackets] with the real moment:**
"**[S]** On my copy-editing automation project, I regularly presented our approach to our company's delivery heads and to the client, a large academic publisher. They understand publishing deeply, but not how LLMs, RAG or agents work.

**[T]** In one demo, I needed them to understand [what: e.g. why we weren't using simple scripts for every rule / how the system finds the right style rule / why the system sometimes needs human feedback], because it affected [a decision, a timeline, their expectations].

**[A]** I **started from their world, not mine**. Instead of explaining embeddings or agents, I [your analogy: e.g. 'compared it to how a copy editor uses the style guide: you don't read all 2,000 rules every time, you go to the right chapter and section, and that's exactly what our system does']. I used **one of their own manuscripts** to show it step by step, kept the jargon out, and checked in with questions like 'does this match how your editors work?' [Anything you deliberately avoided saying?]

**[R]** [Outcome: e.g. 'they understood the trade-off and agreed to ___', or 'they asked much sharper questions afterward'.] The lesson: **explain it in the listener's language**. If they can explain it back to you, you've done it right."

**Anchors:** demos to delivery heads + client (publishing experts, not ML) → needed them to understand [X] → their world, not mine → [analogy] → their own manuscript, step by step → no jargon → checked in → [outcome] → listener's language
**Tell me:** one real thing you explained to them, and how you explained it.

**My answer:**

**Feedback:**

---

### B11. Tell me about a time you had to compromise.
**Tests:** collaboration, ego vs team goals

**Draft (only if true: deterministic scripts kept for simple rules after S03):**
"**[S]** On my copy-editing project, an architect and I disagreed: he wanted deterministic scripts for every style-guide rule; I believed the rules needed an LLM.
**[T]** After we tested it, the data showed scripts couldn't handle contextual rules. But they *did* work well for simple, mechanical rules.
**[A]** I could have pushed for 'LLM for everything', which was my original position. But his approach had real strengths for those simple rules: predictable, cheap and easy to test. So I suggested **a hybrid: deterministic checks for the mechanical rules, and the LLM agent for the contextual ones.** [Who agreed / how it was decided.]
**[R]** [Result: e.g. fewer LLM calls, more predictable output for simple rules.] The lesson: **compromise isn't splitting the difference; it's using each approach where it's genuinely strongest.**"

**Anchors:** scripts vs LLM → test: scripts fail on contextual, fine on mechanical → could push "LLM for everything" → hybrid: scripts for mechanical + agent for contextual → [result] → each approach where it's strongest
**⚠️ Only use this if the hybrid really happened.** Otherwise tell me another compromise: a scope cut for v1, a design you and the architect met halfway on, or a timeline you negotiated.

**My answer:**

**Feedback:**

---

### B12. Tell me about a time you said no to / pushed back on a request.
**Tests:** courage, judgment, respectful pushback
**➡️ Use story:** S03 (pushed back on the deterministic approach with data)

**Answer (from S08, "pushing back on stretching the existing solution"):**
"**[S]** After our v1 release, the client's needs grew a lot: 20+ style guides instead of one, books of 600 to 1,000 pages, and a user feedback loop. The timeline was tight, so there was natural pressure to extend what we already had, including the manuscript parser I'd built, rather than redesign.

**[T]** I didn't think stretching it would work. The parser wasn't designed for book-length context or many style guides, and patching it would have meant problems showing up mid-delivery.

**[A]** I **pushed back, with reasons rather than just a 'no'**: I explained the context limits, how the problem had become many-to-many, and what would likely break. And I **came with an alternative**, not just an objection: an agent-based design, with spec-driven development so we'd surface risks in documents and reviews before writing code. I also took ownership of two of the new components, so the pushback came with a commitment to do the work.

**[R]** The team moved to the agent-harness design early instead of discovering the limits later. [Status.] The lesson: **a good 'no' comes with reasons, an alternative, and an offer to help.**"

**Anchors:** post-v1: 20+ guides, 600–1,000-page books, feedback loop → pressure to stretch what we had (incl. my parser) → pushed back with reasons (context, many-to-many) → came with an alternative (agent harness + spec-driven) → took ownership of 2 components → moved early → good "no" = reasons + alternative + help
**Note:** uses the S08 moment (same as D9 and C8). Use only one of them in the round. Backup for B12 is S03.

**My answer:**

**Feedback:**

---

### B13. Tell me about a time you built trust with a new team or person.
**Tests:** team-first, relationship building
**➡️ Use story:** S05 (trust with the new architect)

**Answer (from S05, relationship angle). ⚠️ Verify the [brackets]:**
"**[S]** A few weeks before our first release, a new architect joined my project. The team had just shrunk from seven to three, and she was taking over a lot of work that had already been done, including approaches I'd driven, like the manuscript parser.

**[T]** For v1 to succeed, she needed to trust what we'd built quickly, and I needed to trust her judgment, even when she challenged my work.

**[A]** First, I made sure she had **full context**: [walked her through the approaches we'd tried and why we'd chosen them, and shared my docs]. Second, when she **reviewed my work in detail and disagreed** with parts of it, I didn't get defensive. I [example: took her feedback seriously and changed ___], because I genuinely felt I'd found someone who could challenge me properly. Third, I made my work **reliable**: when her testers found edge cases, I fixed them quickly, so she could count on my areas. And beyond the project, I'd sometimes go to meet her in the office to ask how she handled everything, including balancing work and personal life, and I took her advice seriously.

**[R]** We delivered v1 together, and she became someone I learn from constantly. [Verify: we're still working together on the agent-based redesign.] The lesson: **trust gets built by being transparent, taking feedback well, and being reliable**, more than by agreeing with someone."

**Anchors:** new architect joins before v1, team 7 → 3 → she inherits my work → full context (approaches + docs) → she challenged my work → no defensiveness, [changed X] → reliable: fast fixes on testers' edge cases → met her in office, took her advice → v1 together → still working together → transparent + take feedback + reliable

**My answer:**

**Feedback:**
