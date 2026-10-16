# F. Hypotheticals – "What would you do if…"

> **How to use this file (important)**
> - **Don't memorize the model answers.** Learn the **Key moves** (the skeleton), then say it in your own words.
>   If you recite these word for word, it will sound scripted, which is mistake #1.
> - Where you see **🔗 Real example hook**, drop in a quick real moment from your own work if you have one.
>   "I actually faced something similar…" turns a hypothetical into proof, and that's the strongest move.
> - Every answer follows Google's official criteria:
>   **Understand + root cause → options with pros/cons → take a stand → success metric → stay open.**
> - **People problems:** private conversation first, manager last. **User harm / security / privacy:** speed and escalation beat politeness.
> - Speaking time: aim for **~2 minutes**, then let them push back. The follow-ups are where you score.

> **Ranked by how often each question is reported in Google behavioral (Googleyness & Leadership) rounds.**
> Ranking is based on candidate reports and Google's published question lists, not official data. Treat it as a guide to priority, not a guarantee.

---

## 🔥 Tier 1 – Most frequently asked (prepare these first)

### F1. A teammate isn't pulling their weight, and it's affecting the deadline.
**Tests:** directness + empathy, accountability

**Model answer:**
"I'd separate two problems: the deadline, which is urgent, and the teammate, which needs care.

On the teammate, I wouldn't assume they're lazy. In my experience it's usually that they're blocked, the task was unclear, they're overloaded with something I can't see, or they're struggling and embarrassed to say so. So I'd talk to them privately, without accusing: 'How's the API piece going? Anything blocking you? I've got some bandwidth if it helps to pair.' That conversation usually tells you the root cause.

If they're blocked, I help unblock. If the task is bigger than estimated, we re-scope together. If they've just got too much on, that's a planning issue.

On the deadline, if it's still at risk after that conversation, I'd raise it with the lead, but framed as *project risk*, not a complaint about a person: 'The payments module is at risk for Friday. Here are the options: cut X, move someone over, or slip by two days.' That gives the lead what they need to decide without throwing anyone under the bus.

Success is the deadline met or consciously renegotiated, and the teammate not feeling ambushed."

**Key moves:** split deadline vs person → don't assume → private, curious conversation → offer help → escalate *the risk*, not the person, with options
**Likely follow-up:** *"What if it keeps happening after you've talked?"* → Then it's a pattern and the manager needs to know. Be factual, specific, and tell the teammate you're doing it.

**My answer:**

**Feedback:**

---

### F2. Your manager asks you to ship by Friday, but you've found a bug that could affect users.
**Tests:** user focus, integrity, judgment

**Model answer:**
"The first thing I need to know is how bad the bug is, because that changes everything. A cosmetic glitch is very different from data loss, a security hole, or users getting charged wrong. I'd quickly figure out: how many users hit it, how severe, and is there a workaround?

Then I'd go to my manager immediately, not on Thursday night, with the facts and options, not just a problem:
- **Option 1:** fix it and ship Friday, if the fix is small and safe.
- **Option 2:** ship on Friday with the affected feature behind a flag or turned off.
- **Option 3:** ship with a known-issue note and a fast follow-up, which is fine only if the impact is minor.
- **Option 4:** slip by a day or two.

For minor issues, I'd recommend what I think is best, but it's genuinely my manager's call. There might be business context I don't have, like a partner launch tied to that date.

But if it's something that harms users, like corrupting data, a privacy leak, or wrong charges, I'd push back firmly. Shipping something we *know* hurts users breaks trust, and that's much more expensive than a delay. I'd say that clearly and respectfully, and if needed suggest we bring in the tech lead.

Success: we ship something users can trust, and my manager never gets surprised."

**Key moves:** assess severity first → tell manager early → bring options, not just a problem → minor means their call, serious user harm means firm pushback → no surprises
**Likely follow-up:** *"Manager still says ship it, and it's serious."* → Escalate respectfully (tech lead, or the launch/quality process), document the risk; don't silently comply on real user harm.

**My answer:**

**Feedback:**

---

