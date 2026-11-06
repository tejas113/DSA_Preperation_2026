# Arrays & Strings: Scenario Question Bank (Google L3 style)

Google doesn't say "two pointers" or "sliding window". It gives a short, vague scenario, and **you** have to notice which technique fits and what the cost is.
This file has one scenario per solved problem in this repo, plus two more variants of each, so you practise the *recognition* step and not just the solution.
Problem numbers match [problems.md](problems.md).

**Disguised on purpose:** scenarios avoid words like "subarray", "window", "pair sum", "prefix", "two pointers" and "sorted array" when those words would give the technique away. Each one has an **Ask first** line (the clarifying questions a good candidate asks, which is how you discover the structure), a **Spot it** line (the clue that gives the technique away) and a **Brute force** line (so you can say what the technique improves).

**How to use:** read only the **Scenario** line, then say out loud: *what is being asked (a pair, a stretch, a count, a max/min, a rearrangement)? does order matter? what is the O(n²) answer, and what work does it repeat?* Only then read the rest. About half of the variants deliberately cross over into a neighbouring technique (sliding window to prefix sums, hash to sort, greedy to DP, ...) so you learn where each technique stops working.

---

## Part 1. The 5-step "Which array technique?" framework

1. **Read the input.** Before you think about technique, ask what the data looks like.
   - **Sorted** (or can I sort it)? Sorted input points to two pointers, binary search, or a scan of adjacent items.
   - **Duplicates? Negatives? Zeros?** Negatives break sliding windows on sums. Zeros break division. Duplicates change `set` vs `Counter`, and force skip-forward logic in 3Sum.
   - **Size limits.** `n` up to 1,000 allows `O(n²)`. `n` up to 100,000 wants `O(n log n)` or better. `n` up to 1,000,000 or more wants `O(n)`. Tiny `n` (under 20) hints at exponential search.
   - **Value range.** Small fixed range (26 letters, ages 0 to 120, values `1..n`) means a counting array or the array's own indices can replace a hash map.
   - **Static or a stream?** A stream rules out sorting and anything that needs a second pass.

2. **Name what is being asked.** Finish this sentence: *"I must return a ___ of the ___."*
   - **A pair or triple** that meets a condition: hash lookup (unordered) or two pointers (ordered).
   - **A contiguous stretch** (longest, shortest, count, best sum): sliding window, prefix sums, or Kadane.
   - **A count of stretches that hit an exact value:** prefix sum + hash map.
   - **A yes/no about repeats or membership:** hash set.
   - **A max or min over all choices:** one-pass running best, greedy, or sort + scan.
   - **A rearrangement** (partition, rotate, remove, merge): in-place read/write pointers, or reversals.
   - **Ranges that overlap:** sort, then compare neighbours.
   - **"List all":** that is backtracking, not an array trick (see the Backtracking repo).

3. **Does order matter?**
   - Order **irrelevant** (a bag of numbers): sort or hash. You can throw the positions away.
   - Order **relevant but the answer is contiguous**: window or prefix sums. Never sort, it destroys contiguity.
   - Order **relevant and you must return positions**: hash with indices, or sort pairs of `(value, index)`.
   - Order **relevant and you must keep relative order** (stable removal): read/write pointer, not swap-with-last.

4. **Can I modify the input? Can I use extra space?**
   - `O(1)` extra space: two pointers, read/write pointers, reversals, using the array itself as the hash.
   - `O(n)` space allowed: hash map, prefix array, output buffer.
   - Mutation not allowed: copy first (say the cost), or use an approach that only reads.
   - Sorting in Python uses `O(n)` internal space. Say "sort in place, ignoring the sort's internals" only if the interviewer agrees.

5. **Brute force first, then remove the repeated work.** Say the `O(n²)` (or `O(n³)`) answer out loud, then ask *"what am I recomputing?"*
   - Re-scanning to ask "have I seen this?" → remember it in a **set or map**.
   - Re-adding the same numbers for every range → **prefix sums** (or a running window sum).
   - Re-checking pairs whose answer is already known from order → **two pointers** (one pointer move rules out a whole row of pairs).
   - Re-sorting or re-counting a window → **add one, remove one**.
   - Comparing every pair for overlap → **sort**, then only neighbours can overlap.
   - Re-finding the max of each window → **monotonic deque**.

| Input size `n` | Target time | What fits |
|---|---|---|
| ≤ 20 | exponential | backtracking, bitmask |
| ≤ 1,000 to 5,000 | `O(n²)` | nested loops, simple DP |
| ≤ 100,000 | `O(n log n)` | sort + scan, heap, binary search |
| ≥ 1,000,000 | `O(n)` | one pass, hash, window, pointers |

**Say-it-out-loud template:** *"The brute force checks every [pair / stretch] in `O(n²)`. It repeats [work]. If I [remember it in a map / keep a running total / move a pointer], each element is handled once, so it is `O(n)` time and `O(?)` space. It needs [sorted / all positive / no mutation constraint], which I should confirm."*

**Questions to ask the interviewer (cheap and impressive):**
- **Input:** Is it sorted? Can it be empty or have one element? Can values repeat? Can they be negative or zero?
- **Size:** How large can `n` get, and how large can the values get? (decides `O(n²)` vs `O(n log n)`, and overflow)
- **Output:** The values, the indices, a count, or all of them? If several answers exist, any one or a specific one (the first, the smallest)?
- **Guarantee:** Is an answer guaranteed to exist? What do I return if none does (`-1`, `[]`, `None`)?
- **Reuse:** Can the same element be used twice? Does "pair" mean two distinct positions?
- **Mutation:** May I modify the input in place? Can I use extra memory, and how much?
- **Shape of the data:** One query or many on the same data? Is it a stream, or does it fit in memory? (decides whether to precompute, and whether sorting is allowed)
- **Meaning of "contiguous":** Must the items be adjacent, or can I skip? (subarray vs subsequence is a different problem)
- **Boundaries:** Do touching ranges count as overlapping? Is the end inclusive?

---

## Part 2. Signal → technique cheat sheet

Problem numbers match [problems.md](problems.md). **gap** means the repo has no write-up for it yet (see Part 6). Techniques owned by other repos are named so you still recognise them.

| What the question says | It is really | Technique | Problems |
|---|---|---|---|
| "have we seen this before", "any repeats", "any repeat within the last k" | membership test | **hash set**, or map of last index | 1, 12, 13 |
| "two items that add to a target", unordered, return positions | complement lookup | **hash map** `value → index` | 3 |
| "two items that add to a target", already in order | each pointer move rules out a whole row of pairs | **two pointers** from both ends | 17 |
| "three items that add to 0", "no repeated triples" | fix one, then the pair problem | **sort + two pointers** | 18 |
| "same letters", "can I build X from Y", "do the counts match" | frequency comparison | **hash map / 26-slot array** | 2, 10 |
| "group the things that are equivalent" | canonical key per item | **hash map keyed by a normalised form** | 4, 9, 11 |
| "k most common", "top k" | frequency, then pick | **hash + bucket by count** (or heap) | 5; Heap repo |
| "longest run of back-to-back values", list order irrelevant | start only at the beginning of a run | **set**, `if x - 1 not in set` | 6 |
| "add / remove / pick random in O(1)" | a data structure design | **hash map + array**, swap-with-last on delete | 8 |
| "both ends", "mirror", "palindrome", "at most one mistake" | compare symmetric positions | **two pointers inward** | 14, 15 |
| "is A spelled out in order inside B" | one pointer per sequence | **two pointers (side by side)** | 16 |
| "tallest wall", "most water", "which side can I discard" | the smaller side is the bottleneck | **two pointers + greedy discard** | 19, 20 |
| "arrange into 2 or 3 groups in place", "remove a value in place" | partition | **three-way pointers / read-write pointer** | 21, 48, 49, 53 |
| "merge two ordered lists", "overlap of two ordered lists" | advance the one that finishes first | **two pointers across two inputs** | 47, 38 |
| "longest stretch where a rule holds" (rule only gets worse as the stretch grows) | grow right, shrink left | **variable sliding window** | 23, 24, 29 |
| "shortest stretch whose total reaches a target", all values positive | shrink while still valid | **variable sliding window** | 26, 27 |
| "every stretch of length k", "does any k-long stretch contain ..." | add one, remove one | **fixed sliding window** | 25 |
| "the biggest value in every stretch of length k" | candidates that can still win | **monotonic deque** | 28 |
| "how many stretches add up to exactly k" (negatives possible) | two prefix totals differ by k | **prefix sum + hash map** | 33 |
| "sum of any range", many queries | `prefix[j] - prefix[i]` | **prefix sums** | 33 (idea), gap |
| "add x to a whole range", many updates, read once at the end | store the change at the two ends | **difference array** | gap |
| "best total of a stretch", values can be negative | keep the best ending here | **Kadane / running best** | 32 |
| "everything except me", "product / sum of all others" | what is on my left × what is on my right | **prefix and suffix passes** | 31, 60 |
| "best buy then sell later", "best pair with i < j" | running minimum so far | **one pass with a running best** | 22, 58 |
| "merge overlapping", "insert a range", "is there any clash" | neighbours are the only ones that can overlap | **sort by start, compare with the last** | 34, 35, 41 |
| "fewest to remove / fewest arrows / most that fit" | keep the earliest finisher | **sort by end + greedy** | 36, 40 |
| "how many at the same moment", "fewest rooms / machines" | count open minus closed | **sweep over sorted starts and ends** (or heap) | 37 |
| "closest", "smallest gap", "adjacent equal", "k-th" | sorting makes the relevant items neighbours | **sort + scan** | 59, 61, 41 |
| "ordered data, find / first / last / insertion point" | halve the search space | **binary search** (Binary-Search repo) | 26 (alt.) |
| "smallest X such that it works", where bigger X always works | the feasibility test is monotone | **binary search on the answer** (Binary-Search repo) | Binary-Search repo: Koko |
| "next bigger / next warmer / nearest taller to the left" | unresolved items wait on a stack | **monotonic stack** (Stack repo) | Stack repo: Daily Temperatures |
| "values are 1..n", "find the missing / repeated one in O(1) space" | the array's indices are the hash | **cyclic sort / sign marking** | 45 (idea), gap |
| "k-th largest", "top k of a stream", "merge k ordered lists" | keep only the k best | **heap** (Heap repo) | Heap repo: Kth Largest |
| "can I reach the end", "fewest hops", "where must I start" | one summary number is enough | **greedy scan** | 55, 56, 57 |
| "more than half of the entries are the same" | pairs of different items cancel | **Boyer-Moore vote** | 54 |
| "rotate", "peel layers", "set whole rows and columns" | index arithmetic on a grid | **matrix in place** | 43, 44, 45, 46 |
| "convert", "parse", "without the built-in", "follow the rules exactly" | careful simulation | **one scan + `join`** | 61–70 |
| "how many ways", "min cost over choices", "a choice now changes later options" | overlapping subproblems | **DP** (DP repo) | DP repo |
| "list every ...", "all combinations" | enumeration | **backtracking** (Backtracking repo) | Backtracking repo |

**Red flags that you're being tested on arrays:** "in place", "O(1) extra space", "contiguous", "consecutive", "longest/shortest ...", "exactly k", "without sorting", "return the indices", and any input described as "already ordered".

### Sliding window or prefix sum? (negatives!)

A sliding window is valid only if **growing the window can push the property in one direction** and shrinking pushes it back. Ask: *"If I add the next element, can the property flip from bad to good and then back to bad?"*

