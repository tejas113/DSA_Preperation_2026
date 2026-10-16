# S01 – Took over manuscript parsing → LLM orchestrator parser + classifier
**Source:** current project (copy-editing automation) · **Answers:** A3 ⭐, A14, E11 ⭐, E1 ⭐, C2, E13, D4
**Googleyness shown:** ambiguity, bias to action, ownership, root-cause thinking

> Say **"a large academic publisher"**, not the client's name (confidentiality). Check every [bracket] is true.

## STAR (2–3 min spoken)
**S – Situation**
- I work on a GenAI system that automates copy-editing for a large academic publisher: it reads a submitted manuscript and applies the publisher's style-guide rules automatically.
- Everything downstream depends on **parsing the manuscript correctly**. If we misread the structure, every rule gets applied to the wrong thing.
- The manuscripts come as DOCX with **no consistent structure**. We had around **5,000 samples** across many article types.

**T – Task**
- A few weeks before v1, the senior MLE who owned parsing had to take a month off for a family emergency. **I was asked to take parsing over.**
- A deterministic parser wasn't going to work universally, and nobody had a clear answer for what would.

**A – Action**
- **Studied the data before writing code.** I went through samples across article types and catalogued the structural patterns: how front matter, headings, sections and references show up. [How many patterns/types did you find?]
- **Chose the design deliberately:**
  - pure rule-based parsing → too brittle for this many layouts
  - sending the whole document to an LLM → context limits and hallucination risk
  - ✅ **an LLM orchestrator**: first *classify* the manuscript and its sections, then route each part to a focused extraction step. [Verify this matches what you built.]
- **Split the testing** with my intern across sample types, and kept a running doc of patterns, decisions and open edge cases, so the senior could pick it up when he came back.
- When our new architect brought in testers, I fed every newly found edge case back into **hardening the parser**.

**R – Result**
- The parser + classifier became **the foundation of v1** and is still in use. [Any number? e.g. "handled ~X% of the samples correctly", "cut manual parsing from X to Y".]
- I went on to own **parsing, front-matter and body-matter rule application** for the v1 release.
- **Lesson:** with messy real-world data, study the data first and design around the patterns you actually see, not the ones you assume. Test against real samples, not ideal ones.

## Anchors
senior on leave → I take parsing → 5,000 DOCX, no structure → study patterns first → rules too brittle / whole-doc LLM too big → **classify, then route** → intern + testers → edge cases → v1 foundation

## "I" vs "We"
- **Me:** pattern analysis, parser/classifier design and build, hardening it.
- **Others:** intern helped test samples; testers (brought in by the architect) found edge cases; the senior MLE's earlier work [what did he have before you took over?].

## Follow-ups to expect
1. **"Why not a deterministic parser?"** → layouts vary too much; every new format breaks it. [Give one concrete example of two manuscripts that differ.]
2. **"Why not just give the whole document to the LLM?"** → context limits on long manuscripts, and output becomes unreliable. Classifying first keeps each LLM call small and focused.
3. **"How did you measure whether it worked?"** → [your evaluation: a sample set checked by testers? accuracy %?] ⚠️ *Prepare this. It's the most likely follow-up.*
4. **"How did you handle hallucination?"** → [e.g. structured output / validation / schema checks?]
5. **"What would you do differently?"** → design for longer documents from the start (links to S08: it didn't scale to 600–1,000-page books).

## Re-angle
- **E1 Ambiguity:** lead with "nobody knew how to parse 5,000 unstructured manuscripts, and the owner was away."
- **E11 Hardest technical problem:** lead with the design choice (classify → route) and why the alternatives failed.
- **C2 End-to-end ownership:** stress that you took over mid-stream, documented everything, and hardened it all the way to release.
