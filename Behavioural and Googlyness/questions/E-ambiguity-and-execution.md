# E. Ambiguity, Execution & Decision-making

> Answers below are built from **your real stories** (03-story-bank/S01–S08), in STAR order, ~2 min spoken.
> - **Don't memorize them.** Read once, then practise from the **Anchors** line in your own words.
> - **[Brackets]** = facts only you know. Fill or verify before the interview. Never invent numbers.
> - Say **"a large academic publisher"**, never the client's name.
> - In the real round you'll get only 1–2 of these, so it's fine that some reuse the same story from a different angle.

---

### E1. Tell me about a time you dealt with an ambiguous situation / unclear requirements.
**⭐ top question** · **Tests:** thriving in ambiguity, bias to action
**➡️ Use story:** S01

**Answer (from S01):**
"**[S]** I'm working on a GenAI system that automates copy-editing for a large academic publisher. It takes a submitted manuscript and applies the publisher's style-guide rules automatically. Everything depends on parsing the manuscript correctly first, and the manuscripts come in as Word documents with no consistent structure. We had around 5,000 samples across many article types.

**[T]** A few weeks before our first release, the senior engineer who owned parsing had to take a month off for a family emergency, and I was asked to take it over. Nobody had a clear answer for how to parse documents this varied. A rules-based parser kept breaking on new layouts.

**[A]** Instead of jumping into code, I started by reducing the ambiguity. I went through samples across the different article types and catalogued the structural patterns, like how front matter, headings and references actually appear. [How many types/patterns?] That turned 'parse anything' into a defined set of cases. Then I chose a design: rather than one big parser, or sending the whole document to an LLM, which hits context limits and hallucinates, I built an **LLM orchestrator that first classifies the manuscript and its sections, then routes each part to a focused extraction step**. I didn't wait for perfect understanding. I shipped a working version, split testing across samples with my intern, and kept hardening it as testers found new edge cases. I also kept a running doc of patterns and decisions, so the senior could pick it up when he returned.

**[R]** That parser became the foundation of our v1 release and is still in use. [Number if you have one: e.g. 'it correctly handled ~X% of our samples.'] What I took away is that when something is ambiguous, the first job is to **make it concrete**: study the real data, write down the cases, then build and learn from feedback, rather than waiting for clarity that isn't coming."

**Anchors:** owner on leave → 5,000 unstructured DOCX → study samples → catalogue patterns → classify then route (not one parser, not whole-doc LLM) → ship + test with intern → doc for handover → v1 foundation → make it concrete
**Likely follow-ups:** "How did you know it was good enough?" → [your evaluation] · "What would you do differently?" → design for longer docs from day one (see S08)

**My answer:**

**Feedback:**

---

### E2. Tell me about a time you had a tight deadline / a project that was running late.
**Tests:** prioritization, communication
**➡️ Use story:** S07

**Answer (from S07):**
"**[S]** Early in my current project, I'd designed an end-to-end architecture for our core flow: retrieve the relevant style-guide rules, then have an agent apply them to the manuscript.

**[T]** We were asked to show a working prototype of it to the client **by that same evening**. So I had a few hours to turn a design into something that actually ran.

**[A]** The key decision was scope. I knew that trying to build everything would leave us with half of each piece and nothing to show. So I picked [a small set of representative rules and one manuscript type] and made sure the **full flow worked end to end** for that slice: retrieval, application, and output. I split the work with my intern: [he handled ___, I handled ___]. I also prepared the demo flow itself, what to show and in what order, so we'd spend the client's time on the value, not on setup.

**[R]** We demoed it that evening, the client liked it, and leadership recognized the work. [Any concrete next step it unlocked?] The lesson I keep coming back to: **under a hard deadline, a thin end-to-end slice beats a polished half.** It's also something I actively use against my tendency to over-engineer."

**Anchors:** my architecture (retrieve → agent applies) → client demo same evening → scope = thin end-to-end slice → split with intern → prepared demo flow → client liked → thin slice > polished half

**My answer:**

**Feedback:**

---

### E3. Tell me about a time you had to make a trade-off.
**Tests:** judgment
**➡️ Use story:** S03

**Answer (from S03, trade-off angle):**
"**[S]** At the start of my current project, we had to choose how to apply a publisher's style-guide rules to manuscripts automatically. There were two real options: a deterministic approach, where you write a script for each rule, or an LLM/agent approach.