### F3. The team made a decision you disagreed with. What do you do?
**Tests:** disagree and commit

**Model answer:**
"It depends on timing. *Before* the decision is final, I'd make sure I voiced my concern once, clearly, with my reasoning and ideally data. Not just 'I don't like it' but 'I'm worried this approach won't handle X, here's why.' I'd also genuinely listen, because often the disagreement is because they know something I don't.

*Once it's decided*, I commit fully. I'd build it as well as if it were my own idea. No dragging my feet, no 'I told you so' later. A team that relitigates every decision can't move.

There are two exceptions. If new information comes up that materially changes the picture, like we discover the load is 10x what we assumed, I'd raise it again, with that data, constructively. And if it's an ethical issue or something that would genuinely harm users, that's not a 'disagree and commit' situation, and I'd escalate.

One thing I'd do while committing is suggest a checkpoint: 'Let's watch latency for the first two weeks.' That way if my concern was right, we catch it early, and if I was wrong, I learn something."

**Key moves:** voice it once, clearly, with reasoning, *before* → listen → once decided, commit 100% → reopen only with new data → ethics/user harm is the exception → propose a checkpoint metric
**🔗 Real example hook:** a decision you disagreed with but committed to

**My answer:**

**Feedback:**

---

### F4. You're given a project with a vague goal and no clear owner. What do you do?
**Tests:** ambiguity, bias to action

**Model answer:**
"I'd treat the ambiguity as part of the job, not a blocker.

Step one is understanding the *real* problem. I'd talk to whoever raised it and the likely users or stakeholders: what pain are we solving, how will we know it's solved, what's the deadline pressure? Often 'improve X' means something very specific to one person.

Step two, I'd write it down: a one-page doc with the problem, my assumptions, what's in scope and out, open questions, and a proposed first milestone. Then I'd send it to the stakeholders and ask them to poke holes. Writing it down forces clarity and turns vague into concrete very fast.

On ownership, if nobody owns it, I'd offer to drive it, but I'd confirm that with my manager so it's explicit, not assumed.

Then I'd start with something small and reversible, like a prototype or the smallest useful slice, rather than waiting for perfect clarity. Real feedback on a working thing clears up ambiguity far faster than more meetings.

Success would be agreed criteria in that doc, met, plus stakeholders saying 'yes, that's what we needed.'"

**Key moves:** ambiguity is the job → talk to stakeholders, find the real pain → one-page doc with assumptions → make ownership explicit → small reversible first slice → agreed success criteria
**🔗 Real example hook:** a vague task on your project you turned into a concrete plan

**My answer:**

**Feedback:**

---

### F5. Two senior engineers disagree on the design and you're caught in the middle.
**Tests:** navigating conflict, humility

**Model answer:**
"As the junior person, my job isn't to pick the winner. It's to help the disagreement become productive.

Usually when two smart people disagree on design, they're optimizing for different things: one cares about speed of delivery, the other about long-term scale, for example. So I'd try to surface that. I'd offer to write a short doc that lays out both approaches side by side: the requirements, the tradeoffs, the risks, and the open questions. Writing it down depersonalizes it. It stops being 'Alice vs Bob' and becomes 'option A vs option B against these requirements.'

If there's a factual question underneath, like 'Will this handle 10x traffic?', I'd suggest a quick spike or benchmark to answer it with data instead of opinion. I could volunteer to build it, which is a great way for me to learn too.

If they still disagree after that, someone needs to make the call, usually the tech lead or the owner of that system, and I'd help get it in front of them. Once it's decided, I'd commit fully to whichever way it goes.

What I wouldn't do is quietly side with whoever's more senior, or stall my own work waiting. Where I can, I'd build the parts that are the same in both designs."

**Key moves:** don't pick a side → surface what each is optimizing for → write it down side by side → settle facts with a spike → owner decides → commit → keep building the common parts
**🔗 Real example hook:** a design review where you wrote up options or ran a benchmark

**My answer:**

**Feedback:**

---

### F6. A teammate seems to be isolating themselves from the group. What do you do?
**Tests:** empathy, inclusion, team-first

