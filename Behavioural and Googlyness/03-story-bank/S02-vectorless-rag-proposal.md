# S02 – Spoke up as a junior: proposed vectorless RAG, built a PoC, demoed it
**Source:** current project, start (March 2026) · **Answers:** C3, C6, E12, E6, D4
**Googleyness shown:** courage / harder path (hidden trait), moonshot thinking, bias to action

## STAR
**S – Situation**
- At the start of the project, the statement of work had a fairly standard plan: RAG to retrieve style-guide rules, and an agent to apply them.
- The team was 7 MLEs across the US and India. I was the most junior full-timer, and honestly I barely spoke in calls. I was nervous about speaking up as a junior.

**T – Task**
- The style guide is long and highly structured, with **2,000+ rules** organized in chapters and sections. I was worried that standard vector similarity search would lose that structure and pull rules out of context.
- In my own time I'd been learning **vectorless, reasoning-based RAG**: build a tree index of the document, and let the LLM navigate the tree the way a person uses a table of contents. I thought it could fit this problem much better.

**A – Action**
- Instead of staying quiet, I **messaged the senior architect privately** with the idea. That was a lower-pressure way to get past my hesitation.
- He liked it, so I **built a proof of concept**. Because the client data is confidential, I couldn't use the hosted service, so I [built the tree index myself / used the open-source library locally. Verify which]. Then I attached an agent that walks the tree and pulls the relevant rules for the downstream rule application.
- I **demoed it to the team**, showing the agent navigating the tree and fetching rules.
- To keep it fair, I also compared it against **hybrid RAG**, while my intern explored **graph RAG**, so we could choose on evidence rather than on my enthusiasm.

**R – Result**
- The team responded really well, and it was a **turning point for me**: people started coming to me for ideas, which led to me proposing the daily ML sync (S04).
- [⚠️ Fill: **was vectorless adopted?** What did the comparison show? If something else was chosen, say so. That's fine and honest: "we ended up using X because Y, but the exploration shaped how we structured rules."]
- **Lesson:** you don't have to start with a big speech; a private message and a working demo are often more persuasive than an opinion. And ideas should compete on evidence, including mine.

## Anchors
SOW = standard RAG → 2,000+ structured rules → vector search loses structure → learned vectorless on my own → nervous junior → **private message to architect** → PoC (confidential, so local) → demo → compared with hybrid/graph → [outcome] → turning point

## "I" vs "We"
- **Me:** the idea, the PoC, the demo, the hybrid comparison.
- **Others:** the architect's support; the intern's graph-RAG exploration; the team's evaluation.

## Follow-ups to expect
1. **"Explain vectorless RAG simply."** → Instead of embedding chunks and matching by similarity, you build a tree from the document's structure; the LLM reasons over the tree (like reading a table of contents) to find the right section. Better when structure matters; costs more LLM calls. *Be ready to discuss that tradeoff.*
2. **"What are its downsides?"** → more LLM calls (latency/cost); depends on a good tree; [anything you saw].
3. **"Why didn't you raise it in the team call?"** → honest: I was nervous as the junior; messaging privately helped me start. Since then I've become comfortable presenting, even to leadership and the client.
4. **"Did it get used?"** → [fill honestly]

## Re-angle
- **C3 Convinced team to adopt new tech:** lead with the problem with standard RAG, then PoC → demo → evidence.
- **C6 Took a risk / harder path:** lead with the fear of speaking up as a junior, and choosing to push an unproven approach.
- **E12 Aimed higher than asked:** the SOW said standard RAG; you looked for something meaningfully better.