**[T]** It was a genuine trade-off. Deterministic is predictable, cheap and easy to test. The LLM approach is flexible, but less predictable and more expensive. One of our senior architects favoured deterministic, and I leaned toward the agent approach, so we needed to choose carefully.

**[A]** I'd read the full style guide, 2,000+ rules, so I knew a lot of them depend on context. But instead of arguing, I tested it. With my intern, I took a section of the guide, wrote a deterministic function for each rule, and ran them on real manuscripts. The results split into two groups: mechanical rules [example] worked well with scripts, and contextual rules [example] simply couldn't be expressed as a script. On top of that, writing and testing a function per rule was very time-intensive, which wouldn't scale to 2,000+ rules.

**[R]** So we went with the agent approach for rule application, **accepting less predictability in exchange for coverage**, and [if true: kept deterministic checks for the simple mechanical rules]. Then we managed the downside by rewriting the rules into a clearer, LLM-friendly format and testing rigorously. The lesson: a good trade-off decision names what you're giving up, and then puts something in place to manage that cost."

**Anchors:** deterministic (predictable, cheap) vs agent (flexible, less predictable) → read 2,000+ rules → test, not argue → scripts per rule on real manuscripts → mechanical ✓ / contextual ✗ + too slow to scale → chose agent → managed the downside (LLM-friendly rules + testing)

**My answer:**

**Feedback:**

---

### E4. How do you prioritize when you have multiple tasks?
**Tests:** organization

**Answer (method + real example from S01/S05):**
"I use a few simple rules.

First, **anything blocking someone else goes first**: a review, an answer, a dependency. My one hour can save someone else a day.

Second, for the rest I look at **impact and urgency**: what matters most for the current goal, and what has a real deadline. Important-but-not-urgent work, like tech debt, I schedule deliberately so it doesn't get starved.

Third, **when priorities genuinely conflict, I don't guess**. I list what's on my plate and ask my lead which matters most, because they have context I might not.

A real example: before our v1 release, the senior engineer who owned manuscript parsing went on leave, and parsing landed on me **on top of** the front-matter and body-matter rules I already owned. I listed everything out. Parsing went first because every downstream rule depended on it: if parsing was wrong, nothing else mattered. I handed well-defined testing work to my intern so he wasn't blocked on me, and [agreed with my lead/architect what could wait until after v1]. We shipped v1 with parsing as its foundation."

**Anchors:** unblock others first → impact × urgency → conflicts: ask lead → example: parsing + my rules work → parsing first (everything depends on it) → intern gets testing → agreed what waits → v1 shipped

**My answer:**

**Feedback:**

---

### E5. Tell me about a time you used data to make a decision.
**Tests:** analytical thinking
**➡️ Use story:** S03

**Answer (from S03, data angle):**
"**[S]** On my current project, a GenAI copy-editing system for an academic publisher, our team had a real disagreement about the core approach. One senior architect wanted to apply each style-guide rule with a deterministic script. I believed many rules needed an LLM because they depend on context.

**[T]** That was two opinions, and one of them was from a much more senior person. I didn't want it decided by seniority or by who argued harder, so I wanted data.

**[A]** I proposed a small experiment. With my intern, I took a section of the style guide and wrote a deterministic function for each rule in it, then ran them on real manuscripts and looked at where they worked and where they broke. We tracked [how many rules worked vs failed, roughly], and how long each function took to write and test. I presented the results to the team, **including where the deterministic approach worked well**, so it was a fair comparison.

**[R]** The data showed two clear groups: mechanical rules scripts handled fine, and contextual rules they couldn't express. It also showed the effort per rule wouldn't scale to 2,000+ rules. The team agreed on the agent approach. [How did the architect react?] What I learned is that when there's disagreement, **the fastest way to resolve it is to generate evidence**, and to give the other side's idea a genuinely fair test."

**Anchors:** two opinions (senior: scripts / me: LLM) → don't decide by seniority → experiment: style-guide section → script per rule → real manuscripts → tracked worked vs broke + effort → fair demo → mechanical ✓ / contextual ✗ / doesn't scale → team decided → evidence over argument

**My answer:**

**Feedback:**

---

### E6. Tell me about a time you came up with a creative solution.
**Tests:** problem solving, 10x thinking
**➡️ Use story:** S02

**Answer (from S02):**
"**[S]** At the start of my current project, the plan was fairly standard: use RAG, meaning vector search over chunks, to retrieve the right style-guide rules, then an agent to apply them.