**Model answer:**
"The first thing I'd want to figure out is whether this is a *change* or just their style. Some people are naturally quieter, and that's not a problem to fix. But if someone who used to be engaged has gone quiet, that's a signal.

The root cause could be a lot of things: overloaded and heads-down, feeling excluded, a bad experience in a code review, or something personal. I wouldn't guess. I'd reach out one-on-one, informally, like a coffee or a quick chat, and just ask how things are going. Often it's easier to start with work: 'Hey, I'm stuck on X and I know you've worked on it, could I get your take?' That gives them a reason to re-engage and signals their input is valued.

If it's about the team, say they feel talked over in meetings, that's something I can directly help with, by bringing them into discussions or crediting their ideas. If it's workload or something bigger like burnout, I'd encourage them to talk to our manager, and offer to come with them if that helps. I wouldn't go to the manager behind their back unless it seemed serious.

I'd know it's working if they're participating in discussions again and reaching out for help on their own."

**Key moves:** change vs style → don't assume the cause → private, informal, work-based reach-out → fix what *I* control → manager only with their buy-in or if serious
**🔗 Real example hook:** a time you brought a quiet teammate into a discussion
**Likely follow-up:** *"What if they tell you it's none of your business?"* → Respect it, don't push, stay friendly and available; keep including them in normal work.

**My answer:**

**Feedback:**

---

### F7. You realize you'll miss a deadline you committed to.
**Tests:** transparency, ownership

**Model answer:**
"I'd tell people as soon as I know. Bad news early is cheap; bad news on deadline day is really expensive, because nobody can adjust anymore.

Before I raise it, I'd take a little time to understand *why* I'm late, so I can give a credible new estimate. Was it an underestimate, an unexpected dependency, scope creep? Then I'd go to my lead with three things: where I am, the honest reason, and options:
- cut scope and ship the core part on time,
- get help on a specific piece,
- or move the date, with a realistic new estimate.

I'd recommend one, but recognize the lead may have context on what matters more.

I'd also own it. Even if a dependency slipped, I should have flagged the risk earlier.

Afterward, I'd reflect on what went wrong in my estimate. Personally, I've learned to build in time for unknowns and to give status updates before I'm asked, so slippage shows up early."

**Key moves:** tell immediately → understand why → status + reason + options (cut scope / get help / move date) → recommend one → own it → fix my estimation habits
**🔗 Real example hook:** a real time you flagged a slip early (strong if you have one)

**My answer:**

**Feedback:**

---

### F8. You're new on a team and notice a process that seems inefficient.
**Tests:** humility + bias to action

**Model answer:**
"My first assumption would be that the process exists for a reason I don't understand yet. Being new means I'm missing context. Maybe there was an outage two years ago that created this step.

So I'd start by asking questions, not making suggestions: 'Can you help me understand why we do the manual sign-off? What problem does it solve?' Framing it as curiosity, not criticism, matters a lot when you're new.

If the reason still applies, I've learned something. If it turns out the reason no longer applies, or there's a cheaper way to get the same safety, then I'd propose a small, concrete improvement, ideally with a number attached: 'This takes each of us about 30 minutes per release; here's a script that does the same check.' And I'd offer to do the work myself, so I'm not just handing the team more tasks.

I'd start small and reversible, maybe try it for a couple of releases, and measure whether it saved time without losing what the original process protected.

Being new is actually a good position for this. Fresh eyes notice things people have gotten used to. The trick is to combine that with humility."

**Key moves:** assume there's a reason → ask, don't criticize → understand what it protects → small, measurable proposal → I do the work → trial it, measure it
**🔗 Real example hook:** something you improved in your first months on your project

**My answer:**

**Feedback:**

---

## ⭐ Tier 2 – Commonly asked

### F9. How would you make sure your team is inclusive / everyone's voice is heard?
**Tests:** inclusion, team-first

**Model answer:**
"For me inclusion is mostly about small, concrete habits, not big statements. A few things I'd actually do:

