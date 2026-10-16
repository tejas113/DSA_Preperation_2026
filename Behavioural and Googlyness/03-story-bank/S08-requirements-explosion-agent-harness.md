# S08 – Requirements exploded: I said my own parser wouldn't scale, and we moved to an agent harness
**Source:** current project, post-v1 (ongoing) · **Answers:** D9, D5, E9, E3, E14
**Googleyness shown:** intellectual humility (letting go of your own work), thriving in ambiguity, moonshot

## STAR
**S – Situation**
- After v1, the client's needs grew a lot: onboard **20+ style guides** (not one), process **600–1,000-page books** (not just articles), and add a **feedback loop** where a user can reject a suggestion and the rule gets updated.
- It went from *one style guide ↔ many manuscripts* to **many ↔ many**, on a tight timeline.

**T – Task**
- Decide how to scale. The honest problem: **the LLM parser I had built (S01) would not handle book-length context or multiple style guides.**

**A – Action**
- I **said that openly** instead of trying to patch it. Something I'd invested months in wasn't the right base for the new requirements.
- We moved to an **agent-harness design** (agents that plan and act on their own), which was new for the whole team.
- To manage the risk, we used **spec-driven development**: PRDs (L100) → architecture and workstreams (L200) → epics and stories (L300) → code (L400). It's review-heavy, but it forces clarity before code.
- The system has 5 components; **I took full ownership of two**:
  - **C1: style-guide onboarding agent**, which turns each style guide into chapter-wise skill files the agents can use
  - **C2: text-extraction agent harness**
- My v1 experience (the parsing edge cases, the LLM-friendly rule format) went directly into these designs.

**R – Result**
- [Current status: what's working so far? anything delivered?]
- **Lesson:** don't get attached to your own solution. **Be the first to say when it won't scale**, and carry the learnings forward rather than the code.

## Anchors
v1 → 20+ guides, 600–1,000-page books, feedback loop → many-to-many → **my parser won't scale; I said so** → agent harness (new to team) → SDD: L100 PRD → L200 arch → L300 stories → L400 code → I own C1 (style-guide → skill files) + C2 (text extraction) → v1 learnings reused

## Follow-ups to expect
1. **"Was it hard to let go of your parser?"** → honest: yes, but the requirement changed; the learnings carried over.
2. **"Why an agent harness and not a fixed pipeline (e.g. LangGraph states)?"** → [your reasoning: many-to-many, unpredictable structure, the agent needs to decide steps itself]
3. **"How do you test an agent that 'thinks on its own'?"** → [your answer: evals? test sets? the human feedback loop?] ⚠️ Prepare this.
4. **"How does C1 work?"** → [one-paragraph explanation]

## Re-angle
- **D9 Dropped something you invested in:** lead with the parser.
- **D5 Adapted to a big change:** lead with the requirement explosion.
- **E9 / E14 Decision without full info / competing demands:** lead with the tight timeline plus a new technology for the team.
