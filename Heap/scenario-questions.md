# Heap: Scenario Question Bank (Google L3 style)

Google doesn't say "use a priority queue". It gives a short, vague scenario, and **you** have to notice that "I keep needing the current best / the k-th best / the middle of a changing set" is a heap problem, and just as importantly, notice when it **isn't** one.
This file has one scenario per solved problem in this repo, plus two more variants of each, so you practise the *recognition* step and not just the solution.
Problem numbers match [problems.md](problems.md).

**Disguised on purpose:** scenarios avoid words like "heap", "priority queue", "top-k", "median", "k-th largest" and "stream" when those words would give the technique away. Each one has an **Ask first** line (the clarifying questions a good candidate asks), a **Spot it** line (the clue that gives the heap away), and a **Brute force** line (so you can say what the heap improves).

**How to use:** read only the **Scenario** line, then say out loud: *what do I need again and again (the best, the k-th best, the middle)? does the data change or arrive over time? is `k` small compared with `n`?* Only then read the rest. About half of the variants deliberately cross over into a neighbouring technique (sorting, quickselect, bucketing, binary search on the answer, a sweep, a deque, a sorted container) so you learn where a heap stops being the right tool.

---

## Part 1. The 5-step "Is this a heap problem?" framework

1. **Smell test: do I need the current extreme over and over?** A heap earns its place when you repeatedly need the **best, worst, k-th best or middle** of a collection that **changes** (items arrive, leave, or get used up).
   - The data is **fixed** and you need the answer **once**: sort it, or use quickselect. A heap is overkill.
   - The data **arrives over time** and you need an answer after each arrival: a heap.
   - You must **repeatedly take the best, act on it, and put something back** (a simulation): a heap.
   - Only a count or a membership test is needed: a hash map is enough.

2. **Name the heap.** Complete this sentence: *"The heap holds ___. Its root is ___. I pop it when ___."*
   - **Min or max?** Python's `heapq` is a **min-heap**. For a max-heap, push the negative.
   - **What is one entry?** A bare number, or a tuple `(key, tie_break, payload)`. The tie-break stops Python from comparing payloads that may not be comparable.
   - **Is it capped at size `k`?** For "the `k` largest", keep a **min-heap of size `k`**: the root is the smallest of the best `k`, which is exactly the boundary. For "the `k` smallest", keep a **max-heap of size `k`**.
   - **The trap to memorise:** the heap that keeps the *largest* items is a **min**-heap, and the one that keeps the *smallest* items is a **max**-heap. The root is the item you would evict next.

3. **Heap, or something cheaper?** (see Part 2)
   - Everything is available at once and `k` is close to `n`: sort, `O(n log n)`.
   - Everything is available at once and you may reorder it: **quickselect**, `O(n)` average.
   - Keys are small integers or counts bounded by `n`: **bucket / counting**, `O(n)`.
   - The answer is a **value** you can test for feasibility ("how many are ≤ x?"): **binary search on the answer**.
   - You need the **max of every window**: a **monotonic deque**, not a heap.
   - You need removals of arbitrary items, or an ordered view: a **sorted container** or a **lazy-deletion heap**.

4. **Write the loop and the invariant.** Pick the shape:
   - **Capped heap (top-k):** `push(x)`, and if `len > k`, `pop()`. *Invariant:* the heap holds the best `k` seen so far.
   - **Simulation:** `while heap: pop → act → push the leftover`.
   - **Merge:** push one head per source; pop the best; push that source's next item.
   - **Cooldown / hold back:** pop the best, park it in a queue or a `prev` variable, release it later.
   - **Two heaps:** lower half in a max-heap, upper half in a min-heap, sizes balanced.
   - Say the invariant in plain English before coding.

5. **Cost: say it before you code.**
   - Each `heappush` / `heappop` is `O(log size)`. Peeking `heap[0]` is `O(1)`. `heapify` on a list is `O(n)`.
   - Top-k over `n` items with a size-`k` heap: `O(n log k)` time, `O(k)` space.
   - Name **what the heap size is** at each step. That one number is the whole analysis.
   - Hidden costs: re-sorting the heap's contents at the end (`O(k log k)`), copying, and recomputing keys.

**Say-it-out-loud template:** *"I need the [best / k-th best / middle] of a set that keeps changing. A [min / max]-heap of [what] capped at [k / unbounded] keeps its root at [the boundary]. Each of the `n` items costs one push and at most one pop, so `O(n log k)` time and `O(k)` space. If the data were static I'd just sort it, or use quickselect for `O(n)` average."*

**Questions to ask the interviewer (cheap and impressive):**
- **Shape:** Is the data a stream that keeps arriving, or a fixed batch I can read twice?
- **Size:** How large can `n` get, and how large can `k` get compared with `n`? (decides heap vs sort vs quickselect)
- **Output:** Do you need just the k-th item, or all `k` best, and in what order (sorted, any order)?
- **Ties:** How are ties broken (alphabetical, earliest, any)? Do duplicates count separately?
- **Updates:** Can items be removed or changed after they are added? (a plain heap cannot delete from the middle)
- **Memory:** Does everything fit in memory? Is an approximate answer acceptable for a huge stream?
- **Mutation:** May I reorder or modify the input? (quickselect reorders it)
- **Edge cases:** Is `k` ever larger than `n`? Empty input? Negative values?
- **Calls:** Which operation is called most: add, read, remove? (decides which side pays the `log n`)

---

## Part 2. Signal → technique cheat sheet

Problem numbers match [problems.md](problems.md). **gap** means the repo has no write-up for it yet (see Part 6). Techniques that live in other repos are named so you still recognise them.

| What the question says | It is really | Technique | Problems |
|---|---|---|---|
| "the k-th best so far", scores keep arriving | boundary of the best `k` of a growing set | **min-heap of size `k`**, root = answer | 1 |
| "the k-th largest of this batch", one shot | selection, no stream | **min-heap of size `k`**, or **quickselect** | 2 |
| "k nearest / cheapest / smallest by a computed value" | `k` smallest of a derived key | **max-heap of size `k`** on the key (negate) | 3 |
| "k most common / most searched", with a tiebreak | frequency, then best `k` with a custom order | **count, then size-`k` heap** with `(count, word)` ordering | 4 |
| "k-th smallest where rows and columns only go up" | a `k`-way merge in disguise | **heap of frontier cells**, or **binary search on the value** | 5 |
| "k cheapest combinations of one item from each of two lists" | merge `k` ordered lists lazily | **min-heap of next candidates** | 6 |
| "repeatedly take the two biggest, combine, put back" | simulation | **max-heap**, pop twice, push the leftover | 7 |
| "same job can't run again for `n` rounds", "minimum total time" | greedy by remaining count + cooldown | **max-heap of counts + waiting queue**, or the counting formula | 8 |
| "arrange so no two identical neighbours" | greedy: use the most frequent, not the one just used | **max-heap of counts + hold back the last one** | 9 |
| "feed of the 10 latest items across everyone I follow" | merge `k` newest-first lists | **min-heap merge** by timestamp | 10 |
| "the middle value of everything so far" | balance two halves | **two heaps** (max-heap lower, min-heap upper) | 11 |
| "do at most `k` jobs; finishing one unlocks bigger ones; maximise the end result" | unlock by threshold, pick the best of the unlocked | **sort by threshold + max-heap of gains** | 12 |
| "merge `k` ordered lists / streams" | `k`-way merge | **min-heap of current heads** | Linked-List repo (LC 23) |
| "k most frequent items", `k` large or answer unordered | count, then bucket | **bucket by count**, `O(n)` | Arrays-Strings (LC 347) |
| "fewest rooms / machines", "how many overlap" | concurrency | **sort + min-heap of end times**, or a sweep | Arrays-Strings (LC 253) |
| "max of every window of size k" | sliding extreme | **monotonic deque** (not a heap) | Arrays-Strings (LC 239) |
| "shortest path with non-negative costs" | repeatedly settle the cheapest frontier node | **Dijkstra** (a heap of `(distance, node)`) | Graphs repo |
| "smallest value `x` such that at least `k` items are ≤ `x`" | feasibility is monotone | **binary search on the answer** (no heap) | Binary-Search repo |
| "stream is huge, answer may be approximate" | frequency estimate | **count-min sketch + small heap** | gap |
| "remove an arbitrary item", "update an item's priority" | heap has no delete | **lazy deletion**, or an indexed heap / sorted container | gap |
| "items sorted by a number, find best subset under a budget" | greedy with regret | **max-heap of chosen items, evict the worst** | gap |
| "all the data is here, I need the answer once" | selection or sort | **sort** or **quickselect** | 2 (alt.) |