- **Async before sync:** share design docs before meetings so people who think better in writing, or who are less comfortable jumping into a fast debate, can contribute. Some of the best feedback comes in doc comments.
- **Notice who's not talking**, and ask them directly: 'Priya, you worked on the old version, what do you think?' It's a small thing but it changes who participates.
- **Watch for interruptions:** if someone gets cut off, 'Sorry, I think Sam was still making a point.'
- **Credit people by name**, especially in front of leadership.
- **Be mindful of logistics:** meeting times across time zones, not making decisions in hallway conversations that remote people miss.

And as someone who's been new on a team myself, I know how much it helps when someone actively includes you early, so I'd try to do that for new people.

How would I know it's working? If participation is spread out in meetings and reviews, not just the same two voices, and if people feel comfortable disagreeing openly."

**Key moves:** concrete habits, not slogans → async docs → invite quiet voices → stop interruptions → credit by name → logistics/time zones → measure by who participates
**🔗 Real example hook:** how someone included you when you were new, or how you included someone

**My answer:**

**Feedback:**

---

### F10. How would you convince a team working against a deadline to take on an urgent new request?
**Tests:** empathy, influence

**Model answer:**
"First I'd want to genuinely understand their situation. They're under pressure already, and coming in with 'this is urgent, drop everything' won't work and isn't fair.

So I'd start by being clear on *why* the request matters: the actual impact. Is it a customer outage, a revenue risk, a commitment to a partner? 'It's urgent' isn't a reason. I'd also check whether it really needs *their* team, and whether there's a smaller version that solves the core need.

Then I'd go to their lead, not individual engineers, and make it a shared tradeoff decision: 'Here's the impact of not doing this. I know you're focused on the Friday launch. What would it take? Could we do a smaller version? What would slip?' I'd offer whatever I can to reduce their load: I could do part of the work myself, write the spec, or handle the testing.

If it's truly a priority conflict between two important things, the right answer is to escalate together to whoever owns both priorities, not to pressure the team.

Success is the urgent need getting addressed in a way the team agreed to, without burning trust."

**Key moves:** empathy first → clear on the real impact (not just "urgent") → smallest version → go through their lead → frame as shared tradeoff → offer to take load → real conflict means escalate together

**My answer:**

**Feedback:**

---

### F11. You're already at full capacity and your manager asks you to take on more. What do you do?
**Tests:** honest communication, prioritization

**Model answer:**
"I wouldn't just say yes and quietly let quality drop, and I wouldn't just say no. Either way my manager makes a decision without the full picture.

I'd say something like: 'I'd like to help with this. Right now I'm on A, B, and C. If I take this on, something has to move. Which of these matters most?' I'd lay out what's on my plate, the rough effort, and the tradeoff, and let them decide on priorities, since they have the broader context.

I'd also think about options: maybe I can do a smaller part of it, hand off something I'm doing that someone else could pick up, or start it after a specific milestone.

If it's a short-term crunch, like a launch week, I'm happy to stretch for a bit. That's part of being on a team. But if it's becoming the norm, I'd raise it honestly, because sustained overload leads to mistakes and burnout, which isn't good for the team either.

Success: a clear, shared priority list, and nothing dropped by surprise."

**Key moves:** no silent yes, no flat no → show my plate + tradeoff → "which matters most?" → offer options (smaller part / hand off / later) → short crunch is fine, chronic overload gets raised honestly

**My answer:**

**Feedback:**

---

### F12. Two leads give you conflicting instructions. What do you do?
**Tests:** communication, handling ambiguity

**Model answer:**
"I wouldn't just pick one and quietly ignore the other. That leaves someone surprised later, and it puts me in the middle of something I shouldn't be deciding alone.

First, I'd make sure it's a real conflict and not a misunderstanding. Sometimes both can be done, or one lead has context the other doesn't. I'd clarify with each: what's the goal behind this, and what's the deadline?

If it's a genuine conflict, I'd get them talking to each other, ideally in one message or a short meeting: 'Lead A asked for X by Wednesday, Lead B asked for Y by Wednesday, and I can only do one well. Here's what I think the tradeoff is. Can you two align on the priority?' I'd make it transparent and neutral. I'm surfacing a conflict, not complaining.

