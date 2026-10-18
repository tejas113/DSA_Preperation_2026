# Math, Bits & Greedy — Topic-by-Topic Roadmap

The full problem set, grouped into **3 topics** in study order. Do them top to bottom.
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
| **[+] Claude** | Not on either list. Added to close a real gap in technique coverage. Reason given under the topic. |

**Totals:** 22 problems — 4 on both lists · 7 LC150-only · 9 NC150-only · 2 Claude additions.
**Priority split:** 13 Core · 9 Stretch.

**Status key:** ☐ not started · ◐ in progress · ☑ done & code runs.

**Priority key:** **Core** — teaches a distinct technique not covered by any other problem in the list.
**Stretch** — a second/harder rep of a mechanic a Core problem already teaches, or a niche problem that is
unlikely to be asked.

**Scope:** every LC150 problem in the Bit Manipulation, Math and Kadane's sections, every NC150 problem in
Bit Manipulation and Math & Geometry, and the NC150 Greedy problems that aren't array scans — except the ones
already in the other repos (Plus One, Happy Number, Rotate Image, Spiral Matrix, Set Matrix Zeroes and
Multiply Strings are in Arrays-Strings; Sqrt(x) is in Binary-Search) — plus 2 extras for Google.

---

## Topic 1 — Bit Manipulation

**Pattern:** treat numbers as rows of bits, and use `XOR`, `AND`, `OR` and shifts to do in one step what a loop would do slowly.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 1 | Single Number | **LC150 + NC150** | 136 | Easy | Core | ☐ | TBD |
| 2 | Number of 1 Bits | **LC150 + NC150** | 191 | Easy | Core | ☐ | TBD |
| 3 | Counting Bits | NC150 | 338 | Easy | Core | ☐ | TBD |
| 4 | Reverse Bits | **LC150 + NC150** | 190 | Easy | Core | ☐ | TBD |
| 5 | Missing Number | NC150 | 268 | Easy | Core | ☐ | TBD |
| 6 | Sum of Two Integers | NC150 | 371 | Medium | Core | ☐ | TBD |
| 7 | Single Number II | LC150 | 137 | Medium | Stretch | ☐ | TBD |
| 8 | Add Binary | LC150 | 67 | Easy | Stretch | ☐ | TBD |
| 9 | Bitwise AND of Numbers Range | LC150 | 201 | Medium | Stretch | ☐ | TBD |

> **Why these are Core:** #1 is XOR cancelling pairs, #2 is `n & (n - 1)` clearing the lowest set bit, #3 builds
> each count from a smaller one (`bits[i] = bits[i >> 1] + (i & 1)`), #4 builds a result bit by bit, #5 is XOR
> of indices against values, and #6 adds without `+` using XOR (sum without carry) and AND-then-shift (carry).
> **Why #7–#9 are Stretch:** #7 counts bits per position (mod 3), #8 is string addition with a carry, and #9
> finds the common binary prefix of the range. Each is a niche variation.

---

## Topic 2 — Math & Number Tricks

**Pattern:** a short piece of number theory or arithmetic turns a slow loop into a fast one, and most of the difficulty is handling edge cases (overflow, negatives, zero).

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 10 | Reverse Integer | NC150 | 7 | Medium | Core | ☐ | TBD |
| 11 | Palindrome Number | LC150 | 9 | Easy | Core | ☐ | TBD |
| 12 | Pow(x, n) | **LC150 + NC150** | 50 | Medium | Core | ☐ | TBD |
| 13 | Count Primes | **[+] Claude** | 204 | Medium | Core | ☐ | TBD |
| 14 | Implement Rand10() Using Rand7() | **[+] Claude** | 470 | Medium | Core | ☐ | TBD |
| 15 | Factorial Trailing Zeroes | LC150 | 172 | Medium | Stretch | ☐ | TBD |
| 16 | Max Points on a Line | LC150 | 149 | Hard | Stretch | ☐ | TBD |
| 17 | Detect Squares | NC150 | 2013 | Medium | Stretch | ☐ | TBD |

> **Why #10 and #11 are Core:** both are "peel digits with `% 10` and `// 10`", and both test edge cases
> (overflow, negative numbers, the mirrored half).
> **Why #12:** fast exponentiation (square the base, halve the exponent) is a standard building block.
> **Why #13:** the Sieve of Eratosthenes is the standard way to count or list primes, and a common warm-up.
> **Why #14:** **rejection sampling** — build a bigger uniform range from the smaller one, and re-roll values
> you can't use. It is a Google-style question with no relation to the other techniques here.
> **Why #15–#17 are Stretch:** #15 counts factors of 5, #16 is slope hashing with a fractions/GCD trap, and
> #17 is a hash-map design question. All are rarely asked.

---

## Topic 3 — Greedy Leftovers

**Pattern:** make the best local choice and never undo it — but here the "scan" is over characters, ranges or groups, not just an array of numbers.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 18 | Partition Labels | NC150 | 763 | Medium | Core | ☐ | TBD |
| 19 | Valid Parenthesis String | NC150 | 678 | Medium | Core | ☐ | TBD |
| 20 | Maximum Sum Circular Subarray | LC150 | 918 | Medium | Stretch | ☐ | TBD |
| 21 | Hand of Straights | NC150 | 846 | Medium | Stretch | ☐ | TBD |
| 22 | Merge Triplets to Form Target Triplet | NC150 | 1899 | Medium | Stretch | ☐ | TBD |

> **Why #18 is Core:** record the last index of each letter, then cut whenever you reach the farthest last
> index in the current group.
> **Why #19:** track a *range* of possible open-bracket counts (`low`, `high`) so `*` can be `(`, `)` or empty
> — a distinct greedy idea that avoids trying all three.
> **Why #20–#22 are Stretch:** #20 is Kadane run twice (max subarray, and total minus min subarray), #21 is
> a sort or count-and-heap grouping, and #22 is a simple filter. All are rarely asked.

---

## Coverage check — is this enough for a Google math / bits / greedy interview?

**Yes.** These topics are asked far less often than arrays, trees or graphs, and this list covers the core:
the XOR and `n & (n - 1)` tricks, adding without `+`, digit peeling, fast exponentiation, the sieve, rejection
sampling, and two greedy patterns (last-occurrence cuts and range tracking).

**The 9 Stretch problems** (#7, #8, #9, #15, #16, #17, #20, #21, #22) are the ones to drop first if time is
tight — the 13 Core problems cover every distinct technique.

**Deliberately out of scope, with reasons:**
- **Divide Two Integers (LC 29), Integer to English Words, Roman numerals** — Roman numerals are in
  Arrays-Strings; the others are long simulations that are seldom asked.
- **Bitmask DP and subset enumeration with bitmasks** — competitive-programming leaning, excluded from the DP
  and Backtracking repos for the same reason.
- **Geometry beyond #16 and #17** (rectangle overlap, convex hull) — rarely asked in a generalist interview.
- **Greedy array scans** (Jump Game, Gas Station, Candy) — in the Arrays-Strings repo, Topic 8.
