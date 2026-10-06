# Stack — Topic-by-Topic Roadmap

The full problem set, grouped into **4 topics** in study order. Do them top to bottom.
Within each topic, the **Source** column tells you exactly where each problem comes from.

> **Note on source-tag confidence:** same caveat as the other trackers. This list was self-curated from
> memory, because live verification of the exact LeetCode Top 150 / NeetCode 150 category contents isn't
> possible here. Treat LC150 / NC150 tags as best-effort. The **[+] Claude** extras are picked from general
> knowledge of commonly asked interview problems, not from verified company-tagged data.

---

## Source legend

| Badge | Meaning |
|---|---|
| **LC150** | On LeetCode's official *Top Interview 150* list |
| **NC150** | On the *NeetCode 150* list |
| **LC150 + NC150** | On **both** lists — highest-priority, most-asked |
| **[+] Claude** | Not on either list. Added to close a real gap in stack technique coverage. Reason given under the topic. |

**Totals:** 12 problems — 3 on both lists · 2 LC150-only · 3 NC150-only · 4 Claude additions, plus 2 optional
[extras](#extras--optional-do-after-the-main-list) at the bottom (not counted in the numbering).
**Priority split:** 11 Core · 1 Stretch.

**Status key:** ☐ not started · ◐ in progress · ☑ done & code runs.

**Priority key:** **Core** — teaches a distinct stack technique not covered by any other problem in the list.
**Stretch** — a second/harder rep of a mechanic a Core problem already teaches.

**Scope:** every LC150 problem in the Stack section and every NC150 problem in the Stack section, except
Generate Parentheses (it is in the Backtracking repo), plus 4 additions for Google, and 2 optional extras
kept in a separate section at the bottom.

---

## Topic 1 — Stack as "Pending Items"

**Pattern:** push things that are still **waiting** for something (an open bracket, a partial string, a survivor). When the thing they're waiting for arrives, pop them.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 1 | Valid Parentheses | **LC150 + NC150** | 20 | Easy | Core | ☑ | [01-valid-parentheses.md](01-stack-as-pending-items/01-valid-parentheses.md) |
| 2 | Simplify Path | LC150 | 71 | Medium | Core | ☑ | [02-simplify-path.md](01-stack-as-pending-items/02-simplify-path.md) |
| 3 | Decode String | **[+] Claude** | 394 | Medium | Core | ☑ | [03-decode-string.md](01-stack-as-pending-items/03-decode-string.md) |
| 4 | Asteroid Collision | **[+] Claude** | 735 | Medium | Stretch | ☑ | [04-asteroid-collision.md](01-stack-as-pending-items/04-asteroid-collision.md) |

> **Why these are Core:** #1 is the base pattern (an open bracket waits for its closer), #2 pushes and pops
> path parts (`..` pops), and #3 keeps a *pair* on the stack — the string built so far and the repeat count —
> for nested brackets, a common Google-style question.
> **Why #4 is Stretch:** it's a "survivors" stack (a new asteroid collides with the top until one is gone). A
> good simulation, but it needs no new idea beyond #1.

---

## Topic 2 — Monotonic Stack

**Pattern:** keep a stack whose values are always in increasing (or decreasing) order. When a new value breaks the order, pop the items it beats — and each popped item just found its "next greater" (or "next smaller") element.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 5 | Next Greater Element I | **[+] Claude** | 496 | Easy | Core | ☑ | [05-next-greater-element-i.md](02-monotonic-stack/05-next-greater-element-i.md) |
| 6 | Daily Temperatures | NC150 | 739 | Medium | Core | ☑ | [06-daily-temperatures.md](02-monotonic-stack/06-daily-temperatures.md) |
| 7 | Car Fleet | NC150 | 853 | Medium | Core | ☑ | [07-car-fleet.md](02-monotonic-stack/07-car-fleet.md) |
| 8 | Largest Rectangle in Histogram | NC150 | 84 | Hard | Core | ☐ | TBD |

> **Why #5:** it is the cleanest first example of a monotonic stack; #6 then reuses it with indices.
> **Why #7 and #8 are Core:** #7 sorts by position and stacks arrival times (the stack tells you where fleets
> merge). #8 stores indices and uses the popped item's height for the rectangle — the hardest and most-asked
> monotonic-stack problem.
> Next Greater Element II (circular array) is in the [Extras](#extras--optional-do-after-the-main-list) section.

---

## Topic 3 — Expression Evaluation

**Pattern:** scan tokens left to right, keeping a stack of **operands** (and sometimes operators) so each operator can be applied at the right time.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 9 | Evaluate Reverse Polish Notation | **LC150 + NC150** | 150 | Medium | Core | ☑ | [09-evaluate-reverse-polish-notation.md](03-expression-evaluation/09-evaluate-reverse-polish-notation.md) |
| 10 | Basic Calculator II | **[+] Claude** | 227 | Medium | Core | ☐ | TBD |
| 11 | Basic Calculator | LC150 | 224 | Hard | Core | ☐ | TBD |

> **Why these are Core:** #9 is the pure operand stack (pop two, apply, push). #10 adds operator precedence
> (`*` and `/` are applied immediately, `+` and `-` are pushed as signed numbers). #11 adds parentheses, where
> you save the running result and sign on the stack and restart inside the brackets.
> **Why #10:** it is a very commonly asked question that sits between #9 and #11.

---

## Topic 4 — Design with Stacks

**Pattern:** use a stack (or two) inside a data structure to get an `O(1)` operation the plain structure can't do.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 12 | Min Stack | **LC150 + NC150** | 155 | Medium | Core | ☑ | [12-min-stack.md](04-design-with-stacks/12-min-stack.md) |

> **Why #12 is Core:** store `(value, minimum so far)` on every push, so the minimum is always available.
> Implement Queue using Stacks is in the [Extras](#extras--optional-do-after-the-main-list) section.

---

## Coverage check — is this enough for a Google stack interview?

**Yes.** After these 4 topics you will have hands-on reps in: bracket matching, nested decoding, path
simplification, monotonic stacks (next greater, next smaller, histogram), expression evaluation with and
without precedence and parentheses, and stack-based design.

**The 1 Stretch problem** (#4) is the one to drop first if time is tight. The 2 extras are optional on top of that.

**Deliberately out of scope, with reasons:**
- **Generate Parentheses (LC 22)** — it is in NeetCode's Stack section, but it is a backtracking problem and
  is already in the Backtracking repo (#15 there).
- **Trapping Rain Water** — its stack version is a variation of #8; the two-pointer version is in the
  Arrays-Strings repo.
- **Maximal Rectangle (LC 85)** — a Hard that runs #8 on every row of a matrix; rarely asked.
- **Remove K Digits, Online Stock Span, Remove All Adjacent Duplicates** — variations on the monotonic and
  pending-items stacks above.
- **Longest Valid Parentheses (LC 32)** — a Hard that can be solved with a stack or DP; it is a fine extra
  after #1 and #11.

---

## Extras — optional, do after the main list

Not part of the numbered list or the totals above. Each is a small variation on a problem you will already have
done, so do them only if you have time left. Files go in the topic folder, named `E1-…` and `E2-…`.

| # | Problem | Source | LC # | Difficulty | Topic | Builds on | Status | File |
|---|---|---|---|---|---|---|---|---|
| E1 | Next Greater Element II | **[+] Claude** | 503 | Medium | 2 — Monotonic Stack | #5 | ☐ | TBD |
| E2 | Implement Queue using Stacks | **[+] Claude** | 232 | Easy | 4 — Design with Stacks | #12 | ☐ | TBD |

> **E1** is #5 on a circular array (loop twice, use `i % n`). **E2** uses two stacks (`in` and `out`) with
> amortized `O(1)` — a common warm-up, but an easy one.