If they can't agree, it goes to whoever sets priorities for both, usually my manager.

Meanwhile I wouldn't sit idle. I'd work on whatever's common to both or clearly unblocked.

Success is a clear, agreed priority that both leads know about, with no surprises."

**Key moves:** don't silently pick → real conflict or misunderstanding? → understand each goal → put both in one conversation, transparently → manager breaks ties → keep working on common parts

**My answer:**

**Feedback:**

---

### F13. A coworker presents your work as their own in a meeting.
**Tests:** maturity, confidence without drama

**Model answer:**
"In the moment, I wouldn't confront them in front of everyone. It puts people on the defensive and makes the meeting about us instead of the work. If it felt natural, I might add some detail like 'Yeah, when I was building that part, one thing we noticed was…', which makes my involvement clear without calling anyone out.

Afterward, I'd talk to them privately and assume good intent first. Often it's just sloppy phrasing: 'we did' becomes 'I did' when you're nervous presenting. So something like: 'Hey, in the review it sounded like you built the caching layer. I want to make sure people know who to come to with questions. Can we be clear about who did what next time?'

Their reaction tells me a lot. If it was an oversight, it's fixed. If it becomes a pattern, I'd raise it with my manager, framed around visibility and ownership, not grievance.

Longer term, the real fix is making my work visible by default: clear PR descriptions, design docs with my name, short updates in standup. Then credit doesn't depend on who's presenting.

And honestly, I'd try to keep perspective. The team shipping something good matters more than any one meeting."

**Key moves:** no public confrontation → subtle in-the-moment detail → private talk, assume good intent → pattern means manager → make work visible by default → keep perspective
**Likely follow-up:** *"What if your manager was in the meeting and now thinks they did it?"* → Mention it naturally in my next 1:1 as part of a work update, not a complaint.

**My answer:**

**Feedback:**

---

### F14. A feature you launched is getting negative user feedback. What do you do?
**Tests:** user focus, ownership, humility

**Model answer:**
"First, I'd take it seriously and not get defensive. It's my feature, so I own the outcome, not just the launch.

Then I'd try to understand the feedback properly. Is it a bug, a performance issue, or a design problem? How many users? Is it loud feedback from a few people, or a real trend? I'd read the actual comments, look at metrics like usage, drop-off, and error rates, and if possible talk to a few affected users.

Next, triage by severity. If it's actually broken or harmful, a rollback or a feature flag to turn it off buys time. If it's usability, I'd work with the PM and designer on a quick iteration.

I'd also be careful not to overreact. Sometimes people dislike change at first and adoption improves after a couple of weeks, which is why the data matters alongside the comments.

I'd keep stakeholders updated, and close the loop with users: 'We heard you, here's what we changed.'

And then a retrospective. What did we miss before launch? Maybe we needed a smaller rollout or more user testing. That's the lesson I'd carry into the next launch.

Success: the metrics and sentiment recover, and our launch process gets better."

**Key moves:** own it, no defensiveness → understand (bug? perf? design? how many?) → comments + metrics + talk to users → severe means rollback/flag; usability means iterate with PM/design → don't overreact to change aversion → close the loop → retro on launch process

**My answer:**

**Feedback:**

---

### F15. Your users ask for feature A, but data suggests feature B would help them more.
**Tests:** user focus, data-driven thinking

**Model answer:**
"I'd start by recognizing that users are usually right about their *problem* but not always about the *solution*. So the key question is: what's the need behind the request for A?

I'd dig into both sides. On the request side, talk to some of the users asking for A. What are they trying to do, and what's painful today? On the data side, I'd sanity-check what the data actually says and its limits. Is it measuring the right thing? Could it be missing a segment of users?

Often you find A and B are two answers to the same underlying problem. Then the question becomes which solves it better.

If the data is strong, I'd share it with the PM and stakeholders and propose testing B, maybe a small experiment or prototype with real users, rather than just overriding what users asked for. If B wins, we've helped users more. If A wins, the data was missing something and we learned that.