- **All values positive, "sum at least / at most k":** adding makes the sum grow, shrinking makes it fall. **Window**, `O(n)`, `O(1)` space (#26).
- **Property is a count or a set** (distinct characters, no repeats, replacements needed): adding can only make it worse, so the window works regardless of sign (#23, #24, #29).
- **Negatives or zeros are possible, and the target is a sum:** adding an element can lower the sum, so shrinking stops being safe. Use **prefix sum + hash map** (#33).
- **Counter-example to memorise:** `nums = [5, -3, 1]`, `k = 3`. The only stretch that sums to 3 is the whole array. A window that shrinks "while sum > k" drops the `5` at once (sum 5 is too big), and from then on the sum can never come back to 3. The prefix approach sees prefix 3 minus earlier prefix 0 and finds it.
- **Fixed length k** works with any signs, because the window size never changes (#25, #28).
- **Shortest stretch with sum ≥ k and negatives:** neither plain tool works. Prefix sums + a monotonic deque (gap, "Shortest Subarray with Sum at Least K").
- **Rule of thumb:** *sliding window finds ONE best stretch; prefix + hash COUNTS stretches or handles negatives.*

### Sort or hash?

| | Hash (set / map) | Sort + scan |
|---|---|---|
| Time | `O(n)` average | `O(n log n)` |
| Extra space | `O(n)` | `O(1)` in place (Python's sort uses `O(n)` internally) |
| Keeps original positions | yes, store the index as the value | no, sort `(value, index)` pairs to keep them |
| Good for | exact match, counts, "seen before", grouping | closest, adjacent, ranges, intervals, "k-th", deduplicating while scanning |
| Weak at | "closest", "range", "in order" | stream input, very large `n` when `O(n)` is needed |

Pick **hash** for "does this exact thing exist". Pick **sort** when the question is about *nearness or ranges* (closest value, overlapping ranges, smallest gap) or when memory is tight. When the input is already ordered, you need neither: use pointers.

### Two pointers or hash?

Ordered input and a pair/triple question → **two pointers** (`O(n)`, `O(1)` space). Unordered and you need the original positions → **hash**. Unordered and you only need values (3Sum) → **sort, then pointers**, because skipping repeated values is easier on sorted data.

### When it is really greedy or DP

- **Greedy** when one locally best choice can never hurt later, usually after a sort (intervals by end, jump game with the farthest reach, gas station reset). Try a 3 or 4 element counter-example: if you can't break the greedy in 30 seconds, it's probably right.
- **DP** when a choice costs future options: "at most k transactions", "no two adjacent", "number of ways", "weighted" interval scheduling. The moment a stock problem gets a limit, a fee or a cooldown (#58 → DP), or intervals get a weight (#36 → DP), you have left the array tricks. See the DP repo.
- **Heap** when you need the best of a *changing* set: top k, merging k lists, "next free room" (#37 alt.).

---

## Part 3. Complexity patterns

Every array cost is **(number of passes) × (work per element)**, plus any sort. Count them in that order.

| Pattern | Time | Extra space | Why |
|---|---|---|---|
| One pass with `O(1)` work (running min, Kadane, Boyer-Moore, greedy reach) | `O(n)` | `O(1)` | one pass, constant work per element |
| Hash set / map build + lookups | `O(n)` average | `O(n)` | each insert and lookup is `O(1)` average; worst case `O(n)` per op with bad hashing |
| Frequency over a fixed alphabet (26 letters) | `O(n)` | `O(1)` | the table size doesn't grow with `n` |
| Two pointers moving one way each | `O(n)` | `O(1)` | together the pointers move at most `n` steps |
| Sliding window (variable) | `O(n)` | `O(1)` or `O(k)` | `right` moves `n` times and `left` moves at most `n` times *in total*; the inner `while` is amortised, not nested |
| Fixed window, update by add-one-remove-one | `O(n)` | `O(1)` or `O(k)` | `O(1)` per slide; recomputing each window costs `O(nk)` |
| Monotonic deque / stack | `O(n)` | `O(k)` or `O(n)` | each element is pushed once and popped once, so at most `2n` operations |
| Prefix sums: build, then queries | `O(n)` build, `O(1)` per query | `O(n)` | one pass to build; a range sum is two lookups |
| Prefix sum + hash map | `O(n)` | `O(n)` | one pass, one map entry per distinct prefix |
| Prefix and suffix passes | `O(n)` | `O(1)` extra if the output array doubles as the first pass | two linear passes |
| Sort + scan (intervals, 3Sum's outer sort, h-index) | `O(n log n)` | `O(1)` to `O(n)` | the sort dominates the linear scan after it |
| 3Sum: sort + one pointer pair per element | `O(n²)` | `O(1)` | `n` runs of an `O(n)` pointer sweep; the sort is smaller than that |
| Nested loops over all pairs | `O(n²)` | `O(1)` | `n(n-1)/2` pairs, the brute force to quote |
| All stretches, each re-summed | `O(n³)` | `O(1)` | `n²` stretches × `O(n)` to sum |
| Bucket / counting by frequency or by value range | `O(n)` | `O(n)` | no comparisons; the buckets are bounded by `n` or the value range |
| Heap of size k over `n` items | `O(n log k)` | `O(k)` | `n` pushes of `O(log k)` |
| Binary search | `O(log n)` per query | `O(1)` | halves the range each step |
| Binary search on the answer | `O(n log range)` | `O(1)` | `log range` rounds, each a linear feasibility check |
| Matrix `m × n` visited once | `O(m·n)` | `O(1)` if done in place | every cell is touched a constant number of times |
| Parsing / simulating a string | `O(n)` | `O(n)` for the result | one scan; build in a list and `join` |

**How to work out complexity (say it in this order):**
1. **Count the passes.** One loop over the data is `O(n)`. Two sequential loops are still `O(n)` (add, don't multiply).
2. **Look at the work per element.** Constant-time operations (a hash lookup, an index, a comparison) cost `O(1)`. A nested loop that restarts for every element multiplies. A nested loop whose pointer only moves forward and never resets is **amortised**: add up total pointer movement instead of multiplying.
3. **Add the sort, if any.** `O(n log n)` for the sort + the scan after it. The bigger term wins.
4. **Space = what you store.** Hash map or prefix array: `O(n)`. Pointers and counters: `O(1)`. A fixed 26-slot table: `O(1)`. The returned answer is usually not counted as extra space (say so).
5. **Check the hidden costs:** `x in some_list` is `O(n)` (use a set); `list.pop(0)` and `list.insert(0, x)` are `O(n)` (use a deque); string `s += ch` in a loop is `O(n²)` (use a list and `join`); slicing `s[i:j]` copies, so a loop of slices is `O(n·m)`; `sorted(word)` inside a loop is `O(k log k)` per word.

**Rules of thumb**
- **A sliding window with a `while` inside a `for` is still `O(n)`.** Every element enters once and leaves at most once. Say "amortised".
- **`O(1)` extra space with a sort** really means `O(1)` beyond Python's sort. State the assumption out loud.
- **Hashing trades space for time.** If the interviewer says "no extra memory", the answer usually becomes sort + pointers (`O(n log n)`, `O(1)`) or an in-place index trick.
- **Hash worst case is `O(n)` per operation** (bad hashing, adversarial keys). Quote "average `O(1)`" and mention it if asked.
- **A stream or a huge input** rules out sorting everything. Think windows, running state, or a heap of size k.
- **Overflow:** Python ints don't overflow, but in Java/C++ the product in #31 or a sum of large values does. Say "I'd use `long`".

---

## Part 4. The scenarios

Each entry has: **Original question** (the formal LeetCode statement), then **Scenario** (what you'd actually hear), **Ask first**, **Spot it** (the clue that reveals the technique), **Brute force** (the naive answer and its cost), **Solve** (the answer from your write-up), **Cost** (time and space, with the reasoning), **Follow-up** (what they'd push on), and **two more variants (A and B)** on the same pattern. Each variant gives the formal **Question** first, then the disguised **Scenario**, then **Pattern and cost**. Variants marked **(crossover)** leave the entry's technique on purpose, to show you where it stops working. A variant with no LC number is a classic interview question that has no single canonical LeetCode entry.

---

### Topic 1. Arrays & Hashing

---

### 1. Contains Duplicate (#1)

**Original question:** LC 217. Given an integer array `nums`, return `true` if any value appears at least twice, and `false` if every element is distinct.

**Scenario:** Before the nightly settlement run, you are handed the day's feed of transaction IDs. Tell me whether any ID was submitted more than once.

**Ask first:**
1. How many IDs can there be, and do they fit in memory?
2. Do you only need yes/no, or also which IDs repeated?

**Spot it:** "Was anything submitted more than once" is a *membership* question: for each new item, "have I already seen it?"

**Brute force:** Compare every pair, `O(n²)` time, `O(1)` space. Or sort and compare neighbours, `O(n log n)`. Both repeat work: the pair check re-scans old items for every new one.

**Solve:** ([01-contains-duplicate.md](01-arrays-and-hashing/01-contains-duplicate.md))
```python
def containsDuplicate(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

**Cost:** One pass, `O(1)` average per `in` and `add`, so `O(n)` time. `seen` can hold all `n` items when there's no repeat: `O(n)` space. It exits early at the first repeat.
**Follow-up:** *O(1) space?* Sort in place and compare neighbours, `O(n log n)`. *Values are `1..n`?* Use the array itself as the hash (see Variant B). *Stream or too big for memory?* Use a Bloom filter for "probably seen" or an external sort. *Return the repeated IDs?* Keep a second set `dups`.

**More scenarios on the same pattern**

**Variant A (crossover to Floyd / binary search, no spare memory)**
- **Question:** LC 287 Find the Duplicate Number. `nums` has `n + 1` integers, each in `1..n`, with exactly one value repeated (possibly more than twice). Return it without modifying the array and using only `O(1)` extra space.
- **Scenario:** A badge scanner logged `n + 1` visits from `n` possible badge numbers; exactly one badge number was reused. The scanner has almost no memory and its log is read-only. Which number was reused?
- **Pattern and cost:** A set is `O(n)` space and breaks the rule. Treat `i → nums[i]` as a linked list; the repeat is where two paths meet, so Floyd's slow/fast cycle detection finds it in `O(n)` time, `O(1)` space. Or binary search on the value range, counting how many entries are `≤ mid`, `O(n log n)`. Sorting would mutate the input.

**Variant B (crossover to using the array as the hash)**
- **Question:** LC 442 Find All Duplicates in an Array. `nums` has `n` integers in `1..n`; each value appears once or twice. Return all values that appear twice in `O(n)` time and `O(1)` extra space.
- **Scenario:** A warehouse counts `n` bins labelled `1..n`. A tally sheet lists bin labels visited, each at most twice. List the labels visited twice without any scratch space.
- **Pattern and cost:** Value `v` points at index `v - 1`. Flip that cell's sign when you visit it; if it's already negative, `v` is a repeat. `O(n)` time, `O(1)` space, but it **mutates** the input (restore the signs after). Valid only because the values are `1..n`.

---

### 2. Valid Anagram (#2)

**Original question:** LC 242. Given two strings `s` and `t`, return `true` if `t` is an anagram of `s` (same letters with the same counts), and `false` otherwise.

**Scenario:** A spell-checker has two typed codes and must say whether they use exactly the same letters, just shuffled.

**Ask first:**
1. Lowercase English letters only, or arbitrary Unicode?
2. Is the comparison case-sensitive, and are spaces significant?

**Spot it:** "Same letters, same counts, order irrelevant" is a *bag* comparison. A bag is a frequency table.

**Brute force:** Sort both and compare, `O(n log n)`. Or try every rearrangement, `O(n!)`. Sorting works but pays for ordering you never needed.

**Solve:** ([02-valid-anagram.md](01-arrays-and-hashing/02-valid-anagram.md))
```python
from collections import Counter

def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)
```

**Cost:** Each `Counter` reads its string once: `O(n)`. Comparing counters is `O(k)` for `k` distinct characters (`k ≤ n`). Space `O(k)`; with 26 lowercase letters that's `O(1)`.
**Follow-up:** *Unicode?* Keep the dict, size grows with distinct characters. *O(1) space and a tiny alphabet?* A 26-slot array, add for `s`, subtract for `t`, check all zeros. *Many strings to compare?* Use the sorted string or a count tuple as a canonical key (#4).

**More scenarios on the same pattern**

**Variant A (crossover to a fixed window)**
- **Question:** LC 438 Find All Anagrams in a String. Given `s` and `p`, return every start index in `s` where a substring is an anagram of `p`.
- **Scenario:** A fraud team has a long stream of characters from a log and a 5-letter flagged code. Report every position where those same five letters appear, in any order.
- **Pattern and cost:** One frequency table is not enough, because the candidate slides along `s`. Keep a fixed-size window of length `len(p)`, add one letter and remove one. `O(n)` time, `O(1)` space (26 slots). Rebuilding the count for every start would be `O(n·len(p))`.

**Variant B (crossover to "first" with a second pass)**
- **Question:** LC 387 First Unique Character in a String. Return the index of the first character that appears only once in `s`, or `-1`.
- **Scenario:** Users type a code and the app must highlight the first character that nobody else in the code repeats.
- **Pattern and cost:** Pass 1 builds the counts; pass 2 walks the string in original order and returns the first index whose count is 1. Two passes, `O(n)` time, `O(1)` space for 26 letters. Order matters here, so a bare `Counter` is not enough; you need the second scan.

---

### 3. Two Sum (#3)

**Original question:** LC 1. Given an integer array `nums` and an integer `target`, return the indices of the two numbers that add up to `target`. Exactly one solution exists and you may not use the same element twice.

**Scenario:** A gift card has exactly `B` dollars on it. The menu lists dish prices in the order they're printed. Which two dishes (by their position on the menu) use up the card exactly?

**Ask first:**
1. Is there exactly one answer, or could there be several or none?
2. Can the same dish be chosen twice, and can prices be negative or zero?

**Spot it:** "Two items, exact total, return their positions, input not ordered." For each dish, the other dish is *forced*: it must cost `B - price`.

**Brute force:** Try every pair, `O(n²)` time, `O(1)` space. For each item you re-scan the whole list to look for its partner.

**Solve:** ([03-two-sum.md](01-arrays-and-hashing/03-two-sum.md))
```python
def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}                          # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i                  # store AFTER the check
```

**Cost:** One pass, one `O(1)` lookup and one `O(1)` insert per item: `O(n)` time. The map holds up to `n` entries: `O(n)` space. The check-before-store order stops an item pairing with itself and still handles `[3, 3]`.
**Follow-up:** *Already in order and `O(1)` space?* Two pointers (#17). *Stream of numbers arriving over time?* Same map, but now a "find" costs `O(n)` or an "add" does (Variant A). *Return all pairs?* The map must hold lists of indices. *Overflow?* `target - num` can overflow in a fixed-width language.

**More scenarios on the same pattern**

**Variant A (crossover to a data-structure design / stream)**
- **Question:** LC 170 Two Sum III - Data structure design (premium). Design a class with `add(number)` and `find(value)`; `find` returns whether any two stored numbers sum to `value`.
- **Scenario:** A cashier terminal keeps receiving coupon values all day. At any moment a manager asks "can two coupons I've already got cover a bill of exactly V?"
- **Pattern and cost:** Keep a `Counter` of values. `add` is `O(1)`; `find` loops over distinct values and looks up `V - x` in `O(1)`, so `O(n)` per find. (Keep a sorted list instead and `find` becomes two pointers, `O(n)`, but `add` costs `O(n)`.) State the trade-off: it depends on which operation is called more.

**Variant B (crossover from "exact sum" to "remainder")**
- **Question:** LC 1010 Pairs of Songs With Total Durations Divisible by 60. Given `time[i]` (durations in seconds), return the number of pairs `i < j` with `(time[i] + time[j]) % 60 == 0`.
- **Scenario:** A radio station fills its hour in 60-second slots. Given the lengths of tracks, how many pairs of tracks would fill a whole number of minutes together?
- **Pattern and cost:** Same complement idea, but the complement of `r = t % 60` is `(60 - r) % 60`. Count how many earlier tracks have each remainder (60 slots) and add on the fly. `O(n)` time, `O(1)` space (60 slots). The `% 60` on the complement handles the `r = 0` case.

---

### 4. Group Anagrams (#4)

**Original question:** LC 49. Given an array of strings `strs`, group the anagrams together. Return the groups in any order.

**Scenario:** A search team wants to cluster logged keywords so that every shuffled spelling of the same letters lands in one bucket.

**Ask first:**
1. Lowercase letters only, or any characters? Is the order of the groups or of words inside a group important?
2. How many words, and how long can a word be?

**Spot it:** "Group the equivalent ones" means *give every item a label that is identical for equivalent items*, then bucket by label (a **canonical key**).

**Brute force:** Compare every pair of words as anagrams and merge groups: `O(n²·k)`. Re-comparing words that are already known to be related wastes work.

**Solve:** ([04-group-anagrams.md](01-arrays-and-hashing/04-group-anagrams.md))
```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for word in strs:
        key = "".join(sorted(word))
        groups[key].append(word)
    return list(groups.values())
```

**Cost:** For `n` words of length up to `k`: sorting each word is `O(k log k)`, so `O(n·k log k)` time. Worst case (no two words alike) the map holds every word plus its key: `O(n·k)` space. Faster key: a 26-count tuple makes each word `O(k)`, so `O(n·k)` total.
**Follow-up:** *Faster than sorting each word?* Count tuple as the key. *Too many words for memory?* Hash the key and shard by hash. *Case/punctuation?* Normalise before computing the key. *Return the largest group only?* Track the max size while inserting.

**More scenarios on the same pattern**

**Variant A (crossover to a different canonical key)**
- **Question:** LC 249 Group Shifted Strings (premium). Two strings are in the same group if one can be shifted letter-by-letter (wrapping `z → a`) into the other. Group the given strings.
- **Scenario:** A cipher tool receives words that were all Caesar-shifted by different amounts. Cluster the words that came from the same original.
- **Pattern and cost:** The key is the *difference between neighbouring letters* (mod 26), the same for every shift. `O(n·k)` time, `O(n·k)` space. The skill is inventing the canonical form, not the hash map.

**Variant B (crossover to two-level hashing)**
- **Question:** LC 609 Find Duplicate File in System. Given directory listings of the form `"dir file1.txt(content) file2.txt(content)"`, return groups of paths whose files have identical content.
- **Scenario:** A storage team wants to find files in a big drive that have identical content, so they can delete copies.
- **Pattern and cost:** Key = file content; value = list of paths. `O(total characters)`. For huge files, first group by size (cheap), then by a hash of the first few KB, and only then by full content: each level shrinks the comparison set.

---

### 5. Top K Frequent Elements (#5)

**Original question:** LC 347. Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. The answer is unique.

**Scenario:** An analytics dashboard has a raw click log of button IDs and must show the `k` buttons that got clicked the most.

**Ask first:**
1. How large is `k` compared with the number of distinct buttons? Is the answer order important?
2. How are ties broken, if they can happen?

**Spot it:** "Most common" is two steps: *count*, then *pick the best by count*. Counts are bounded by `n`, so you can bucket by count instead of sorting.

**Brute force:** Count, then sort all distinct values by count: `O(n log n)`. Or for each of `k` rounds scan for the max: `O(n·k)`.

**Solve:** ([05-top-k-frequent-elements.md](01-arrays-and-hashing/05-top-k-frequent-elements.md))
```python
def topKFrequent(nums: list[int], k: int) -> list[int]:
    count = {}
    freq = [[] for _ in range(len(nums) + 1)]   # index = frequency
    for n in nums:
        count[n] = 1 + count.get(n, 0)
    for n, c in count.items():
        freq[c].append(n)

    res = []
    for i in range(len(freq) - 1, 0, -1):       # highest frequency first
        for n in freq[i]:
            res.append(n)
            if len(res) == k:
                return res
```

**Cost:** Counting is one pass; filling the buckets loops over at most `n` distinct values; the walk touches `n + 1` buckets and at most `n` stored values: `O(n)` time, `O(n)` space. A heap of size `k` instead is `O(n log k)` time and `O(n)` for the counts.
**Follow-up:** *Huge stream?* Counting sketch (count-min) plus a heap for approximate top-k. *Only the top 1?* A single pass tracking the max. *`k` close to `n`?* Sorting or buckets beats a heap. *Ties alphabetical?* See Variant A.

**More scenarios on the same pattern**

**Variant A (crossover to a heap, ties)**
- **Question:** LC 692 Top K Frequent Words. Return the `k` most frequent words, sorted by frequency high to low, and alphabetically for equal frequency.
- **Scenario:** A search box shows the `k` most-typed queries; when two queries are tied, the alphabetically earlier one wins.
- **Pattern and cost:** Buckets still work, but each bucket must be sorted alphabetically. Or a min-heap of size `k` keyed on `(count, reversed word order)`: `O(n log k)`. The tie-break is the point; say how you'd encode it.

**Variant B (crossover to selection, no counts)**
- **Question:** LC 215 Kth Largest Element in an Array. Return the `k`-th largest element (not the k-th distinct).
- **Scenario:** A leaderboard has `n` scores. Display the score that sits exactly in `k`-th place.
- **Pattern and cost:** No frequencies, so no buckets. Min-heap of size `k`: `O(n log k)` time, `O(k)` space. Quickselect: `O(n)` average, `O(n²)` worst, mutates the array. Sorting: `O(n log n)`.

---

### 6. Longest Consecutive Sequence (#6)

**Original question:** LC 128. Given an unsorted array of integers `nums`, return the length of the longest sequence of consecutive values (like `3, 4, 5, 6`). The algorithm must run in `O(n)` time.

**Scenario:** A raffle sold tickets with scattered numbers, in no particular order. What's the longest stretch of back-to-back ticket numbers that were all sold?

**Ask first:**
1. Can numbers repeat, and can they be negative?
2. Must it be `O(n)`, or is `O(n log n)` acceptable?

**Spot it:** "Back-to-back values, order in the list irrelevant." The positions in the list don't matter; only *membership* of `x + 1` does. And you must start counting only at the *beginning* of a run.

**Brute force:** For each number, count upward by scanning the list each time: `O(n²)` or `O(n³)`. Or sort first: `O(n log n)`. The `O(n)` requirement rules sorting out.

**Solve:** ([06-longest-consecutive-sequence.md](01-arrays-and-hashing/06-longest-consecutive-sequence.md))
```python
def longestConsecutive(nums: list[int]) -> int:
    nums_set = set(nums)
    longest = 0
    for num in nums_set:
        if (num - 1) not in nums_set:       # only start at the beginning of a run
            length = 0
            while num + length in nums_set:
                length += 1
            longest = max(longest, length)
    return longest
```

**Cost:** Building the set is `O(n)`. The inner `while` runs only from run starts, and every number is stepped over by at most one run, so all `while` steps total at most `n`: `O(n)` time, `O(n)` space. This is amortised, not `O(n²)`.
**Follow-up:** *No extra memory?* Sort in place, `O(n log n)`, scan runs. *Return the run itself?* Remember the start. *Stream?* Union-find with union of `x` with `x - 1` and `x + 1`. *Numbers up to 10⁹?* The set doesn't care; a boolean array would.

**More scenarios on the same pattern**

**Variant A (crossover: pairs one apart, counts)**
- **Question:** LC 594 Longest Harmonious Subsequence. A harmonious array has max − min exactly 1. Return the length of the longest harmonious subsequence of `nums`.
- **Scenario:** Athletes' ages are logged; find the largest team in which everyone is either age `a` or age `a + 1`, for some `a`.
- **Pattern and cost:** Order doesn't matter (subsequence), so count each value, then for every `x` with `x + 1` present take `count[x] + count[x + 1]`. `O(n)` time, `O(n)` space. Note: counts, not a run, unlike #6.

**Variant B (crossover to math / XOR)**
- **Question:** LC 268 Missing Number. `nums` has `n` distinct numbers taken from `0..n`. Return the one missing number.
- **Scenario:** Packages are numbered `0` to `n`; one is missing from the delivery manifest. Which one?
- **Pattern and cost:** A set works (`O(n)` space) but there's an `O(1)` space trick: expected sum `n(n + 1)/2` minus actual sum, or XOR of all indices and values. Mention overflow for the sum in fixed-width languages; XOR avoids it.

---

### 7. Encode and Decode Strings (#7)

**Original question:** LC 271 (premium). Design `encode(strs)` that turns a list of strings into one string and `decode(s)` that turns it back into the original list. The strings can contain any characters.

**Scenario:** A messaging channel can carry only one text string per message. Pack a list of user comments into it so the receiver gets back the exact same list, whatever characters people typed.

**Ask first:**
1. Can the comments be empty, or contain separators like `,` or `#`, or digits?
2. Is the list itself ever empty, and must that be distinguishable from a list of one empty comment?

**Spot it:** Any plain delimiter can appear inside the data. So the fix is *describe the length first*, so the reader never has to guess where a piece ends.

**Brute force:** Join with a separator like `","` and split. It breaks the moment a comment contains the separator. Escaping works but needs more rules and extra passes.

**Solve:** ([07-encode-and-decode-strings.md](01-arrays-and-hashing/07-encode-and-decode-strings.md))
```python
def encode(strs: list[str]) -> str:
    return "".join(f"{len(s)}#{s}" for s in strs)

def decode(s: str) -> list[str]:
    res, i = [], 0
    while i < len(s):
        j = i
        while s[j] != "#":                 # find end of the length
            j += 1
        length = int(s[i:j])
        res.append(s[j + 1 : j + 1 + length])
        i = j + 1 + length                 # jump past the content
    return res
```

**Cost:** For `n` total characters: `encode` is `O(n)` when pieces are joined once (repeated `+=` can be `O(n²)`). `decode` moves `i` and `j` only forward and copies each piece once: `O(n)`. Space `O(n)`.
**Follow-up:** *Binary data / huge strings?* Use a fixed-width length header (4 bytes). *Streaming decode?* Works as-is, since it only reads forward. *Corrupted input?* Validate that `s[j]` exists and the length fits.

**More scenarios on the same pattern**

**Variant A (crossover to a tree)**
- **Question:** LC 297 Serialize and Deserialize Binary Tree. Design an algorithm to turn a binary tree into a string and back.
- **Scenario:** A game saves a branching dialogue to disk as one line of text and loads it back exactly.
- **Pattern and cost:** Same principle (unambiguous encoding), but structure comes from pre-order traversal with explicit null markers (`#`). `O(n)` time and space. See the Trees repo.

**Variant B (crossover to run-length compression)**
- **Question:** LC 443 String Compression. Compress a character array in place using counts for runs (`"aabbbc"` → `"a2b3c"`), returning the new length. Use only `O(1)` extra space.
- **Scenario:** A fax-style device sends a line of marks; consecutive repeats must be replaced with the mark and its count, rewriting the same buffer.
- **Pattern and cost:** A read/write pointer pair (Topic 7 technique) on a string. `O(n)` time, `O(1)` space. Watch counts ≥ 10: write each digit as its own character. Not yet written up in this repo (#79).

---

### 8. Insert Delete GetRandom O(1) (#8)

**Original question:** LC 380. Implement `RandomizedSet` with `insert(val)`, `remove(val)` and `getRandom()`, each in average `O(1)` time. `getRandom` returns each current element with equal probability.

**Scenario:** A lottery app keeps a pool of active ticket IDs. People enter and withdraw all the time, and at draw time the app picks a uniformly random winner. All three actions must be near-instant, even with millions of tickets.

**Ask first:**
1. Can the same ID be inserted twice, and what should `insert`/`remove` return when it's a no-op?
2. Is `getRandom` ever called on an empty pool?

**Spot it:** Fast lookup *and* fast random pick *and* fast delete. A hash map can't pick randomly; an array can't delete from the middle quickly. Combine them, and delete by **swapping with the last element**.

**Brute force:** A list: `insert` is `O(1)`, but `remove` is `O(n)` (find, then shift) and a set can't do `getRandom` in `O(1)`. Converting a set to a list per draw is `O(n)`.

**Solve:** ([08-insert-delete-getrandom-o1.md](01-arrays-and-hashing/08-insert-delete-getrandom-o1.md))
```python
import random

class RandomizedSet:
    def __init__(self):
        self.num_map = {}      # value -> index in nums
        self.nums = []

    def insert(self, val: int) -> bool:
        if val in self.num_map:
            return False
        self.num_map[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.num_map:
            return False
        last_val, idx = self.nums[-1], self.num_map[val]
        self.nums[idx] = last_val          # overwrite the hole with the last item
        self.num_map[last_val] = idx
        self.nums.pop()
        del self.num_map[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)
```

**Cost:** Each operation is a few dict lookups plus list operations at the end or at a known index: `O(1)` average. Space `O(n)` for the list and the map. The invariant `nums[num_map[v]] == v` is what keeps `getRandom` uniform.
**Follow-up:** *Duplicates allowed?* Map each value to a set of indices (Variant A). *Weighted random?* Prefix sums + binary search (Variant B). *Thread safety?* Lock around the swap. *Remove the last item itself?* It overwrites itself, then pops: still correct.

**More scenarios on the same pattern**

**Variant A (crossover: duplicates)**
- **Question:** LC 381 Insert Delete GetRandom O(1) - Duplicates allowed. Same API, but a value can be inserted many times; `getRandom` is proportional to the number of copies.
- **Scenario:** A raffle lets people buy several tickets of the same colour; drawing should favour colours with more tickets.
- **Pattern and cost:** `value → set of indices`. On remove, pop any index of the value, move the last element into that hole, and fix both index sets. `O(1)` average per operation.

**Variant B (crossover to prefix sums + binary search)**
- **Question:** LC 528 Random Pick with Weight. Given weights `w`, implement `pickIndex()` that returns index `i` with probability `w[i] / sum(w)`.
- **Scenario:** An ad server must choose one of several campaigns at random, with chance proportional to each campaign's budget.
- **Pattern and cost:** Build prefix sums of the weights once (`O(n)`), pick a random number in `[1, total]`, and binary search the first prefix that is ≥ it: `O(log n)` per pick, `O(n)` space.

---

### 9. Isomorphic Strings (#9)

**Original question:** LC 205. Two strings `s` and `t` are isomorphic if the characters of `s` can be replaced to get `t`, where every occurrence maps to the same character, no two characters map to the same one, and order is preserved.

**Scenario:** Two coded messages arrive. Decide whether one could have been produced from the other by a consistent letter-for-letter substitution, where no two different letters were turned into the same one.

**Ask first:**
1. Same length guaranteed? Can a letter map to itself?
2. Does "no two letters share a cipher letter" apply in both directions?

**Spot it:** "Consistent substitution, no two to the same" is a *two-way* mapping. One map can't catch `"ab" → "aa"`.

**Brute force:** Try every possible mapping: exponential. Or for every pair of positions compare equality in `s` and `t`: `O(n²)`.

**Solve:** ([09-isomorphic-strings.md](01-arrays-and-hashing/09-isomorphic-strings.md))
```python
def isIsomorphic(s: str, t: str) -> bool:
    map_st, map_ts = {}, {}
    for a, b in zip(s, t):
        if a in map_st and map_st[a] != b:
            return False
        if b in map_ts and map_ts[b] != a:
            return False
        map_st[a], map_ts[b] = b, a
    return True
```

**Cost:** One pass with `O(1)` average dict operations: `O(n)` time. Each map has at most one entry per distinct character: `O(k)` space, `O(1)` for a fixed alphabet.
**Follow-up:** *Compare to many strings?* Normalise each to a first-occurrence pattern (Variant B). *Unicode?* Maps grow, same logic. *One map only?* A set of already-used targets does the same job as the second map.

**More scenarios on the same pattern**

**Variant A (crossover to backtracking)**
- **Question:** LC 291 Word Pattern II (premium). Given a `pattern` and a string `s`, decide whether `s` can be split into non-empty pieces so that pattern letters map one-to-one to those pieces.
- **Scenario:** A template says "A B B A" but the sentence has no spaces. Can the text be cut up so the template holds?
- **Pattern and cost:** The cut points are unknown, so a map alone can't decide; you must *try* cut points (backtracking with the same two maps). Exponential worst case. This is where the hash approach stops working.

**Variant B (crossover to canonical-key grouping)**
- **Question:** Given a list of strings, group those that are isomorphic to each other (classic; related to LC 205 and LC 890).
- **Scenario:** A fraud team wants to cluster transaction codes that follow the same repetition shape, like `XYYZ` and `ABBC`, whatever the letters are.
- **Pattern and cost:** Convert each string to its first-occurrence shape (`"abbc"` → `[0,1,1,2]`) and use it as a hash key (#4's idea). `O(n·k)` time, `O(n·k)` space.

---

### 10. Ransom Note (#10)

**Original question:** LC 383. Given `ransomNote` and `magazine`, return `true` if `ransomNote` can be built using letters from `magazine`. Each letter in `magazine` can be used once.

**Scenario:** A scrapbook maker has a sheet of letter stickers and wants to know whether they have enough stickers of each letter to spell a message.

**Ask first:**
1. Only lowercase letters? Is case important?
2. Does each sticker really get used only once?

**Spot it:** Supply and demand. Count what's available, then spend it.

**Brute force:** For each letter of the note, search the magazine and delete it: `O(n·m)`.

**Solve:** ([10-ransom-note.md](01-arrays-and-hashing/10-ransom-note.md))
```python
from collections import defaultdict

def canConstruct(ransomNote: str, magazine: str) -> bool:
    count = defaultdict(int)
    for char in magazine:
        count[char] += 1
    for char in ransomNote:
        if count[char] <= 0:
            return False
        count[char] -= 1
    return True
```

**Cost:** One pass over each string: `O(m + n)` time. `O(k)` space, `O(1)` for 26 letters.
**Follow-up:** *Early exit when the note is longer than the magazine?* Yes. *Unicode?* The dict handles it. *Many notes against one magazine?* Build the supply once.

**More scenarios on the same pattern**

**Variant A (crossover: many words, one supply)**
- **Question:** LC 1160 Find Words That Can Be Formed by Characters. Given `words` and a string `chars`, return the sum of lengths of words that can be formed from `chars` (each letter used once per word).
- **Scenario:** A letter-tile game gives a rack of tiles. Score the total length of the dictionary words playable from that rack (each word judged on its own).
- **Pattern and cost:** Build the rack count once; for each word, compare its count. `O(total characters)`.

**Variant B (crossover to "steps" instead of yes/no)**
- **Question:** LC 1347 Minimum Number of Steps to Make Two Strings Anagram. Given equal-length `s` and `t`, return the minimum number of characters you must replace in `t` to make it an anagram of `s`.
- **Scenario:** Two label printers must end up with the same multiset of letters; count the fewest letters one printer has to swap out.
- **Pattern and cost:** Count `s` minus count `t`; the answer is the sum of positive differences. `O(n)` time, `O(1)` space.

---

### 11. Word Pattern (#11)

**Original question:** LC 290. Given a `pattern` and a string `s`, return `true` if `s` follows the pattern: there is a one-to-one mapping between letters in `pattern` and words in `s`.

**Scenario:** A style guide has a template like "A B B A". Does a given sentence follow it, with one distinct word per label and no two labels sharing a word?

**Ask first:**
1. Are words separated by exactly one space? Can there be extra spaces?
2. Must pattern length equal the word count?

**Spot it:** Same two-way mapping as #9, now between letters and whole words.

**Brute force:** For every pair of positions compare equality in both sequences: `O(n²)`.

**Solve:** ([11-word-pattern.md](01-arrays-and-hashing/11-word-pattern.md))
```python
def wordPattern(pattern: str, s: str) -> bool:
    words = s.split(" ")
    if len(pattern) != len(words):
        return False
    char_to_word, word_to_char = {}, {}
    for char, word in zip(pattern, words):
        if char in char_to_word and char_to_word[char] != word:
            return False
        if word in word_to_char and word_to_char[word] != char:
            return False
        char_to_word[char], word_to_char[word] = word, char
    return True
```

**Cost:** `split` is `O(n)` and the loop is one pass with `O(1)` dict operations: `O(n)` time, `O(n)` space (the word list and maps).
**Follow-up:** *Multiple spaces?* `split()` without an argument. *Check the length first?* Yes, before touching the maps. *Huge sentence?* Iterate words lazily.

**More scenarios on the same pattern**

**Variant A (crossover: pattern applied to a list of words)**
- **Question:** LC 890 Find and Replace Pattern. Given a list of `words` and a `pattern`, return the words that match the pattern under some one-to-one letter mapping.
- **Scenario:** From a dictionary, list the words that have the same repeating shape as "ABBA" (a letter repeated in the same places).
- **Pattern and cost:** Run the two-way check (or compare first-occurrence shapes) for each word. `O(n·k)` for `n` words of length `k`.

**Variant B (crossover to union-find)**
- **Question:** LC 737 Sentence Similarity II (premium). Two sentences are similar if the words at each position are equal or connected through pairs of similar words (similarity is transitive).
- **Scenario:** A recommender treats words as synonyms if they were paired, and also if they are linked through a chain of pairs. Are two sentences equivalent word by word?
- **Pattern and cost:** A plain map only catches direct pairs. Transitivity turns the pairs into a graph, so use union-find or BFS (Graphs repo). This is where hashing stops being enough.

---

### 12. Contains Duplicate II (#12)

**Original question:** LC 219. Given an integer array `nums` and an integer `k`, return `true` if there are two distinct indices `i` and `j` with `nums[i] == nums[j]` and `abs(i - j) <= k`.

**Scenario:** A rate-limiter flags a user ID if it appears twice among any `k` consecutive requests.

**Ask first:**
1. Is `k` inclusive (distance of exactly `k` counts)?
2. Can `k` be `0`, or larger than the list?

**Spot it:** "Seen before" plus a distance limit. The only occurrence that matters is the *latest* one, since it's the closest.

**Brute force:** Check every pair within distance `k`: `O(n·k)`. Or all pairs, `O(n²)`.

**Solve:** ([12-contains-duplicate-ii.md](01-arrays-and-hashing/12-contains-duplicate-ii.md))
```python
def containsNearbyDuplicate(nums: list[int], k: int) -> bool:
    seen = {}                                  # value -> most recent index
    for i, num in enumerate(nums):
        if num in seen and i - seen[num] <= k:
            return True
        seen[num] = i                          # always overwrite with the latest index
    return False
```

**Cost:** One pass with `O(1)` dict operations: `O(n)` time. One entry per distinct value: `O(n)` space (a set limited to the last `k` items would be `O(k)`).
**Follow-up:** *`O(k)` memory?* Keep a set of the last `k` items and evict `nums[i - k]` as you go. *Also close in value (±t)?* Variant A. *Stream?* Same map, works online.

**More scenarios on the same pattern**

**Variant A (crossover to buckets / ordered set)**
- **Question:** LC 220 Contains Duplicate III. Return `true` if there are two distinct indices `i`, `j` with `abs(i - j) <= indexDiff` and `abs(nums[i] - nums[j]) <= valueDiff`.
- **Scenario:** A monitoring tool flags two sensor readings that are close in time (within `k` readings) and also close in value (within `t`).
- **Pattern and cost:** Equality is no longer enough, so a plain map fails. Bucket values by width `t + 1`: neighbours can only be in the same or adjacent bucket. `O(n)` time, `O(k)` space. (Or a sorted set, `O(n log k)`.)

**Variant B (crossover to a design problem)**
- **Question:** LC 359 Logger Rate Limiter (premium). Implement `shouldPrintMessage(timestamp, message)` returning `true` only if the message has not been printed in the last 10 seconds.
- **Scenario:** A logging service must not repeat the same message within 10 seconds.
- **Pattern and cost:** Map `message → last time printed`. `O(1)` per call; memory grows with distinct messages, so clean up old keys (or use a queue of recent messages) if the stream is unbounded.

---

### 13. Happy Number (#13)

**Original question:** LC 202. A number is happy if repeatedly replacing it with the sum of the squares of its digits eventually reaches `1`. If it loops forever in a cycle that doesn't include `1`, it isn't. Return whether `n` is happy.

**Scenario:** A puzzle game applies a rule over and over to a score: replace it with the sum of the squares of its digits. Will the score eventually become 1, or will it go round in circles forever?

**Ask first:**
1. What is the range of `n`? Can it be `0`?
2. Do you want the number of steps, or only yes/no?

**Spot it:** A deterministic sequence that either ends or repeats. "Repeats" means the same value shows up twice, and "have I seen this?" detects that.

**Brute force:** Run until `1`: it never terminates on a loop. A step cap (for example 1000 iterations) works in practice but isn't a proof.

**Solve:** ([13-happy-number.md](01-arrays-and-hashing/13-happy-number.md))
```python
def isHappy(n: int) -> bool:
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(digit) ** 2 for digit in str(n))
    return n == 1
```

**Cost:** The number of digits is `O(log n)`, and after the first step the value is small (three digits at most), so the chain is short: `O(log n)` time and `O(log n)` space for `seen`. Floyd's fast/slow pointers bring space to `O(1)`.
**Follow-up:** *`O(1)` space?* Fast/slow on the sequence. *Prove termination?* Numbers above three digits shrink, so the sequence lives in a small range and must repeat or reach 1. *Avoid the string conversion?* Use `% 10` and `// 10`.

**More scenarios on the same pattern**

**Variant A (crossover to cycle detection on an array)**
- **Question:** LC 457 Circular Array Loop. In `nums`, each value says how many steps to move forward or backward (wrapping around). Return whether there is a cycle of length > 1 that moves in a single direction.
- **Scenario:** A board game gives every square a "jump this many squares" instruction (forward or back, wrapping around the board). Could a token get stuck in a loop of two or more squares?
- **Pattern and cost:** Not a set problem: treat `i → (i + nums[i]) % n` as a linked list and run slow/fast pointers, checking direction consistency. `O(n)` time, `O(1)` space.

**Variant B (crossover to math)**
- **Question:** LC 258 Add Digits. Repeatedly add all digits of `num` until a single digit remains; return it.
- **Scenario:** A ticket validator repeatedly sums the digits of a ticket number until one digit is left.
- **Pattern and cost:** A loop is `O(log n)`, but there's an `O(1)` closed form: `0` if `num == 0`, otherwise `1 + (num - 1) % 9`. Spotting that no data structure is needed is the lesson.

---

### Topic 2. Two Pointers

---

### 14. Valid Palindrome (#14)

**Original question:** LC 125. A phrase is a palindrome if, after lowercasing and removing all non-alphanumeric characters, it reads the same forward and backward. Given a string `s`, return `true` if it is a palindrome.

**Scenario:** A kiosk checks whether a customer's reference phrase reads the same backward as forward, ignoring spaces, punctuation and capital letters.

**Ask first:**
1. Do digits count as characters? What about an empty string or one with only punctuation?
2. May I build a cleaned copy, or must it use `O(1)` extra space?

**Spot it:** "Reads the same from both ends" is *symmetry*: compare position `i` with position `n - 1 - i`, walking inward.

**Brute force:** Clean the string, reverse it, compare: `O(n)` time, `O(n)` space. Correct, but it builds two extra copies.

**Solve:** ([14-valid-palindrome.md](02-two-pointers/14-valid-palindrome.md))
```python
def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

**Cost:** The pointers only move inward, so together they visit each character at most once (the inner skip loops don't restart): `O(n)` time. Only two indices: `O(1)` space.
**Follow-up:** *Allow one mistake?* #15. *A linked list?* Find the middle, reverse the second half. *Unicode?* `isalnum` works; mention normalisation. *Stream?* Can't do in one pass without storing it.

**More scenarios on the same pattern**

**Variant A (crossover to expand-around-centre / DP)**
- **Question:** LC 5 Longest Palindromic Substring. Return the longest palindromic substring of `s`.
- **Scenario:** A genealogy tool scans a long family-tree code for its longest mirror-symmetric stretch.
- **Pattern and cost:** One pair of pointers isn't enough, because you don't know where the centre is. Expand outward from each of the `2n - 1` centres: `O(n²)` time, `O(1)` space. (A DP table gives the same time with `O(n²)` space; Manacher's gets `O(n)`.)

**Variant B (crossover to a hash count)**
- **Question:** LC 409 Longest Palindrome. Given a string of letters, return the length of the longest palindrome that can be built from its letters (rearranging allowed).
- **Scenario:** From a bag of letter tiles, how long can a mirror-symmetric word be, if you may pick any letters and arrange them freely?
- **Pattern and cost:** Rearrangement means order is irrelevant, so count letters: use every pair, plus one centre if any letter has an odd count. `O(n)` time, `O(1)` space.

---

### 15. Valid Palindrome II (#15)

**Original question:** LC 680. Given a string `s`, return `true` if it can become a palindrome after deleting **at most one** character.

**Scenario:** A vanity-plate checker accepts a plate if it reads the same both ways, or would if you removed at most one character.

**Ask first:**
1. Exactly one deletion, or at most one? (zero is allowed)
2. Lowercase letters only?

**Spot it:** Same inward comparison as #14, but the first mismatch is a *fork*: drop the left character or drop the right one.

**Brute force:** Try deleting each of the `n` characters and check the rest: `O(n²)` time.

**Solve:** ([15-valid-palindrome-ii.md](02-two-pointers/15-valid-palindrome-ii.md))
```python
def validPalindrome(s: str) -> bool:
    def is_pali(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_pali(left + 1, right) or is_pali(left, right - 1)
        left += 1
        right -= 1
    return True
```

**Cost:** The outer scan is at most `n` steps, then at most two `O(n)` checks, only once: `O(n)` time, `O(1)` space. No slicing, so no hidden copies.
**Follow-up:** *At most `k` deletions?* Variant A (DP). *Return which index to delete?* Return whichever branch succeeded. *Why only one fork?* After the single allowed deletion the rest must match exactly, so no further branching.

**More scenarios on the same pattern**

**Variant A (crossover to DP)**
- **Question:** LC 1216 Valid Palindrome III (premium). Return `true` if `s` can become a palindrome by removing at most `k` characters.
- **Scenario:** The plate checker now tolerates up to `k` removed characters.
- **Pattern and cost:** With one deletion there are two branches; with `k`, the branches multiply. Use DP on the longest palindromic subsequence: `n - LPS <= k`. `O(n²)` time, `O(n)` space with rolling rows. See the DP repo.

**Variant B (crossover to two sequences)**
- **Question:** LC 408 Valid Word Abbreviation (premium). Given `word` and `abbr` (where digits stand for a count of skipped letters), return whether `abbr` abbreviates `word`.
- **Scenario:** A directory shows `i12n` for long names. Does the short form match a given full name?
- **Pattern and cost:** One pointer per string, side by side, jumping the word pointer by the parsed number. `O(n + m)` time, `O(1)` space. Watch leading zeros (not allowed).

---

### 16. Is Subsequence (#16)

**Original question:** LC 392. Given strings `s` and `t`, return `true` if `s` is a subsequence of `t` (obtained by deleting some characters of `t` without changing the order of the rest).

**Scenario:** A playlist app has a long radio schedule and a short wish list of songs in a preferred order. Do all the wished songs play in that order, with other songs allowed in between?

**Ask first:**
1. Must the wish-list items be in the same order, and may other items sit between them?
2. One wish list, or millions of them against the same schedule?

**Spot it:** "In order, gaps allowed." Walk the long list once; advance in the short list only when you find its next item.

**Brute force:** Generate all subsequences of `t`: exponential. Or recursion matching/skipping: `O(2^n)`. Greedy earliest-match makes it linear.

**Solve:** ([16-is-subsequence.md](02-two-pointers/16-is-subsequence.md))
```python
def isSubsequence(s: str, t: str) -> bool:
    i = j = 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)
```

**Cost:** `j` scans `t` once and `i` only advances forward: `O(|t|)` time, `O(1)` space.
**Follow-up:** *Millions of queries against one `t`?* Preprocess `t` into `char → sorted index list` and binary search for the next position per character: `O(|t|)` once, `O(|s| log |t|)` per query (Variant A). *Stream?* Works online. *Return the matching indices?* Record them as you go.

**More scenarios on the same pattern**

**Variant A (crossover to binary search)**
- **Question:** LC 792 Number of Matching Subsequences. Given `s` and a list `words`, return how many words are subsequences of `s`.
- **Scenario:** A very long DNA read is checked against thousands of short probes; count how many probes occur in order inside the read.
- **Pattern and cost:** Rescanning `s` per word costs `O(|s|·W)`. Build `char → indices` once, then binary search per character, `O(total word length · log |s|)`. Or bucket words by their next needed letter and sweep `s` once.

**Variant B (crossover to sort + subsequence check)**
- **Question:** LC 524 Longest Word in Dictionary through Deleting. Return the longest word in `dictionary` that is a subsequence of `s`; if tied, the lexicographically smallest.
- **Scenario:** A word-game finds the longest dictionary word that can be spelled by crossing out letters from a rack string.
- **Pattern and cost:** Two-pointer check per word (`O(|s|)` each). Sort the dictionary by (length desc, alphabetical) and return the first match: `O(W log W + W·|s|)`.

---

### 17. Two Sum II - Input Array Is Sorted (#17)

**Original question:** LC 167. Given a 1-indexed array `numbers` sorted in non-decreasing order, find two numbers that add up to `target`. Return their indices (1-indexed). Use only `O(1)` extra space.

**Scenario:** A catalog is listed from cheapest to priciest. A shopper has a voucher for exactly `B` dollars and wants two items that use it up. Report their positions (starting at 1). No scratch memory.

**Ask first:**
1. Exactly one valid pair? Duplicate prices allowed?
2. Can I use extra memory? (If yes, #3's hash map also works.)

**Spot it:** "Already ordered" plus "pair" plus "no extra memory". If the sum is too small you *must* raise the small end; too big, lower the big end.

**Brute force:** All pairs, `O(n²)`. Or a hash map, `O(n)` time but `O(n)` space. Binary search for each complement: `O(n log n)`.

**Solve:** ([17-two-sum-ii.md](02-two-pointers/17-two-sum-ii.md))
```python
def twoSum(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
```

**Cost:** `left` only goes up and `right` only goes down; they meet after at most `n` moves: `O(n)` time, `O(1)` space. Each move discards an element that cannot be in any valid pair.
**Follow-up:** *Unsorted?* Hash map (#3) or sort a copy of `(value, index)` pairs. *All pairs?* Skip duplicates after a hit. *Count of pairs?* Same walk, count and skip equal runs.

**More scenarios on the same pattern**

**Variant A (crossover to "closest")**
- **Question:** LC 16 3Sum Closest. Given `nums` and `target`, return the sum of three integers closest to `target`.
- **Scenario:** A procurement tool picks three parts whose total cost is as close as possible to a budget, not necessarily equal.
- **Pattern and cost:** An exact-match hash lookup can't answer "closest". Sort, fix one, then two pointers on the rest, tracking the best gap. `O(n²)` time, `O(1)` space.

**Variant B (pointers on an implicit range)**
- **Question:** LC 633 Sum of Square Numbers. Given a non-negative integer `c`, return whether there exist integers `a` and `b` with `a² + b² = c`.
- **Scenario:** A tile designer wants to know if a floor area `c` can be covered by two square blocks whose areas add up exactly to `c`.
- **Pattern and cost:** No array exists, but `0..sqrt(c)` is an ordered range. `a = 0`, `b = floor(sqrt(c))`, then move like #17. `O(sqrt c)` time, `O(1)` space.

---

### 18. 3Sum (#18)

**Original question:** LC 15. Given an integer array `nums`, return all triplets `[nums[i], nums[j], nums[k]]` with distinct indices and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets.

**Scenario:** An accounting ledger lists credits and debits. Find every distinct combination of three entries that cancels out to zero, without reporting the same combination twice.

**Ask first:**
1. Do you want values or indices? Can the same value be used in different triplets?
2. Is the order of the triplets, or inside a triplet, important?

**Spot it:** Three items and a fixed total reduce to "fix one, then the pair problem on the rest". "No repeated triplets" means ordering the data so equal values sit together.

**Brute force:** Three nested loops, `O(n³)`, plus a set to remove repeated triples.

**Solve:** ([18-3sum.md](02-two-pointers/18-3sum.md))
```python
def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    for i, a in enumerate(nums):
        if a > 0:
            break
        if i > 0 and nums[i - 1] == a:
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            total = a + nums[l] + nums[r]
            if total > 0:
                r -= 1
            elif total < 0:
                l += 1
            else:
                res.append([a, nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
    return res
```

**Cost:** Sort `O(n log n)`; then `n` outer iterations, each a two-pointer sweep of `O(n)`: `O(n²)` time (the sort is dominated). `O(1)` extra space beyond the output and the sort's internals.
**Follow-up:** *4Sum / kSum?* Wrap another loop per extra number: `O(n^(k-1))` (Variant A). *Unsorted and no sorting allowed?* Hash set per fixed element, but deduplication is harder. *Count only?* Same, no result list.

**More scenarios on the same pattern**

**Variant A (generalising to k)**
- **Question:** LC 18 4Sum. Return all unique quadruplets that sum to `target`.
- **Scenario:** A budget needs every distinct set of four expense lines that adds to a fixed figure.
- **Pattern and cost:** Two nested loops fix two numbers, two pointers do the rest: `O(n³)` time, `O(1)` space. Write a recursive `kSum` that reduces to 2Sum at `k = 2`. Skip duplicates at every level.

**Variant B (counting, not listing)**
- **Question:** LC 259 3Sum Smaller (premium). Count triplets `i < j < k` with `nums[i] + nums[j] + nums[k] < target`.
- **Scenario:** How many ways can a team pick three members whose combined salaries stay under a budget?
- **Pattern and cost:** Sort, fix `i`, and when `nums[i] + nums[l] + nums[r] < target` all `r - l` choices of the middle element work, so add `r - l` and move `l`. `O(n²)` time, `O(1)` space. Sorting is fine because order of indices doesn't matter for the count.

---

### 19. Container With Most Water (#19)

**Original question:** LC 11. Given `height` of `n` vertical lines at positions `0..n-1`, choose two lines that, with the x-axis, form a container holding the most water. Return the maximum amount.

**Scenario:** A street has poles of different heights at equal spacing. A city will stretch a cover between two poles; its capacity is the distance between them times the shorter pole's height. Which pair gives the biggest capacity?

**Ask first:**
1. Does the water level depend on the shorter line only (no tilting)?
2. Are all heights non-negative? Is `n` at least 2?

**Spot it:** Capacity = width × shorter height. Starting at the widest pair, the **shorter pole is the bottleneck**, so moving the taller one can only shrink the area.

**Brute force:** Try every pair, `O(n²)`.

**Solve:** ([19-container-with-most-water.md](02-two-pointers/19-container-with-most-water.md))
```python
def maxArea(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        width = right - left
        max_water = max(max_water, width * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water
```

**Cost:** The pointers move toward each other, `n - 1` steps at most: `O(n)` time, `O(1)` space. Each move discards a pole that can't beat what's already been measured.
**Follow-up:** *Prove the move?* Any container using the shorter pole with a narrower width has height ≤ that pole, so it's no better. *Three poles?* Different problem. *Heights unsorted?* They are, that is the point: the walls themselves aren't ordered, the greedy argument replaces sortedness.

**More scenarios on the same pattern**

**Variant A (crossover: sort + two pointers on weights)**
- **Question:** LC 881 Boats to Save People. Each boat carries at most two people and a weight limit `limit`. Given `people` weights, return the minimum number of boats.
- **Scenario:** A ferry takes at most two passengers per trip within a weight limit. Fewest trips for a queue of people?
- **Pattern and cost:** Sort, then pair the heaviest with the lightest if they fit; otherwise the heaviest goes alone. `O(n log n)` time, `O(1)` extra. The pointers only work *after* sorting.

**Variant B (crossover to a monotonic stack)**
- **Question:** LC 84 Largest Rectangle in Histogram. Given bar heights, return the area of the largest rectangle in the histogram.
- **Scenario:** A billboard company wants the biggest rectangular ad that fits under a skyline of building heights.
- **Pattern and cost:** Two pointers can't decide here, because the rectangle's height comes from a bar *inside* the range. Use a monotonic stack to find, for each bar, the nearest smaller bar on both sides: `O(n)` time, `O(n)` space (Stack repo).

---

### 20. Trapping Rain Water (#20)

**Original question:** LC 42. Given `n` non-negative integers representing an elevation map where each bar has width 1, compute how much water it can trap after raining.

**Scenario:** A row of buildings of different heights stands side by side. After a storm, how much water is held between them in total?

**Ask first:**
1. Water spilling off the two ends is lost, right? (Yes: the end walls are not closed.)
2. Heights non-negative? Empty input?

**Spot it:** The water above bar `i` = min(tallest wall on the left, tallest wall on the right) − height. The question is how to know those two maxima without rescanning.

**Brute force:** For each bar scan left and right for the tallest walls: `O(n²)`.

**Solve:** ([20-trapping-rain-water.md](02-two-pointers/20-trapping-rain-water.md))
```python
def trap(height: list[int]) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
    return water
```

**Cost:** One pass, pointers moving inward: `O(n)` time, `O(1)` space. The prefix/suffix-max array version is `O(n)` time and `O(n)` space but easier to derive: say it first, then optimise.
**Follow-up:** *Why is the smaller side safe?* If `left_max < right_max`, the water above the left bar is capped by `left_max`, whatever is in between. *2D version?* Variant A. *Stream of bars?* Need the prefix/suffix idea with a stack.

**More scenarios on the same pattern**

**Variant A (crossover to a heap)**
- **Question:** LC 407 Trapping Rain Water II. Given an `m × n` height map, return the volume of trapped water.
- **Scenario:** A city planner models a whole district's elevation grid and wants the total water that pools after rain.
- **Pattern and cost:** Two pointers on one dimension no longer define the bottleneck. Start from the border in a min-heap and flood inward, always expanding the lowest wall. `O(mn log(mn))` time, `O(mn)` space (Heap repo).

**Variant B (crossover to a monotonic stack)**
- **Question:** LC 739 Daily Temperatures. For each day, return the number of days until a warmer temperature (or `0`).
- **Scenario:** For every day in a forecast, tell me how many days I must wait until the weather is hotter.
- **Pattern and cost:** "Nearest bigger on the right" for every element: a stack of unresolved days, popped when a hotter day arrives. Each day is pushed once and popped once: `O(n)` time, `O(n)` space (Stack repo). #20 can also be solved this way.

---

### 21. Sort Colors (#21)

**Original question:** LC 75. Given an array `nums` with `n` objects coloured red (0), white (1) or blue (2), sort them in place so that same colours are adjacent, in the order 0, 1, 2. Do not use a library sort.

**Scenario:** A conveyor belt carries crates tagged 0, 1 or 2. Regroup them on the belt so all 0s come first, then 1s, then 2s, in a single sweep, with no second belt.

**Ask first:**
1. Are the values guaranteed to be only 0, 1 and 2?
2. Must it be one pass and `O(1)` space, or is a counting pass fine?

**Spot it:** A tiny fixed set of values, rearranged in place. This is a *three-way partition*: grow a "0 zone" at the front and a "2 zone" at the back, with a scanner between them.

**Brute force:** Sort, `O(n log n)`. Or count each value then rewrite: two passes, `O(n)`, `O(1)`. The one-pass swap is the improvement.

**Solve:** ([21-sort-colors.md](02-two-pointers/21-sort-colors.md))
```python
def sortColors(nums: list[int]) -> None:
    l, r = 0, len(nums) - 1
    i = 0
    while i <= r:
        if nums[i] == 0:
            nums[l], nums[i] = nums[i], nums[l]
            l += 1
            i += 1
        elif nums[i] == 2:
            nums[r], nums[i] = nums[i], nums[r]
            r -= 1                    # do NOT advance i: the swapped-in value is unchecked
        else:
            i += 1
```

**Cost:** Each element is examined at most twice (once at `i`, and maybe once more after being swapped in from `r`): `O(n)` time, `O(1)` space.
**Follow-up:** *Why not advance `i` after swapping with `r`?* The value that arrives from the right has never been inspected. *Why advance after a swap with `l`?* Everything between `l` and `i` is already known to be 1. *More than three colours?* Variant B.

**More scenarios on the same pattern**

**Variant A (two-way partition)**
- **Question:** LC 905 Sort Array By Parity. Move all even integers before all odd ones, in any order, in place.
- **Scenario:** A call centre queue should put all priority tickets (even IDs) ahead of the rest, using the same queue.
- **Pattern and cost:** A two-way partition: pointers from both ends, swap an odd on the left with an even on the right. `O(n)` time, `O(1)` space. Not stable: it doesn't preserve relative order (a read/write pointer is stable, a swap isn't).

**Variant B (crossover to counting sort)**
- **Question:** Sort Colors with `k` colours (follow-up of LC 75; classic Sort Colors II). Sort the array of values in `1..k` in place.
- **Scenario:** A recycling plant sorts items into `k` bins by label on a belt.
- **Pattern and cost:** A single swap pass doesn't extend cleanly. Counting sort: `O(n + k)` time, `O(k)` space. Or recursive partitioning on min/max colour: `O(n log k)`, `O(1)` space. The trade: the less space you use, the fiddlier the code.

---

### Topic 3. Sliding Window

---

### 22. Best Time to Buy and Sell Stock (#22)

**Original question:** LC 121. Given `prices` where `prices[i]` is the price on day `i`, choose one day to buy and a later day to sell. Return the maximum profit, or `0` if no profit is possible.

**Scenario:** A resale shop logs the daily price of a limited-edition sneaker. You may buy one pair on some day and sell it on a later day. What's the most you could have made?

**Ask first:**
1. Exactly one buy and one sell, and the sell must be strictly after the buy?
2. If prices only fall, do I return `0` or a negative number?

**Spot it:** "Best pair `i < j` maximising `prices[j] - prices[i]`." For each sell day the best buy day is simply the cheapest day *so far*: a running minimum, no need to remember which day it was.

**Brute force:** Try every buy/sell pair: `O(n²)`.

**Solve:** ([22-best-time-to-buy-and-sell-stock.md](03-sliding-window/22-best-time-to-buy-and-sell-stock.md))
```python
def maxProfit(prices: list[int]) -> int:
    min_price = float("inf")
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit
```

**Cost:** One pass, constant work per day: `O(n)` time, `O(1)` space.
**Follow-up:** *Many transactions?* #58 (greedy). *At most two or `k`?* DP (Variant A). *Return the days?* Track the index of `min_price` and update the best pair together. *Stream?* Works online.

**More scenarios on the same pattern**

**Variant A (crossover to DP)**
- **Question:** LC 123 Best Time to Buy and Sell Stock III. Same prices, but at most **two** transactions (a new buy only after the previous sell).
- **Scenario:** The shop may now complete two buy-and-sell rounds, never holding more than one pair at once.
- **Pattern and cost:** A single running minimum isn't enough: you must remember the best result after the first sale. A small state machine (`buy1, sell1, buy2, sell2`), `O(n)` time, `O(1)` space. See the DP repo.

**Variant B (running best of a combined expression)**
- **Question:** LC 1014 Best Sightseeing Pair. For indices `i < j`, the score is `values[i] + values[j] + i - j`. Return the maximum score.
- **Scenario:** A tour guide scores a pair of sights by their ratings, minus a penalty equal to the distance between them. Which pair scores best?
- **Pattern and cost:** Split the score into `(values[i] + i) + (values[j] - j)` and keep the running best of the first part. Same shape as #22: `O(n)` time, `O(1)` space.

---

### 23. Longest Substring Without Repeating Characters (#23)

**Original question:** LC 3. Given a string `s`, find the length of the longest substring without repeated characters.

**Scenario:** A door scanner reads a stream of badge IDs. What's the longest uninterrupted run of scans in which no badge appears twice?

**Ask first:**
1. Which characters can appear (ASCII, Unicode)? Is case significant?
2. Do you want the length only, or the run itself?

**Spot it:** "Longest contiguous run where a rule holds, and the rule only gets worse as the run grows." Grow on the right; when a repeat appears, shrink from the left until it's gone.

**Brute force:** Check every substring for repeats: `O(n³)`, or `O(n²)` with a set per start.

**Solve:** ([23-longest-substring-without-repeating-characters.md](03-sliding-window/23-longest-substring-without-repeating-characters.md))
```python
def lengthOfLongestSubstring(s: str) -> int:
    seen = set()
    left = 0
    max_length = 0
    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_length = max(max_length, right - left + 1)
    return max_length
```

**Cost:** `right` moves `n` times and `left` moves at most `n` times in total (it never goes back), so the inner `while` is amortised: `O(n)` time. Space `O(min(n, alphabet))`.
**Follow-up:** *Faster shrink?* Store each character's last index and jump `left` directly. *Return the substring?* Remember the best `left`. *Stream?* Works online, but you only know the max so far.

**More scenarios on the same pattern**

**Variant A (at most two kinds)**
- **Question:** LC 904 Fruit Into Baskets. Given `fruits`, where `fruits[i]` is a tree's fruit type, collect fruit along a contiguous run of trees using two baskets (each holds one type). Return the maximum number of fruits.
- **Scenario:** A picker walks down a row of trees and can carry only two kinds of fruit. What's the longest stretch of consecutive trees they can pick from?
- **Pattern and cost:** The same shrinking window, but the rule is "at most 2 distinct types", tracked with a count map. `O(n)` time, `O(1)` space. This is #29 with `k = 2`.

**Variant B (window carries a sum)**
- **Question:** LC 1695 Maximum Erasure Value. Remove a contiguous subarray of **unique** elements to maximise its sum.
- **Scenario:** A contest awards points for a run of consecutive rounds in which no player's score card repeats. Find the run with the highest total.
- **Pattern and cost:** Window with a set, plus a running sum added on entry and subtracted on exit. `O(n)` time, `O(n)` space. Positive values are what make the shrink rule safe: with negatives the best run might need to include a repeat's earlier part, so you'd need a different tool.

---

### 24. Longest Repeating Character Replacement (#24)

**Original question:** LC 424. Given a string `s` of uppercase letters and an integer `k`, you may change at most `k` characters. Return the length of the longest substring containing the same letter after the changes.

**Scenario:** A billboard shows a row of coloured bulbs. An electrician can swap at most `k` bulbs. What's the longest unbroken block of one colour they can create?

**Ask first:**
1. Replacements must be inside the chosen block, right? (Yes, replace only within the substring.)
2. Letters limited to `A-Z`?

**Spot it:** "Longest stretch with at most `k` fixes." A block is fixable if `length - (count of its most common letter) <= k`.

**Brute force:** For each substring count letters and test: `O(n²·26)`.

**Solve:** ([24-longest-repeating-character-replacement.md](03-sliding-window/24-longest-repeating-character-replacement.md))
```python
from collections import defaultdict

def characterReplacement(s: str, k: int) -> int:
    count = defaultdict(int)
    l = max_freq = res = 0
    for r in range(len(s)):
        count[s[r]] += 1
        max_freq = max(max_freq, count[s[r]])
        while (r - l + 1) - max_freq > k:        # more fixes needed than allowed
            count[s[l]] -= 1
            l += 1
        res = max(res, r - l + 1)
    return res
```

**Cost:** `r` moves `n` times, `l` at most `n` times in total: `O(n)` time. `count` has at most 26 keys: `O(1)` space. `max_freq` is never decreased on purpose: only a larger one can improve the answer.
**Follow-up:** *Why is a stale `max_freq` safe?* The answer only grows when `max_freq` grows. *Lowercase and uppercase?* Bigger map, same logic. *Return the block?* Record `l` when `res` improves.

**More scenarios on the same pattern**

**Variant A (the same budget idea on bits)**
- **Question:** LC 1004 Max Consecutive Ones III. Given a binary array and `k`, return the maximum number of consecutive `1`s if you can flip at most `k` `0`s.
- **Scenario:** A sensor log marks each minute online (1) or offline (0). If up to `k` offline minutes can be explained away, what's the longest apparent uptime run?
- **Pattern and cost:** "Invalid when more than `k` zeros inside". `O(n)` time, `O(1)` space. (Listed as #74 in the appendix; not written yet.)

**Variant B (budget of exactly one deletion)**
- **Question:** LC 1493 Longest Subarray of 1's After Deleting One Element. Delete exactly one element from a binary array; return the length of the longest non-empty subarray of only `1`s.
- **Scenario:** A game streak counter drops one "miss" from the record. How long can the longest hit streak become?
- **Pattern and cost:** Window with at most one zero; answer is `window size - 1` (you must delete one element, even if there is no zero). `O(n)` time, `O(1)` space. The "exactly one" detail is a classic off-by-one trap.

---

### 25. Permutation in String (#25)

**Original question:** LC 567. Given strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1` (a substring of `s2` that is an anagram of `s1`).

**Scenario:** A lab has a long DNA read and a short marker. Does the read contain a stretch made of exactly the same letters as the marker, in any order?

**Ask first:**
1. Lowercase letters only? Is `s1` longer than `s2` possible?
2. Substring means contiguous, right?

**Spot it:** A fixed-length stretch (the marker's length) compared by *letter counts*. Slide it one step: add the new letter, remove the old one.

**Brute force:** Sort or count every substring of length `len(s1)` from scratch: `O(n·k log k)` or `O(n·k)`.

**Solve:** ([25-permutation-in-string.md](03-sliding-window/25-permutation-in-string.md))
```python
def checkInclusion(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False
    c1, c2 = [0] * 26, [0] * 26
    for i in range(len(s1)):
        c1[ord(s1[i]) - ord("a")] += 1
        c2[ord(s2[i]) - ord("a")] += 1
    if c1 == c2:
        return True
    for i in range(len(s1), len(s2)):
        c2[ord(s2[i]) - ord("a")] += 1
        c2[ord(s2[i - len(s1)]) - ord("a")] -= 1
        if c1 == c2:
            return True
    return False
```

**Cost:** `n = len(s2)`. Each slide is `O(1)` for the update and `O(26)` for the comparison: `O(26n) = O(n)` time, `O(1)` space.
**Follow-up:** *Avoid the 26-compare?* Keep a `matches` counter updated on each add/remove. *Return all start indices?* Collect instead of returning (that is LC 438, #73). *Unicode?* Use a `Counter` instead of a fixed array.

**More scenarios on the same pattern**

**Variant A (counting windows)**
- **Question:** LC 1358 Number of Substrings Containing All Three Characters. Given a string of `a`, `b`, `c`, return the number of substrings containing at least one of each.
- **Scenario:** A security log has three event types. How many contiguous time spans contain all three?
- **Pattern and cost:** Window that shrinks while valid; for each right end, every left start up to the smallest valid one works. Or track the last position of each letter: for each `r`, add `min(last_a, last_b, last_c) + 1`. `O(n)` time, `O(1)` space.

**Variant B (fixed window with a set)**
- **Question:** LC 2461 Maximum Sum of Distinct Subarrays With Length K. Return the maximum sum of a length-`k` subarray whose elements are all distinct, or `0`.
- **Scenario:** A fund looks at every `k`-day span in which no day's return repeats, and wants the best total.
- **Pattern and cost:** Fixed window with a count map and a running sum. `O(n)` time, `O(k)` space. Same add-one/remove-one machinery as #25.

---

### 26. Minimum Size Subarray Sum (#26)

**Original question:** LC 209. Given an array of **positive** integers `nums` and a positive integer `target`, return the minimal length of a contiguous subarray whose sum is at least `target`, or `0` if none exists.

**Scenario:** A courier's log lists parcels delivered each day (never negative). What's the shortest run of consecutive days that adds up to at least `T` parcels?

**Ask first:**
1. Are all values positive? (This is the key question: it decides the technique.)
2. Is `T` ever larger than the total? Return `0`?

**Spot it:** "Shortest contiguous run reaching a total", and totals only grow when you add (positives). Add until you reach `T`, then shrink from the left as far as you can.

**Brute force:** Every start and end, summing: `O(n³)`, or `O(n²)` with running sums.

**Solve:** ([26-minimum-size-subarray-sum.md](03-sliding-window/26-minimum-size-subarray-sum.md))
```python
def minSubArrayLen(target: int, nums: list[int]) -> int:
    l = current_sum = 0
    min_len = float("inf")
    for r in range(len(nums)):
        current_sum += nums[r]
        while current_sum >= target:
            min_len = min(min_len, r - l + 1)
            current_sum -= nums[l]
            l += 1
    return min_len if min_len != float("inf") else 0
```

**Cost:** `r` moves `n` times, `l` at most `n` times in total: `O(n)` time, `O(1)` space. Alternative: prefix sums + binary search, `O(n log n)` (valid only because positive values make prefix sums strictly increasing).
**Follow-up:** *Negatives allowed?* The window breaks. Variant A. *Count the subarrays instead?* Variant B. *Stream?* Works online.

**More scenarios on the same pattern**

**Variant A (crossover: negatives break the window)**
- **Question:** LC 862 Shortest Subarray with Sum at Least K. `nums` may contain negatives. Return the length of the shortest non-empty subarray with sum at least `k`, or `-1`.
- **Scenario:** The courier log now includes returns, which subtract from the total. What's the shortest run of days reaching at least `K` net parcels?
- **Pattern and cost:** Adding an element can now lower the sum, so shrinking is unsafe. Use prefix sums and a monotonic deque of candidate start indices: `O(n)` time, `O(n)` space. This is the clearest example of "window fails with negatives" (not yet in the repo).

**Variant B (counting, product condition)**
- **Question:** LC 713 Subarray Product Less Than K. Given positive integers `nums` and `k`, return the number of contiguous subarrays whose product is strictly less than `k`.
- **Scenario:** A growth model multiplies daily factors (all above zero). How many runs of consecutive days have a combined growth under `K`?
- **Pattern and cost:** Window with a running product; for each `r`, add `r - l + 1` valid subarrays ending at `r`. `O(n)` time, `O(1)` space. Works because every factor is ≥ 1 (positive integers), so the product only grows.

---

### 27. Minimum Window Substring (#27)

**Original question:** LC 76. Given strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. Return `""` if none exists.

**Scenario:** A support agent must find the shortest excerpt of a long chat transcript that mentions every keyword letter from a checklist, as many times as the checklist requires.

**Ask first:**
1. Do duplicates in `t` need matching counts? Is the answer guaranteed unique?
2. Case-sensitive?

**Spot it:** "Shortest stretch that *covers* a required multiset." Grow until covered, then shrink while still covered. Track coverage with a `have`/`need` counter rather than comparing maps.

**Brute force:** Check every substring against the requirement: `O(n²·m)` or worse.

**Solve:** ([27-minimum-window-substring.md](03-sliding-window/27-minimum-window-substring.md))
```python
from collections import Counter, defaultdict

def minWindow(s: str, t: str) -> str:
    t_freq, s_freq = Counter(t), defaultdict(int)
    have, need = 0, len(t_freq)
    res, res_len, l = [-1, -1], float("inf"), 0
    for r in range(len(s)):
        char = s[r]
        s_freq[char] += 1
        if char in t_freq and s_freq[char] == t_freq[char]:
            have += 1
        while have == need:
            if r - l + 1 < res_len:
                res, res_len = [l, r], r - l + 1
            left_char = s[l]
            s_freq[left_char] -= 1
            if left_char in t_freq and s_freq[left_char] < t_freq[left_char]:
                have -= 1
            l += 1
    l, r = res
    return s[l : r + 1] if res_len != float("inf") else ""
```

**Cost:** `m = len(s)`, `n = len(t)`. Counting `t` is `O(n)`; `l` and `r` each pass over `s` once with `O(1)` work: `O(m + n)` time. `O(m + n)` space in the worst case (`O(distinct characters)` in practice).
**Follow-up:** *Why `have`/`need`?* Comparing two maps each step would cost `O(k)` each. *Return all minimal windows?* Collect ties. *Unicode?* Maps handle it.

**More scenarios on the same pattern**

**Variant A (crossover to a heap + window)**
- **Question:** LC 632 Smallest Range Covering Elements from K Lists. Given `k` sorted lists, find the smallest range `[a, b]` containing at least one number from each list.
- **Scenario:** A broadcaster has `k` regional schedules (each in time order) and wants the shortest time span that includes at least one show from every region.
- **Pattern and cost:** Same "cover everything" goal, but the elements come from `k` ordered lists. Keep a min-heap with one element per list and track the current max; advance the smallest. `O(N log k)` time, `O(k)` space (Heap repo).

**Variant B (crossover to "at most k" subtraction)**
- **Question:** LC 1248 Count Number of Nice Subarrays. Given `nums` and `k`, return the number of contiguous subarrays containing exactly `k` odd numbers.
- **Scenario:** How many stretches of a delivery route contain exactly `k` fragile parcels (odd-coded)?
- **Pattern and cost:** "Exactly `k`" has no monotone window, but "at most `k`" does. Answer = `atMost(k) - atMost(k - 1)`, each `O(n)`. Or prefix counts + hash map like #33. `O(n)` time, `O(1)` or `O(n)` space.

---

### 28. Sliding Window Maximum (#28)

**Original question:** LC 239. Given an integer array `nums` and a window size `k` that moves one step at a time from the left to the right, return the maximum of each window.

**Scenario:** A monitoring dashboard receives per-minute CPU readings. It must show the highest reading within every 5-minute stretch as time moves on.

**Ask first:**
1. Is `k` fixed, and can it exceed the length of the data?
2. Online (a stream) or all data upfront?

**Spot it:** "Max of every fixed-size stretch." A new, larger value makes every older, smaller value in the stretch useless: keep a deque of candidates that can still become a maximum.

**Brute force:** Scan each window: `O(n·k)`. A heap with lazy deletion: `O(n log n)`.

**Solve:** ([28-sliding-window-maximum.md](03-sliding-window/28-sliding-window-maximum.md))
```python
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    q = deque()                        # values, decreasing front to back
    output = []
    l = 0
    for r in range(len(nums)):
        while q and q[-1] < nums[r]:
            q.pop()
        q.append(nums[r])
        if r + 1 >= k:
            output.append(q[0])
            if nums[l] == q[0]:        # the max is leaving the window
                q.popleft()
            l += 1
    return output
```

**Cost:** Each value is pushed once and popped at most once (from the back when smaller, or the front when it leaves): at most `2n` deque operations, `O(n)` time. The deque holds at most `k` values: `O(k)` space.
**Follow-up:** *Why not a heap?* Heap is `O(n log n)` and needs lazy deletion. *Stream?* Works online. *Minimum instead?* Flip the comparison. *Median?* Variant A.

**More scenarios on the same pattern**

**Variant A (crossover to two heaps)**
- **Question:** LC 480 Sliding Window Median. Return the median of each window of size `k`.
- **Scenario:** The dashboard now shows the typical (middle) reading in each 5-minute stretch.
- **Pattern and cost:** A monotonic deque only knows the extreme. Use two heaps (or a sorted list) with lazy deletion: `O(n log k)` time, `O(k)` space (Heap repo).

**Variant B (two deques for a range condition)**
- **Question:** LC 1438 Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit. Return the length of the longest subarray where the difference between its largest and smallest value is at most `limit`.
- **Scenario:** A thermostat log: what's the longest stretch in which readings varied by no more than `L` degrees?
- **Pattern and cost:** A variable window needing the current max and min: two monotonic deques. Shrink while `max - min > limit`. `O(n)` time, `O(n)` space.

---

### 29. Longest Substring with At Most K Distinct Characters (#29)

**Original question:** LC 340 (premium). Given a string `s` and an integer `k`, return the length of the longest substring that contains at most `k` distinct characters.

**Scenario:** A music app looks at a listening history and wants the longest unbroken stretch that involved no more than `k` different artists.

**Ask first:**
1. Can `k` be `0`, or larger than the number of distinct characters?
2. What are the possible characters?

**Spot it:** "Longest stretch with at most `k` different kinds." The count of kinds only grows when the stretch grows: a variable window with a count map.

**Brute force:** Every substring, count distinct: `O(n²)` to `O(n³)`.

**Solve:** ([29-longest-substring-with-at-most-k-distinct-characters.md](03-sliding-window/29-longest-substring-with-at-most-k-distinct-characters.md))
```python
from collections import defaultdict

def lengthOfLongestSubstringKDistinct(s: str, k: int) -> int:
    if k == 0 or not s:
        return 0
    char_count = defaultdict(int)
    l = max_len = 0
    for r in range(len(s)):
        char_count[s[r]] += 1
        while len(char_count) > k:
            char_count[s[l]] -= 1
            if char_count[s[l]] == 0:
                del char_count[s[l]]       # forgetting this overcounts distinct characters
            l += 1
        max_len = max(max_len, r - l + 1)
    return max_len
```

**Cost:** `r` moves `n` times, `l` at most `n` times: `O(n)` time. The map has at most `k + 1` keys: `O(k)` space.
**Follow-up:** *Exactly `k` distinct?* `atMost(k) - atMost(k - 1)`. *Stream?* Works online. *Unicode?* Map handles it. *Why delete at zero?* `len(map)` is the distinct count.

**More scenarios on the same pattern**

**Variant A (k = 2, the classic)**
- **Question:** LC 159 Longest Substring with At Most Two Distinct Characters (premium). Same as #29 with `k = 2`.
- **Scenario:** A river survey logs one species per marker; find the longest run involving at most two species.
- **Pattern and cost:** Identical window, `O(n)` time, `O(1)` space. The interview version of "Fruit Into Baskets".

**Variant B (crossover: the window can't decide)**
- **Question:** LC 395 Longest Substring with At Least K Repeating Characters. Return the length of the longest substring in which every character appears at least `k` times.
- **Scenario:** A fraud model needs the longest stretch of transactions in which every merchant that shows up does so at least `k` times.
- **Pattern and cost:** Not monotone: extending a stretch can make a rare character *worse* or *better*. Fix instead the number of distinct characters (1 to 26) and run a window for each target: `O(26n)`. Or divide and conquer, splitting at any character with total count `< k`: `O(n²)` worst, `O(26n)` typical.

---

### 30. Substring with Concatenation of All Words (#30)

**Original question:** LC 30. Given a string `s` and an array `words` of strings of the same length, return all starting indices in `s` of substrings that are a concatenation of every word in `words` exactly once, in any order, with no characters in between.

**Scenario:** A genome browser has a long sequence and a set of equal-length tags. Report every position where the sequence is exactly all the tags glued together, each used once, in any order.

**Ask first:**
1. Can `words` contain duplicates? Are all words the same length?
2. Can matches overlap?

**Spot it:** A fixed-length stretch made of *chunks* of fixed width. Slide by whole chunks, once per starting offset, and compare chunk counts.

**Brute force:** At every start, split into chunks and count: `O(n · total_len)`.

**Solve:** ([30-substring-with-concatenation-of-all-words.md](03-sliding-window/30-substring-with-concatenation-of-all-words.md))
```python
from collections import Counter, defaultdict

def findSubstring(s: str, words: list[str]) -> list[int]:
    if not s or not words:
        return []
    word_len, num_words = len(words[0]), len(words)
    word_freq, ans = Counter(words), []
    for offset in range(word_len):
        l = r = offset
        seen, count = defaultdict(int), 0
        while r + word_len <= len(s):
            word = s[r : r + word_len]
            r += word_len
            if word in word_freq:
                seen[word] += 1
                count += 1
                while seen[word] > word_freq[word]:
                    left_word = s[l : l + word_len]
                    seen[left_word] -= 1
                    count -= 1
                    l += word_len
                if count == num_words:
                    ans.append(l)
            else:
                seen.clear()
                count = 0
                l = r
    return ans
```

**Cost:** `l` = word length. There are `l` offsets; each offset's pass moves forward through `s` in `O(n / l)` chunk steps costing `O(l)` each: `O(n · l)` total. Space `O(k · l)` for the maps.
**Follow-up:** *Why one pass per offset?* Chunks must align; each offset class is independent. *Words differ in length?* Window by characters isn't enough; this method no longer works. *Rarely asked in interviews:* know the idea, not the code.

**More scenarios on the same pattern**

**Variant A (fixed window + rolling hash)**
- **Question:** LC 187 Repeated DNA Sequences. Return all 10-letter sequences that occur more than once in a DNA string.
- **Scenario:** A lab wants every 10-base fragment that appears at least twice in a long genome.
- **Pattern and cost:** Fixed 10-wide window; put each fragment in a set / count map. `O(n)` windows, `O(10)` to slice, so `O(10n)`. Encode as 2 bits per base (20-bit integer) to hash in `O(1)`; space `O(n)`.

**Variant B (crossover to binary search on the answer)**
- **Question:** LC 1044 Longest Duplicate Substring. Return any longest substring that occurs at least twice in `s`.
- **Scenario:** A plagiarism checker wants the longest passage that appears twice in a document.
- **Pattern and cost:** If a length `L` repeats, so does every shorter one: binary search on `L` (monotone), checking each `L` with a rolling hash fixed window in `O(n)`. `O(n log n)` time, `O(n)` space. A hard problem; know the shape: **search on the answer + fixed window**.

---

### Topic 4. Prefix Sum, Kadane & Running Products

---

### 31. Product of Array Except Self (#31)

**Original question:** LC 238. Given an integer array `nums`, return an array `answer` where `answer[i]` is the product of all the elements of `nums` except `nums[i]`. It must run in `O(n)` and must not use division.

**Scenario:** A retailer has a growth multiplier for each region. For every region, it needs the combined multiplier of all the *other* regions. The finance system's division is disabled because some multipliers are zero.

**Ask first:**
1. Can the array contain zeros or negatives? Is the product guaranteed to fit in 32 bits?
2. May the output array count as the only extra space?

**Spot it:** "Everything except me" = "everything on my left" × "everything on my right". Two running products, one from each side.

**Brute force:** For each index multiply all others: `O(n²)`. Or total product ÷ `nums[i]`: `O(n)` but fails with zeros (and division is banned).

**Solve:** ([31-product-of-array-except-self.md](04-prefix-sum-and-kadane/31-product-of-array-except-self.md))
```python
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):                 # res[i] = product of everything left of i
        res[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):     # multiply in everything right of i
        res[i] *= suffix
        suffix *= nums[i]
    return res
```

**Cost:** Two sequential passes, `O(1)` work each: `O(n)` time. The output array doubles as the prefix store, so extra space is `O(1)` (the answer isn't counted).
**Follow-up:** *Zeros?* Handled naturally (no division). *Overflow?* Use a wider type or big integers; say so. *Sum instead of product?* Total − `nums[i]`, no passes needed. *Two zeros?* Everything is `0`, and the code produces that.

**More scenarios on the same pattern**

**Variant A (prefix vs suffix sums)**
- **Question:** LC 724 Find Pivot Index. Return the leftmost index where the sum of the numbers strictly to its left equals the sum of the numbers strictly to its right, or `-1`.
- **Scenario:** A warehouse wants a shelf position where the stock on the left side weighs the same as on the right side.
- **Pattern and cost:** Left sum is a running total; right sum = total − left − `nums[i]`. One pass after computing the total: `O(n)` time, `O(1)` space.

**Variant B (range queries)**
- **Question:** LC 303 Range Sum Query - Immutable. Given `nums`, answer many queries `sumRange(left, right)`.
- **Scenario:** A reporting tool is asked for the total sales between day `i` and day `j`, thousands of times over a fixed history.
- **Pattern and cost:** Build prefix sums once, answer each query as `prefix[j + 1] - prefix[i]`. `O(n)` build, `O(1)` per query, `O(n)` space. Re-summing per query is `O(n)` each. Note the *many queries on fixed data* clue.

---

### 32. Maximum Subarray (#32)

**Original question:** LC 53. Given an integer array `nums`, find the contiguous non-empty subarray with the largest sum, and return its sum.

**Scenario:** A fund reports its daily profit or loss in a long list. Over which run of consecutive days did it earn the most in total, and how much was that?

**Ask first:**
1. Can all values be negative? (Then the answer is the largest single element.)
2. Do you want the sum only, or also the start and end days?

**Spot it:** "Best contiguous total, values can be negative." The best run ending today is either today alone (if the past is a net loss) or the past plus today.

**Brute force:** All start/end pairs with a running sum: `O(n²)`.

**Solve:** ([32-maximum-subarray.md](04-prefix-sum-and-kadane/32-maximum-subarray.md))
```python
def maxSubArray(nums: list[int]) -> int:
    max_sum = float("-inf")
    current_sum = 0
    for num in nums:
        if current_sum < 0:
            current_sum = 0            # a negative past only hurts
        current_sum += num
        max_sum = max(max_sum, current_sum)
    return max_sum
```

**Cost:** One pass, constant work per element: `O(n)` time, `O(1)` space. Start `max_sum` at `-inf`, not `0`, so an all-negative array still returns its largest element.
**Follow-up:** *Also return the indices?* Remember where the current run restarted. *Circular array?* Variant A. *Product instead of sum?* Variant B (negatives flip the sign). *Divide and conquer?* `O(n log n)`; mention but prefer Kadane.

**More scenarios on the same pattern**

**Variant A (crossover: wraps around)**
- **Question:** LC 918 Maximum Sum Circular Subarray. The array is circular; the subarray may wrap from the end back to the start. Return the maximum sum.
- **Scenario:** The fund's year is a loop (December flows into January). Which run of consecutive months, possibly crossing the year end, earned the most?
- **Pattern and cost:** Answer = max(Kadane max, total − Kadane min). Edge case: if every number is negative, the second option would be an empty run, so return the Kadane max. `O(n)` time, `O(1)` space.

**Variant B (crossover: negatives flip products)**
- **Question:** LC 152 Maximum Product Subarray. Return the largest product of a contiguous non-empty subarray.
- **Scenario:** A model multiplies daily factors that can be above or below zero (a negative flips the sign). Which run has the biggest combined factor?
- **Pattern and cost:** Plain Kadane fails, because a very negative run can become the biggest after one more negative. Track both the max and the min product ending here. `O(n)` time, `O(1)` space (DP repo).

---

### 33. Subarray Sum Equals K (#33)

**Original question:** LC 560. Given an integer array `nums` and an integer `k`, return the total number of contiguous subarrays whose sum equals `k`.

**Scenario:** An account statement lists the daily net change (credits and debits). How many different stretches of consecutive days net out to exactly `K`?

**Ask first:**
1. Can values be negative or zero? (If all positive, a window would work.)
2. Do you want a count, or the stretches themselves?

**Spot it:** "How many stretches sum to exactly `K`", with negatives. A stretch's sum = difference of two running totals. For today's running total `T`, I need the number of earlier running totals equal to `T - K`.

**Brute force:** All start/end pairs, `O(n²)` with running sums (`O(n³)` if re-summed).

**Solve:** ([33-subarray-sum-equals-k.md](04-prefix-sum-and-kadane/33-subarray-sum-equals-k.md))
```python
from collections import defaultdict

def subarraySum(nums: list[int], k: int) -> int:
    seen_count = defaultdict(int)
    seen_count[0] = 1                  # the empty prefix
    total = count = 0
    for n in nums:
        total += n
        count += seen_count[total - k] # look up BEFORE recording today's total
        seen_count[total] += 1
    return count
```

**Cost:** One pass, `O(1)` average per lookup and insert: `O(n)` time. The map holds up to `n + 1` distinct prefix totals: `O(n)` space.
**Follow-up:** *Why not a sliding window?* Negatives: the sum can drop after you add, so shrinking isn't safe (see Part 2). *Longest such stretch?* Store the *first index* of each total (Variant A). *Overflow?* Prefix totals can grow large. *Two-dimensional version?* 2D prefix sums.

**More scenarios on the same pattern**

**Variant A (store the first index, not a count)**
- **Question:** LC 525 Contiguous Array. Given a binary array, return the maximum length of a contiguous subarray with an equal number of `0` and `1`.
- **Scenario:** A switch log marks each minute on or off. What's the longest stretch with equal on and off minutes?
- **Pattern and cost:** Treat `0` as `-1`, so the question becomes "longest stretch with sum 0". Map each prefix total to its *first* index; the answer is the largest gap. `O(n)` time, `O(n)` space.

**Variant B (remainders instead of exact values)**
- **Question:** LC 974 Subarray Sums Divisible by K. Return the number of contiguous subarrays whose sum is divisible by `k`.
- **Scenario:** How many stretches of consecutive orders total a multiple of the pallet size `K`?
- **Pattern and cost:** Two prefix totals with the same remainder mod `K` mean the stretch between them is divisible. Count remainders (normalise negatives with `% K`). `O(n)` time, `O(K)` space.

---

### Topic 5. Intervals

---

### 34. Merge Intervals (#34)

**Original question:** LC 56. Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return an array of the non-overlapping intervals that cover all the input.

**Scenario:** A calendar app holds a pile of booked time blocks in no particular order. Show the user the continuous busy periods, with overlapping blocks combined.

**Ask first:**
1. Do touching intervals (`[1,4]` and `[4,5]`) count as overlapping?
2. Is the input sorted? May I modify it?

**Spot it:** "Combine whatever overlaps." If I order the blocks by start time, only the *latest merged block* can overlap the next one.

**Brute force:** Compare every pair repeatedly until nothing merges: `O(n²)` or worse.

**Solve:** ([34-merge-intervals.md](05-intervals/34-merge-intervals.md))
```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda i: i[0])
    results = [intervals[0]]
    for start, end in intervals[1:]:
        last_end = results[-1][1]
        if start <= last_end:
            results[-1][1] = max(last_end, end)     # max, because the new block may be inside
        else:
            results.append([start, end])
    return results
```

**Cost:** The sort is `O(n log n)`; the scan is `O(n)`: `O(n log n)` time. `O(n)` space for the output and the sort.
**Follow-up:** *Already sorted?* `O(n)`, skip the sort. *Streaming insertions?* Keep a sorted structure. *Huge intervals list?* External sort. *Empty input?* Guard `intervals[0]` (the write-up assumes non-empty).

**More scenarios on the same pattern**

**Variant A (merge across several lists)**
- **Question:** LC 759 Employee Free Time (premium). Given each employee's working intervals (each list sorted and non-overlapping), return the common free time intervals for all employees.
- **Scenario:** A manager wants the times when nobody on the team is booked.
- **Pattern and cost:** Flatten all the intervals, sort by start (or heap-merge the sorted lists), merge, and the gaps between merged blocks are the answer. `O(N log N)` (or `O(N log k)` with a heap).

**Variant B (counting what survives)**
- **Question:** LC 1288 Remove Covered Intervals. Remove every interval that is fully covered by another; return the number remaining.
- **Scenario:** A broadcaster has overlapping ad slots, and any slot completely inside another is redundant. How many slots remain?
- **Pattern and cost:** Sort by start ascending, end descending; sweep with the maximum end seen. An interval is covered when its end ≤ that maximum. `O(n log n)` time, `O(1)` extra.

---

### 35. Insert Interval (#35)

**Original question:** LC 57. Given a list of non-overlapping `intervals` sorted by start time and a `newInterval`, insert it so the list stays sorted and non-overlapping, merging if needed.

**Scenario:** A clinic's bookings are already listed in time order with no clashes. A new appointment request arrives: put it in the right place, absorbing any bookings it touches.

**Ask first:**
1. Is the input guaranteed in order and non-overlapping?
2. Do touching intervals merge?

**Spot it:** The list is already in order, so there are exactly three phases: blocks entirely *before*, blocks that *overlap*, blocks entirely *after*.

**Brute force:** Append and re-sort and re-merge: `O(n log n)` (correct, but ignores the existing order).

**Solve:** ([35-insert-interval.md](05-intervals/35-insert-interval.md))
```python
def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    results, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < new_interval[0]:      # entirely before
        results.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= new_interval[1]:     # overlapping: absorb
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    results.append(new_interval)
    while i < n:                                            # entirely after
        results.append(intervals[i])
        i += 1
    return results
```

**Cost:** One index, each interval visited once across three loops: `O(n)` time, `O(n)` space for the output.
**Follow-up:** *Find the start with binary search?* `O(log n)` to find the position, but copying is still `O(n)`. *Many insertions?* Use a balanced tree or sorted container. *In place?* Possible but fiddly.

**More scenarios on the same pattern**

**Variant A (insert-if-free, a design problem)**
- **Question:** LC 729 My Calendar I. Implement `book(start, end)` that adds an event if it doesn't overlap any existing event (half-open `[start, end)`), returning true/false.
- **Scenario:** A room-booking API accepts a request only when the room is free for the whole slot.
- **Pattern and cost:** Keep events sorted; binary search the neighbours and check both. With a plain list it's `O(n)` per booking (find is `O(log n)`, insert shifts); a balanced tree gives `O(log n)`. Brute force compares against all events: `O(n)`.

**Variant B (crossover to a design problem on ranges)**
- **Question:** LC 715 Range Module (premium). Design a structure tracking ranges with `addRange`, `queryRange` and `removeRange`.
- **Scenario:** A spectrum tool marks frequency bands as occupied or free and answers whether a band is fully occupied.
- **Pattern and cost:** Generalises #35: keep disjoint sorted intervals; add merges, remove splits. `O(n)` per op with a list; `O(log n)` with a balanced tree. The skill is correct case analysis, not a new idea.

---

### 36. Non-overlapping Intervals (#36)

**Original question:** LC 435. Given an array of `intervals`, return the minimum number of intervals you need to remove to make the rest non-overlapping.

**Scenario:** An events team has a list of activities with start and end times. Fewest activities to cancel so that the rest never clash?

**Ask first:**
1. Do touching intervals (`[1,2]` and `[2,3]`) count as clashing?
2. Are weights or priorities involved? (If so, greedy fails: it becomes DP.)

**Spot it:** "Fewest to remove" = "most that fit". Always keep the activity that **finishes earliest**: it leaves the most room for the rest.

**Brute force:** Try all subsets: `O(2^n)`.

**Solve:** ([36-non-overlapping-intervals.md](05-intervals/36-non-overlapping-intervals.md))
```python
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda x: x[1])          # by END time
    removals = 0
    prev_end = float("-inf")
    for start, end in intervals:
        if start >= prev_end:
            prev_end = end                      # keep it
        else:
            removals += 1                       # clashes: drop the later-ending one
    return removals
```

**Cost:** Sort `O(n log n)`, scan `O(n)`: `O(n log n)` time, `O(1)` extra space.
**Follow-up:** *Weighted?* DP + binary search (Variant A). *Sort by start instead?* Also works, but you must keep the smaller end on a clash. *Touching allowed?* `>=` versus `>`.

**More scenarios on the same pattern**

**Variant A (crossover: weights make greedy fail)**
- **Question:** LC 1235 Maximum Profit in Job Scheduling. Given jobs with `startTime`, `endTime` and `profit`, return the maximum profit with no two overlapping jobs.
- **Scenario:** Each activity pays a different fee. Maximise total fees with no clashes.
- **Pattern and cost:** Earliest-finish greedy fails (a short cheap job can block a long expensive one). Sort by end; `dp[i] = max(dp[i-1], profit + dp[last job ending before start_i])` with binary search for the last compatible job. `O(n log n)` (DP repo).

**Variant B (longest chain)**
- **Question:** LC 646 Maximum Length of Pair Chain. A pair `(c, d)` follows `(a, b)` if `b < c`. Return the length of the longest chain.
- **Scenario:** Tasks must follow each other strictly (each starts after the last ends). How many can be strung together?
- **Pattern and cost:** The same greedy as #36: sort by end, take whenever the start is after the last chosen end. `O(n log n)` time, `O(1)` extra. (The DP version, LIS-like, is `O(n²)`.)

---

### 37. Meeting Rooms II (#37)

**Original question:** LC 253 (premium). Given an array of meeting time `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of conference rooms required.

**Scenario:** A conference centre has a day's list of sessions with start and end times. How many rooms must it open so that no two simultaneous sessions share a room?

**Ask first:**
1. If a session ends at 10:00 and another starts at 10:00, can they share a room?
2. Do you need the room assignment, or only the count?

**Spot it:** "How many at the same moment" = peak concurrency. Only the *order of starts and ends* matters, not which meeting they belong to.

**Brute force:** For every moment count the open meetings: `O(n²)`.

**Solve:** ([37-meeting-rooms-ii.md](05-intervals/37-meeting-rooms-ii.md))
```python
def minMeetingRooms(intervals: list[list[int]]) -> int:
    start = sorted(i[0] for i in intervals)
    end = sorted(i[1] for i in intervals)
    res = count = s = e = 0
    while s < len(intervals):
        if start[s] < end[e]:
            s += 1
            count += 1                  # a meeting starts: need a room
        else:
            e += 1
            count -= 1                  # a meeting ends (also on a tie): free a room
        res = max(res, count)
    return res
```

**Cost:** Sorting two arrays is `O(n log n)`; the sweep is `O(n)`: `O(n log n)` time, `O(n)` space. The min-heap version (sort by start, heap of end times) is also `O(n log n)` time, `O(n)` space.
**Follow-up:** *Assign the rooms?* Use the heap version. *Weights?* Heap holds loads. *Streaming?* Heap online. *Ties?* Process ends before starts at equal times.

**More scenarios on the same pattern**

**Variant A (crossover: difference array)**
- **Question:** LC 1094 Car Pooling. A car has `capacity` seats. Given `trips[i] = [numPassengers, from, to]`, return whether all trips can be completed without exceeding capacity.
- **Scenario:** A shuttle picks up and drops off groups along a route. Is it ever over capacity?
- **Pattern and cost:** Same peak-concurrency idea, but with weights: add passengers at `from` and subtract at `to` in a difference array (or sort the events), take the running sum. `O(n log n)` or `O(n + range)` time.

**Variant B (crossover to a heap)**
- **Question:** LC 218 The Skyline Problem. Given buildings `[left, right, height]`, return the key points of the skyline.
- **Scenario:** A city planner draws the outline made by overlapping buildings of various heights.
- **Pattern and cost:** Sweep sorted events, and keep a max-heap of active heights; output a point whenever the maximum changes. `O(n log n)` time, `O(n)` space (Heap repo).

---

### 38. Interval List Intersections (#38)

**Original question:** LC 986. You are given two lists of closed intervals, `firstList` and `secondList`, each pairwise disjoint and sorted. Return the intersection of the two lists.

**Scenario:** Two colleagues each have a list of free time slots for the day, in time order and without overlaps inside each list. When are they both free?

**Ask first:**
1. Are both lists in order and free of internal overlaps? (That's the whole trick.)
2. Do touching slots count as a one-point overlap?

**Spot it:** Two ordered lists and "both at once". Whichever slot *ends first* can't match anything further, so advance it.

**Brute force:** Compare every slot of one list with every slot of the other: `O(m·n)`.

**Solve:** ([38-interval-list-intersections.md](05-intervals/38-interval-list-intersections.md))
```python
def intervalIntersection(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
    i = j = 0
    res = []
    while i < len(first) and j < len(second):
        start = max(first[i][0], second[j][0])
        end = min(first[i][1], second[j][1])
        if start <= end:
            res.append([start, end])
        if first[i][1] < second[j][1]:
            i += 1
        else:
            j += 1
    return res
```

**Cost:** Each step advances at least one pointer: at most `m + n` steps, `O(m + n)` time, `O(1)` extra (the output isn't counted).
**Follow-up:** *Unsorted?* Sort first, `O(n log n)`. *`k` lists?* Heap or pairwise merge. *Overlap lengths only?* Sum `end - start`. *Open endpoints?* Change `<=` to `<`.

**More scenarios on the same pattern**

**Variant A (crossover: intersect plain lists)**
- **Question:** LC 350 Intersection of Two Arrays II. Return the intersection of two arrays, where each element appears as many times as it shows in both.
- **Scenario:** Two stores' sorted-by-SKU stock lists: which items (with multiplicity) do both carry?
- **Pattern and cost:** If both are already ordered, two pointers: `O(m + n)`, `O(1)`. Unordered: a `Counter` of the smaller one, `O(m + n)` time, `O(min(m, n))` space. If one list is on disk, stream it against the in-memory counter.

**Variant B (crossover: find a slot of given length)**
- **Question:** LC 1229 Meeting Scheduler (premium). Given two people's availability slots and a duration, return the earliest common time slot of at least that length, or empty.
- **Scenario:** Find the first time both of you can meet for 45 minutes.
- **Pattern and cost:** Sort both lists, then #38's two-pointer walk, returning the first intersection of length ≥ duration. `O(m log m + n log n)`.

---

### 39. Summary Ranges (#39)

**Original question:** LC 228. Given a sorted unique integer array `nums`, return the smallest sorted list of ranges that cover all the numbers exactly. Each range `[a, b]` is shown as `"a->b"` if `a != b`, else `"a"`.

**Scenario:** A ticketing system has issued numbers in increasing order with no repeats. Print them in compact form, so `3,4,5,9,11,12` becomes `3->5, 9, 11->12`.

**Ask first:**
1. Is the input guaranteed in increasing order with no duplicates?
2. Negative numbers? Empty input?

**Spot it:** Runs of "each is one more than the last" in ordered data. One pointer finds the start; an inner scan finds the end.

**Brute force:** There's no big gain over this: the straightforward scan is already `O(n)`. A naive version that rescans from each element is `O(n²)`.

**Solve:** ([39-summary-ranges.md](05-intervals/39-summary-ranges.md))
```python
def summaryRanges(nums: list[int]) -> list[str]:
    res, i, n = [], 0, len(nums)
    while i < n:
        start = nums[i]
        while i + 1 < n and nums[i] + 1 == nums[i + 1]:
            i += 1
        res.append(str(start) if start == nums[i] else f"{start}->{nums[i]}")
        i += 1
    return res
```

**Cost:** Nested loops, but `i` only moves forward and each element is stepped over once: `O(n)` time. `O(1)` extra space beyond the output.
**Follow-up:** *Duplicates allowed?* Treat equal neighbours as part of the run. *Gaps instead of runs?* Variant A. *Overflow?* `nums[i] + 1` in fixed width.

**More scenarios on the same pattern**

**Variant A (the complement: the gaps)**
- **Question:** LC 163 Missing Ranges (premium). Given a sorted unique array in the range `[lower, upper]`, return the shortest sorted list of ranges that covers every missing number.
- **Scenario:** An ID block `0..99` is partly issued; list the unissued stretches.
- **Pattern and cost:** One pass comparing each number with the previous one (start with `lower - 1`, end with `upper + 1`). `O(n)` time, `O(1)` extra.

**Variant B (longest run)**
- **Question:** LC 485 Max Consecutive Ones. Return the maximum number of consecutive `1`s in a binary array.
- **Scenario:** What's the longest streak of passed tests in a CI history?
- **Pattern and cost:** Running count reset on `0`, `O(n)` time, `O(1)` space. If `k` flips are allowed, it becomes a sliding window (#24, #74).

---

### 40. Minimum Number of Arrows to Burst Balloons (#40)

**Original question:** LC 452. Balloons are given as horizontal spans `points[i] = [x_start, x_end]`. An arrow shot vertically at `x` bursts every balloon with `x_start <= x <= x_end`. Return the minimum number of arrows needed to burst all balloons.

**Scenario:** A carnival wall has paint strips of different widths, and one dart thrown straight at position `x` pops every strip it crosses. Fewest darts to pop them all?

**Ask first:**
1. Do touching spans (`[1,2]` and `[2,3]`) share a point? (Yes: one dart at `x = 2`.)
2. Can coordinates be huge (overflow when subtracting)?

**Spot it:** Same shape as #36: group overlapping spans; aim at the **earliest ending** span so the dart is as useful as possible.

**Brute force:** Try all subsets of dart positions: exponential. Or try each span end as a candidate and cover greedily without sorting: `O(n²)`.

**Solve:** ([40-minimum-number-of-arrows-to-burst-balloons.md](05-intervals/40-minimum-number-of-arrows-to-burst-balloons.md))
```python
def findMinArrowShots(points: list[list[int]]) -> int:
    if not points:
        return 0
    points.sort(key=lambda x: x[1])
    arrows, prev_end = 1, points[0][1]
    for start, end in points[1:]:
        if start > prev_end:            # not reached by the current dart
            arrows += 1
            prev_end = end
    return arrows
```

**Cost:** Sort `O(n log n)`, scan `O(n)`: `O(n log n)` time, `O(1)` extra.
**Follow-up:** *Weighted or limited darts?* Different problem. *Same as #36?* Yes: answer = number kept in #36 (note `>` vs `>=`). *Sort by start?* Works, but you track the min end of the group.

**More scenarios on the same pattern**

**Variant A (crossover: partition by last occurrence)**
- **Question:** LC 763 Partition Labels. Partition a string into as many parts as possible so that each letter appears in at most one part; return the sizes.
- **Scenario:** A librarian splits a shelf of coded books into the most sections possible, so that no code appears in two sections.
- **Pattern and cost:** Each letter defines an interval from first to last occurrence. Scan with the farthest last-occurrence; cut when `i` reaches it. `O(n)` time, `O(1)` space (26 letters).

**Variant B (crossover to sort by start + heap)**
- **Question:** LC 1353 Maximum Number of Events That Can Be Attended. Each event has a start and end day and you attend one event per day. Return the maximum number of events you can attend.
- **Scenario:** A student picks one talk per day from a list of multi-day workshops. How many can be attended?
- **Pattern and cost:** Sort by start; each day, push the ends of events that have started into a min-heap and attend the one that ends soonest. `O(n log n)` time, `O(n)` space (Heap repo). The greedy is "earliest deadline first".

---

### 41. Meeting Rooms (#41)

**Original question:** LC 252 (premium). Given an array of meeting time `intervals`, determine whether a person could attend all meetings.

**Scenario:** Can a single person attend every session on today's schedule, or does something clash?

**Ask first:**
1. Does a meeting ending at 10:00 clash with one starting at 10:00?
2. Is the schedule in order?

**Spot it:** "Does anything overlap?" Order by start time; then only *neighbours* can clash.

**Brute force:** Compare all pairs: `O(n²)`.

**Solve:** ([41-meeting-rooms.md](05-intervals/41-meeting-rooms.md))
```python
def canAttendMeetings(intervals: list[list[int]]) -> bool:
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True
```

**Cost:** Sort `O(n log n)`, scan `O(n)`: `O(n log n)` time, `O(1)` extra.
**Follow-up:** *Return the clashing pair?* Return the neighbours. *How many rooms?* #37. *Why neighbours only?* If any pair clashes, some adjacent pair clashes after sorting.

**More scenarios on the same pattern**

**Variant A (crossover to a heap with ties and delays)**
- **Question:** LC 2402 Meeting Rooms III. There are `n` rooms; meetings are given by start and end and take the lowest-numbered free room, otherwise they wait for the room that frees first (keeping their duration). Return the room that hosted the most meetings.
- **Scenario:** A hospital assigns operating rooms to procedures; delayed ones wait for the next free room. Which room is busiest?
- **Pattern and cost:** Two heaps (free rooms by number, busy rooms by free-time). `O(m log m + m log n)`. Simulation, not just a sweep.

**Variant B (same as #37 in disguise)**
- **Question:** LC 2406 Divide Intervals Into Minimum Number of Groups. Divide the intervals into the minimum number of groups so no two intervals in a group overlap; return that number.
- **Scenario:** A school splits sports sessions into the fewest tracks so that sessions in the same track never clash.
- **Pattern and cost:** It is the peak number of simultaneous intervals: sort starts and ends, sweep. `O(n log n)` time, `O(n)` space. Learn to recognise "minimum groups" as "maximum overlap".

---

### Topic 6. Matrix / 2D Array

---

### 42. Valid Sudoku (#42)

**Original question:** LC 36. Determine if a `9 x 9` Sudoku board is valid. Only filled cells need to be validated: each row, each column and each of the nine `3 x 3` boxes must contain the digits `1-9` without repetition. The board may be partially filled and need not be solvable.

**Scenario:** A puzzle app lets users fill a grid by hand and wants an instant check that nothing repeats within a row, a column, or any of the nine marked blocks, even if the puzzle isn't finished.

**Ask first:**
1. Do I only check the current state, not whether it can be solved?
2. How are empty cells represented?

**Spot it:** Three overlapping "no repeats" rules over the same 81 cells. Remember what each row, column and block has already seen.

**Brute force:** For each cell compare against its row, column and block: constant per cell, so it's `O(81 · 27)`, fixed. The real improvement is code simplicity: one set per group instead of re-scanning.

**Solve:** ([42-valid-sudoku.md](06-matrix/42-valid-sudoku.md))
```python
from collections import defaultdict

def isValidSudoku(board: list[list[str]]) -> bool:
    rows, cols, boxes = defaultdict(set), defaultdict(set), defaultdict(set)
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == ".":
                continue
            box = (r // 3, c // 3)
            if val in rows[r] or val in cols[c] or val in boxes[box]:
                return False
            rows[r].add(val)
            cols[c].add(val)
            boxes[box].add(val)
    return True
```

**Cost:** The board is fixed at 81 cells, so the loop is a constant `O(1)` time and `O(1)` space (at most 81 entries). For an `n × n` board it would be `O(n²)` time and space.
**Follow-up:** *Solve it?* Variant A (backtracking). *Bitmasks instead of sets?* One integer per row/column/box, same cost, faster. *`n × n` board?* Box index `(r // sqrt(n), c // sqrt(n))`.

**More scenarios on the same pattern**

**Variant A (crossover to backtracking)**
- **Question:** LC 37 Sudoku Solver. Fill in the empty cells so the board is a valid solution.
- **Scenario:** The app's "solve it for me" button.
- **Pattern and cost:** Validity checks aren't enough; you must *search*: try a digit, recurse, undo. Worst case exponential, pruned heavily by the same row/column/box sets (Backtracking repo).

**Variant B (same sets, different shape)**
- **Question:** LC 2133 Check if Every Row and Column Contains All Numbers. An `n × n` matrix is valid if every row and column contains all integers from `1` to `n`. Return whether it is valid.
- **Scenario:** A rota grid must show each of `n` staff exactly once per row and per column. Is it fair?
- **Pattern and cost:** One set per row and column (or one pass with a seen set per line). `O(n²)` time, `O(n)` space.

---

### 43. Rotate Image (#43)

**Original question:** LC 48. You are given an `n x n` 2D `matrix` representing an image. Rotate the image by 90 degrees clockwise, **in place**.

**Scenario:** A photo editor must turn a square picture a quarter-turn clockwise inside the same memory buffer, because there isn't room for a second copy.

**Ask first:**
1. Is the matrix always square? Clockwise or counter-clockwise?
2. Is `O(n²)` extra space forbidden?

**Spot it:** "Rotate in place". A rotation is a **transpose** (swap across the diagonal) followed by **reversing each row**.

**Brute force:** Copy into a new matrix with `new[c][n-1-r] = old[r][c]`: `O(n²)` time, `O(n²)` space.

**Solve:** ([43-rotate-image.md](06-matrix/43-rotate-image.md))
```python
def rotate(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):               # start at i + 1: each pair swapped once
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
```

**Cost:** The transpose touches about `n²/2` pairs; reversing touches every cell once: `O(n²)` time (linear in the number of cells), `O(1)` extra space.
**Follow-up:** *Counter-clockwise?* Transpose, then reverse each column (or reverse each row first, then transpose). *Non-square?* Not in place: Variant A. *180 degrees?* Reverse rows, then reverse each row.

**More scenarios on the same pattern**

**Variant A (crossover: non-square can't be in place)**
- **Question:** LC 867 Transpose Matrix. Return the transpose of an `m × n` matrix.
- **Scenario:** A reporting tool turns rows into columns for a rectangular table.
- **Pattern and cost:** A non-square result has a different shape, so you must allocate a new matrix: `O(m·n)` time and space. The in-place trick of #43 only works because the shape stays square.

**Variant B (row operation, small change)**
- **Question:** LC 832 Flipping an Image. For each row of a binary matrix, flip it horizontally, then invert it (`0 ↔ 1`).
- **Scenario:** A scanner mirrors an image and swaps black and white.
- **Pattern and cost:** Two pointers per row: swap and invert as they meet. `O(m·n)` time, `O(1)` extra. Careful with the middle element in odd-length rows.

---

### 44. Spiral Matrix (#44)

**Original question:** LC 54. Given an `m x n` matrix, return all elements in spiral order.

**Scenario:** A robot vacuum has a map of a rectangular floor. Output the cells in the order it will clean them: the outer ring first, then spiralling inward.

**Ask first:**
1. Is the matrix always non-empty? Can it be a single row or column?
2. Clockwise from the top-left?

**Spot it:** "Peel the outer ring." Keep four shrinking boundaries: `top`, `bottom`, `left`, `right`.

**Brute force:** There's no asymptotic improvement over `O(m·n)`. The naive version marks visited cells in a separate matrix (`O(m·n)` extra space); boundaries avoid it.

**Solve:** ([44-spiral-matrix.md](06-matrix/44-spiral-matrix.md))
```python
def spiralOrder(matrix: list[list[int]]) -> list[int]:
    if not matrix:
        return []
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            res.append(matrix[top][col])
        top += 1
        for row in range(top, bottom + 1):
            res.append(matrix[row][right])
        right -= 1
        if top <= bottom:                           # guard: a single remaining row
            for col in range(right, left - 1, -1):
                res.append(matrix[bottom][col])
            bottom -= 1
        if left <= right:                           # guard: a single remaining column
            for row in range(bottom, top - 1, -1):
                res.append(matrix[row][left])
            left += 1
    return res
```

**Cost:** Every cell is visited exactly once: `O(m·n)` time, `O(1)` extra (the output isn't counted).
**Follow-up:** *Why the two guards?* Without them a single row or column is traversed twice. *Counter-clockwise?* Swap direction order. *Fill a spiral instead?* Variant A.

**More scenarios on the same pattern**

**Variant A (the reverse: generate a spiral)**
- **Question:** LC 59 Spiral Matrix II. Given `n`, generate an `n × n` matrix filled with `1..n²` in spiral order.
- **Scenario:** A game designer wants a numbered square labyrinth that spirals inward.
- **Pattern and cost:** Same four boundaries, but writing instead of reading. `O(n²)` time and space (the output).

**Variant B (diagonal bounce)**
- **Question:** LC 498 Diagonal Traverse. Return all elements of an `m × n` matrix in diagonal order (alternating up-right and down-left).
- **Scenario:** A printer prints a grid along its anti-diagonals, changing direction at the edges.
- **Pattern and cost:** Index arithmetic (`r + c` is constant along a diagonal); change direction at the borders. `O(m·n)` time, `O(1)` extra. Not yet written up in the repo (#76).

---

### 45. Set Matrix Zeroes (#45)

**Original question:** LC 73. Given an `m x n` integer matrix, if an element is `0`, set its entire row and column to `0`. You must do it in place.

**Scenario:** A spreadsheet has a rule: if any cell in a row or column holds a 0, the whole row and column must be wiped to 0. Do it in the same sheet, using as little extra memory as you can.

**Ask first:**
1. Must it be `O(1)` extra space, or is `O(m + n)` fine?
2. Can zeros created by the process cause further wiping? (No: use only the original zeros.)

**Spot it:** In place, "extra bookkeeping needed". The first row and first column can serve as the marker storage.

**Brute force:** Copy the matrix and read zeros from the copy: `O(m·n)` space. Or two sets of rows and columns to wipe: `O(m + n)` space.

**Solve:** ([45-set-matrix-zeroes.md](06-matrix/45-set-matrix-zeroes.md))
```python
def setZeroes(matrix: list[list[int]]) -> None:
    m, n = len(matrix), len(matrix[0])
    col_zero = False
    for i in range(m):                              # 1. mark in first row / column
        if matrix[i][0] == 0:
            col_zero = True
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    for i in range(1, m):                           # 2. zero inner cells from the markers
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if matrix[0][0] == 0:                           # 3. then the first row
        for j in range(n):
            matrix[0][j] = 0
    if col_zero:                                    # 4. then the first column
        for i in range(m):
            matrix[i][0] = 0
```

**Cost:** Each cell is visited a constant number of times: `O(m·n)` time, `O(1)` extra space (one boolean). The order matters: wiping the first row or column early would destroy the markers.
**Follow-up:** *`O(m + n)` is fine?* Two sets, simpler and less error-prone. *Why `col_zero`?* `matrix[0][0]` can't mark both the first row and the first column. *Mutation not allowed?* Copy first.

**More scenarios on the same pattern**

**Variant A (crossover: 2D prefix sums)**
- **Question:** LC 304 Range Sum Query 2D - Immutable. Answer many queries for the sum of the sub-rectangle between `(row1, col1)` and `(row2, col2)`.
- **Scenario:** A heat map is queried again and again for the total reading in a rectangular region.
- **Pattern and cost:** Build a 2D prefix table once (`O(m·n)`), answer each query in `O(1)` with inclusion-exclusion. Many queries on fixed data is the clue.

**Variant B (crossover to binary search)**
- **Question:** LC 74 Search a 2D Matrix. Each row is sorted, and each row's first value is greater than the previous row's last. Return whether `target` is in the matrix.
- **Scenario:** A price table is listed row by row, increasing across the whole table. Is price `P` present?
- **Pattern and cost:** Treat it as one flattened ordered list and binary search: `O(log(m·n))` time, `O(1)` space. Index maths replaces any scan (Binary-Search repo).

---

### 46. Game of Life (#46)

**Original question:** LC 289. Given an `m x n` board where each cell is live (`1`) or dead (`0`), compute the next state using the rules: a live cell with fewer than 2 or more than 3 live neighbours dies; a live cell with 2 or 3 survives; a dead cell with exactly 3 live neighbours becomes live. All updates happen simultaneously. Update the board in place.

**Scenario:** A simulation updates a grid of cells where every cell's next state depends on its neighbours' *current* states, and all cells change at once. Update the grid without allocating a second one.

**Ask first:**
1. Are the updates simultaneous (based on the old state)?
2. Is the board finite, with the edges treated as dead?

**Spot it:** In place + "depends on the old value of neighbours". Encode both old and new state in one number.

**Brute force:** Copy the board, read from the copy, write to the original: `O(m·n)` time, `O(m·n)` space.

**Solve:** ([46-game-of-life.md](06-matrix/46-game-of-life.md))
```python
def gameOfLife(board: list[list[int]]) -> None:
    rows, cols = len(board), len(board[0])
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(rows):
        for c in range(cols):
            live = 0
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and abs(board[nr][nc]) == 1:
                    live += 1                      # abs: -1 still means "was alive"
            if board[r][c] == 1 and (live < 2 or live > 3):
                board[r][c] = -1                   # live -> dead
            elif board[r][c] == 0 and live == 3:
                board[r][c] = 2                    # dead -> live
    for r in range(rows):
        for c in range(cols):
            board[r][c] = 1 if board[r][c] > 0 else 0
```

**Cost:** Each cell checks 8 neighbours (a constant), then one clean-up pass: `O(m·n)` time, `O(1)` extra space.
**Follow-up:** *Infinite board?* Variant A. *Only a few live cells?* Store live cells in a set. *Why the codes `-1` and `2`?* They preserve the old state while recording the new one.

**More scenarios on the same pattern**

**Variant A (crossover: sparse, unbounded board)**
- **Question:** Game of Life on an infinite board (the follow-up of LC 289).
- **Scenario:** The same simulation, but the world has no edges, and almost every cell is empty.
- **Pattern and cost:** An array can't be infinite. Keep a set of live cells; for each live cell, count neighbours with a `Counter`; apply the rules to cells with a count. `O(L)` per step for `L` live cells, `O(L)` space.

**Variant B (in-place gravity)**
- **Question:** LC 1861 Rotating the Box. A box grid contains stones, obstacles and empty cells. Rotate the box 90 degrees clockwise; stones fall to the bottom due to gravity. Return the result.
- **Scenario:** A game tilts a board; falling pieces settle against obstacles.
- **Pattern and cost:** Per row, a read/write pointer from the right (settle stones before rotation), then an index-mapped copy. `O(m·n)` time. The rotation itself needs a new (non-square) matrix.

---

### Topic 7. In-Place Array Manipulation

---

### 47. Merge Sorted Array (#47)

**Original question:** LC 88. You are given two integer arrays `nums1` and `nums2` sorted in non-decreasing order, and integers `m` and `n` for the number of valid elements in each. `nums1` has length `m + n`, with the last `n` slots empty. Merge `nums2` into `nums1` in place so it is sorted.

**Scenario:** Two daily logs, each in time order, must be combined into the first log's buffer, which already has empty space reserved at its end. No spare buffer is allowed.

**Ask first:**
1. Is the spare space at the *end* of the first array?
2. Are duplicates allowed, and is stability important?

**Spot it:** Merging from the **front** would overwrite values not yet read. From the **back**, you only write into slots that are empty or already consumed.

**Brute force:** Copy `nums2` into the spare slots and sort: `O((m + n) log (m + n))`. Or merge into a new array: `O(m + n)` space.

**Solve:** ([47-merge-sorted-array.md](07-in-place-array-manipulation/47-merge-sorted-array.md))
```python
def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    p1, p2, p = m - 1, n - 1, m + n - 1
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
    while p2 >= 0:                       # leftovers of nums2; leftovers of nums1 are already in place
        nums1[p] = nums2[p2]
        p2 -= 1
        p -= 1
```

**Cost:** Each pointer only moves backward: at most `m + n` steps, `O(m + n)` time, `O(1)` space.
**Follow-up:** *Why not copy `nums1` leftovers?* They're already in their final slots. *Merge `k` arrays?* Heap, `O(N log k)`. *Linked lists instead?* No shifting is needed, merge from the front.

**More scenarios on the same pattern**

**Variant A (two pointers from the ends)**
- **Question:** LC 977 Squares of a Sorted Array. Given an array sorted in non-decreasing order, return an array of the squares of each number, also sorted.
- **Scenario:** A sensor's readings (including negatives) are listed from lowest to highest; report their squared magnitudes in order.
- **Pattern and cost:** The largest square is at one of the two ends. Two pointers inward, writing the result from the back. `O(n)` time, `O(n)` output. Squaring and sorting would be `O(n log n)`.

**Variant B (crossover to binary search)**
- **Question:** LC 4 Median of Two Sorted Arrays. Return the median of two sorted arrays in `O(log(m + n))` time.
- **Scenario:** Two regional ranked lists must be combined and the middle score reported, without merging them.
- **Pattern and cost:** Merging is `O(m + n)`. The log bound needs a binary search on the partition point of the smaller array (Binary-Search repo).

---

### 48. Remove Element (#48)

**Original question:** LC 27. Given an integer array `nums` and a value `val`, remove all occurrences of `val` in place. The relative order of the other elements may be changed (the write-up keeps it). Return `k`, the number of elements not equal to `val`; the first `k` slots must hold them.

**Scenario:** A list of user records has to drop every entry with a given banned ID, reusing the same array. Report how many entries remain.

**Ask first:**
1. Must the order of the remaining elements be kept?
2. Do the slots after position `k` matter? (No.)

**Spot it:** "Remove in place and return the new length". Read everything, write only what is kept.

**Brute force:** Delete each match with `list.pop` / shift the rest: `O(n²)`. Or build a new list: `O(n)` space.

**Solve:** ([48-remove-element.md](07-in-place-array-manipulation/48-remove-element.md))
```python
def removeElement(nums: list[int], val: int) -> int:
    index = 0                              # write pointer
    for i in range(len(nums)):             # read pointer
        if nums[i] != val:
            nums[index] = nums[i]
            index += 1
    return index
```

**Cost:** One pass: `O(n)` time, `O(1)` space.
**Follow-up:** *Matches are rare and order doesn't matter?* Swap the match with the last element and shrink: fewer writes. *Order must be kept?* The read/write pointer is stable; the swap version isn't. *Return the removed count?* `n - index`.

**More scenarios on the same pattern**

**Variant A (move, don't remove)**
- **Question:** LC 283 Move Zeroes. Move all `0`s to the end of the array while keeping the relative order of the non-zero elements, in place.
- **Scenario:** A task list should push empty slots to the end without reordering the real tasks.
- **Pattern and cost:** Write pointer for non-zeros, then fill the rest with zeros (or swap as you go). `O(n)` time, `O(1)` space. Not yet written up (#77).

**Variant B (crossover: write backward)**
- **Question:** LC 1089 Duplicate Zeros. Duplicate each `0` in a fixed-length array, shifting the rest right and discarding what falls off. Modify in place.
- **Scenario:** A tape needs a blank copied after every blank, within the same length.
- **Pattern and cost:** A forward pass would overwrite unread values. Count zeros first, then fill from the back, like #47. `O(n)` time, `O(1)` space.

---

### 49. Remove Duplicates from Sorted Array (#49)

**Original question:** LC 26. Given an integer array `nums` sorted in non-decreasing order, remove the duplicates in place so each unique element appears only once, keeping the relative order. Return the number of unique elements `k`.

**Scenario:** A log of IDs is already in order, with repeated entries. Compact the same array so each ID appears once, and report how many IDs remain.

**Ask first:**
1. Is the array definitely in order?
2. Do I need to keep the first or the last occurrence? (Same for plain values.)

**Spot it:** Because the data is ordered, equal values are neighbours: compare each element only with the last *kept* one.

**Brute force:** A `set` plus rebuilding the list: `O(n)` time but `O(n)` space and it needs ordering again. Deleting duplicates one at a time: `O(n²)`.

**Solve:** ([49-remove-duplicates-from-sorted-array.md](07-in-place-array-manipulation/49-remove-duplicates-from-sorted-array.md))
```python
def removeDuplicates(nums: list[int]) -> int:
    writer = 0
    for reader in range(1, len(nums)):
        if nums[reader] != nums[writer]:
            writer += 1
            nums[writer] = nums[reader]
    return writer + 1
```

**Cost:** One pass: `O(n)` time, `O(1)` space. (Empty input would need a guard before indexing `nums[0]`.)
**Follow-up:** *Allow two copies?* #53. *Unsorted?* Needs a hash set (Variant A). *Linked list?* Same idea with `next` pointers.

**More scenarios on the same pattern**

**Variant A (crossover: unsorted means a hash set)**
- **Question:** Remove duplicates in place from an **unsorted** array, keeping the first occurrence of each value, and return the new length.
- **Scenario:** An unordered list of customer IDs must be de-duplicated in its own buffer, keeping first appearances in order.
- **Pattern and cost:** Adjacent comparison no longer works. Read/write pointer plus a `seen` set: `O(n)` time, `O(n)` space. Without extra memory, the only option is sorting (loses original order) or `O(n²)` scanning.

**Variant B (crossover to a stack)**
- **Question:** LC 1209 Remove All Adjacent Duplicates in String II. Repeatedly remove `k` equal adjacent characters from a string until none remain; return the result.
- **Scenario:** A text cleaner deletes any run of `k` identical characters, and runs can form again after deletions.
- **Pattern and cost:** Removals expose new neighbours, so the previous kept character matters: use a stack of `(char, count)`. `O(n)` time, `O(n)` space (Stack repo).

---

### 50. Rotate Array (#50)

**Original question:** LC 189. Given an integer array `nums`, rotate the array to the right by `k` steps, where `k` is non-negative.

**Scenario:** A shift schedule lists `n` workers in order. Each week everyone moves `k` places to the right (the last `k` wrap to the front). Update the schedule in place.

**Ask first:**
1. Can `k` exceed `n`? (Use `k % n`.)
2. In place with `O(1)` extra space?

**Spot it:** "Rotate in place". Three reversals: reverse the first `n - k`, reverse the last `k`, then reverse all.

**Brute force:** Shift by one, `k` times: `O(n·k)`. Or build a new list with slicing: `O(n)` time, `O(n)` space.

**Solve:** ([50-rotate-array.md](07-in-place-array-manipulation/50-rotate-array.md))
```python
def rotate(nums: list[int], k: int) -> None:
    n = len(nums)
    k %= n

    def reverse(start: int, end: int) -> None:
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

    reverse(0, n - k - 1)
    reverse(n - k, n - 1)
    reverse(0, n - 1)
```

**Cost:** Three reversals touch about `2n` elements in total: `O(n)` time, `O(1)` space.
**Follow-up:** *Rotate left?* Reverse in a different order, or use `k = n - k`. *Why does it work?* Each half is reversed twice (back to normal order) and the halves swap. *Empty array?* `k % 0` raises; guard.

**More scenarios on the same pattern**

**Variant A (crossover to binary search)**
- **Question:** LC 153 Find Minimum in Rotated Sorted Array. A sorted array of distinct values was rotated at an unknown pivot. Return the minimum element in `O(log n)` time.
- **Scenario:** A circular log was cut and re-spliced at some point. Find the earliest entry.
- **Pattern and cost:** The rotated data still has structure (two ordered halves), so binary search, comparing `mid` with the right end. `O(log n)` time, `O(1)` space (Binary-Search repo). A scan is `O(n)`.

**Variant B (strings)**
- **Question:** LC 796 Rotate String. Return whether `goal` can be obtained by rotating `s` some number of positions.
- **Scenario:** Two circular wheel labels: are they the same label, just turned?
- **Pattern and cost:** `goal` is a rotation of `s` iff lengths match and `goal in s + s`. `O(n)` with a linear search (KMP), `O(n²)` worst case with a naive search.

---

### 51. Next Permutation (#51)

**Original question:** LC 31. Rearrange `nums` into the lexicographically next greater permutation. If no such arrangement exists, rearrange into the lowest possible order (ascending). Do it in place with `O(1)` extra memory.

**Scenario:** A combination lock steps through all arrangements of its dials in dictionary order. Given the current arrangement, produce the next one; after the last one, wrap back to the first.

**Ask first:**
1. Can there be repeated values?
2. Should it wrap around to the smallest arrangement when there is no next one?

**Spot it:** "The next larger arrangement, in place." Find the rightmost spot where a bigger digit could go, bump it minimally, and then make the tail as small as possible.

**Brute force:** Generate all permutations and find the next: `O(n!)`.

**Solve:** ([51-next-permutation.md](07-in-place-array-manipulation/51-next-permutation.md))
```python
def nextPermutation(nums: list[int]) -> None:
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:      # 1. last "ascent": the pivot
        i -= 1
    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:                 # 2. smallest value bigger than the pivot, from the right
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    left, right = i + 1, n - 1                    # 3. reverse the tail (it is non-increasing)
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```

**Cost:** Three sequential scans, each at most `n`: `O(n)` time, `O(1)` space.
**Follow-up:** *Previous permutation?* Mirror the comparisons. *k-th permutation?* Variant B. *Why `>=` and `<=`?* They handle duplicates.

**More scenarios on the same pattern**

**Variant A (same engine, digits)**
- **Question:** LC 556 Next Greater Element III. Given a positive integer `n`, return the smallest integer larger than `n` made of the same digits, or `-1` (also `-1` if it exceeds 32 bits).
- **Scenario:** A ticket printer wants the next larger ticket number that reuses the same digits.
- **Pattern and cost:** Digits → next permutation; add an overflow check. `O(d)` for `d` digits.

**Variant B (crossover to math)**
- **Question:** LC 60 Permutation Sequence. Return the `k`-th permutation of `1..n`.
- **Scenario:** A game wants the 1000th arrangement of `n` tokens without listing the earlier ones.
- **Pattern and cost:** Repeated next-permutation is `O(n·k)`. Use the factorial number system: `k // (n-1)!` picks the first digit, and so on. `O(n²)` with list removals, `O(n)` space.

---

### 52. Plus One (#52)

**Original question:** LC 66. A large integer is stored as an array of digits (most significant first). Add one to it and return the resulting array of digits.

**Scenario:** A car's odometer is stored as an array of digits. Increment it by one kilometre.

**Ask first:**
1. Is there a leading zero? (No, except for the number 0 itself.)
2. May I modify the input array?

**Spot it:** Elementary-school addition: work from the least significant digit and stop as soon as the carry is absorbed.

**Brute force:** Convert to an integer, add one, convert back. Fine in Python, but it overflows in fixed-width languages and misses the point of the exercise.

**Solve:** ([52-plus-one.md](07-in-place-array-manipulation/52-plus-one.md))
```python
def plusOne(digits: list[int]) -> list[int]:
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits                  # all were 9s
```

**Cost:** Worst case (all 9s) `O(n)`; typically `O(1)` since the carry stops early. Space `O(1)`, except the all-9s case allocates a longer list.
**Follow-up:** *Add `k` instead of one?* Variant A. *Two big numbers?* Variant B. *Overflow?* This is exactly why digit arrays exist.

**More scenarios on the same pattern**

**Variant A (add a number)**
- **Question:** LC 989 Add to Array-Form of Integer. Given the array form of an integer `num` and an integer `k`, return the array form of `num + k`.
- **Scenario:** A big-counter stored as digits needs to jump forward by a given amount.
- **Pattern and cost:** Add digit by digit from the end, carrying through `k`'s digits too. `O(max(n, log k))` time.

**Variant B (two strings)**
- **Question:** LC 415 Add Strings. Add two non-negative integers given as strings, without converting to integers.
- **Scenario:** A bank's legacy system stores huge balances as text. Add two of them.
- **Pattern and cost:** Two pointers from the right with a carry, building the result in a list. `O(max(m, n))` time and space.

---

### 53. Remove Duplicates from Sorted Array II (#53)

**Original question:** LC 80. Given a sorted integer array `nums`, remove some duplicates in place so that each unique element appears **at most twice**. Return the new length.

**Scenario:** An ordered event log may keep at most two entries per ID. Trim the log in place and report its new length.

**Ask first:**
1. Is the array sorted?
2. Is the limit always two, or could it be `K`?

**Spot it:** Same read/write pointer as #49, but compare with the element **two slots behind the writer**.

**Brute force:** Count occurrences with a dict and rebuild: `O(n)` time, `O(n)` space.

**Solve:** ([53-remove-duplicates-from-sorted-array-ii.md](07-in-place-array-manipulation/53-remove-duplicates-from-sorted-array-ii.md))
```python
def removeDuplicates(nums: list[int]) -> int:
    if len(nums) <= 2:
        return len(nums)
    writer = 2
    for reader in range(2, len(nums)):
        if nums[reader] != nums[writer - 2]:
            nums[writer] = nums[reader]
            writer += 1
    return writer
```

**Cost:** One pass: `O(n)` time, `O(1)` space.
**Follow-up:** *At most `K`?* Start `writer` at `K` and compare with `nums[writer - K]` (Variant A). *Unsorted?* Counter + write pointer (Variant B). *Why does comparing with `writer - 2` work?* Sorted order guarantees that if `nums[writer - 2] == nums[reader]`, then the slot in between also holds that value.

**More scenarios on the same pattern**

**Variant A (general K)**
- **Question:** LC 80 generalised: keep at most `K` copies of each value in a sorted array, in place.
- **Scenario:** A quota system allows up to `K` entries per customer in a sorted log.
- **Pattern and cost:** `writer` starts at `K`; compare with `nums[writer - K]`. `O(n)` time, `O(1)` space.

**Variant B (crossover: unsorted needs counts)**
- **Question:** Keep at most two copies of each value in an **unsorted** array, in place, preserving order.
- **Scenario:** The same quota rule, but the log arrives unordered.
- **Pattern and cost:** The `writer - 2` trick relies on sorted order. Use a `Counter` and a write pointer: `O(n)` time, `O(n)` space. Without extra memory you'd have to sort first and lose the original order.

---

### Topic 8. Greedy & One-Pass Array Scans

---

### 54. Majority Element (#54)

**Original question:** LC 169. Given an array `nums` of size `n`, return the majority element, the element that appears more than `⌊n / 2⌋` times. You may assume it always exists.

**Scenario:** A poll collected `n` votes, and one candidate got strictly more than half of them. Name the winner using as little memory as possible, in one pass.

**Ask first:**
1. Is a majority guaranteed to exist? (If not, a verification pass is needed.)
2. Is the data a stream, or can I re-read it?

**Spot it:** "More than half" means pairs of *different* votes can cancel each other, and the majority still survives the cancelling.

**Brute force:** Count with a hash map: `O(n)` time but `O(n)` space. Sorting and taking the middle element: `O(n log n)`. Counting each candidate by rescanning: `O(n²)`.

**Solve:** ([54-majority-element.md](08-greedy-one-pass-scans/54-majority-element.md))
```python
def majorityElement(nums: list[int]) -> int:
    count = 0
    candidate = None
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    return candidate
```

**Cost:** One pass, constant work: `O(n)` time, `O(1)` space.
**Follow-up:** *Not guaranteed?* Add a second pass that counts the candidate. *More than `n/3`?* Two candidates (Variant A). *Stream?* Works online. *Sorted?* The middle element is the answer (Variant B).

**More scenarios on the same pattern**

**Variant A (two candidates)**
- **Question:** LC 229 Majority Element II. Return all elements that appear more than `⌊n / 3⌋` times, in `O(n)` time and `O(1)` space.
- **Scenario:** A survey reports every option that was picked by more than a third of respondents.
- **Pattern and cost:** At most two such values can exist, so keep two candidates and two counters, then verify both in a second pass. `O(n)` time, `O(1)` space.

**Variant B (crossover: ordered data)**
- **Question:** Given an array **sorted** in non-decreasing order in which one value occurs more than `n/2` times, return it.
- **Scenario:** A pre-sorted vote list has a clear winner.
- **Pattern and cost:** The majority must occupy the middle position, so `nums[n // 2]` in `O(1)`. Spotting that the extra structure removes the need for any algorithm is the lesson.

---

### 55. Jump Game (#55)

**Original question:** LC 55. You are given an integer array `nums`; you start at index 0, and each `nums[i]` is the maximum jump length from `i`. Return `true` if you can reach the last index.

**Scenario:** A path of stepping stones has a number on each stone: the farthest you can leap from it. Starting on the first stone, can you get to the last one?

**Ask first:**
1. Is `nums[i]` the maximum jump, or exactly the jump length?
2. Are all values non-negative?

**Spot it:** Reachability depends on one number: the **farthest index reached so far**. Everything up to it is reachable.

**Brute force:** DFS or DP over all jump choices from every index: `O(n²)` (or exponential without memo).

**Solve:** ([55-jump-game.md](08-greedy-one-pass-scans/55-jump-game.md))
```python
def canJump(nums: list[int]) -> bool:
    max_reach = 0
    target = len(nums) - 1
    for i in range(len(nums)):
        if i > max_reach:              # stuck before reaching i
            return False
        max_reach = max(max_reach, i + nums[i])
        if max_reach >= target:
            return True
    return True
```

**Cost:** One pass: `O(n)` time, `O(1)` space.
**Follow-up:** *Fewest jumps?* #56. *Return the path?* Track a parent. *Jumps can go backwards?* BFS (Variant A).

**More scenarios on the same pattern**

**Variant A (crossover to BFS)**
- **Question:** LC 1306 Jump Game III. From index `start`, you can jump to `i + arr[i]` or `i - arr[i]`. Return whether you can reach any index with value `0`.
- **Scenario:** A board game lets a token jump exactly the number written on its square, forward or backward. Can it land on a "goal" square?
- **Pattern and cost:** Moves go both directions with exact lengths, so the farthest-reach summary no longer works. BFS/DFS with a visited array: `O(n)` time, `O(n)` space (Graphs repo).

**Variant B (crossover to DP + deque)**
- **Question:** LC 1696 Jump Game VI. From index `i` you can jump up to `k` steps; each visited index adds its value (can be negative). Return the maximum score to reach the last index.
- **Scenario:** A hiker takes strides of at most `k` steps and collects points (or penalties) on each stop. What's the best total at the finish?
- **Pattern and cost:** Maximising a sum needs DP: `dp[i] = nums[i] + max(dp[i-k..i-1])`, with a monotonic deque for the sliding max. `O(n)` time, `O(n)` space (DP repo).

---

### 56. Jump Game II (#56)

**Original question:** LC 45. Given the same setup as Jump Game, return the minimum number of jumps to reach the last index. It's guaranteed you can reach it.

**Scenario:** On the same stepping stones, what's the fewest leaps needed to get from the first stone to the last?

**Ask first:**
1. Is the last index guaranteed to be reachable?
2. Is a single-element array possible (answer `0`)?

**Spot it:** "Fewest hops" = BFS by layers, but the layers are just ranges. Track where the current layer ends and the farthest reach of the next one.

**Brute force:** DP, `dp[i] = min(dp[j] + 1)` over all `j` that can reach `i`: `O(n²)`. Or BFS building the graph.

**Solve:** ([56-jump-game-ii.md](08-greedy-one-pass-scans/56-jump-game-ii.md))
```python
def jump(nums: list[int]) -> int:
    n = len(nums)
    if n <= 1:
        return 0
    jumps = current_end = max_reach = 0
    for i in range(n - 1):
        max_reach = max(max_reach, i + nums[i])
        if i == current_end:           # finished scanning this layer: take a jump
            jumps += 1
            current_end = max_reach
    return jumps
```

**Cost:** One pass over `n - 1` indices: `O(n)` time, `O(1)` space.
**Follow-up:** *Unreachable end?* Return `-1` when `max_reach` stalls. *Why not DP?* `O(n²)`. *Count the number of ways?* That is DP.

**More scenarios on the same pattern**

**Variant A (interval covering)**
- **Question:** LC 1024 Video Stitching. Given video `clips` (start, end), return the fewest clips needed to cover `[0, time]`, or `-1`.
- **Scenario:** A broadcaster has many overlapping recorded segments. What's the fewest needed to cover a whole event?
- **Pattern and cost:** The same layer-by-layer greedy: for each point, the farthest end among clips starting at or before it. Sort or bucket by start. `O(n log n)` (or `O(n + time)`).

**Variant B (crossover to a heap)**
- **Question:** LC 871 Minimum Number of Refueling Stops. A car starts with `startFuel`, travels toward `target`, and `stations[i] = [position, fuel]` can be refuelled. Return the minimum number of stops, or `-1`.
- **Scenario:** A delivery van must cross a desert with fuel depots along the way. Fewest refuels?
- **Pattern and cost:** Greedy again, but the choice is *which depot's fuel to take, in hindsight*: keep a max-heap of fuel from stations passed, and refuel from the biggest when stuck. `O(n log n)` (Heap repo).

---

### 57. Gas Station (#57)

**Original question:** LC 134. There are `n` gas stations on a circular route. `gas[i]` is the fuel at station `i`, and `cost[i]` is the fuel to travel from `i` to `i + 1`. Return the starting station's index if you can complete the circuit once clockwise starting with an empty tank, otherwise `-1`. A solution, if it exists, is unique.

**Scenario:** A delivery truck runs a loop of depots. Each depot gives some fuel, and the leg to the next depot burns some fuel. Which depot should it start from to finish the loop without running dry?

**Ask first:**
1. Is the answer guaranteed unique if it exists?
2. Does the truck start with an empty tank?

**Spot it:** A running tank that must never go negative, on a loop. If you run dry at station `j` after starting at `s`, none of the stations between `s` and `j` can be a valid start either.

**Brute force:** Try every start and simulate the loop: `O(n²)`.

**Solve:** ([57-gas-station.md](08-greedy-one-pass-scans/57-gas-station.md))
```python
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    if sum(gas) < sum(cost):           # not enough fuel in total
        return -1
    total = res = 0
    for i in range(len(gas)):
        total += gas[i] - cost[i]
        if total < 0:                  # cannot start at any of the stations so far
            total = 0
            res = i + 1
    return res
```

**Cost:** Two linear passes (the sums, then the loop): `O(n)` time, `O(1)` space. A single-pass version keeps `total_surplus` alongside the current tank.
**Follow-up:** *Why is the global check enough?* If total gas ≥ total cost, one start must exist, and the reset finds it. *Return all starts?* Different problem. *Prefix-sum view?* The answer is the index after the minimum prefix of `gas - cost`.

**More scenarios on the same pattern**

**Variant A (prefix minimum)**
- **Question:** LC 1413 Minimum Value to Get Positive Step by Step Sum. Given `nums`, return the minimum positive starting value such that the running sum is never below 1.
- **Scenario:** A trader starts a day with a float of cash and makes a series of gains and losses. What's the smallest float that never lets the balance hit zero?
- **Pattern and cost:** Running sum, track its minimum; the answer is `1 - min_prefix` (at least 1). `O(n)` time, `O(1)` space.

**Variant B (greedy by counting)**
- **Question:** LC 621 Task Scheduler. Given tasks (letters) and a cooldown `n` between equal tasks, return the minimum number of time units to finish all tasks.
- **Scenario:** A printer must wait `n` rounds before running the same job type again. Shortest total schedule?
- **Pattern and cost:** No simulation needed: the most frequent task creates `(max_freq - 1)` gaps of length `n + 1`; the answer is `max(len(tasks), (max_freq - 1)(n + 1) + count_of_max)`. `O(len(tasks))` time, `O(1)` space. The skill is spotting the closed-form greedy.

---

### 58. Best Time to Buy and Sell Stock II (#58)

**Original question:** LC 122. Given `prices`, you may buy and sell as many times as you like, but you can hold at most one share at a time. Return the maximum profit.

**Scenario:** A trader can buy and sell a commodity every day, any number of times, holding at most one unit at a time. What's the best total profit over the price history?

**Ask first:**
1. Unlimited transactions, no fees, no cooldown?
2. May I sell and buy on the same day?

**Spot it:** With unlimited trades, every upward day-to-day step can be captured. No need to pick buy and sell days.

**Brute force:** Recursion over buy/sell/skip choices per day: exponential. DP with two states: `O(n)` time. The greedy is simpler.

**Solve:** ([58-best-time-to-buy-and-sell-stock-ii.md](08-greedy-one-pass-scans/58-best-time-to-buy-and-sell-stock-ii.md))
```python
def maxProfit(prices: list[int]) -> int:
    max_profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            max_profit += prices[i] - prices[i - 1]
    return max_profit
```

**Cost:** One pass: `O(n)` time, `O(1)` space.
**Follow-up:** *Transaction fee or cooldown?* The greedy breaks; use a state machine (Variants A, B). *Return the trades?* Merge consecutive rising days. *At most `k` trades?* DP.

**More scenarios on the same pattern**

**Variant A (crossover to DP: a fee)**
- **Question:** LC 714 Best Time to Buy and Sell Stock with Transaction Fee. Same as #58, but each transaction costs a fixed `fee`.
- **Scenario:** The trader now pays a flat fee on every completed trade.
- **Pattern and cost:** Capturing every small rise would burn fees. Two states (`cash`, `hold`) updated each day. `O(n)` time, `O(1)` space (DP repo).

**Variant B (crossover to DP: a cooldown)**
- **Question:** LC 309 Best Time to Buy and Sell Stock with Cooldown. After selling you cannot buy the next day.
- **Scenario:** After closing a position, the broker forces a one-day wait before the next purchase.
- **Pattern and cost:** Three states (`hold`, `sold`, `rest`). `O(n)` time, `O(1)` space (DP repo).

---

### 59. H-Index (#59)

**Original question:** LC 274. Given an array `citations` (the citation count of each paper), return the researcher's h-index: the maximum `h` such that the researcher has at least `h` papers with at least `h` citations each.

**Scenario:** A university ranks a researcher using the largest number `h` for which they have `h` papers that each have been cited at least `h` times. Given the citation counts, find `h`.

**Ask first:**
1. Are counts non-negative integers? Can the list be empty?
2. Is the data already ordered? Is `n` large enough that a sort matters?

**Spot it:** "Largest `h` such that `h` items have at least `h`". After ordering, the paper at position `i` has `n - i` papers at least as cited.

**Brute force:** Try each `h` from `n` down and count qualifying papers: `O(n²)`.

**Solve:** ([59-h-index.md](08-greedy-one-pass-scans/59-h-index.md))
```python
def hIndex(citations: list[int]) -> int:
    citations.sort()
    n = len(citations)
    for i in range(n):
        papers_remaining = n - i
        if citations[i] >= papers_remaining:
            return papers_remaining
    return 0
```

**Cost:** Sort `O(n log n)`, scan `O(n)`: `O(n log n)` time, `O(1)` extra. A counting version caps each count at `n` and buckets: `O(n)` time, `O(n)` space.
**Follow-up:** *Already ordered?* Binary search (Variant A). *Huge counts?* Cap at `n` (the bucket version). *Why can `h` never exceed `n`?* You only have `n` papers.

**More scenarios on the same pattern**

**Variant A (crossover to binary search)**
- **Question:** LC 275 H-Index II. `citations` is sorted in ascending order. Solve it in logarithmic time.
- **Scenario:** The citation list is already ranked. Find `h` without a full scan.
- **Pattern and cost:** Binary search for the first index with `citations[i] >= n - i`. `O(log n)` time, `O(1)` space.

**Variant B (crossover: bucket by frequency)**
- **Question:** LC 451 Sort Characters By Frequency. Sort a string in decreasing order of character frequency.
- **Scenario:** A word cloud lists letters from most to least common.
- **Pattern and cost:** Count, then bucket by count (like #5) or sort by count: `O(n)` with buckets, `O(n + k log k)` with a sort. `O(n)` space.

---

### 60. Candy (#60)

**Original question:** LC 135. `n` children stand in a line, each with a rating. Give each child at least one candy; a child with a higher rating than an adjacent child must get more candies than that neighbour. Return the minimum total number of candies.

**Scenario:** A teacher hands out sweets to a line of students, each with a performance score. Everyone gets at least one, and anyone who scored higher than a direct neighbour must get more than that neighbour. What's the fewest sweets needed?

**Ask first:**
1. Do equal ratings need equal or unequal candy counts? (Neither: no constraint between equals.)
2. Is the line a row (not a circle)?

**Spot it:** Two constraints, left and right. Satisfy them **one direction at a time**, then combine with `max`.

**Brute force:** Repeatedly fix violations until none remain: `O(n²)` worst case.

**Solve:** ([60-candy.md](08-greedy-one-pass-scans/60-candy.md))
```python
def candy(ratings: list[int]) -> int:
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):                         # left neighbour rule
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):                # right neighbour rule, keep the left result
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)
```

**Cost:** Two passes plus a sum: `O(n)` time, `O(n)` space (a one-pass `O(1)`-space slope-counting version exists but is fiddly).
**Follow-up:** *Circular line?* Different problem. *`O(1)` space?* Count up/down slopes. *Equal ratings must get equal candies?* Different problem.

**More scenarios on the same pattern**

**Variant A (two passes of running max/min)**
- **Question:** LC 581 Shortest Unsorted Continuous Subarray. Find the shortest subarray that, if sorted, makes the whole array sorted; return its length.
- **Scenario:** A leaderboard is almost in order. What's the smallest stretch that needs re-sorting?
- **Pattern and cost:** Left-to-right running max marks the last out-of-place position on the right; right-to-left running min marks the first on the left. Two passes: `O(n)` time, `O(1)` space.

**Variant B (up-then-down shape)**
- **Question:** LC 845 Longest Mountain in Array. A mountain subarray strictly increases then strictly decreases (length ≥ 3). Return the length of the longest one.
- **Scenario:** From an elevation profile, find the longest hill (a climb followed by a descent).
- **Pattern and cost:** Count the up-slope and down-slope lengths around each peak: `O(n)` time, `O(1)` space.

---

### Topic 9. String Manipulation & Parsing

These are less about choosing a technique and more about **careful simulation**. Practise the clarifying questions: they are most of the points.

---

### 61. Longest Common Prefix (#61)

**Original question:** LC 14. Write a function to find the longest common prefix string among an array of strings. If there is none, return `""`.

**Scenario:** A file manager wants to show the folder path shared by every file in a selection, so it can display the shorter relative names.

**Ask first:**
1. Can the list be empty, or contain an empty string?
2. Case-sensitive?

**Spot it:** A prefix shared by *all* strings is shared by the two that are most different. After sorting, those are the first and the last.

**Brute force:** Compare each string with every other: `O(n²·m)`. Or vertical scanning: `O(n·m)`, and no sort.

**Solve:** ([61-longest-common-prefix.md](09-string-manipulation-and-parsing/61-longest-common-prefix.md))
```python
def longestCommonPrefix(strs: list[str]) -> str:
    if not strs:
        return ""
    strs.sort()
    first, last = strs[0], strs[-1]
    i = 0
    while i < len(first) and i < len(last) and first[i] == last[i]:
        i += 1
    return first[:i]
```

**Cost:** Sorting `n` strings of length up to `m` is `O(n·m log n)`; the compare is `O(m)`. Space `O(1)` beyond the sort. Vertical scanning is `O(n·m)` and avoids the sort.
**Follow-up:** *Many queries over the same strings?* Build a trie (Variant A). *Huge strings?* Compare in blocks. *Why only first and last?* The strings between them share any prefix those two share.

**More scenarios on the same pattern**

**Variant A (crossover to a trie)**
- **Question:** LC 208 Implement Trie (Prefix Tree). Implement `insert`, `search` and `startsWith`.
- **Scenario:** An autocomplete box must answer "does any stored word start with this text?" instantly, thousands of times.
- **Pattern and cost:** Build a tree keyed by character. `O(m)` per operation, `O(total characters)` space. Sorting-based tricks help once; a trie helps for repeated queries (Trees repo).

**Variant B (sort + binary search)**
- **Question:** LC 1268 Search Suggestions System. After each typed character of `searchWord`, suggest up to three product names with the common prefix, in lexicographic order.
- **Scenario:** A shop's search box suggests up to three products after every keystroke.
- **Pattern and cost:** Sort the products once; for each prefix binary search the first match and take the next three. `O(n log n + L log n)` for `L` typed characters. A trie gives `O(L)` lookups with more memory.

---

### 62. Reverse Words in a String (#62)

**Original question:** LC 151. Given a string `s`, reverse the order of the words. A word is a sequence of non-space characters. The result must have a single space between words and no leading or trailing spaces.

**Scenario:** A formatting tool needs a sentence's words listed in reverse order, cleaning up extra spaces on the way.

**Ask first:**
1. Can there be leading, trailing or repeated spaces?
2. May I use the built-in `split` and `join`? Is `O(1)` extra space required?

**Spot it:** Walking from the **end** produces the words already in the right order.

**Brute force:** `" ".join(s.split()[::-1])`: `O(n)`, short and acceptable. The scan-from-the-end version has the same cost; it shows control and leads to the in-place follow-up (Variant A).

**Solve:** ([62-reverse-words-in-a-string.md](09-string-manipulation-and-parsing/62-reverse-words-in-a-string.md))
```python
def reverseWords(s: str) -> str:
    words = []
    i = len(s) - 1
    while i >= 0:
        while i >= 0 and s[i] == " ":
            i -= 1
        if i < 0:
            break
        j = i
        while i >= 0 and s[i] != " ":
            i -= 1
        words.append(s[i + 1 : j + 1])
    return " ".join(words)
```

**Cost:** Each character is visited at most twice: `O(n)` time, `O(n)` space (the words and the joined string). With a mutable char array: reverse the whole thing, then reverse each word: `O(1)` extra.
**Follow-up:** *In place?* Variant A. *Unicode?* No change. *Keep original spacing?* Different problem.

**More scenarios on the same pattern**

**Variant A (in place on a char array)**
- **Question:** LC 186 Reverse Words in a String II (premium). Given a character array, reverse the order of the words in place.
- **Scenario:** An embedded device with no spare memory must reverse a sentence in its own buffer.
- **Pattern and cost:** Reverse the entire array, then reverse each word back: `O(n)` time, `O(1)` space.

**Variant B (reverse inside each word)**
- **Question:** LC 557 Reverse Words in a String III. Reverse the characters of each word while keeping word order and whitespace.
- **Scenario:** A puzzle app mirrors each word individually.
- **Pattern and cost:** Split on spaces and reverse each (or two pointers per word). `O(n)` time, `O(n)` space.

---

### 63. Roman to Integer (#63)

**Original question:** LC 13. Convert a Roman numeral string to an integer. Smaller symbols before larger ones subtract (`IV = 4`).

**Scenario:** A film-credit scanner reads copyright years written in Roman numerals and needs the numeric year.

**Ask first:**
1. Is the input guaranteed to be a valid numeral?
2. What's the maximum value (3999)?

**Spot it:** A symbol is **subtracted** when the one after it is bigger, otherwise added. Only the next symbol matters.

**Brute force:** There's no meaningful improvement: parsing pairs with a big lookup table is the same `O(n)`.

**Solve:** ([63-roman-to-integer.md](09-string-manipulation-and-parsing/63-roman-to-integer.md))
```python
def romanToInt(s: str) -> int:
    roman_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total, n = 0, len(s)
    for i in range(n):
        if i < n - 1 and roman_map[s[i]] < roman_map[s[i + 1]]:
            total -= roman_map[s[i]]
        else:
            total += roman_map[s[i]]
    return total
```

**Cost:** One pass: `O(n)` time (at most 15 characters, effectively `O(1)`), `O(1)` space.
**Follow-up:** *Validate input?* Add rules for repeats and legal subtractive pairs. *Reverse direction?* #68.

**More scenarios on the same pattern**

**Variant A (positional value, other base)**
- **Question:** LC 171 Excel Sheet Column Number. Given a column title like `"AB"`, return its column number.
- **Scenario:** A spreadsheet API converts a column label to its numeric index.
- **Pattern and cost:** Treat it as base 26 with digits `1..26`: `result = result * 26 + value`. `O(n)` time, `O(1)` space.

**Variant B (crossover: number to words)**
- **Question:** LC 273 Integer to English Words. Convert a non-negative integer to its English words.
- **Scenario:** A cheque printer must write amounts in words.
- **Pattern and cost:** Process in chunks of three digits with lookup tables and the scale words (thousand, million, ...). `O(digits)`. Edge cases (zero, teens, spacing) are the whole challenge.

---

### 64. Find the Index of the First Occurrence in a String (#64)

**Original question:** LC 28. Given strings `haystack` and `needle`, return the index of the first occurrence of `needle` in `haystack`, or `-1` if it's not part of `haystack`.

**Scenario:** A document viewer's "find" box must report where the search term first appears in a long document.

**Ask first:**
1. Can `needle` be empty? What should be returned? (`0` by convention.)
2. Case-sensitive?

**Spot it:** A fixed-length window sliding over the text, comparing to the pattern.

**Brute force:** That *is* the brute force: for each start compare up to `m` characters, `O((n - m + 1)·m)` worst case, fine for typical inputs.

**Solve:** ([64-find-the-index-of-the-first-occurrence-in-a-string.md](09-string-manipulation-and-parsing/64-find-the-index-of-the-first-occurrence-in-a-string.md))
```python
def strStr(haystack: str, needle: str) -> int:
    n, m = len(haystack), len(needle)
    if m > n:
        return -1
    for i in range(n - m + 1):
        if haystack[i : i + m] == needle:
            return i
    return -1
```

**Cost:** `O((n - m + 1)·m)` worst case (like `"aaaaaaaaab"` searching `"aaaa"`), `O(n)` typical; `O(m)` temporary for the slice. KMP guarantees `O(n + m)` time with `O(m)` space.
**Follow-up:** *Guarantee linear time?* KMP or Rabin-Karp. *Many patterns?* Aho-Corasick. *Empty needle?* Return `0` and say so.

**More scenarios on the same pattern**

**Variant A (KMP failure table)**
- **Question:** LC 459 Repeated Substring Pattern. Return whether `s` can be built by repeating a shorter substring.
- **Scenario:** A pattern detector checks whether a code is just a motif repeated.
- **Pattern and cost:** `s` is periodic iff `s` appears in `(s + s)[1:-1]`, or via the KMP prefix table: `n % (n - lps[-1]) == 0`. `O(n)` time.

**Variant B (KMP again)**
- **Question:** LC 214 Shortest Palindrome. Add characters only in front of `s` to make it a palindrome; return the shortest result.
- **Scenario:** An engraver may add characters only at the start of a nameplate to make it read the same both ways.
- **Pattern and cost:** Find the longest palindromic prefix with KMP on `s + "#" + reverse(s)`. `O(n)` time and space. Brute-force expansion is `O(n²)`.

---

### 65. Multiply Strings (#65)

**Original question:** LC 43. Given two non-negative integers `num1` and `num2` represented as strings, return their product as a string. You must not use a built-in big-integer library or convert the inputs directly to integers.

**Scenario:** A calculator for astronomical values receives two huge numbers as text. Return the product as text, doing the long multiplication yourself.

**Ask first:**
1. Can the inputs be `"0"` or contain leading zeros?
2. How long can they get?

**Spot it:** Long multiplication: digit `i` times digit `j` lands in position `i + j + 1`, with the carry going to `i + j`.

**Brute force:** Multiply `num1` by each digit of `num2` and add shifted partial products: `O(m·n)` but with more intermediate strings.

**Solve:** ([65-multiply-strings.md](09-string-manipulation-and-parsing/65-multiply-strings.md))
```python
def multiply(num1: str, num2: str) -> str:
    if num1 == "0" or num2 == "0":
        return "0"
    m, n = len(num1), len(num2)
    res = [0] * (m + n)
    for i in range(m - 1, -1, -1):
        d1 = ord(num1[i]) - ord("0")
        for j in range(n - 1, -1, -1):
            d2 = ord(num2[j]) - ord("0")
            total = d1 * d2 + res[i + j + 1]
            res[i + j + 1] = total % 10
            res[i + j] += total // 10
    digits = "".join(map(str, res)).lstrip("0")
    return digits
```

**Cost:** Every digit pair is multiplied once: `O(m·n)` time, `O(m + n)` space.
**Follow-up:** *Faster?* Karatsuba, `O(n^1.58)`. *Negative numbers?* Handle the sign separately. *Why is the result at most `m + n` digits?* The product of an `m`-digit and an `n`-digit number fits in `m + n` digits.

**More scenarios on the same pattern**

**Variant A (addition)**
- **Question:** LC 67 Add Binary. Given two binary strings, return their sum as a binary string.
- **Scenario:** A hardware tool adds two long bit patterns given as text.
- **Pattern and cost:** Two pointers from the right with a carry. `O(max(m, n))` time and space.

**Variant B (crossover to math: fast exponentiation)**
- **Question:** LC 50 Pow(x, n). Implement `x` raised to the power `n`.
- **Scenario:** A compound-growth calculator must raise a rate to a large power quickly.
- **Pattern and cost:** Repeated multiplication is `O(n)`. Squaring (`x^n = (x^(n/2))²`) gives `O(log n)` time. Handle negative `n` and overflow (Math-Bits-Greedy repo).

---

### 66. String to Integer (atoi) (#66)

**Original question:** LC 8. Implement `myAtoi(s)`: skip leading whitespace, read an optional sign, read digits until a non-digit or the end, clamp to the 32-bit signed range, and return the integer (`0` if no digits).

**Scenario:** A web form accepts a quantity typed by users, who may add spaces, a sign, or stray text after the number. Read it forgivingly, but never let the result leave the 32-bit range.

**Ask first:**
1. What about `"  -  42"` or `"+-12"`? (Stop at the first invalid character.)
2. Should values outside 32 bits clamp or error?

**Spot it:** A strict sequence of phases: whitespace → sign → digits → stop. Never go back.

**Brute force:** There is no better algorithm. The risk is correctness, not speed.

**Solve:** ([66-string-to-integer-atoi.md](09-string-manipulation-and-parsing/66-string-to-integer-atoi.md))
```python
def myAtoi(s: str) -> int:
    i, n = 0, len(s)
    while i < n and s[i] == " ":
        i += 1
    if i >= n:
        return 0
    sign = 1
    if s[i] == "-":
        sign, i = -1, i + 1
    elif s[i] == "+":
        i += 1
    res = 0
    while i < n and "0" <= s[i] <= "9":
        res = res * 10 + (ord(s[i]) - ord("0"))
        i += 1
    res *= sign
    return max(-(2**31), min(2**31 - 1, res))
```

**Cost:** One pass: `O(n)` time, `O(1)` space. Python integers don't overflow; in Java or C++ you must check for overflow *before* multiplying by 10.
**Follow-up:** *Fixed-width language?* Check `res > (INT_MAX - digit) // 10` before each step. *Hex, decimals, exponents?* Variant A. *Why not `int(s)`?* It accepts underscores and other forms this problem rejects.

**More scenarios on the same pattern**

**Variant A (a state machine)**
- **Question:** LC 65 Valid Number. Return whether `s` is a valid number (integer or decimal, optional exponent).
- **Scenario:** A spreadsheet validates whether a typed cell is a legal numeric literal.
- **Pattern and cost:** Same phased scan, but with more states (sign, digits, dot, exponent). Build a small state machine. `O(n)` time, `O(1)` space.

**Variant B (overflow is the point)**
- **Question:** LC 7 Reverse Integer. Reverse the digits of a signed 32-bit integer; return `0` if the result overflows.
- **Scenario:** A legacy device reverses a counter value but must not wrap past the 32-bit limit.
- **Pattern and cost:** Pop digits with `% 10`, push with `* 10`; check overflow *before* the multiply. `O(log |x|)` time, `O(1)` space.

---

### 67. Length of Last Word (#67)

**Original question:** LC 58. Given a string `s` consisting of words and spaces, return the length of the last word. A word is a maximal substring of non-space characters.

**Scenario:** A terminal's status line must report how long the last word on a line is, ignoring trailing spaces.

**Ask first:**
1. Can there be trailing spaces? Is at least one word guaranteed?
2. Does punctuation count as part of a word?

**Spot it:** Only the end of the string matters. Scan backward: skip spaces, then count characters.

**Brute force:** `len(s.split()[-1])`. Fine, but it creates a list of all words.

**Solve:** ([67-length-of-last-word.md](09-string-manipulation-and-parsing/67-length-of-last-word.md))
```python
def lengthOfLastWord(s: str) -> int:
    length, i = 0, len(s) - 1
    while i >= 0 and s[i] == " ":
        i -= 1
    while i >= 0 and s[i] != " ":
        length += 1
        i -= 1
    return length
```

**Cost:** At most one backward pass: `O(n)` worst case, often far less. `O(1)` space.
**Follow-up:** *Length of the first word?* Scan forward. *Streaming?* Keep the length of the current word and reset on a space.

**More scenarios on the same pattern**

**Variant A (counting words)**
- **Question:** LC 434 Number of Segments in a String. Return the number of segments (maximal runs of non-space characters).
- **Scenario:** An editor shows a live word count.
- **Pattern and cost:** Count positions where a non-space follows a space (or start). `O(n)` time, `O(1)` space.

**Variant B (two pointers over characters)**
- **Question:** LC 345 Reverse Vowels of a String. Reverse only the vowels of a string.
- **Scenario:** A word-play app swaps the vowel positions of a word end to end.
- **Pattern and cost:** Two pointers inward, skipping consonants, swapping vowels. `O(n)` time, `O(n)` for the mutable copy of the string.

---

### 68. Integer to Roman (#68)

**Original question:** LC 12. Convert an integer (1 to 3999) to a Roman numeral.

**Scenario:** A printing tool formats chapter numbers in Roman numerals.

**Ask first:**
1. What's the maximum input (3999)?
2. Should I use the standard subtractive forms (`IV`, `IX`, `XL`, ...)?

**Spot it:** Greedy, largest value first, **if** the subtractive forms are in the table like ordinary symbols.

**Brute force:** Handling each digit position with if/else chains: the same `O(1)` work with more code.

**Solve:** ([68-integer-to-roman.md](09-string-manipulation-and-parsing/68-integer-to-roman.md))
```python
def intToRoman(num: int) -> str:
    value_map = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                 (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    roman = []
    for val, symbol in value_map:
        count, num = divmod(num, val)
        roman.append(symbol * count)
    return "".join(roman)
```

**Cost:** The table has 13 entries and the output has at most 15 characters: `O(1)` time and space.
**Follow-up:** *Larger numbers?* Add overline notation or repeat M. *Validate?* #63 backwards.

**More scenarios on the same pattern**

**Variant A (base conversion with an off-by-one)**
- **Question:** LC 168 Excel Sheet Column Title. Given a column number, return its title (`1 → A`, `27 → AA`).
- **Scenario:** A report generator names spreadsheet columns from numbers.
- **Pattern and cost:** Base 26 with digits `1..26`, so subtract 1 before each `% 26` and `// 26`. `O(log₂₆ n)` time. The off-by-one is the whole difficulty.

**Variant B (plain base conversion)**
- **Question:** LC 504 Base 7. Return the base 7 representation of an integer.
- **Scenario:** A game displays scores in a custom base.
- **Pattern and cost:** Repeated `divmod`; handle zero and negatives. `O(log n)` time and space.

---

### 69. Zigzag Conversion (#69)

**Original question:** LC 6. The string `s` is written in a zigzag pattern on `numRows` rows, then read line by line. Return the string read row by row.

**Scenario:** A banner printer lays text out in a zigzag over a fixed number of lines, and the output must be read line by line.

**Ask first:**
1. What if there is one row, or more rows than characters?
2. Is the direction changing at the first and last row?

**Spot it:** A point bouncing between the top and bottom row. Keep one bucket per row and a direction.

**Brute force:** Build the 2D grid explicitly: `O(rows × cols)` space. Buckets avoid it.

**Solve:** ([69-zigzag-conversion.md](09-string-manipulation-and-parsing/69-zigzag-conversion.md))
```python
def convert(s: str, numRows: int) -> str:
    if numRows == 1 or numRows >= len(s):
        return s
    rows = [""] * numRows
    current_row, step = 0, 1
    for char in s:
        rows[current_row] += char
        if current_row == numRows - 1:
            step = -1
        elif current_row == 0:
            step = 1
        current_row += step
    return "".join(rows)
```

**Cost:** One pass, `O(1)` per character: `O(n)` time, `O(n)` space for the row buckets (repeated `+=` on small row strings is fine; use lists for large inputs).
**Follow-up:** *Closed form?* Rows repeat every `2(numRows - 1)` characters, so you can compute indices directly (Variant A). *Reverse the conversion?* Same mapping, inverted.

**More scenarios on the same pattern**

**Variant A (index formula, no simulation)**
- **Question:** LC 6 again, but with `O(1)` extra space beyond the output.
- **Scenario:** The banner printer has almost no working memory.
- **Pattern and cost:** For each row `r`, jump by `2(numRows - 1)`, adding the "diagonal" character at `j + cycle - 2r`. `O(n)` time, `O(1)` extra.

**Variant B (snake order on a grid)**
- **Question:** Print a matrix in snake order: left-to-right on even rows, right-to-left on odd rows.
- **Scenario:** A warehouse picker walks the aisles back and forth.
- **Pattern and cost:** Row index parity chooses direction. `O(m·n)` time, `O(1)` extra beyond the output. Same "bounce" idea as #69 on a grid.

---

### 70. Text Justification (#70)

**Original question:** LC 68. Given an array of `words` and a `maxWidth`, format the text so each line has exactly `maxWidth` characters and is fully justified: pack as many words as fit, distribute extra spaces as evenly as possible (extras to the left), and left-justify the last line and any single-word line.

**Scenario:** A typesetter fills lines of a fixed width with words, spreading the spaces so both edges are flush, except for the final line.

**Ask first:**
1. How are the extra spaces distributed when they don't divide evenly?
2. Is the last line left-justified? What about a line with one word?

**Spot it:** Two separate sub-problems: (1) which words fit on a line (greedy), (2) how to spread the spaces (even division with a remainder).

**Brute force:** There's no asymptotic gain available; the challenge is to get the rules right.

**Solve:** ([70-text-justification.md](09-string-manipulation-and-parsing/70-text-justification.md))
```python
def fullJustify(words: list[str], maxWidth: int) -> list[str]:
    def justify_line(line_words: list[str], line_len: int) -> str:
        if len(line_words) == 1:                         # single word: left-justified
            return line_words[0] + " " * (maxWidth - line_len)
        gaps = len(line_words) - 1
        space_per_gap, extra = divmod(maxWidth - line_len, gaps)
        out = ""
        for i, word in enumerate(line_words):
            out += word
            if i != gaps:
                out += " " * (space_per_gap + (1 if i < extra else 0))   # extras go left
        return out

    result, line, line_len = [], [], 0
    for word in words:
        if line_len + len(line) + len(word) > maxWidth:  # len(line) = minimum spaces needed
            result.append(justify_line(line, line_len))
            line, line_len = [], 0
        line.append(word)
        line_len += len(word)
    last = " ".join(line)                                # last line: left-justified
    result.append(last + " " * (maxWidth - len(last)))
    return result
```

**Cost:** Each word is placed once and each line is built in time proportional to its width: `O(n)` time for `n` total characters, `O(n)` output.
**Follow-up:** *Minimise raggedness instead?* Variant B (DP). *Hyphenation?* Out of scope. *Streaming?* Lines are independent once packed.

**More scenarios on the same pattern**

**Variant A (distributing spaces)**
- **Question:** LC 1592 Rearrange Spaces Between Words. Rearrange the spaces so there is an equal number between every adjacent pair of words, with any extras at the end.
- **Scenario:** A text cleaner evens out the gaps in a spaced-out headline.
- **Pattern and cost:** Count spaces and words; `divmod(spaces, words - 1)` (guard the single-word case). `O(n)` time and space.

**Variant B (crossover to DP)**
- **Question:** Word wrap that **minimises the total raggedness** (sum of squared trailing spaces on each line), classic interview question.
- **Scenario:** A layout engine wants the prettiest paragraph, not just a valid one.
- **Pattern and cost:** Greedy line packing can be globally suboptimal. DP over the word index: `dp[i] = min(dp[j] + cost(j, i))`. `O(n²)` time, `O(n)` space (DP repo).

---

## Part 5. Common traps to say out loud

Interviewers listen for these. Say the relevant one *before* you code it; it signals you've been burned before.

**Boundaries and shape**
- **Off-by-one at the edges.** Is the end inclusive? Window size is `right - left + 1`. A `range(n - 1)` skips the last element on purpose in #56 and by mistake almost everywhere else. Test the first and last index by hand.
- **Empty and single-element input.** `intervals[0]` on an empty list crashes (#34). `k % len(nums)` with an empty array crashes (#50). One element: is the answer `0`, the element itself, or `True`? Say it.
- **All equal / all negative / all zero.** Kadane with `max_sum = 0` instead of `-inf` is wrong for all-negative input (#32). Zeros break division (#31).
- **Touching ranges.** `[1,4]` and `[4,5]`: do they overlap? Merging uses `<=` (#34); "fewest to remove" uses `>=` to keep touching ones (#36); balloons treat touching as shared (#40); meetings let `[0,5]` and `[5,10]` share a room (#37). Ask every time.
- **Duplicates.** `[3, 3]` with target 6 (#3): check the map *before* storing. 3Sum needs skip-forward logic on all three positions (#18). A set silently collapses duplicates (#6).

**Values and numbers**
- **Integer overflow.** Python is safe; Java/C++ are not. Danger spots: a running sum, a running product (#31, #713), `target - num`, `left + right` for a midpoint (use `left + (right - left) // 2`), `abs(INT_MIN)`, and multiplying by 10 while parsing (#66). Say "I'd use `long`".
- **Negative numbers.** Sliding window on sums breaks (#26 vs #33). `%` and `//` behave differently for negatives across languages; `-7 % 5` is `3` in Python and `-2` in C++/Java.
- **Sum, product or index out of the guaranteed range.** Confirm the constraints before you pick `int`.

**Input handling**
- **Mutating the input.** Sorting, in-place marking (#45, #46, `-` sign tricks) and swapping change the caller's data. Ask, or copy and state the `O(n)` cost. Also watch for aliasing: `[[0] * n] * m` makes `m` references to the same row.
- **Forgetting to sort first.** Two pointers, binary search, interval merging and "skip equal neighbours" all silently give wrong answers on unsorted input. Say "this needs sorted data, so I'll sort first (`O(n log n)`)".
- **Losing the original indices after sorting.** If the output is positions (Two Sum), sort `(value, index)` pairs, or use a hash map instead.
- **Stability.** Swap-based partitioning (#21) isn't stable; read/write pointers (#48) are. If order must be preserved, say which you chose.

**Technique-specific**
- **Sliding window with negatives.** Shrinking assumes the sum falls when you remove an element. With negatives it can rise. Use prefix sum + hash map (#33). Counter-example: `[5, -3, 1]`, `k = 3`.
- **Check-before-store in hash maps.** Store first and an element pairs with itself (#3).
- **Forgetting `del` at zero count** in a window's count map overcounts distinct keys (#29).
- **Not advancing `i` after a swap with the right pointer** in the three-way partition (#21).
- **Stale state is sometimes fine.** `max_freq` in #24 is intentionally never lowered; explain why if asked.
- **Prefix-sum base case.** Forgetting `seen[0] = 1` misses every stretch that starts at index 0 (#33).
- **Merging needs `max` of the ends,** not just the new end (`[1,10]` then `[2,6]`) (#34).
- **Mixed up "subarray" and "subsequence".** Contiguous vs not changes the technique completely. Ask.

**Python-specific**
- `s += ch` in a loop is `O(n²)`; collect in a list and `"".join` (#7, #69).
- `x in some_list` is `O(n)`; use a `set`. `list.pop(0)` and `list.insert(0, x)` are `O(n)`; use `deque`.
- Slicing (`s[i:j]`) copies. A loop of slices is `O(n·m)` (#64).
- `defaultdict` **inserts a key on a read** (`d[missing]`), which can silently change `len(d)` or give extra keys (#33 note, #29).
- Don't modify a list while iterating over it.
- `float("inf")` mixed with ints is fine, but remember to convert the sentinel back to `0` or `-1` at the end (#26).

---

## Part 6. Known gaps: important array problems this repo doesn't cover yet

**Already planned in [problems.md](problems.md), appendix #71–80, not written up yet.** Do these first; each is a short rep of a technique you already own:

| # | Problem | Why it matters for scenario questions |
|---|---|---|
| 77 | Move Zeroes (LC 283) | The most common in-place warm-up; read/write pointer |
| 74 | Max Consecutive Ones III (LC 1004) | The "budget of fixes" window; appears constantly in disguise |
| 73 | Find All Anagrams in a String (LC 438) | Fixed window returning every match |
| 75 | Contiguous Array (LC 525) | Prefix sum + hash map where you store the *first index* |
| 78 | First Missing Positive (LC 41) | The array as its own hash table (cyclic sort) |
| 76 | Diagonal Traverse (LC 498) | Matrix index arithmetic |
| 71, 72 | Backspace String Compare, One Edit Distance | Two pointers from the back, `O(1)` space |
| 79, 80 | String Compression, Compare Version Numbers | Read/write pointer on characters; parsing |

**Not in the repo at all, and likely to be asked** (techniques named in Part 2 as **gap**):

| Problem | Technique | Why add it | Where it might live |
|---|---|---|---|
| Largest Rectangle in Histogram (LC 84) | Monotonic stack | The hard version of "nearest smaller on both sides" | Stack repo (Daily Temperatures and Next Greater Element are already there; confirm this one) |
| Quickselect (the `O(n)` average way to do LC 215) | Partition-based selection | The heap version is in the Heap repo; interviewers often ask for the no-heap follow-up | not covered |
| Koko Eating Bananas, Capacity to Ship Packages | Binary search on the answer | "Smallest speed / capacity that works" has no visible binary search | Binary-Search repo covers Koko; add shipping/split-array style |
| Car Pooling (LC 1094), Corporate Flight Bookings (LC 1109) | Difference array / sweep | "Add to a whole range, read once" | not covered |
| Range Sum Query 2D (LC 304) | 2D prefix sums | Many rectangle-sum queries on fixed data | not covered |
| Subarray Sums Divisible by K (LC 974) | Prefix sum remainders + hash | Extends #33 to remainders | not covered |
| Subarray Product Less Than K (LC 713) | Window with counting | The standard "count the stretches" window | not covered |
| Shortest Subarray with Sum at Least K (LC 862) | Prefix sums + monotonic deque | The case where a window fails with negatives | not covered |
| Find the Duplicate Number (LC 287), Find All Numbers Disappeared (LC 448) | Floyd cycle, sign marking | `O(1)` space with read-only or in-place constraints | not covered |
| 3Sum Closest (LC 16), 4Sum (LC 18) | Sort + pointers, generalised | Direct follow-ups to #18 | not covered |
| Majority Element II (LC 229) | Boyer-Moore, two candidates | The usual follow-up to #54 | not covered |
| Partition Labels (LC 763) | Greedy on last occurrence | Interval thinking on strings | not covered |
| Employee Free Time (LC 759), Meeting Rooms III (LC 2402), Merge k Sorted Lists | Merge + heap | Scheduling scenarios Google likes | Heap repo has Task Scheduler and scheduling heaps; confirm these |
| Shortest Unsorted Continuous Subarray (LC 581), Longest Mountain (LC 845) | Two passes with running max/min | Shape-of-array scenarios | not covered |
| Maximum Sum Circular Subarray (LC 918) | Kadane variant | Per the tracker, lives in the Math-Bits-Greedy repo | Math-Bits-Greedy |
| Sort Characters by Frequency (LC 451), Maximum Gap (LC 164) | Bucket / counting sort | "Beat `O(n log n)`" scenarios | not covered |
| Logger Rate Limiter (LC 359), Moving Average from Data Stream (LC 346), Two Sum III (LC 170) | Design with hash / deque | Google likes small design-flavoured array questions | not covered |
| Rolling hash / Rabin-Karp | Fixed window with a hash | Repeated-substring scenarios | not covered |

**Notes on the repo's own labels** (so you can answer well if asked):
- #22 (Best Time to Buy and Sell Stock) is filed under Sliding Window, but it is a *running minimum* single pass. Explain it that way.
- #31 (Product of Array Except Self) sits in the prefix-sum topic because it uses prefix and suffix passes, not prefix *sums*.
- #37 has both a sweep and a heap version in its write-up. Know both, and when each wins (sweep: fewer moving parts; heap: also gives room assignments).

**Confidence note:** the LeetCode numbers in the variants were written from memory, in the same spirit as the tracker's own caveat in [problems.md](problems.md). Before relying on a number, search the title on LeetCode. The techniques, costs and counter-examples are the part to trust and rehearse.