**[T]** I was worried standard vector search was the wrong fit. The style guide has 2,000+ rules organized in chapters and sections, and a rule's meaning often depends on where it sits. Similarity search over chunks tends to lose that structure and pull rules out of context.

**[A]** I'd been learning about **vectorless, reasoning-based RAG** in my own time. Instead of embeddings, you build a tree from the document's structure, and the LLM navigates it the way a person uses a table of contents. I thought it matched this problem much better. I shared the idea privately with the senior architect, and when he was interested, I built a proof of concept. Because the client data is confidential, I [built the tree index myself / ran the library locally] instead of using a hosted service, and attached an agent that walks the tree to fetch the relevant rules. To keep myself honest, I compared it with hybrid RAG while my intern explored graph RAG.

**[R]** I demoed it to the team and they responded really well. [Outcome: was it adopted, or what did you learn from the comparison?] It also changed how I was seen on the team. The lesson: **look at the shape of the data before picking the standard tool.** Here, the structure of the document *was* the information."

**Anchors:** plan = standard vector RAG → style guide is hierarchical, 2,000+ rules → similarity loses structure → vectorless: tree + LLM navigates like a table of contents → private pitch → PoC (confidential, so local) → compared hybrid/graph → demo → [outcome] → shape of the data first

**My answer:**

**Feedback:**

---

### E7. Tell me about a time you built something from nothing.
**Tests:** initiative, ownership
**➡️ Use story:** S07 (prototype from my architecture) or S02 PoC

**Answer (from S02 + S07, "zero to working" angle):**
"**[S]** When my current project started, there was no working system yet, just a statement of work saying 'retrieve the style-guide rules, apply them with an agent.'

**[T]** I took it on myself to turn that into something real: first a retrieval approach that actually fit the data, then an end-to-end architecture we could show.

**[A]** I started with retrieval. I proposed and built a **vectorless RAG proof of concept**, a tree index over the style guide with an agent that navigates it to find the relevant rules, and demoed it to the team. Then I designed the **end-to-end architecture**: retrieve the right rules, then have an agent apply them to the manuscript. When we were asked to show the client a working prototype by the same evening, my intern and I built a thin end-to-end slice of that architecture [on a few representative rules] and demoed it.

**[R]** The client liked it, it became the starting point for the real build, and leadership recognized the work. [Anything it led to?] What I learned about building from zero: **get something end-to-end working early**, even if small, because a running thing gets real feedback, and slides don't."

**Anchors:** only a SOW → vectorless PoC → demo → end-to-end architecture (retrieve → agent applies) → same-day client prototype (thin slice with intern) → client liked → starting point of real build → end-to-end early

**My answer:**

**Feedback:**

---

### E8. Tell me about a time you improved a process.
**Tests:** ownership, efficiency mindset
**➡️ Use story:** S04

**Answer (from S04):**
"**[S]** On my current project, our ML team was split between the US and India. There was no ML-specific sync, just a general evening huddle, and people logged off right after. Findings stayed in silos: I'd talk to the onshore architect, and the offshore side often didn't know what had been tried.

**[T]** It wasn't my job to set team process; I was one of the most junior people. But I could see we were repeating work and losing time in the discovery phase, which is exactly when you should be learning fastest.

**[A]** I proposed to our offshore ML lead that we hold a **short daily ML sync** just to share findings, approaches and blockers. I kept it low-cost on purpose so it was easy to say yes. I also started **writing observations and decisions into shared docs**, so context didn't depend on one conversation or one person. And when people still weren't aligned before v1, I went to senior teammates one-on-one, walked them through the approach, and **got them talking directly** with the architects instead of me relaying everything.

**[R]** The sync was adopted [and is still running?]. Alignment got noticeably better [concrete effect?], and it's when the offshore team started noticing my work. One honest lesson: for a while I was the bridge myself, which meant late nights. The real fix wasn't me relaying, it was **docs and direct connections**, which scale."

**Anchors:** US/India split → no ML sync → silos → not my role → proposed short daily sync (low cost) → shared docs → 1:1s, connect people directly → adopted → noticed → don't be the single relay

**My answer:**

**Feedback:**

---

### E9. Tell me about a time you made a decision without all the information.
**Tests:** bias to action
**➡️ Use story:** S08