And I'd close the loop with users either way, so they don't feel ignored.

Success is the underlying user problem actually getting solved, measured by usage, task completion, or fewer complaints."

**Key moves:** users know their problem, not always the solution → find the need behind A → question the data's limits → share with PM → small experiment → close the loop with users → measure the underlying problem

**My answer:**

**Feedback:**

---

### F16. You join a team whose codebase is messy with almost no tests. What do you do?
**Tests:** humility, pragmatism, bias to action

**Model answer:**
"My first instinct might be 'this needs a rewrite,' and I'd be suspicious of that instinct. The code probably got this way for real reasons, like deadline pressure or changing requirements, and a rewrite is risky and rarely gets prioritized.

So first, I'd understand: talk to the team about the history, which parts break most often, and which parts change most. Not all mess is equally costly. A messy module nobody touches is fine; a messy module that changes weekly and causes incidents is the real problem.

Then I'd improve it incrementally, using the 'leave it better than you found it' approach. Whenever I touch a piece of code, I add tests around it first, then clean up. That way the improvement rides along with feature work instead of competing with it.

For the highest-risk areas, I'd propose a focused effort to the team with a clear justification, like 'This module caused 4 incidents last quarter, I'd like to spend a few days adding tests', so it's a tradeoff the team agrees on.

I'd also try to stop new mess: suggest tests as a review norm and maybe a CI check for coverage on new code.

Success: fewer incidents and faster, more confident changes in the areas that matter."

**Key moves:** distrust the rewrite instinct → learn the history → prioritize by risk × change frequency → tests first whenever I touch code → justified focused effort → stop new mess (review norms, CI) → measure incidents and change speed

**My answer:**

**Feedback:**

---

## 📌 Tier 3 – Less common, but still possible

### F17. The only teammate who knows a critical system leaves mid-project. What do you do?
**Tests:** ambiguity, ownership

**Model answer:**
"If there's still time before they leave, the most valuable thing is knowledge transfer, and I'd volunteer to be the person who absorbs it. I'd set up a few focused sessions, record them if possible, and write things down as we go: architecture, how to deploy, the weird failure modes, the 'don't touch this' areas. The most valuable knowledge is usually what's *not* in the code: why things were built the way they were.

If they've already left, I'd start by mapping what we know and don't know: read the code, docs, commit history, past incident reports, and talk to anyone who's worked adjacent to the system. Most people who leave are also happy to answer a few quick questions.

I'd tell my lead honestly about the risk: 'We now have a knowledge gap on X. Here's what I think it means for the timeline.' It might slip a bit while we ramp up, and they need to know.

Longer term, I'd fix the root cause, which is a single point of failure. Write the docs and runbooks as I learn, and make sure at least two people understand the system, so this doesn't happen again.

Success: the project continues with a realistic adjusted plan, and the system is no longer a one-person risk."

**Key moves:** before they leave: volunteer for structured knowledge transfer, capture the *why* → after: code/docs/history/neighbours/quick questions → tell lead the timeline risk honestly → fix the root cause: docs, runbooks, at least two people

**➡️ Use story:** 🔗 real example hook: S01 (the senior MLE went on leave and I took over parsing)
**My answer:**

**Feedback:**

---

### F18. Your project needs a skill nobody on the team has (including you). What do you do?
**Tests:** learning, resourcefulness

**Model answer:**
"I'd see it as a chance to learn something, but in a structured way, because the project can't wait for me to become an expert.

First, I'd figure out exactly how deep we need to go. Often we need maybe 20% of the skill to do 80% of the work. Then I'd look for help before reinventing anything: is there another team at the company who knows this, internal docs, an existing library, a past project that did something similar? At a company the size of Google, someone has almost certainly solved a version of this. Reaching out to them is often the fastest path.

In parallel, I'd learn by doing: official docs, then a small throwaway prototype to hit the real problems early, rather than weeks of reading.