**Red flags that you're being tested on heaps:** "k-th", "top k", "k closest", "most frequent", "repeatedly pick the largest/smallest", "merge k", "median of a stream", "schedule with a cooldown", "next available", and any question where the first idea is "sort it, take one, then sort again".

### Heap or sort?

| | Heap | Sort |
|---|---|---|
| Time for the best `k` of `n` | `O(n log k)` | `O(n log n)` |
| Extra space | `O(k)` | `O(1)` to `O(n)` |
| Works on a stream | **yes** | no (needs all the data) |
| Gives the full order | no (only the extreme) | yes |
| Good when | `k` is much smaller than `n`; data arrives over time; you repeatedly take the best | `k` is close to `n`; one-shot batch; you need everything ordered |

If `k` is close to `n`, a heap does `n` pushes of `log k ≈ log n`: no better than sorting. If the data is a fixed batch, sorting once is simpler and often enough.

### Heap or quickselect?

- **Quickselect** (#2 alternative): `O(n)` average, `O(1)` extra space, **reorders the input**, needs all the data upfront, worst case `O(n²)` (rare with a random pivot).
- **Heap:** `O(n log k)`, works on a **stream**, does not touch the input, predictable.
- Pick quickselect when the interviewer says "can you do better than `n log k`?" and the data is static. Pick the heap when it arrives over time or must stay unmodified.

### Heap or bucket / counting?

When keys are **counts bounded by `n`** (top k frequent elements), you can place each item on a shelf indexed by its count and read from the top: `O(n)`, no log factor. A heap is the answer when keys are arbitrary (distances, timestamps), when the output order depends on a tie-break, or when the data is a stream.

### Heap or monotonic deque / sorted container?

- **Max of each window:** a monotonic deque is `O(n)`; a heap with lazy deletion is `O(n log n)`. Prefer the deque.
- **Need to delete arbitrary items, or find the predecessor / successor:** a heap can't. Use a sorted container (a balanced tree) or lazy deletion. See Sliding Window Median (Variant A of #11).
- **Need the middle:** two heaps (#11), or a sorted container with an index.

### When it is really greedy or DP

Most heap problems are **greedy with a heap supplying the "best available now"** (#7, #8, #9, #12). A heap simulation is correct when the greedy rule is correct, so say why the greedy is safe (for example "always use the most frequent remaining letter that isn't the last one placed"). If a choice now **costs future options** and a counter-example breaks the greedy, it is DP instead. See the DP repo.

---

## Part 3. Complexity patterns

Every heap cost is **(number of heap operations) × log(heap size)**. Count the operations first, then the size.

| Pattern | Heap size | Operations | Time | Extra space | Notes |
|---|---|---|---|---|---|
| Size-`k` heap over `n` items (Kth Largest, K Closest, Top K Words) | `k + 1` | `n` pushes, up to `n` pops | `O(n log k)` | `O(k)` | beats sorting when `k` ≪ `n`; works on a stream |
| Same, building from a list with `heapify` first (#1 `__init__`) | `n` then `k` | `O(n)` heapify + `n - k` pops | `O(n + (n - k) log n)` | `O(n)` | the write-up trims with pops, so it is `O(n log n)` |
| One `add` on an existing size-`k` heap | `k + 1` | 1 push + ≤ 1 pop | `O(log k)` | `O(1)` | the per-item cost on a stream |
| Quickselect (#2 alt.) | none | partitions | `O(n)` average, `O(n²)` worst | `O(1)` | reorders the input in place |
| Counting first, then heap (Top K Frequent Words) | `k + 1` | `u` pushes, `u` = distinct items | `O(n + u log k)` | `O(u)` | counting is one `O(n)` pass |
| Heap simulation (Last Stone Weight) | `n`, shrinking | ≤ `n` rounds × (2 pops + 1 push) | `O(n log n)` | `O(n)` | `heapify` first is `O(n)` |
| Cooldown scheduler (Task Scheduler) | ≤ 26 | one round per time step | `O(T)` where `T` is the answer, `T ≤ len(tasks)·(n + 1)` | `O(1)` | alphabet bounded, so each op is `O(log 26) = O(1)`; formula is `O(len(tasks))` |
| Hold-back greedy (Reorganize String) | ≤ 26 | `n` pops + ≤ `n` pushes | `O(n log k)`, effectively `O(n)` | `O(k)` | `k` distinct letters |
| `k`-way merge of `m` lists, take `k` items (K Pairs, Twitter feed, Merge k Lists) | ≤ `m` | `k` pops + ≤ `k` pushes | `O(k log m)` (+ `O(m)` to start) | `O(m)` | the heap holds one head per list |
| Frontier heap on a matrix (#5 `k`-way merge idea) | `n` rows | `k` pops + ≤ `k` pushes | `O((n + k) log n)` | `O(n)` | beats pushing all `n²` cells |
| Push every cell into a size-`k` heap (#5 as written) | `k + 1` | `n²` pushes | `O(n² log k)` | `O(k)` | simplest, not the fastest |
| Two heaps (Find Median) | `n / 2` each | `addNum`: ≤ 3 heap ops; `findMedian`: 0 | `add` `O(log n)`, `median` `O(1)` | `O(n)` | stores every number |
| Sort + one heap (IPO) | ≤ `n` | `n` pushes, ≤ `k` pops | `O(n log n + k log n)` | `O(n)` | the sort and the heap are both needed |
| Binary search on the answer (#5 alt.) | none | `log(range)` rounds × an `O(n)` count | `O(n log(range))` | `O(1)` | no heap at all |

**How to work out complexity (say it in this order):**
1. **Say what is in the heap.** One entry per item? Per list? Per distinct letter? Capped at `k`? The size is the base of every `log`.
2. **Count the operations.** Each item is pushed at most once and popped at most once. In a merge, each pop is followed by at most one push.
3. **Multiply:** operations × `O(log size)`. Add the `O(n)` of any counting or `heapify`.
4. **Space = the heap + the answer + any counter or queue.**
5. **Compare with the alternative** out loud: a sort is `O(n log n)` with all the data in hand; quickselect is `O(n)` average; a heap is `O(n log k)` and streams.

**Rules of thumb**
- **`k` small → heap wins; `k ≈ n` → sort.** If `k = n`, the heap is just a slow sort.
- **Bounded alphabets make `log` a constant.** A heap of at most 26 letters costs `O(1)` per operation, so Task Scheduler and Reorganize String are effectively linear.
- **`heapify` is `O(n)`, not `O(n log n)`.** Building the heap from a list is faster than `n` pushes.
- **Python's `heapq` has no `peek`-and-replace beyond `heapreplace` / `heappushpop`.** `heappushpop(heap, x)` pushes then pops in one `O(log n)` call. It's the neat way to cap a heap: push, and the smallest falls out.
- **A heap gives the extreme in `O(1)` but the sorted order only by popping everything** (`O(n log n)`). Iterating over `heap` is *not* sorted.
- **There is no decrease-key and no delete in `heapq`.** Use lazy deletion (mark and skip on pop), or push a new entry and ignore the stale one.
- **A stream or a huge input** usually means a capped heap. Mention a count-min sketch only if exact counts do not fit in memory.

---

## Part 4. The scenarios

Each entry has: **Original question** (the formal LeetCode statement), then **Scenario** (what you'd actually hear), **Ask first**, **Spot it** (the clue that reveals the technique), **Brute force** (the naive answer and its cost), **Solve** (the answer from your write-up), **Cost** (time and space, with the reasoning), **Follow-up** (what they'd push on), and **two more variants (A and B)** on the same pattern. Each variant gives the formal **Question** first, then the disguised **Scenario**, then **Pattern and cost**. Variants marked **(crossover)** leave the entry's technique on purpose, to show you where it stops working. A variant with no LC number is a classic interview question that has no single canonical LeetCode entry.

---

### Topic 1. Top-K & Kth Element

---

### 1. Kth Largest Element in a Stream (#1)

**Original question:** LC 703. Design a class that finds the `k`-th largest element in a stream of numbers (the `k`-th largest in sorted order, not the `k`-th distinct). Implement `KthLargest(k, nums)` and `add(val)`, which adds `val` and returns the current `k`-th largest.

**Scenario:** A game server receives player scores all day long. After every new score, a banner must show the score currently sitting in `k`-th place.

**Ask first:**
1. Do duplicate scores each take their own place? (They do for "k-th largest".)
2. Can fewer than `k` scores exist when I'm asked? What should I return?

**Spot it:** Data **arrives over time** and I need the **k-th best after each arrival**. I only ever need the best `k`; everything below that can be forgotten, and the smallest of the best `k` is the answer.

**Brute force:** Keep all scores in a list and re-sort after every add: `O(n log n)` per add. Or insert into a sorted list: `O(n)` per add.

**Solve:** ([01-kth-largest-element-in-a-stream.md](01-top-k-and-kth-element/01-kth-largest-element-in-a-stream.md))
```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = nums                      # note: reuses (and trims) the caller's list
        heapq.heapify(self.min_heap)
        while len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.min_heap, val)
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)          # the smallest of k + 1 is no longer in the top k
        return self.min_heap[0]                   # smallest of the top k = the k-th largest
```

**Cost:** `__init__` is `heapify` `O(n)` plus up to `n - k` pops of `O(log n)`: `O(n log n)`. Each `add` is one push and at most one pop on a heap of at most `k + 1` items: `O(log k)`. Space `O(k)`.
**Follow-up:** *Scores can be removed?* A heap can't delete from the middle; use lazy deletion or a sorted container (Variant A). *`k` very small (like 3)?* Three variables, no heap (Variant B). *Read the k-th far more often than you add?* Cache the root: it is already `O(1)`. *Don't mutate the caller's list?* Copy it first.

**More scenarios on the same pattern**

**Variant A (crossover: removals break a plain heap)**
- **Question:** Design a leaderboard that supports `add(score)`, `remove(score)` and `kth()` for the current `k`-th largest score. (Classic design question, no single LC entry.)
- **Scenario:** Players can also delete their accounts, and their scores must disappear from the ranking. The banner must still show the correct `k`-th place.
- **Pattern and cost:** `heapq` cannot remove an arbitrary item. Option 1: **lazy deletion**, a counter of "pending removals"; when the root is marked removed, pop it. `O(log n)` amortised. Option 2: a sorted container (balanced tree), `O(log n)` for add, remove and k-th-by-index. Say why a plain heap is not enough.

**Variant B (crossover: tiny `k` needs no heap)**
- **Question:** LC 414 Third Maximum Number. Given an integer array, return the third distinct maximum number, or the maximum if there are fewer than three distinct numbers.
- **Scenario:** A podium shows the bronze-medal score from a list of results. Ties on the same score share a medal.
- **Pattern and cost:** `k = 3` is a constant, so three variables are enough: `O(n)` time, `O(1)` space. A heap would work but adds nothing. Note "distinct" here differs from #1.

---

### 2. Kth Largest Element in an Array (#2)

**Original question:** LC 215. Given an integer array `nums` and an integer `k`, return the `k`-th largest element in the array (the `k`-th largest in sorted order, not the `k`-th distinct element). Can you solve it without sorting?

**Scenario:** A support team has one day's list of response times. Report the time that is `k`-th from the slowest.

**Ask first:**
1. Is this a one-off over a fixed list, or will more data arrive later?
2. May I reorder the list? Is `O(n)` average acceptable, or must it be worst-case guaranteed?

**Spot it:** A **single query on fixed data**, so there is no need to keep a structure around for later. Choose between a size-`k` heap (`O(n log k)`) and quickselect (`O(n)` average).

**Brute force:** Sort and index: `O(n log n)`. Correct, but it pays to order everything when only one position matters.

**Solve:** ([02-kth-largest-element-in-an-array.md](01-top-k-and-kth-element/02-kth-largest-element-in-an-array.md))
```python
import heapq, random

def findKthLargest(nums: list[int], k: int) -> int:      # heap version
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]

def findKthLargestQuickSelect(nums: list[int], k: int) -> int:   # O(n) average, 3-way split
    target_index = len(nums) - k
    left, right = 0, len(nums) - 1
    while True:
        pivot = nums[random.randint(left, right)]
        less, i, greater = left, left, right
        while i <= greater:
            if nums[i] < pivot:
                nums[less], nums[i] = nums[i], nums[less]
                less += 1
                i += 1
            elif nums[i] > pivot:
                nums[i], nums[greater] = nums[greater], nums[i]
                greater -= 1
            else:
                i += 1
        if target_index < less:
            right = less - 1
        elif target_index > greater:
            left = greater + 1
        else:
            return pivot
```

**Cost:** Heap: each of `n` numbers does one push and at most one pop on at most `k + 1` items: `O(n log k)` time, `O(k)` space. Quickselect: each round discards a large part of the range, so `O(n)` average (`O(n²)` worst, very unlikely with a random pivot), `O(1)` space, and it **reorders `nums`**. The 3-way split keeps lists full of equal values fast.
**Follow-up:** *Better than `n log k`?* Quickselect. *Data is a stream?* #1. *Must not modify the input?* Heap, or copy first. *Guaranteed worst-case `O(n)`?* Median of medians (mention only). *`k` close to `n`?* Search for the `(n - k + 1)`-th smallest instead.

**More scenarios on the same pattern**

**Variant A (crossover to bucketing)**
- **Question:** LC 347 Top K Frequent Elements. Given an integer array `nums` and `k`, return the `k` most frequent elements.
- **Scenario:** A retailer wants the `k` best-selling product codes from a long order log.
- **Pattern and cost:** Count first (`O(n)`). A size-`k` heap on the counts is `O(n log k)`. But counts are bounded by `n`, so bucket the codes by count and read from the top: `O(n)` time, `O(n)` space, no log factor. The heap is the right call when the keys aren't small integers (see the Arrays-Strings repo).

**Variant B (crossover to binary search)**
- **Question:** LC 658 Find K Closest Elements. Given a **sorted** array `arr`, a count `k` and a target `x`, return the `k` integers closest to `x`, sorted ascending.
- **Scenario:** A price list is already ordered from cheapest to dearest. Find the `k` prices nearest to a customer's budget.
- **Pattern and cost:** Because the data is ordered, the answer is a contiguous block: binary search for the left edge of the block, `O(log(n - k) + k)`. A heap would be `O(n log k)` and ignores the order you were given. Spotting the structure beats applying the heap.

---

### 3. K Closest Points to Origin (#3)

**Original question:** LC 973. Given an array of `points` where `points[i] = [xi, yi]` and an integer `k`, return the `k` closest points to the origin `(0, 0)` (Euclidean distance). The answer may be in any order.

**Scenario:** A ride-hailing app has the coordinates of every available driver. Given the rider at the centre of the map, return the `k` drivers nearest to them.

**Ask first:**
1. Does the order of the `k` results matter? Can I compare squared distances instead of taking square roots?
2. How are ties broken at the boundary, and can `k` exceed the number of drivers?

**Spot it:** "Best `k` by a **computed** value." The key (distance) isn't stored in the input, so compute it, and keep a **max**-heap of the `k` smallest distances: the root is the furthest of the closest, the one to evict.

**Brute force:** Compute all distances, sort, take `k`: `O(n log n)`.

**Solve:** ([03-k-closest-points-to-origin.md](01-top-k-and-kth-element/03-k-closest-points-to-origin.md))
```python
import heapq

def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    max_heap = []                                   # entries are (-distance, x, y)
    for x, y in points:
        dist = x * x + y * y                        # squared: no sqrt needed to compare
        heapq.heappush(max_heap, (-dist, x, y))     # negate: min-heap on -dist = max-heap on dist
        if len(max_heap) > k:
            heapq.heappop(max_heap)                 # evict the furthest
    return [[x, y] for _, x, y in max_heap]
```

**Cost:** One push and at most one pop per point on a heap of at most `k + 1` items: `O(n log k)` time, `O(k)` space. Ties compare `x` then `y` (all ints, never an error); any valid set of `k` is accepted.
**Follow-up:** *Better than `n log k`?* Quickselect on the distances, `O(n)` average. *Points arrive over time?* Same heap, works online. *Many queries with different centres?* Build a spatial index (k-d tree). *Points have an id and distance ties?* Use `(-dist, id)` to avoid comparing payloads.

**More scenarios on the same pattern**

**Variant A (a size-5 heap per group)**
- **Question:** LC 1086 High Five. Given a list of `[studentId, score]`, return each student's average of their top five scores.
- **Scenario:** A school wants each student's best-five average from a messy log of test results, in student order.
- **Pattern and cost:** A **dictionary of small min-heaps**, one per student, capped at 5. `O(n log 5) = O(n)` time, `O(students × 5)` space. The same cap-and-evict move, once per key.

**Variant B (crossover: no heap, a partition)**
- **Question:** Return the `k` closest points to the origin without a heap, in `O(n)` average time. (The standard follow-up to LC 973.)
- **Scenario:** The same driver lookup, but the dispatcher wants it faster for a huge fleet and doesn't mind reordering the list.
- **Pattern and cost:** Quickselect on the squared distances (same partition idea as #2): after partitioning, the first `k` positions hold the closest `k`. `O(n)` average, `O(1)` extra, reorders the input, not suited to a stream.

---

### 4. Top K Frequent Words (#4)

**Original question:** LC 692. Given an array of strings `words` and an integer `k`, return the `k` most frequent strings, sorted by frequency from highest to lowest. For words with the same frequency, sort them in alphabetical order.

**Scenario:** A search box suggests the `k` most-typed queries today. When two queries were typed equally often, the alphabetically earlier one should be shown first.

**Ask first:**
1. Must the output be ordered (frequency, then alphabetical), or just the set?
2. Is the whole log available at once, or does it keep growing?

**Spot it:** Two steps: **count**, then **pick the best `k` by a custom order**. The tie-break is the trap: for equal counts, the alphabetically *larger* word is the *worse* one and must be evicted first.

**Brute force:** Count, then sort all distinct words by `(-count, word)` and take `k`: `O(n + u log u)` for `u` distinct words.

**Solve:** ([04-top-k-frequent-words.md](01-top-k-and-kth-element/04-top-k-frequent-words.md))
```python
from collections import Counter
import heapq

class Pair:
    def __init__(self, count: int, word: str):
        self.count, self.word = count, word
    def __lt__(self, other: "Pair") -> bool:
        if self.count != other.count:
            return self.count < other.count     # fewer uses = worse = evicted first
        return self.word > other.word           # tie: alphabetically later = worse

def topKFrequent(words: list[str], k: int) -> list[str]:
    freq_map = Counter(words)
    min_heap = []
    for word, count in freq_map.items():
        heapq.heappush(min_heap, Pair(count, word))
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    res = []
    while min_heap:
        res.append(heapq.heappop(min_heap).word)
    return res[::-1]                            # worst-first, so reverse
```

**Cost:** Counting is one `O(n)` pass; each of `u` distinct words costs one push and at most one pop on at most `k + 1` items: `O(n + u log k)`. The final `k` pops are `O(k log k)`. Space `O(u)`.
**Follow-up:** *Why a class instead of a tuple?* A tuple `(count, word)` evicts the alphabetically *smaller* word first, the wrong way (you can't negate a string). *Shortcut?* `heapq.nsmallest(k, freq_map, key=lambda w: (-freq_map[w], w))`. *Counts bounded by `n`?* Bucket by count, sort each bucket alphabetically. *Huge stream?* Variant B.

**More scenarios on the same pattern**

**Variant A (crossover to buckets, no heap)**
- **Question:** LC 347 Top K Frequent Elements. Return the `k` most frequent elements of an integer array.
- **Scenario:** A retailer wants the `k` bestselling item codes.
- **Pattern and cost:** No tie-break and no output order, so buckets (shelves indexed by count) beat the heap: `O(n)` time and space. Choose the heap when the tie-break, or a stream, makes the shelves awkward.

**Variant B (crossover to approximate counting)**
- **Question:** Find the `k` most frequent items in a stream far too large for the distinct items to fit in memory. (Classic design question.)
- **Scenario:** A global ad network sees billions of events and can only keep a small table in memory. It still wants the busiest `k` campaigns.
- **Pattern and cost:** Exact counts need `O(u)` space. A **count-min sketch** estimates counts in `O(1)` space per item, and a size-`k` heap holds the current best by estimate. Time `O(log k)` per event, space `O(sketch + k)`. The answer is approximate (counts may be over-estimated, never under).

---

### 5. Kth Smallest Element in a Sorted Matrix (#5)

**Original question:** LC 378. Given an `n x n` matrix where each row and each column is sorted in ascending order, return the `k`-th smallest element in the matrix (the `k`-th in sorted order, not the `k`-th distinct).

**Scenario:** A pricing table lists values that rise from left to right in every row and from top to bottom in every column. Which price is the `k`-th cheapest in the whole table?

**Ask first:**
1. Are the rows and columns guaranteed to go up (non-decreasing), and is it square?
2. How large can `n` be, and can values repeat?

**Spot it:** A matrix that is ordered two ways is `n` ordered lists. The smallest overall is always at the top-left of what's left, so you can **merge lazily**, or **count how many cells are ≤ a guessed value** and binary search on that value.

**Brute force:** Flatten all `n²` cells and sort: `O(n² log n)`.

**Solve:** ([05-kth-smallest-element-in-a-sorted-matrix.md](01-top-k-and-kth-element/05-kth-smallest-element-in-a-sorted-matrix.md))
```python
import heapq

def kthSmallest(matrix: list[list[int]], k: int) -> int:     # heap version as written
    n = len(matrix)
    max_heap = []                                            # negated values: max-heap, size k
    for r in range(n):
        for c in range(n):
            heapq.heappush(max_heap, -matrix[r][c])
            if len(max_heap) > k:
                heapq.heappop(max_heap)
    return -max_heap[0]

def kthSmallestBinarySearch(matrix: list[list[int]], k: int) -> int:   # search on the value
    n = len(matrix)
    left, right = matrix[0][0], matrix[n - 1][n - 1]

    def count_less_equal(mid: int) -> int:
        count, row, col = 0, n - 1, 0                        # start bottom-left
        while row >= 0 and col < n:
            if matrix[row][col] <= mid:
                count += row + 1                             # the whole column above is <= mid too
                col += 1
            else:
                row -= 1
        return count

    while left < right:
        mid = (left + right) // 2
        if count_less_equal(mid) < k:
            left = mid + 1
        else:
            right = mid
    return left
```

**Cost:** Heap as written: all `n²` cells pushed onto a heap of at most `k + 1`: `O(n² log k)` time, `O(k)` space. Binary search: each count walks `row` up and `col` right, at most `2n` steps, and the search halves the value range: `O(n log(max − min))` time, `O(1)` space. The faster heap idea (not coded): a `k`-way merge pushing only `(matrix[r][0], r, 0)` per row, then the next cell of the popped row: `O((n + k) log n)`.
**Follow-up:** *Better than the simple heap?* The `k`-way merge or the binary search. *Values are huge, `n` small?* Heap merge. *Rows only sorted, not columns?* The search-by-count trick breaks; merge only. *Return the position?* Track `(r, c)` in the merge.

**More scenarios on the same pattern**

**Variant A (crossover: an implicit table, binary search wins)**
- **Question:** LC 668 Kth Smallest Number in Multiplication Table. In an `m x n` table where cell `(i, j)` is `i * j`, return the `k`-th smallest value.
- **Scenario:** A school poster shows every product of two numbers. Which number is `k`-th smallest on the poster, without printing it?
- **Pattern and cost:** There is no stored matrix to heap over (`m·n` can be `10⁹`), but "how many cells are ≤ `x`" is `sum(min(x // i, n))`, `O(m)`. Binary search the value: `O(m log(m·n))` time, `O(1)` space.

**Variant B (crossover: search on the answer + two pointers)**
- **Question:** LC 719 Find K-th Smallest Pair Distance. Given an integer array and `k`, return the `k`-th smallest absolute difference among all pairs `(i, j)` with `i < j`.
- **Scenario:** A city has `n` stations along a road. Of all pairwise distances, which is the `k`-th shortest?
- **Pattern and cost:** There are `n²/2` pairs, far too many to heap. Sort the array, binary search the distance `d`, and count pairs with difference ≤ `d` using two pointers in `O(n)`. `O(n log n + n log(max))` time, `O(1)` space. A heap would be a `k`-way merge of sorted differences, which is slower for large `k`.

---

### 6. Find K Pairs with Smallest Sums (#6)

**Original question:** LC 373. You are given two integer arrays `nums1` and `nums2` sorted in non-decreasing order, and an integer `k`. Return the `k` pairs `(u, v)` with the smallest sums, where `u` is from `nums1` and `v` is from `nums2`.

**Scenario:** Two suppliers each publish a price list, cheapest first. A buyer must pick one item from each. List the `k` cheapest combinations by total cost.

**Ask first:**
1. Are both lists already ordered, and could either be empty?
2. How large is `k` compared with `len(nums1) × len(nums2)`?

**Spot it:** There are `m·n` possible pairs, but the cheapest are found by **merging `m` ordered lists** (row `i` is `nums1[i] + nums2[0], nums1[i] + nums2[1], ...`). You never need to build them all.

**Brute force:** Build all `m·n` pairs and sort: `O(mn log(mn))`.

**Solve:** ([06-find-k-pairs-with-smallest-sums.md](01-top-k-and-kth-element/06-find-k-pairs-with-smallest-sums.md))
```python
import heapq

def kSmallestPairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    if not nums1 or not nums2:
        return []
    min_heap, result = [], []
    for i in range(min(len(nums1), k)):                     # one candidate per row
        heapq.heappush(min_heap, (nums1[i] + nums2[0], i, 0))
    while min_heap and len(result) < k:
        pair_sum, i, j = heapq.heappop(min_heap)
        result.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):                              # the next pair in this row
            heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))
    return result
```

**Cost:** The start pushes at most `min(m, k)` items; then at most `k` rounds of one pop and at most one push on a heap of at most `min(m, k)`: `O(k log min(m, k))` time. Space `O(min(m, k))` for the heap plus `O(k)` for the output. Each `(i, j)` is pushed at most once, so no `seen` set is needed.
**Follow-up:** *Why only `(i, j+1)` after a pop?* Each row is walked in order, and row starts are seeded upfront. *Three lists?* Heap of triples, same idea. *Return only the sums?* Same loop. *`k` larger than all pairs?* The heap empties and the loop stops.

**More scenarios on the same pattern**

**Variant A (merge k ordered lists)**
- **Question:** LC 23 Merge k Sorted Lists. Merge `k` sorted linked lists into one sorted list.
- **Scenario:** `k` regional log servers each produce events in time order; combine them into one global timeline.
- **Pattern and cost:** Same machine: a heap holding the current head of each list. `O(N log k)` time for `N` total nodes, `O(k)` space. Divide and conquer (merge pairs) gives the same time with `O(1)` extra (Linked-List repo).

**Variant B (crossover: merge + a window)**
- **Question:** LC 632 Smallest Range Covering Elements from K Lists. Given `k` sorted lists, find the smallest range `[a, b]` that includes at least one number from each list.
- **Scenario:** `k` regional schedules, each in time order. What's the shortest time span that includes at least one show from every region?
- **Pattern and cost:** A min-heap with one element per list, while tracking the current maximum; the range is `[heap root, max]`. Pop the smallest, push that list's next element, update the best range. `O(N log k)` time, `O(k)` space. A heap *and* a running window.

---

### Topic 2. Scheduling & Greedy with a Heap

---

### 7. Last Stone Weight (#7)

**Original question:** LC 1046. You are given an array of integers `stones` where `stones[i]` is the weight of the `i`-th stone. Each turn, take the two heaviest stones and smash them together: if they are equal, both are destroyed; otherwise the lighter is destroyed and the heavier is reduced by the lighter's weight. Return the weight of the last remaining stone, or `0` if none remain.

**Scenario:** A recycling machine is fed a pile of scrap blocks. Each cycle, it grabs the two heaviest blocks and crushes them together. If they weigh the same, both disappear; otherwise a smaller block (the difference) is returned to the pile. What's left at the end?

**Ask first:**
1. If exactly one block remains, do I return its weight; if none, `0`?
2. Can there be many blocks (so repeated sorting is too slow)?

**Spot it:** "Repeatedly take the **two biggest**, then put something back." The pile changes after every step, so the "biggest" changes too. That is a priority queue in plain words.

**Brute force:** Re-sort the list after every smash: `O(n² log n)`. Or scan for the two maxima each round: `O(n²)`.

**Solve:** ([07-last-stone-weight.md](02-scheduling-and-greedy-with-a-heap/07-last-stone-weight.md))
```python
import heapq

def lastStoneWeight(stones: list[int]) -> int:
    max_heap = [-s for s in stones]                 # negate: Python's heap is a min-heap
    heapq.heapify(max_heap)
    while len(max_heap) > 1:
        first = heapq.heappop(max_heap)             # heaviest (most negative)
        second = heapq.heappop(max_heap)            # second heaviest
        if first != second:
            heapq.heappush(max_heap, first - second)   # still negative: the leftover weight
    return -max_heap[0] if max_heap else 0
```

**Cost:** `heapify` is `O(n)`. There are at most `n - 1` rounds, each with 2 pops and at most 1 push of `O(log n)`: `O(n log n)` time. The heap is a new list of `n` negated weights: `O(n)` space.
**Follow-up:** *Why negate?* `heapq` is a min-heap, and the most negative number is the heaviest. *Could you do it in place?* Yes: negate `stones` itself and heapify. *Weights are small integers?* Bucket by weight. *Smash three at a time?* Pop three, same loop.

**More scenarios on the same pattern**

**Variant A (the same loop, with the other end)**
- **Question:** LC 1167 Minimum Cost to Connect Sticks. You have sticks with given lengths. Connecting two sticks of lengths `x` and `y` costs `x + y` and produces one stick of length `x + y`. Return the minimum total cost to connect all sticks into one.
- **Scenario:** A workshop joins pieces of rope into one rope. Each join costs the sum of the two pieces. What's the cheapest order?
- **Pattern and cost:** Always join the **two shortest** (a min-heap, no negation). It's Huffman coding's merge step. `O(n log n)` time, `O(n)` space. The greedy is right because a short piece joined early is re-counted in every later join, so keep it small.

**Variant B (crossover: a fixed number of operations)**
- **Question:** LC 1962 Remove Stones to Minimize the Total. Given piles of stones and `k`, perform exactly `k` operations: choose a pile and remove `floor(pile / 2)` stones from it. Return the minimum total number of stones remaining.
- **Scenario:** A warehouse may halve the biggest bin's contents up to `k` times. What's the smallest total that can remain?
- **Pattern and cost:** Each time, halve the **largest** pile (the biggest saving). A max-heap: pop, halve, push back, `k` times. `O(n + k log n)` time, `O(n)` space. A bounded number of rounds, not "until one is left".

---

### 8. Task Scheduler (#8)

**Original question:** LC 621. You are given an array of CPU `tasks`, each a letter (task type), and a cooldown `n`. Each unit of time the CPU either does one task or idles. Two tasks of the same type must be separated by at least `n` units. Return the minimum number of units to finish all tasks.

**Scenario:** A server runs jobs of different types. After running a job of one type, it must wait `n` ticks before running that type again, though it can run other types or sit idle in between. What's the shortest total time to finish everything?

**Ask first:**
1. Is the cooldown measured in ticks between two runs of the same type, and may the CPU idle?
2. Is the order of the output schedule needed, or only the total time?

**Spot it:** "Minimum time with a cooldown." Always run the **type with the most remaining copies that is ready now**, and park the one just used until its cooldown ends.

**Brute force:** Try every ordering of tasks: exponential. A simulation that picks greedily without a heap scans all 26 types each tick: `O(T · 26)`, fine in practice. The heap makes the "most remaining among ready" explicit.

**Solve:** ([08-task-scheduler.md](02-scheduling-and-greedy-with-a-heap/08-task-scheduler.md))
```python
from collections import Counter, deque
import heapq

def leastInterval(tasks: list[str], n: int) -> int:
    count = Counter(tasks)
    max_heap = [-val for val in count.values()]     # remaining counts of ready types
    heapq.heapify(max_heap)
    time = 0
    q = deque()                                     # [remaining_count, available_time] of cooling types
    while max_heap or q:
        time += 1
        if max_heap:
            cnt = 1 + heapq.heappop(max_heap)       # run one copy (counts are negative)
            if cnt:
                q.append([cnt, time + n])           # cooling until time + n
        if q and q[0][1] == time:
            heapq.heappush(max_heap, q.popleft()[0])   # cooldown over: ready again
    return time

def leastIntervalFormula(tasks: list[str], n: int) -> int:     # O(len(tasks)), no simulation
    counts = Counter(tasks)
    max_freq = max(counts.values())
    max_freq_count = sum(1 for f in counts.values() if f == max_freq)
    return max(len(tasks), (max_freq - 1) * (n + 1) + max_freq_count)
```

**Cost:** The loop runs once per time step, `T` steps with `T ≤ len(tasks)·(n + 1)`. The heap and queue hold at most 26 types, so each step is `O(log 26) = O(1)`: `O(T)` time, `O(1)` space. The formula version is `O(len(tasks))` time, `O(1)` space.
**Follow-up:** *Why is a simulation correct?* Using the most frequent ready type never hurts, because the busiest type creates the longest chain of forced gaps. *Return the schedule?* Record the letter (or idle) per tick. *Why the formula?* The most frequent type forces `(max_freq - 1)` blocks of size `n + 1`, plus a final row of every type tied for the max. *`n = 0`?* The answer is `len(tasks)`.

**More scenarios on the same pattern**

**Variant A (crossover: sort by arrival + min-heap)**
- **Question:** LC 1834 Single-Threaded CPU. Given `tasks[i] = [enqueueTime, processingTime]`, a CPU that processes one task at a time always picks, among tasks that have arrived, the one with the shortest processing time (ties by smaller index). Return the order the tasks are processed.
- **Scenario:** A print server receives jobs at different times; whenever it frees up, it prints the shortest waiting job first. In what order do jobs print?
- **Pattern and cost:** Sort tasks by arrival; keep a min-heap of `(processing, index)` for the arrived ones; when the heap is empty, jump the clock to the next arrival. `O(n log n)` time, `O(n)` space. Two structures, one sort and one heap, like IPO (#12).

**Variant B (crossover to a sweep)**
- **Question:** LC 253 Meeting Rooms II (premium). Given meeting time intervals `[start, end]`, return the minimum number of conference rooms required.
- **Scenario:** A conference centre has a day's sessions. How many rooms must it open?
- **Pattern and cost:** Sort by start and keep a **min-heap of end times** of busy rooms; reuse the room that frees first, if free. `O(n log n)` time, `O(n)` space. A sweep over separately sorted starts and ends does the same with no heap (Arrays-Strings repo, #37).

---

### 9. Reorganize String (#9)

**Original question:** LC 767. Given a string `s`, rearrange its characters so that no two adjacent characters are the same. Return any valid rearrangement, or `""` if it is impossible.

**Scenario:** A signage company has a set of letter tiles and must arrange them in a row so that no two identical tiles touch. Output any valid row, or say it can't be done.

**Ask first:**
1. Any valid arrangement, or a specific one (like lexicographically smallest)?
2. Lowercase letters only?

**Spot it:** "No two neighbours alike." Place the **most frequent letter that isn't the one just placed**. Hold the last placed letter out for one round so it can't be chosen twice in a row.

**Brute force:** Try every permutation: `O(n!)`. Sort and interleave halves is a shortcut that works (see the even/odd fill below).

**Solve:** ([09-reorganize-string.md](02-scheduling-and-greedy-with-a-heap/09-reorganize-string.md))
```python
from collections import Counter
import heapq

def reorganizeString(s: str) -> str:
    count = Counter(s)
    max_heap = [[-cnt, char] for char, cnt in count.items()]
    heapq.heapify(max_heap)
    prev = None                                     # the letter held back for one round
    res = []
    while max_heap or prev:
        if prev and not max_heap:                   # only the held-back letter is left: impossible
            return ""
        cnt, char = heapq.heappop(max_heap)
        res.append(char)
        cnt += 1                                    # one copy used (counts are negative)
        if prev:
            heapq.heappush(max_heap, prev)          # the previous letter may be used again now
            prev = None
        if cnt != 0:
            prev = [cnt, char]                      # hold this one for the next round
    return "".join(res)

def reorganizeStringFill(s: str) -> str:            # O(n), no heap
    count = Counter(s)
    max_char = max(count, key=count.get)
    if count[max_char] > (len(s) + 1) // 2:
        return ""
    res, idx = [""] * len(s), 0
    while count[max_char] > 0:                      # most frequent letter on even positions
        res[idx] = max_char
        idx += 2
        count[max_char] -= 1
    for char, cnt in count.items():                 # everything else fills the rest
        while cnt > 0:
            if idx >= len(s):
                idx = 1
            res[idx] = char
            idx += 2
            cnt -= 1
    return "".join(res)
```

**Cost:** `n` placements, each one pop and at most one push on a heap of at most `k` distinct letters (`k ≤ 26`): `O(n log k)`, effectively `O(n)`. Space `O(k)` for the heap plus `O(n)` for the output. The impossibility test: the most frequent letter may appear at most `(n + 1) // 2` times.
**Follow-up:** *Why is the check `count > (n + 1) // 2`?* A letter can occupy at most every other position. *Lexicographically smallest?* Different greedy. *Why `prev`?* Without it the same letter could be popped twice in a row. *Skip the heap?* Even/odd fill, `O(n)`.

**More scenarios on the same pattern**

**Variant A (a gap of `k`, not 1)**
- **Question:** LC 358 Rearrange String k Distance Apart (premium). Rearrange `s` so that the same characters are at least distance `k` from each other, or return `""`.
- **Scenario:** A broadcaster plays songs from several artists and wants the same artist not to repeat within `k` slots.
- **Pattern and cost:** The same max-heap, but the held-back letters now wait in a **queue of length `k`** (as in Task Scheduler #8): after placing a letter, park it, and release the one that was placed `k` steps ago. `O(n log 26)` time, `O(n)` space.

**Variant B (crossover: no heap needed)**
- **Question:** LC 1054 Distant Barcodes. In a warehouse, barcodes are arranged in a row. Rearrange them so no two adjacent barcodes are equal. It is guaranteed an answer exists.
- **Scenario:** A conveyor loads parcels with colour codes; no two neighbouring parcels may share a code, and a valid arrangement always exists.
- **Pattern and cost:** Since an answer is guaranteed, skip the heap: sort values by frequency (most frequent first) and fill positions `0, 2, 4, ...` then `1, 3, 5, ...`. `O(n log n)` or `O(n)` with counting, `O(n)` space.

---

### 10. Design Twitter (#10)

**Original question:** LC 355. Design a simplified Twitter where users can post tweets, follow or unfollow other users, and see the 10 most recent tweets in their news feed (from themselves and the users they follow). Implement `postTweet(userId, tweetId)`, `getNewsFeed(userId)`, `follow(followerId, followeeId)` and `unfollow(followerId, followeeId)`.

**Scenario:** A small social app lets people post short messages and follow each other. Opening the app must show the 10 most recent messages from the people you follow, plus your own.

**Ask first:**
1. Is a user's own feed included, and how fast must `getNewsFeed` be?
2. Which operation is called most often: posting, following, or reading the feed?

**Spot it:** Each followed account is an **ordered list (newest first)**. The feed is a merge of those lists, and I only need the first 10 items: that is a **`k`-way merge** with a heap that holds one candidate per list.

**Brute force:** Collect all tweets of everyone I follow, sort by time, take 10: `O(T log T)` for `T` tweets in total.

**Solve:** ([10-design-twitter.md](02-scheduling-and-greedy-with-a-heap/10-design-twitter.md))
```python
from collections import defaultdict
import heapq

class Twitter:
    def __init__(self):
        self.count = 0                               # global clock, decreasing: smaller = newer
        self.tweet_map = defaultdict(list)           # userId -> [[count, tweetId], ...] oldest first
        self.follow_map = defaultdict(set)           # userId -> set of followeeIds

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweet_map[userId].append([self.count, tweetId])
        self.count -= 1

    def getNewsFeed(self, userId: int) -> list[int]:
        res, min_heap = [], []
        self.follow_map[userId].add(userId)          # see your own tweets
        for followeeId in self.follow_map[userId]:
            if followeeId in self.tweet_map and self.tweet_map[followeeId]:
                index = len(self.tweet_map[followeeId]) - 1
                count, tweetId = self.tweet_map[followeeId][index]
                min_heap.append([count, tweetId, followeeId, index - 1])
        heapq.heapify(min_heap)
        while min_heap and len(res) < 10:
            count, tweetId, followeeId, index = heapq.heappop(min_heap)
            res.append(tweetId)
            if index >= 0:                           # push this user's next-older tweet
                count, tweetId = self.tweet_map[followeeId][index]
                heapq.heappush(min_heap, [count, tweetId, followeeId, index - 1])
        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follow_map[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.follow_map[followerId] and followerId != followeeId:
            self.follow_map[followerId].remove(followeeId)
```

**Cost:** `postTweet`, `follow`, `unfollow`: `O(1)`. `getNewsFeed`: start with at most `F` entries (`F` = accounts followed, including yourself), `O(F)` to heapify, then at most 10 pops and 10 pushes: `O(F + 10 log F)`. Space `O(U + T)` for follow relationships and all tweets. The heap inside a feed call is `O(F)`.
**Follow-up:** *Millions of followees?* Cache or precompute feeds ("fan-out on write") and trade write cost for read speed. *Pagination?* Keep a cursor (the last timestamp). *Why a decreasing counter?* So the min-heap pops the newest first. *Unfollow while reading?* The feed is built from a snapshot of the follow set.

**More scenarios on the same pattern**

**Variant A (crossover: heap or three pointers)**
- **Question:** LC 264 Ugly Number II. An ugly number has only prime factors 2, 3 and 5. Return the `n`-th ugly number.
- **Scenario:** A puzzle app lists numbers that are built only from 2s, 3s and 5s. What's the `n`-th one in order?
- **Pattern and cost:** Three ordered streams (`×2`, `×3`, `×5` of earlier results) merged on the fly. A min-heap with a seen-set: `O(n log n)` time, `O(n)` space. Three pointers (a tiny DP) give `O(n)` time and `O(n)` space with no heap. Know both and why the pointers work (each stream is already in order).

**Variant B (crossover to binary search)**
- **Question:** LC 786 K-th Smallest Prime Fraction. Given a sorted array `arr` of `1` and primes, consider all fractions `arr[i] / arr[j]` for `i < j`. Return the `k`-th smallest fraction as `[arr[i], arr[j]]`.
- **Scenario:** A recipe site lists every ratio of two ingredient amounts (small over large). Which ratio is `k`-th smallest?
- **Pattern and cost:** Each denominator `j` is an ordered list of fractions, so a `k`-way merge heap works: seed `(arr[0] / arr[j], 0, j)` for each `j`, pop `k` times, advancing `i`. `O((n + k) log n)`. Or binary search the fraction value and count with two pointers: `O(n log(precision))`, `O(1)` space.

---

### Topic 3. Two Heaps

---

### 11. Find Median from Data Stream (#11)

**Original question:** LC 295. The median is the middle value in an ordered list, or the average of the two middle values if the list has even length. Implement `MedianFinder` with `addNum(num)` and `findMedian()`, which returns the median of all elements so far.

**Scenario:** A latency monitor receives response times one at a time. At any moment, an engineer may ask for the typical (middle) response time over everything seen so far.

**Ask first:**
1. How often is the middle read compared with how often numbers are added?
2. Is the range of values bounded (for example, 0 to 100)? Are duplicates common?

**Spot it:** "The **middle** of data that **keeps growing**." The middle splits the data into a lower half and an upper half; I only need the **largest of the lower half** and the **smallest of the upper half**, which are exactly two heap roots.

**Brute force:** Keep a list and sort on every query: `O(n log n)` per query. Or insert into a sorted list: `O(n)` per add.

**Solve:** ([11-find-median-from-data-stream.md](03-two-heaps/11-find-median-from-data-stream.md))
```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []                              # max-heap (negated): the lower half
        self.large = []                              # min-heap: the upper half

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        if self.small and self.large and (-self.small[0] > self.large[0]):   # order: small <= large
            heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.small) > len(self.large) + 1:                            # size: small may be 1 bigger
            heapq.heappush(self.large, -heapq.heappop(self.small))
        elif len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
```

**Cost:** `addNum` does at most about three heap operations on heaps of at most `n` items: `O(log n)`. `findMedian` reads the roots: `O(1)`. Space `O(n)` since every number is stored.
**Follow-up:** *All numbers in `[0, 100]`?* A 101-slot frequency array and a walk to the middle: `O(1)` add, `O(101)` median, `O(1)` space (Variant B). *99% in `[0, 100]`?* Same array plus two counters for outliers. *Sliding window median?* Variant A. *Why must `small` hold the extra item?* So the odd-count median is always at `-small[0]`.

**More scenarios on the same pattern**

**Variant A (crossover: removals need lazy deletion)**
- **Question:** LC 480 Sliding Window Median. Given an array and a window size `k`, return the median of each window as it moves.
- **Scenario:** A monitoring dashboard shows the typical response time over the last `k` readings, updating with every new reading.
- **Pattern and cost:** Elements now **leave**. A plain heap can't delete from the middle, so use two heaps with **lazy deletion** (a "to remove" counter, cleaned when it reaches a root) or a sorted container: `O(n log k)` time, `O(k)` space. The balancing logic needs care with the outgoing element's side.

**Variant B (crossover to counting)**
- **Question:** Find the median of a stream when all values are integers in `[0, 100]`. (The LC 295 follow-up.)
- **Scenario:** A thermostat logs temperatures that are always whole degrees between 0 and 100. Report the middle reading at any time.
- **Pattern and cost:** No heaps needed. Keep a count per value and a running total `n`; to find the median, walk the 101 buckets until the cumulative count reaches `n/2`. `O(1)` add, `O(101) = O(1)` median, `O(1)` space. The bound on the values replaces the data structure.

---

### 12. IPO (#12)

**Original question:** LC 502. A company wants to maximise its capital before an IPO and can complete at most `k` distinct projects. Project `i` has `profits[i]` and needs a minimum `capital[i]` to start. Starting with capital `w`, finishing a project adds its profit to your capital. Return the maximum capital after finishing at most `k` projects.

**Scenario:** A startup can take on at most `k` jobs, one after another. Each job requires some minimum cash on hand to start and pays a profit that is added to the cash. Starting with some cash `w`, what's the most cash it can have at the end?

**Ask first:**
1. Can projects be done in any order, and is each done at most once?
2. Are profits non-negative? (If so, capital never decreases, which makes the greedy safe.)

**Spot it:** "Do up to `k` things; finishing one **unlocks** more." In each round, **make every project I can afford available**, then **pick the most profitable of those**. The affordable set only grows, so two structures work together: a list sorted by required capital, and a max-heap of profits.

**Brute force:** Try every choice of `k` projects in every order: exponential. Or each round scan all projects for the best affordable one: `O(k·n)`.

**Solve:** ([12-ipo.md](03-two-heaps/12-ipo.md))
```python
import heapq

def findMaximizedCapital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
    n = len(profits)
    projects = sorted(zip(capital, profits))         # by required capital
    max_heap = []                                    # profits of affordable, not-yet-done projects (negated)
    i = 0
    for _ in range(k):
        while i < n and projects[i][0] <= w:         # unlock everything affordable now
            heapq.heappush(max_heap, -projects[i][1])
            i += 1
        if not max_heap:                             # nothing affordable: stop early
            break
        w += -heapq.heappop(max_heap)                # take the most profitable
    return w
```

**Cost:** Sorting is `O(n log n)`. Each project is pushed at most once (`O(n log n)` total) and there are at most `k` pops of `O(log n)`: `O(n log n + k log n)` time, `O(n)` space.
**Follow-up:** *Why is the greedy correct?* Taking the biggest affordable profit never reduces what you can afford later, since profits are non-negative. *Negative profits?* The greedy breaks (you would skip them anyway, but they could also be needed to unlock). *Fewer than `k` affordable?* The heap empties and the loop stops. *Pointer `i` only moves forward:* each project enters the heap once.

**More scenarios on the same pattern**

**Variant A (crossover: hindsight with a max-heap)**
- **Question:** LC 871 Minimum Number of Refueling Stops. A car starts with `startFuel` and must reach `target` miles away. `stations[i] = [position, fuel]`. The car uses one fuel per mile and can refuel at stations. Return the minimum number of refuelling stops, or `-1` if it can't reach.
- **Scenario:** A delivery van crosses a desert with fuel depots along the way. What's the fewest depots it must stop at?
- **Pattern and cost:** Drive as far as possible; whenever you can't reach the next depot, **in hindsight** refuel at the passed depot with the most fuel (a max-heap of fuel amounts). `O(n log n)` time, `O(n)` space. Same unlock-then-pick-best shape as #12.

**Variant B (crossover: regret by evicting the worst)**
- **Question:** LC 630 Course Schedule III. Given `courses[i] = [duration, lastDay]`, take courses one at a time, each finishing by its last day. Return the maximum number of courses you can take.
- **Scenario:** A student picks lectures, each with a length and a deadline, and wants to attend as many as possible.
- **Pattern and cost:** Sort by deadline; add each course's duration to a running total and push it on a max-heap; if the total exceeds the deadline, **drop the longest course taken so far**. `O(n log n)` time, `O(n)` space. The heap undoes an earlier choice: greedy with regret.

---

## Part 5. Common traps to say out loud

Interviewers listen for these. Say the relevant one *before* you code it.

**Python's `heapq`**
- **It is a min-heap only.** For a max-heap push `-x` and negate when you pop or peek. Say "I'm negating because Python's heap is a min-heap" so it doesn't look like a mistake.
- **For the k largest, the heap is a MIN-heap of size `k`** (root = k-th largest). For the k smallest, a MAX-heap of size `k`. Mixing these up is the most common bug.
- **Strings can't be negated.** For a "reverse alphabetical" tie-break, write a class with `__lt__` (#4), or encode the order some other way.
- **Tuples compare left to right.** If two keys tie, Python compares the next field, which may not be comparable (a custom object, a node). Add a tie-breaker such as an index: `(key, index, payload)`.
- **`heap[0]` on an empty heap raises `IndexError`.** Guard it, especially at `k > n` and on the first `add`.
- **Iterating over a heap is not sorted.** `[x for x in heap]` is in heap order. Sorted output means popping everything.
- **`heapq.heapify(nums)` mutates the list you pass in** (#1's `__init__` reuses and trims the caller's list). Copy first if the caller still needs it.
- **There is no decrease-key and no delete.** Use lazy deletion (skip stale entries on pop) or a sorted container.

**Algorithm choice**
- **Using a heap when sorting once is enough.** If the data is fixed and `k` is close to `n`, `sorted(...)` is simpler and just as fast.
- **Not mentioning quickselect** for "k-th largest" (#2). Say the `O(n)` average and the cost: it reorders the input.
- **Heap of everything instead of a heap of `k`.** Pushing all `n` items and popping `k` is `O(n log n)`; capping at `k` is `O(n log k)` and `O(k)` space.
- **Forgetting that duplicates count separately** for "k-th largest" (not "k-th distinct").
- **Mutating an item inside the heap** (a list entry changed in place) silently breaks the heap invariant. Pop, change, push.

**Problem-specific**
- **Task Scheduler:** release a cooled-down task *before* the next step uses the heap, and idle ticks still count as time (#8).
- **Reorganize String:** check feasibility with `max_count <= (n + 1) // 2` up front; the held-back `prev` is what prevents repeats (#9).
- **Two heaps:** restore the order invariant (`max(small) <= min(large)`) *and* the size invariant after every add. Do them in that order (#11).
- **Median result is a float,** even for an odd count (`2.0`) (#11).
- **K closest points:** compare squared distances; taking `sqrt` is unneeded and introduces floating-point error (#3).
- **`k` larger than the data:** the heap simply never evicts; return everything (#3, #6).
- **Stale entries in lazy deletion** must be removed from the root *before* you read it.
- **Merging lists:** push the next item of the list you just popped from, not of a different list (#6, #10).

---

## Part 6. Known gaps: important heap problems this repo doesn't cover yet

Per [problems.md](problems.md), several heap-adjacent problems were deliberately placed elsewhere or left out. For scenario questions, you should still be able to *recognise* them.

**Lives in a sibling repo (revise it there):**

| Problem | Technique | Where |
|---|---|---|
| Merge k Sorted Lists (LC 23) | `k`-way merge with a heap, or divide and conquer | Linked-List repo |
| Top K Frequent Elements (LC 347) | Count + buckets (a heap on the counts also works) | Arrays-Strings repo (#5) |
| Meeting Rooms II (LC 253) | Min-heap of end times, or a sweep | Arrays-Strings repo (#37) |
| Sliding Window Maximum (LC 239) | Monotonic deque (a heap with lazy deletion is the slower alternative) | Arrays-Strings repo (#28) |
| Network Delay Time, Path With Minimum Effort | Dijkstra's heap of `(distance, node)` | Graphs repo |

**Not in any repo yet, and likely to be asked:**

| Problem | Technique | Why add it |
|---|---|---|
| Minimum Cost to Connect Sticks (LC 1167) | Min-heap, merge the two smallest | The textbook greedy-with-a-heap warm-up; listed as out of scope in the tracker |
| Sliding Window Median (LC 480) | Two heaps + lazy deletion, or a sorted container | The natural follow-up to #11; tests removals |
| Smallest Range Covering Elements from K Lists (LC 632) | Heap + running maximum | Hard; the tracker lists it as out of scope |
| Single-Threaded CPU (LC 1834) | Sort + min-heap | A very typical "scheduler" scenario |
| Rearrange String k Distance Apart (LC 358) | Max-heap + queue | The generalisation of #9 with the #8 queue |
| Minimum Number of Refueling Stops (LC 871), Course Schedule III (LC 630) | Heap used for hindsight / regret | The most subtle uses of a heap in a greedy |
| Ugly Number II (LC 264), K-th Smallest Prime Fraction (LC 786) | Heap-merge of implicit ordered lists | Recognising a merge when no lists are given |
| High Five (LC 1086), Reduce Array Size to The Half (LC 1338) | A heap or sort per group; heap on counts | Easy reps of the capped-heap and count-then-heap moves |
| Furthest Building You Can Reach (LC 1642) | Min-heap holding the `ladders` biggest jumps | A clean "keep the `k` biggest" in disguise |
| Count-min sketch + heap for approximate top-k | Streams that don't fit in memory | The usual "what if the stream is too big?" answer |
| Indexed heap / lazy deletion design | Heap with updates and removals | The standard answer to "what if an item's priority changes?" |

**Notes on the repo's own write-ups** (so you can answer well if asked):
- **#1** reuses the caller's `nums` as the heap (`self.min_heap = nums`), which heapifies and trims it in place. Fine on LeetCode; say you'd copy it otherwise.
- **#5** as written pushes every cell into a size-`k` heap, `O(n² log k)`. The write-up also describes the faster `k`-way merge, `O((n + k) log n)`, and the binary-search version, `O(n log(max − min))`. In an interview, mention the merge or the search first.
- **#2's QuickSelect** was rewritten as an iterative 3-way partition after the two-way version raised `RecursionError` on inputs full of equal values. Know why a 3-way split matters.
- **#8** has both a simulation and a counting formula in the write-up. Know both, and why the formula `(max_freq - 1) * (n + 1) + max_freq_count` works.
- **#11's** write-up also describes the bounded-value follow-ups (all values in `[0, 100]`, 99% in `[0, 100]`), which are not coded. Rehearse them.

**Confidence note:** the LeetCode numbers in the variants were written from memory, in the same spirit as the tracker's own caveat in [problems.md](problems.md). Before relying on a number, search the title on LeetCode. The techniques, costs and traps are the part to trust and rehearse.
