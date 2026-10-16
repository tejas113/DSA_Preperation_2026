# S03 – Disagreed with a senior architect: settled it by testing *his* approach
**Source:** current project, discovery phase · **Answers:** B2 ⭐, E5, E3, B12 (and B1 if you have no peer-conflict story)
**Googleyness shown:** intellectual humility, data over opinion, respectful courage

> This is one of your **strongest** stories. A junior disagreeing with a senior, resolved with evidence, not ego.

## STAR
**S – Situation**
- During the discovery phase, we had to decide the core approach for applying style-guide rules.
- One of our senior architects preferred a **deterministic approach**: write a script for each rule and apply them programmatically. It's predictable, testable and cheap.

**T – Task**
- I'd read the **entire style guide end to end**, 2,000+ rules, and many of them depend on context and judgment. I didn't think scripts could cover them, and that an LLM/agent approach was needed.
- But I was the junior, disagreeing with a senior on the core architecture. I needed to resolve it without it becoming *my opinion vs his seniority*.

**A – Action**
- Instead of arguing in the abstract, I suggested we **test it**. With my intern, I took a section of the style guide and **wrote deterministic functions for each rule** in it, then ran them on real manuscripts.
- We found two groups:
  - rules that worked well deterministically, the mechanical ones [give one example, e.g. a formatting/punctuation rule]
  - rules a script *can't* express because they need context or judgment [give one example, e.g. "spell out numbers below ten, except in technical contexts"]
- I also noted that writing and testing a function per rule was **very time-intensive**, and that wouldn't scale to 2,000+ rules.
- I **demoed the findings to the team**, including the cases where deterministic worked well, so it was a fair comparison and not a takedown.

**R – Result**
- The team agreed deterministic-only wasn't suitable, and we went with RAG + agent for rule application. [If true: "with deterministic checks kept for the simple mechanical rules." That's a great balanced detail if it happened.]
- [Relationship: how did the architect react? e.g. "He appreciated that we'd actually tested his idea."]
- **Lesson:** when you disagree with someone more senior, don't debate. **Run the experiment, and give their idea a genuinely fair test.** It might be right, and if it's not, the data makes the case without making it personal.

## Anchors
deterministic (senior) vs agentic (me) → read all 2,000+ rules → junior vs senior → **test his approach** → intern + style-guide section → functions per rule → 2 groups: mechanical ✓ / contextual ✗ + too slow to scale → fair demo → team decision → [relationship]

## "I" vs "We"
- **Me:** read the guide fully, proposed the test, built and tested functions with the intern, presented findings.
- **Others:** the intern co-built the functions; the team made the call.

## Follow-ups to expect
1. **"What if the data had supported him?"** → "Then we'd have gone deterministic, and that's fine. The goal was the right approach, not me being right."
2. **"How did you make sure the test was fair?"** → used real manuscripts, picked a representative section [how did you pick it?], showed where deterministic worked well.
3. **"Did he push back?"** → [honest answer]
4. **"What's the downside of the LLM approach?"** → less predictable, harder to test, cost/latency. Mention how you mitigated it [validation, structured outputs, rewriting rules into LLM-friendly form, see S05].

## Re-angle
- **B2 Disagreed with a senior:** as written.
- **E5 Used data to decide:** lead with "we had two opinions, so we generated data".
- **E3 Trade-off:** predictability/cost of deterministic vs coverage/flexibility of the LLM approach.