I'd be honest with my lead about the risk to the timeline, and suggest we have an expert review our approach before we commit to it, so we don't build on a wrong foundation.

And I'd document what I learn, so the next person on the team doesn't start from zero.

Success is the project moving forward with a sound approach, and the team now having that skill."

**Key moves:** how deep do we need? → find existing experts/docs/libraries first → learn by building a small prototype → be honest about timeline risk → expert review before committing → document for the team
**🔗 Real example hook:** a technology you had to pick up quickly on your project (also feeds slot 9)

**My answer:**

**Feedback:**

---

### F19. You notice a teammate's code has a security / privacy issue that's already in production.
**Tests:** integrity, user trust, kindness

**Model answer:**
"This one is urgent because real users are exposed right now, so speed matters more than the social awkwardness.

First I'd quickly confirm it's real and gauge the severity. Is user data actually exposed, is it exploitable, how many users? I'd spend minutes on this, not days.

Then I'd tell the teammate directly and immediately, without blame: 'Hey, I think I found an issue in the auth change, can we look at it together right now?' Everyone ships bugs, and the goal is fixing it, not who caused it.

If it's serious, like actual data exposure, I'd make sure it goes through the proper security or incident process right away, even if the teammate would rather quietly patch it. That process exists because there may be obligations we don't know about, like notifying users. I'd loop in the tech lead or on-call. Hiding a security issue to protect someone's feelings would be the wrong call.

Then I'd help fix it, and afterward push for a blameless postmortem focused on *why our system let it through*: missing test, review checklist gap, no static analysis. That way it can't happen again for anyone.

Success: users protected fast, a systemic fix in place, and the teammate feels supported, not shamed."

**Key moves:** urgency first, users exposed → verify fast → tell teammate directly, no blame → serious means proper security/incident process, no quiet patching → help fix → blameless postmortem and systemic fix

**My answer:**

**Feedback:**

---

### F20. Someone on your team makes an offhand comment that excludes or offends a colleague.
**Tests:** inclusion, courage

**Model answer:**
"I wouldn't let it pass. Silence signals that it's acceptable, both to the person who said it and to the person it hurt.

How I respond depends on the severity. For something offhand and probably unintentional, I'd redirect lightly in the moment, like 'Hmm, not sure that's fair' or just steering the conversation back, and then talk to the person privately afterward. Most people don't mean harm, and a private, non-accusatory conversation lets them actually hear it: 'I don't think you meant it this way, but that comment about X could land badly, especially for Y.'

I'd also check in with the colleague who was affected, privately. Not to make it a big deal, but so they know someone noticed and has their back. I'd ask what, if anything, they'd want me to do, because it's their experience.

If it's serious, like clearly discriminatory, or it's a pattern, I'd escalate to the manager or HR. That's not something a peer conversation should handle alone.

The goal is a team where everyone feels safe to show up and contribute. That directly affects how well we work."

**Key moves:** don't stay silent → light redirect in the moment → private conversation, assume no intent → check in with the affected person, respect their wishes → serious or a pattern means manager/HR

**My answer:**

**Feedback:**

---

### F21. You're asked to use user data in a way you think users wouldn't expect or agree to. What do you do?
**Tests:** integrity, user trust, privacy

**Model answer:**
"This is a line I take seriously. User trust is the foundation of a company like Google, and it's very hard to win back once it's lost.

First, I'd make sure I understand the request correctly. Maybe there's consent I don't know about, or the data is anonymized and aggregated. I'd ask: 'Did users agree to this use? Has this been through privacy review?'

If my concern still stands, I'd raise it clearly with whoever asked, focusing on the user: 'If users found out we were doing this, would they be surprised or upset? If yes, that's a problem, even if it's technically allowed.'

I'd also suggest alternatives that achieve the goal more respectfully: using aggregated or anonymized data, asking for explicit opt-in, or collecting less data.

And I'd make sure it goes through the proper privacy review process. That's exactly what it's for. If I was still asked to proceed without that, I wouldn't. I'd escalate, because building it would make me complicit.

I'd frame all of this as protecting the product, not blocking the team."