**Answer (from S08):**
"**[S]** After our v1 release, the client's requirements grew a lot. Instead of one style guide, they wanted to onboard 20+; instead of articles, books of 600 to 1,000 pages; and a feedback loop where users can reject a suggestion and the rule gets updated. And the timeline was tight.

**[T]** We had to choose an architecture without knowing exactly how these new inputs would behave. Some of the style guides weren't even available yet [verify]. And I had to be honest that the parser I'd built for v1 wouldn't handle book-length documents or multiple guides.

**[A]** I said that openly instead of trying to patch it. We decided to move to an **agent-harness design**, where agents plan and act rather than following a fixed pipeline, because a many-to-many problem with unpredictable documents needs that flexibility. That was new for the whole team, so we **reduced the risk with process**: spec-driven development, writing and reviewing PRDs first, then architecture, then stories, then code. That way the unknowns were surfaced and discussed before we committed to code. I took ownership of two of the five components: the **style-guide onboarding agent**, which turns each guide into chapter-wise skill files, and the **text-extraction harness**.

**[R]** [Current status: what's working so far?] The lesson: when you can't have all the information, **decide on the direction, but make the decision process itself safe**: write things down, review early, and keep what you learned even when you drop what you built."

**Anchors:** requirements exploded (20+ guides, 600–1,000-page books, feedback loop) → tight timeline → unknowns → my parser won't scale, said so → agent harness (flexible) → spec-driven: PRD → arch → stories → code → I own C1 (guide → skill files) + C2 (extraction) → [status]

**My answer:**

**Feedback:**

---

### E10. Tell me about a time you focused on the user / customer.
**Tests:** "focus on the user and all else will follow" (Google's #1 value)

**⚠️ No story yet. Best candidate from your project (tell me if any of this is true):**
Your users are the **publisher's copy editors**. Did you ever:
- talk to them or watch how they actually check rules, and change something because of it?
- notice an output format they found hard to use (e.g. how the UI shows suggested edits) and fix it?
- shape the **feedback loop** (users rejecting a suggestion → rule updates) around how they really work?

**Skeleton once you have it:** who the user is → what they were struggling with (in their words) → what you learned by looking closely → what you changed → how you knew it helped them.

**My answer:**

**Feedback:**

---

### E11. What's the most technically challenging problem you've solved?
**⭐ very common** · **Tests:** RRK, GCA, depth
**➡️ Use story:** S01

**Answer (from S01, technical-depth angle):**
"Parsing unstructured manuscripts for our copy-editing automation system.

**[S/T]** The system applies a publisher's style-guide rules to submitted manuscripts automatically. To apply a rule you first need to know *what* you're looking at: title, abstract, headings, body, references. But manuscripts arrive as Word files with no consistent structure across around 5,000 samples. When the engineer who owned parsing went on leave before our first release, I took it over.

**[A]** I considered three approaches:
- **Rule-based parsing:** predictable, but every new layout broke it. With this much variety we'd be writing exceptions forever.
- **Sending the whole document to an LLM:** simple, but long manuscripts hit context limits, and the output became unreliable.
- What I built: an **LLM orchestrator**. First, a **classification step** identifies the manuscript type and its sections. Then each section is **routed to a focused extraction step**, so every LLM call is small and specific. [Add one technical detail you're proud of: e.g. structured/JSON output, validation, how you handled tables or footnotes.]

To make it robust, I catalogued structural patterns across article types, tested against real samples, and when testers found new edge cases, fed them back as fixes.

**[R]** It became the foundation of our v1 release. [Metric if you have it.] It also taught me its own limits: it wasn't designed for 600 to 1,000-page books, which is why our next version moved to an agent-based design. That's a lesson I carry: **design around the input sizes you'll have next, not just the ones you have now.**"

**Anchors:** need structure before rules → Word files, ~5,000 samples, no consistency → took over → 3 options: rules (brittle) / whole-doc LLM (context, unreliable) / **classify → route** (small focused calls) → patterns + real samples + edge-case loop → v1 foundation → limit: book length → design for next input size
**⚠️ Be ready for deep technical follow-ups:** prompts, output schema, how you validated, error handling, cost/latency, how you evaluated accuracy.

**My answer:**

**Feedback:**

---

### E12. Tell me about a time you aimed for something far more ambitious than what was asked.
**Tests:** moonshot / 10x thinking
**➡️ Use story:** S02

**Answer (from S02, ambition angle):**
"**[S]** When my current project kicked off, the statement of work asked for standard RAG to retrieve style-guide rules. That's the conventional approach, and it would have been perfectly acceptable to just build that.

**[T]** But I didn't think 'acceptable' was good enough for this problem. The style guide is a 2,000+ rule, deeply structured document, and standard vector search tends to lose that structure. I wanted retrieval that actually understood where a rule lives and why.

**[A]** I'd been studying **vectorless, reasoning-based RAG** on my own, which navigates a document's structure like a table of contents instead of matching embeddings. I pitched it to the senior architect, built a proof of concept that worked within the client's confidentiality limits [how], and demoed it. I didn't just push my idea, though. I set it against hybrid RAG, and my intern explored graph RAG, so the team could pick on evidence.

**[R]** [Outcome: adopted? influenced the final design?] For me personally, it was the moment I stopped being the quiet junior and started shaping the technical direction. The lesson: **the spec is the floor, not the ceiling**. But an ambitious idea still has to earn its place with evidence."

**Anchors:** SOW = standard RAG (acceptable) → 2,000+ structured rules → wanted better → self-learned vectorless → pitched → PoC within confidentiality → compared with hybrid/graph → [outcome] → spec is the floor

**My answer:**

**Feedback:**

---

### E13. Tell me about a time you had to deliver with limited resources (time, people, tools).
**Tests:** resourcefulness
**➡️ Use story:** S05

**Answer (from S05):**
"**[S]** About [one month] before our v1 release on my current project, the team changed a lot in a few weeks. Architects rolled off, our interns finished, and my intern moved to another company. **We went from seven ML engineers to three**, with a lot still unproven.

**[T]** We still had to deliver v1. I owned manuscript parsing plus the front-matter and body-matter rule application. My senior handled back matter, reference validation and deployment.

**[A]** With fewer people, we couldn't afford to discover problems late. Our new architect brought in testers to check manuscripts rigorously, and I made sure every edge case they found went straight into **hardening the parser**, instead of piling up. As a team we rewrote the style-guide rules into a form an LLM could follow reliably, which cut down on errors we'd otherwise have to chase by hand. [Add what *you* cut, deferred or simplified to fit three people: e.g. 'I focused v1 on the article types that covered most of our samples and deferred the rare ones.'] And with clear ownership split between the three of us, nobody was waiting on anyone.

**[R]** In about [a month] we built the full flow: parse the manuscript, apply the rules, output JSON, and render the suggested edits in the UI. **We delivered v1.** The lesson: with limited people, **structure beats heroics**. Clear ownership, rigorous testing and focusing on what v1 actually needs got us there."

**Anchors:** ~1 month to v1 → team 7 → 3 → my scope: parsing + front/body rules → testers → edge cases → harden parser → rules rewritten LLM-friendly → [what I cut] → clear ownership → parse → apply → JSON → UI → v1 shipped → structure > heroics
**⚠️ Never** mention terminations or "management issues". Just "roll-offs and people leaving".

**My answer:**

**Feedback:**

---

### E14. Tell me about a time several people wanted different things from you at once.
**Tests:** prioritization, stakeholder communication
**➡️ Use story:** S04

**Answer (from S03 + S04, "caught between two directions" angle):**
"**[S]** Early on my current project, our two senior architects, one in the US and one in India, had different visions. The offshore architect wanted a deterministic, script-per-rule approach; the onshore architect was more open to an LLM/agent approach. I was working closely with both, so I was effectively getting pulled two ways.

**[T]** I needed to keep moving without quietly picking a side, and without being the person both sides relied on to relay everything.

**[A]** A few things. First, I made the disagreement **testable**: with my intern, I built deterministic functions for a section of the style guide and ran them on real manuscripts, so both architects could look at the same evidence. Second, I proposed a **daily ML sync** so both sides heard findings at the same time, instead of through me. Third, I wrote my observations into **shared docs**, and when people still weren't aligned, I asked senior teammates to **connect directly** with the architects.

**[R]** The experiment settled the core question, the team aligned on the agent approach, and the sync became a regular habit. What I learned: when people want different things from you, **don't absorb the conflict yourself**. Make it visible, give everyone the same information, and get the decision-makers talking to each other."

**Anchors:** two architects, two visions (scripts vs agent) → pulled both ways → don't pick silently, don't be the relay → test it (scripts on real manuscripts) → daily ML sync → shared docs → connect people directly → aligned → don't absorb the conflict

**My answer:**

**Feedback:**