**Key moves:** trust is the foundation → clarify (consent? anonymized? reviewed?) → "would users be surprised?" test → offer alternatives (aggregate, opt-in, less data) → privacy review → won't build it without review; escalate

**My answer:**

**Feedback:**

---

### F22. A launch would help most users but makes the product unusable for some (e.g. accessibility). What do you do?
**Tests:** inclusion, user focus, courage

**Model answer:**
"I don't think 'it works for most users' is a good enough answer when the product becomes *unusable* for a group of people, especially for accessibility, where those users often don't have an alternative. Google's mission is about making information universally accessible, and 'universally' matters.

First, I'd quantify and understand it: who exactly is affected, how badly, can they still complete the core task some other way? Is it a fix that takes two days or two months?

Then I'd raise it clearly with the team and PM, with options:
- delay a short time to fix it, if the fix is small,
- launch to everyone but keep the old experience available for the affected users until the fix lands,
- launch with a committed, scheduled fix, which is acceptable only if there's a real workaround in the meantime.

What I'd push back on is launching and leaving it as a 'later' item with no date, because those usually never happen.

I'd also suggest we prevent this next time: accessibility checks in the design review and in testing, so we catch it before it's a launch tradeoff.

Success: nobody locked out, and accessibility becomes part of our launch checklist."

**Key moves:** "most users" isn't enough when someone's locked out → understand who/how badly/workaround → options (short delay / keep old path / committed fix with workaround) → no undated "later" → prevent: a11y in design review + tests

**My answer:**

**Feedback:**

---

### F23. You finish your sprint work two days early. What do you do?
**Tests:** ownership, initiative, team-first

**Model answer:**
"First, I'd double-check that my work is actually *done*, not just code-complete: tests, docs, monitoring, edge cases. 'Done' often has a long tail.

Then I'd look at the team before myself. Is anyone blocked or behind on something that affects the sprint goal? Helping a teammate land their piece usually has more impact than starting something new. I'd mention it in standup: 'I've got capacity, anyone want a hand or a reviewer?' Code reviews are also an easy, high-value thing to pick up.

If the team's in good shape, I'd pull the next priority from the backlog after a quick check with my lead, so I'm working on what matters most, not just what I find interesting.

If even that's covered, I'd go after the small stuff that never gets prioritized: a flaky test, missing documentation, a slow build, tech debt that annoys everyone.

And I'd let my lead know I finished early. That's useful data for future estimation."

**Key moves:** truly done? → team before self → offer help and reviews in standup → next priority, confirmed with lead → tech debt / flaky tests / docs → tell lead (estimation data)
**🔗 Real example hook:** something you picked up unasked when you had spare time (also feeds slot 5)

**My answer:**

**Feedback:**

---

### F24. Your team is spread across time zones and communication keeps breaking down. What do you do?
**Tests:** collaboration, inclusion, process

**Model answer:**
"First, I'd want to know specifically *what's* breaking down. Is it decisions being made without one group? Slow handoffs? Duplicated work? Misunderstandings? The fix depends on the actual failure, so I'd ask people on both sides.

Common root causes are that decisions happen in meetings or chats the other time zone isn't in, and handoffs depend on someone being awake.

Some changes I'd suggest, and offer to help set up:
- **Write things down by default:** decisions recorded in a shared doc or thread, not just in a call, so the other side can catch up.
- **Clear handoff notes** at the end of each day: what's done, what's blocked, what needs an answer.
- **Rotate meeting times** so it's not always the same group taking late or early calls. That's a fairness thing, and people notice.
- **Protect a small overlap window** for things that really need real-time discussion.

I'd suggest trying these for a few weeks and then checking in with the team, since process changes should be tested, not imposed.

Success: fewer blocked handoffs, less rework, and both sides feeling included in decisions."

**Key moves:** diagnose what exactly is breaking → decisions in writing → daily handoff notes → rotate meeting times (fairness) → protected overlap window → trial, then retro

**➡️ Use story:** 🔗 real example hook: S04 (onshore/offshore bridge)
**My answer:**

**Feedback:**
