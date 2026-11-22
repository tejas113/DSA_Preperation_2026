# Linked List: Scenario Question Bank (Google L3 style)

Google doesn't say "reverse a linked list" or "use fast and slow pointers". It gives a short, vague scenario about a chain of records where each one only knows the next, and **you** have to work out which pointer technique fits, and what to watch for with the head.
This file has one scenario per solved problem in this repo, plus two more variants of each, so you practise the *recognition* step and not just the solution.
Problem numbers match [problems.md](problems.md). The repo has write-ups for 18 of the 20 tracked problems; #10 (Intersection of Two Linked Lists) and #18 (Sort List) are still **TBD** in the tracker, so they appear here as variants and in the gaps list (Part 6) instead of as their own entries.

**Disguised on purpose:** scenarios avoid words like "linked list", "node", "pointer", "cycle", "dummy", "slow/fast" and "in place" when those words would give the technique away. They talk about chains of cars, playlists, records that each name the next one, and so on. Each one has an **Ask first** line (the clarifying questions a good candidate asks), a **Spot it** line (the clue that gives the technique away), and a **Brute force** line (so you can say what the technique improves).

**How to use:** read only the **Scenario** line, then say out loud: *what can I reach from one record (only the next one)? can the first record change? can I copy the data into an array, or must I rewire in place? what is the `O(n)`-space answer, and can I drop the space?* Only then read the rest. About half of the variants deliberately cross over into a neighbouring technique (arrays, stacks, heaps, hash maps, binary search, graphs) so you learn where pointer tricks stop being the right tool.

---

## Part 1. The 5-step "Which linked-list technique?" framework

1. **Read the structure and the rules.** Before choosing a technique, ask what you are allowed to do.
   - **Singly or doubly linked?** Singly: you can only walk forward, so "the previous node" must be remembered.
   - **Sorted?** Merging, de-duplicating and sorting all depend on it.
   - **Can there be a cycle? Can two lists share a tail?** (changes termination and the choice of pointers)
   - **May the head change?** If yes, put a **dummy node** in front, so the head is never a special case.
   - **May I modify the nodes, or only read them?** Rewiring `next` modifies the list.
   - **Extra space?** `O(1)` extra rules out copying into an array or a hash set. `O(n)` is fine otherwise.
   - **Length known?** One pass vs two passes, and whether "from the end" needs a gap pointer.

2. **Name what is being asked.** Finish: *"I must produce a ___ by changing ___."*
   - **A different order** (reverse all, reverse a range, reverse in groups, rotate, interleave): **pointer rewiring**.
   - **A position found by shape** (the middle, the n-th from the end, where a loop starts, where two chains meet): **fast/slow or gap pointers**.
   - **A new list built from old ones** (merge, add, partition, filter, de-duplicate): **dummy node + tail**.
   - **A copy, or constant-time lookup into the list** (deep copy with random links, an LRU cache): **hash map + list**.
   - **Yes/no about the structure** (loop? palindrome? shared tail?): fast/slow, or reverse-and-compare.

3. **Choose the technique** (see Part 2). Say the cheaper alternative too:
   - **Copy the values into an array** and use indices: `O(n)` space, trivial to code, always an acceptable first answer. The follow-up is "now do it in `O(1)` space".
   - **A hash set / map of visited nodes:** `O(n)` space, works for cycles and intersections. The follow-up is the pointer trick.
   - **Recursion:** short and elegant, but `O(n)` call-stack space and Python's recursion limit (about 1000). Say it.

4. **Write the loop and the invariant.** The three habits that prevent almost every bug:
   - **Save `next` before overwriting `curr.next`.** (`nxt = curr.next` first.)
   - **Use a dummy node** whenever the head can be removed or replaced, and return `dummy.next`.
   - **Say what each pointer means** and what stays true after each step (for example: "`prev` is the fully reversed part so far, `curr` is the untouched rest").
   - **Draw** `1 → 2 → 3 → None` with the pointers marked, and trace a 0-, 1- and 2-node list.

5. **Cost: say it before you code.**
   - Almost everything is **`O(n)` time** (each node visited a constant number of times) and **`O(1)` space** (a few pointers).
   - Exceptions: merging `k` lists (`O(N log k)`), merge sort on a list (`O(n log n)`), hash-map designs (`O(n)` space), and recursion (`O(n)` stack).
   - Count the passes: "one pass to find the middle, one to reverse, one to merge: three passes, still `O(n)`".

**Say-it-out-loud template:** *"I'll keep [pointers and what each means]. Each node is visited [once / a constant number of times], so `O(n)` time. I only keep [a few pointers], so `O(1)` space. Because [the head can change / I might delete the first node], I'll add a dummy node. Before I overwrite `curr.next` I'll save it. The brute force copies the values into an array: `O(n)` space."*

**Questions to ask the interviewer (cheap and impressive):**
- **Shape:** Singly or doubly linked? Could the list be empty, or have one node? Can there be a cycle?
- **Order:** Is it sorted? Ascending? Are duplicates possible?
- **Output:** Return the new head? Modify in place? May I create new nodes, or must I reuse the existing ones?
- **Space:** Is `O(1)` extra space required, or may I use a hash map or an array? Is recursion acceptable (depth)?
- **Position meaning:** Is `n` or `k` one-indexed? What if `n` is larger than the list? What counts as "the middle" for an even length (first or second)?
- **Mutation:** May I change the node values, or only the links? (swapping values is a cheat in some problems)
- **Size:** Can the list be very long (millions)? (recursion depth, memory)
- **Shared structure:** Can two lists share a tail? Do I have to leave the originals unchanged (deep copy)?
- **Concurrency / reuse:** For a design question, which operations are called most often?

---

## Part 2. Signal → technique cheat sheet

Problem numbers match [problems.md](problems.md). **gap** means the repo has no write-up for it yet (see Part 6). Techniques owned by other repos are named so you still recognise them.

| What the question says | It is really | Technique | Problems |
|---|---|---|---|
| "flip the order of the chain" | point each `next` backward | **three pointers** `prev, curr, nxt` | 1 |
| "flip only the part between positions `L` and `R`" | reverse a sub-range, reconnect both ends | **dummy + `leftPrev`, reverse `R - L + 1` nodes** | 2 |
| "flip the order in blocks of `k`, leave a short last block alone" | repeated sub-range reversal | **count length, reverse each full block** | 3 |
| "shift everything `k` places toward the front" | rotate | **close into a ring, cut at the new tail** (`k % n`) | 4 |
| "find the middle in one pass" | one pointer moves twice as fast | **slow / fast** | 5 |
| "does the chain loop back on itself" | the fast pointer laps the slow one | **Floyd's tortoise and hare** | 6 |
| "where does the loop start" | phase 2: reset one pointer to the head | **Floyd, two phases** | 7 |
| "remove the n-th from the end" | keep a gap of `n` between two pointers | **gap pointers + dummy** | 8 |
| "interleave first, last, second, second-last, ..." | middle, reverse the half, weave | **middle + reverse + merge** | 9 |
| "do two chains share a tail?" (find the shared point) | equalise the walked distance | **switch heads at the end** | gap (#10) |
| "is it the same forwards and backwards" | middle, reverse the half, compare | **middle + reverse + compare** | 11 |
| "values `1..n`, one repeated, read-only, `O(1)` space" | the array is a chain `i → nums[i]` with a loop | **Floyd on an array** | 12 |
| "merge two ordered chains" | take the smaller front each time | **dummy + tail** | 13 |
| "add two numbers stored digit by digit" | walk both with a carry | **dummy + tail + carry** | 14 |
| "delete every value that appears more than once" (the head may go) | skip whole runs | **dummy + `prev` (last kept)** | 15 |
| "merge `k` ordered chains" | `k`-way merge | **min-heap of heads**, or divide and conquer | 16 |
| "put all smaller values first, keep relative order" | two lists, joined | **two dummy lists** | 17 |
| "sort a chain in `O(n log n)`" | merge sort on a list | **middle + split + merge** | gap (#18) |
| "copy a chain whose records also point to random others" | old → new mapping | **hash map**, or interleave copies (`O(1)` space) | 19 |
| "get and put in `O(1)`, evict the least recently used" | a map to nodes plus a recency order | **hash map + doubly linked list** | 20 |
| "the data is in an array or a string, not a chain" | same ideas, index arithmetic | **two pointers / read-write pointers** | Arrays-Strings repo |
| "the structure branches" | a tree or graph | **DFS / BFS** | Trees / Graphs repos |
| "merge `k` ordered streams, take the first `m`" | heap of heads | **heap** | Heap repo |
| "pick a random node, list length unknown, one pass" | uniform sampling | **reservoir sampling** | gap |

**Red flags that you're being tested on linked lists:** "each record only knows the next one", "in place", "constant extra space", "one pass", "the head may change", "the n-th from the end", "the middle", "reverse", "reorder", "loops back", "shares a tail", "merge", "copy with extra links", "`O(1)` get and put".

### Rewire in place, or copy to an array?

| | Copy values into an array | Rewire the links in place |
|---|---|---|
| Space | `O(n)` | `O(1)` |
| Code | trivial, index arithmetic | pointer juggling, easy to break |
| Good as | the safe first answer | the follow-up ("now in `O(1)` space") |
| Danger | none, but it may not satisfy the space limit | losing `next`, creating a cycle, forgetting to cut |

Interviewers often **expect you to state the array version first**, then improve it. Say it and its cost.

### Hash map or pointer trick?

- **Cycle detection:** a `set` of visited nodes is `O(n)` space and trivially correct. Floyd's two pointers is `O(1)` space. Know both and say which uses which.
- **Intersection of two lists:** a set of nodes from one list, or the head-switching trick (`O(1)` space).
- **Deep copy with random pointers:** a map `old → new` (`O(n)`), or weave copies between originals (`O(1)`).
- **Random access to a node** (LRU cache): a hash map from key to node is unavoidable.

### When do I need a dummy node?

Whenever the **head can change**: removing the first node (#8, #15), inserting before the first (#2, #3), building a new list (#13, #14, #16, #17). A dummy costs `O(1)` space and removes a whole class of head bugs. If the head can *never* change (reversal returns a new head via `prev`, finding the middle), you don't need one.

### Recursion or iteration?

Recursion is short (`reverseList`, `mergeTwoLists`) but costs `O(n)` stack and can hit Python's recursion limit on long lists. Prefer **iteration**, and mention the recursive version as a follow-up when asked.

### When it is really something else

- **Sorted order and `k` lists:** a **heap** (Heap repo).
- **Only the value order matters, and you may rebuild:** an **array and a sort**.
- **Need the n-th element many times:** a list is the wrong structure; convert to an array.
- **A shortest or cheapest "path" through links:** that is a **graph** problem.

---

## Part 3. Complexity patterns

Every list cost is **(number of passes) × (work per node)**. Count the passes first.

| Pattern | Time | Extra space | Why |
|---|---|---|---|
| Reverse the whole list (iterative) | `O(n)` | `O(1)` | one pass, three pointers |
| Reverse the whole list (recursive) | `O(n)` | `O(n)` | one stack frame per node; recursion limit |
| Reverse a range / reverse in `k`-groups | `O(n)` | `O(1)` | each node reversed once; groups need a length pass first |
| Rotate right by `k` | `O(n)` | `O(1)` | one pass for the length, then at most `length - 1` steps; `k % length` first |
| Find the middle (slow/fast) | `O(n)` | `O(1)` | `fast` ends after about `n / 2` loops |
| Cycle detection (Floyd) | `O(n)` | `O(1)` | the gap shrinks by 1 per step inside the cycle |
| Cycle start (Floyd, two phases) | `O(n)` | `O(1)` | phase 1 up to about `n`; phase 2 at most the distance to the start |
| Cycle detection with a visited set | `O(n)` | `O(n)` | one set entry per node |
| n-th from the end (gap pointers) | `O(n)` | `O(1)` | one pass, the gap stays fixed |
| Reorder / palindrome (middle + reverse + weave/compare) | `O(n)` | `O(1)` | three passes, each at most `n` steps |
| Palindrome by copying to an array | `O(n)` | `O(n)` | the array holds every value |
| Merge two sorted lists | `O(m + n)` | `O(1)` | each loop step moves one node |
| Add two numbers | `O(max(m, n))` | `O(max(m, n))` for the output | one step per column plus a final carry |
| Remove duplicates / partition (dummy + tail) | `O(n)` | `O(1)` | one pass, nodes relinked, not copied |
| Merge `k` lists with a heap | `O(N log k)` | `O(k)` | each of `N` nodes pushed and popped once, heap holds at most `k` |
| Merge `k` lists, one after another | `O(N · k)` | `O(1)` | the growing result is re-walked each time |
| Merge `k` lists, divide and conquer | `O(N log k)` | `O(log k)` (recursion) | `log k` rounds, each touches all `N` nodes |
| Merge sort on a list | `O(n log n)` | `O(log n)` recursion (or `O(1)` bottom-up) | split by middle, merge in `O(n)` |
| Deep copy with a map | `O(n)` | `O(n)` | one map entry per node |
| Deep copy by interleaving | `O(n)` | `O(1)` extra | three passes; copies are woven into the original |
| LRU cache: `get` and `put` | `O(1)` | `O(capacity)` | dict finds the node; a doubly linked list moves it in a fixed number of pointer changes |

**How to work out complexity (say it in this order):**
1. **Count the passes** over the list. Three sequential passes are still `O(n)` (add, don't multiply).
2. **Look at the work per node.** Re-pointing a `next` is `O(1)`. A heap push is `O(log k)`. A dict lookup is `O(1)` average.
3. **Nested loops that never reset** are amortised: slow/fast, gap pointers and the inner skip in Remove Duplicates each visit every node once in total.
4. **Space = what you store.** A few pointers: `O(1)`. A set or map of nodes: `O(n)`. Recursion: `O(depth)`. The returned list is not counted as extra space when you reuse the input nodes; it is counted when you create new nodes (Add Two Numbers).
5. **State the brute force** (copy to an array, or a visited set) and then what the pointer trick saves.

**Rules of thumb**
- **A linked list gives `O(1)` insert/delete at a known node but `O(n)` access by index.** That is the whole reason to pair it with a hash map (LRU).
- **Slow/fast is still `O(n)`,** not `O(n²)`: the fast pointer covers the list once.
- **`k` lists merged naively, one by one, is `O(N · k)`.** Say "heap or divide and conquer gives `O(N log k)`".
- **Recursion on a long list can overflow Python's stack** (about 1000 frames). Say it, and prefer a loop.
- **Don't count the output list as extra space** when you reuse the input nodes; do count it when you build new ones.

---

## Part 4. The scenarios

Each entry has: **Original question** (the formal LeetCode statement), then **Scenario** (what you'd actually hear), **Ask first**, **Spot it** (the clue that reveals the technique), **Brute force** (the naive answer and its cost), **Solve** (the answer from your write-up), **Cost** (time and space, with the reasoning), **Follow-up** (what they'd push on), and **two more variants (A and B)** on the same pattern. Each variant gives the formal **Question** first, then the disguised **Scenario**, then **Pattern and cost**. Variants marked **(crossover)** leave the entry's technique on purpose, to show you where it stops working. A variant with no LC number is a classic interview question that has no single canonical LeetCode entry.

The code below assumes the usual `ListNode(val, next)` class from your write-ups.

---

### Topic 1. Reversal & Pointer Rewiring

---

### 1. Reverse Linked List (#1)

**Original question:** LC 206. Given the head of a singly linked list, reverse the list, and return the reversed list.

**Scenario:** A train's cars are coupled in a chain, and each car only knows which car is directly behind it. The depot needs the chain flipped so the last car leads, without borrowing any extra cars for bookkeeping.

**Ask first:**
1. Can the chain be empty or have a single car? Should I return the new first car?
2. Must it be done by re-coupling the existing cars (no new ones), and may I use recursion?

**Spot it:** Each record can only look **forward**. To flip the direction I must **remember the previous record** before I let go of the next one.

**Brute force:** Copy all values into an array, then rewrite the list's values from the end: `O(n)` time, `O(n)` space. Or push every node on a stack and re-link them while popping: `O(n)` space.

**Solve:** ([01-reverse-linked-list.md](01-reversal-and-rewiring/01-reverse-linked-list.md))
```python
def reverseList(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next          # save the rest BEFORE overwriting
        curr.next = prev         # point backward
        prev = curr              # prev: fully reversed part so far
        curr = nxt               # curr: the untouched rest
    return prev

def reverseListRecursive(head):  # O(n) stack
    if not head or not head.next:
        return head
    new_head = reverseListRecursive(head.next)
    head.next.next = head        # the node after head now points back to head
    head.next = None
    return new_head
```

**Cost:** The loop visits each node once and changes one pointer per node: `O(n)` time, `O(1)` space. The recursive version is `O(n)` time but `O(n)` space (one frame per node) and can hit Python's recursion limit.
**Follow-up:** *Recursively?* The version above, and say its stack cost. *Only part of the list?* #2. *Reverse in groups?* #3. *Why save `nxt` first?* Overwriting `curr.next` would lose the rest of the list. *Doubly linked?* Swap `prev` and `next` on every node.

**More scenarios on the same pattern**

**Variant A (the recursive form, as a stated constraint)**
- **Question:** Reverse a singly linked list using recursion only, and state the space cost. (The classic follow-up of LC 206.)
- **Scenario:** The depot's software is written in a recursive style: the flip must be expressed as "flip everything behind me, then fix my own link".
- **Pattern and cost:** Trust that the recursive call returns the reversed rest, then make `head.next.next = head` and `head.next = None`. `O(n)` time, **`O(n)` space** for the call stack, and a recursion-depth risk for very long lists. The iterative version is `O(1)`.

**Variant B (crossover to a stack)**
- **Question:** LC 445 Add Two Numbers II. Two non-negative integers are stored as linked lists with the **most significant digit first**. Add them and return the sum as a linked list, without reversing the input lists.
- **Scenario:** Two receipts list digits from the biggest place value down. Add them, and don't modify the receipts.
- **Pattern and cost:** The carry flows from the *end*, but the lists run from the *front*. Push each list's digits on a stack, pop to add from the least significant digit, and build the answer by inserting at the front. `O(m + n)` time, `O(m + n)` space. Or reverse both lists, add, and reverse the result (modifies the input).

---

### 2. Reverse Linked List II (#2)

**Original question:** LC 92. Given the head of a singly linked list and two integers `left` and `right` with `left <= right`, reverse the nodes of the list from position `left` to position `right` (1-indexed), and return the reversed list.

**Scenario:** A playlist is a chain of tracks. The user selects the stretch from track `L` to track `R` and presses "reverse selection". Everything outside that stretch stays exactly as it is.

**Ask first:**
1. Are `left` and `right` 1-indexed, and can `left` be `1` (the first track)?
2. Can `left == right`? Must I do it in one pass?

**Spot it:** A reversal in the **middle**, so I must reconnect **both ends**. The head can change when `left = 1`, so I need a dummy in front.

**Brute force:** Copy the list into an array, reverse the slice `array[left-1:right]`, and rebuild: `O(n)` time, `O(n)` space.

**Solve:** ([02-reverse-linked-list-ii.md](01-reversal-and-rewiring/02-reverse-linked-list-ii.md))
```python
def reverseBetween(head, left: int, right: int):
    dummy = ListNode(0, head)
    left_prev, cur = dummy, head
    for _ in range(left - 1):                 # 1) stop at position `left`
        left_prev, cur = cur, cur.next
    prev = None
    for _ in range(right - left + 1):         # 2) reverse exactly right - left + 1 nodes
        tmp_next = cur.next
        cur.next = prev
        prev = cur
        cur = tmp_next
    left_prev.next.next = cur                 # 3) old `left` node (now the tail) joins the rest
    left_prev.next = prev                     #    node before `left` joins the new front
    return dummy.next
```

**Cost:** The two loops together visit at most `right` nodes: `O(n)` time. Only a handful of pointers: `O(1)` space.
**Follow-up:** *One pass?* This is one pass. *Why a dummy?* If `left = 1` the head changes. *Reverse blocks of `k`?* #3. *Why `leftPrev.next.next = cur`?* After reversing, `leftPrev.next` still points at the old first node of the range, which is now the tail.

**More scenarios on the same pattern**

**Variant A (crossover: groups of varying length)**
- **Question:** LC 2074 Reverse Nodes in Even Length Groups. Split the list into consecutive groups of sizes `1, 2, 3, ...` (the last group may be shorter). Reverse every group with an **even** length, and return the head.
- **Scenario:** A conveyor sorts parcels into batches of growing size; batches of even size are reversed before shipping.
- **Pattern and cost:** The same range reversal as #2, but you first compute each group's real length (the last group may be cut short). `O(n)` time, `O(1)` space. The skill is counting the real group size before deciding to reverse.

**Variant B (crossover to gap pointers)**
- **Question:** LC 1721 Swapping Nodes in a Linked List. Swap the values of the `k`-th node from the beginning and the `k`-th node from the end.
- **Scenario:** A queue manager swaps the person `k` places from the front with the person `k` places from the back.
- **Pattern and cost:** Find the `k`-th from the start; then use a **gap of `k`** between two pointers to find the `k`-th from the end in the same pass. Swap the values (or relink). `O(n)` time, `O(1)` space. Mixes #2's positions with #8's gap.

---

### 3. Reverse Nodes in k-Group (#3)

**Original question:** LC 25. Given the head of a linked list, reverse the nodes of the list `k` at a time, and return the modified list. `k` is a positive integer and is at most the length of the list. If the number of nodes is not a multiple of `k`, the left-out nodes at the end remain as they are. You may not alter the values in the nodes; only the nodes themselves may be changed.

**Scenario:** A shipping line loads containers in a chain. They must be re-ordered in blocks of exactly `k`: the order inside each full block is flipped, and a final short block (fewer than `k`) is left untouched.

**Ask first:**
1. If the last block has fewer than `k` items, do I leave it as it is?
2. May I only relink nodes, or may I swap values? Is `O(1)` extra space required?

**Spot it:** #2 repeated. The new twist is **"is there a full block left?"**, which a length count answers up front.

**Brute force:** Copy to an array and reverse each full slice of `k`, then rebuild: `O(n)` time, `O(n)` space. Recursion: reverse the first `k` if they exist, then recurse on the rest: `O(n/k)` stack.

**Solve:** ([03-reverse-nodes-in-k-group.md](01-reversal-and-rewiring/03-reverse-nodes-in-k-group.md))
```python
def reverseKGroup(head, k: int):
    if not head or k == 1:
        return head
    length, curr = 0, head
    while curr:                               # step 1: how many nodes?
        length += 1
        curr = curr.next
    groups = length // k                      # only FULL groups get reversed
    dummy = ListNode(0, head)
    left_prev, cur = dummy, head
    for _ in range(groups):
        prev, count = None, k
        while count > 0:                      # step 2: reverse k nodes
            tmp_next = cur.next
            cur.next = prev
            prev = cur
            cur = tmp_next
            count -= 1
        tail = left_prev.next                 # step 3: reconnect: old first node is now the tail
        tail.next = cur                       #    tail -> the rest
        left_prev.next = prev                 #    previous part -> new first node
        left_prev = tail                      #    advance to the end of this group
    return dummy.next
```

**Cost:** One pass for the length, then each node is reversed once: `O(n)` time, `O(1)` space (no recursion).
**Follow-up:** *`k > length`?* `groups = 0`, the list is unchanged. *Reverse the short last group too?* Drop the length check and reverse whatever is left. *Why count first?* To know a full group exists before reversing it (a reversed partial group would have to be undone). *Pairs only?* Variant A.

**More scenarios on the same pattern**

**Variant A (the `k = 2` special case)**
- **Question:** LC 24 Swap Nodes in Pairs. Swap every two adjacent nodes and return the head, without changing the node values.
- **Scenario:** A seating chart swaps every two neighbouring guests, moving the people (not their name tags).
- **Pattern and cost:** #3 with `k = 2`. With a dummy and one `prev` pointer: `O(n)` time, `O(1)` space. A recursive version is `O(n)` stack. Tracker note: this is why Swap Nodes in Pairs is out of scope in the repo.

**Variant B (crossover to arrays)**
- **Question:** LC 541 Reverse String II. Given a string `s` and `k`, reverse the first `k` characters for every `2k` characters counting from the start of the string.
- **Scenario:** A text tool flips every other block of `k` letters in a message.
- **Pattern and cost:** The same block reversal, but with random access: reverse the slice `s[i:i+k]` for `i = 0, 2k, 4k, ...` with two pointers. `O(n)` time, `O(n)` space (strings are immutable in Python). The array version needs no length pass or relinking.

---

### 4. Rotate List (#4)

**Original question:** LC 61. Given the head of a linked list, rotate the list to the right by `k` places.

**Scenario:** A shift roster is a chain of people. Each week, everyone moves `k` positions toward the end, and the people who fall off the end go to the front. Produce next week's roster.

**Ask first:**
1. Can `k` be larger than the list length (or very large)? Can the list be empty?
2. Rotate right means the last `k` nodes move to the front, correct?

**Spot it:** Moving the last `k` to the front is a **cut and rejoin** at one place. Closing the list into a ring makes the cut easy: find the new tail, break after it.

**Brute force:** Rotate right by one, `k` times: `O(n·k)`. Or copy to an array and slice: `O(n)` space.

**Solve:** ([04-rotate-list.md](01-reversal-and-rewiring/04-rotate-list.md))
```python
def rotateRight(head, k: int):
    if not head or not head.next or k == 0:
        return head
    length, tail = 1, head
    while tail.next:                          # find the length and the old tail
        tail = tail.next
        length += 1
    k %= length                               # rotating by `length` changes nothing
    if k == 0:
        return head
    tail.next = head                          # close the ring
    new_tail = head
    for _ in range(length - k - 1):           # the new tail sits at index length - k - 1
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None                      # cut the ring
    return new_head
```

**Cost:** One pass for the length, then at most `length - 1` steps: `O(n)` time, `O(1)` space.
**Follow-up:** *`k` is huge (like 2·10⁹)?* `k % length` makes it cheap. *Rotate left?* Use `length - k`. *Why the `k == 0` check before closing the ring?* Otherwise you would close the ring and cut at the wrong spot. *Why not rotate by one `k` times?* `O(n·k)`.

**More scenarios on the same pattern**

**Variant A (crossover to arrays)**
- **Question:** LC 189 Rotate Array. Rotate an array to the right by `k` steps, in place with `O(1)` extra space.
- **Scenario:** The same weekly shift, but the roster is stored in an array.
- **Pattern and cost:** With random access, use **three reversals**: reverse all, reverse the first `k`, reverse the rest. `O(n)` time, `O(1)` space. For the list, a ring and a cut is simpler; for the array, reversals are.

**Variant B (length first, then split)**
- **Question:** LC 725 Split Linked List in Parts. Split a linked list into `k` consecutive parts whose sizes differ by at most one, with earlier parts no smaller than later ones.
- **Scenario:** A warehouse splits one long delivery chain into `k` routes, as equal as possible, with any extra stops given to the earlier routes.
- **Pattern and cost:** Count the length `n`; each part has `n // k` nodes, and the first `n % k` parts get one more. Walk, cut each part off with `node.next = None`. `O(n + k)` time, `O(1)` extra space beyond the `k` heads.

---

### Topic 2. Fast & Slow (and Gap) Pointers

---

### 5. Middle of the Linked List (#5)

**Original question:** LC 876. Given the head of a singly linked list, return the middle node of the linked list. If there are two middle nodes, return the second middle node.

**Scenario:** A support queue is a chain of tickets, and each ticket only knows the next one. Without counting them first, find the ticket that sits in the middle (the later of the two if there is an even number).

**Ask first:**
1. For an even length, is the "middle" the first or the second of the two?
2. Can the list be empty?

**Spot it:** "Find the middle in **one pass**, without knowing the length." If one pointer moves twice as fast, it reaches the end exactly when the other is halfway.

**Brute force:** Walk once to count `n`, then walk again to the `n // 2`-th node: two passes, `O(n)` time, `O(1)` space. (Fine, but slow/fast is one pass.)

**Solve:** ([05-middle-of-the-linked-list.md](02-fast-slow-and-gap-pointers/05-middle-of-the-linked-list.md))
```python
def middleNode(head):
    slow = fast = head
    while fast and fast.next:        # fast can still jump twice
        slow = slow.next             # 1 step
        fast = fast.next.next        # 2 steps
    return slow                      # index n // 2: the second middle for even n
```

**Cost:** `fast` reaches the end after about `n / 2` loops, each `O(1)`: `O(n)` time, `O(1)` space.
**Follow-up:** *First middle for even length?* Loop while `fast.next and fast.next.next`. *Why is it still `O(n)`?* About `n/2` iterations, constant work each. *Use it for?* #9 (reorder), #11 (palindrome), and merge sort on a list.

**More scenarios on the same pattern**

**Variant A (middle + the node before it)**
- **Question:** LC 2095 Delete the Middle Node of a Linked List. Delete the middle node (the `⌊n/2⌋`-th, 0-indexed) and return the head.
- **Scenario:** A playlist drops the middle track; the player can't count the tracks first.
- **Pattern and cost:** Slow/fast again, but you need the node **before** the middle to unlink it. Start `fast` one step ahead (or track `prev`), and use a dummy for a one-node list. `O(n)` time, `O(1)` space.

**Variant B (crossover to sampling)**
- **Question:** LC 382 Linked List Random Node. Return the value of a random node from a singly linked list, each node equally likely, without knowing the length.
- **Scenario:** A game picks a random level from a chain of levels whose length it can't store.
- **Pattern and cost:** Not a pointer-speed trick. Use **reservoir sampling**: walk the list once, and replace the pick with node `i` with probability `1 / (i + 1)`. `O(n)` time per pick, `O(1)` space. If `n` is known and many picks are needed, copy to an array for `O(1)` per pick.

---

### 6. Linked List Cycle (#6)

**Original question:** LC 141. Given `head`, the head of a linked list, determine if the linked list has a cycle in it (some node can be reached again by continuously following `next`). Return `true` if there is a cycle.

**Scenario:** A set of records each names the record to read next. A bug may have made one record point back to an earlier one. Without writing anything down, decide whether following the "next" links ever stops.

**Ask first:**
1. May I use extra memory (a set of visited records), or must it be `O(1)`?
2. Can the chain be empty? Can a record point to itself?

**Spot it:** "Does it ever end?" with **no memory allowed**. Two walkers at different speeds on a loop must eventually meet, like runners on a circular track.

**Brute force:** Remember every visited record in a set and stop on a repeat: `O(n)` time, `O(n)` space. Correct, and a good first answer.

**Solve:** ([06-linked-list-cycle.md](02-fast-slow-and-gap-pointers/06-linked-list-cycle.md))
```python
def hasCycle(head) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next                    # 1 step
        fast = fast.next.next               # 2 steps
        if slow == fast:                    # identity comparison: they met inside a loop
            return True
    return False                            # fast hit the end: no loop
```

**Cost:** No cycle: `fast` ends after about `n / 2` loops. With a cycle: `slow` enters within `n` steps, then `fast` closes the gap by 1 per step: at most about one more lap. `O(n)` time, `O(1)` space.
**Follow-up:** *Where does the cycle start?* #7. *How long is the cycle?* Count steps from the meeting point back to it. *Why do they always meet?* Inside the loop the gap changes by 1 each step, so it must hit 0. *Why not move `fast` by 3?* It can skip over `slow` forever for some loop lengths.

**More scenarios on the same pattern**

**Variant A (crossover: a number sequence)**
- **Question:** LC 202 Happy Number. Repeatedly replace a number by the sum of the squares of its digits; return `true` if it reaches `1`, or `false` if it loops forever in a cycle that doesn't include `1`.
- **Scenario:** A puzzle game repeatedly transforms a score. Will it reach 1, or go round in circles?
- **Pattern and cost:** There is no list, but `next(n)` defines one. Floyd's fast/slow on the sequence uses `O(1)` space; a `set` of seen values is `O(log n)`. Spotting that *any* repeating sequence is a "linked list" is the lesson (Arrays-Strings repo, #13).

**Variant B (crossover: an array of jumps)**
- **Question:** LC 457 Circular Array Loop. Each `nums[i]` says how far to move forward or backward (wrapping around). Return `true` if there is a cycle of length greater than one that moves in a single direction.
- **Scenario:** A board game's squares say "jump this many squares, forward or back, wrapping around". Can a token get stuck in a loop of two or more squares?
- **Pattern and cost:** Floyd on the implicit list `i → (i + nums[i]) % n`, but with extra rules: a one-square loop doesn't count, and all moves in the cycle must share a direction. `O(n)` time, `O(1)` space.

---

### 7. Linked List Cycle II (#7)

**Original question:** LC 142. Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return `null`. Do not modify the linked list.

**Scenario:** After finding that a chain of records loops back, an engineer wants to know **which** record is the first one that is reached twice, so she can fix that single link.

**Ask first:**
1. Return the node itself or its index? What if there is no loop?
2. May I use a set (`O(n)`), or is `O(1)` space required? May I modify the list?

**Spot it:** Detection (#6) plus **where the loop begins**. The distances work out so that after the meeting, one walker restarted at the head and one at the meeting point, both moving 1 step at a time, meet exactly at the start of the loop.

**Brute force:** Walk the chain with a set of visited nodes; the first node seen twice is the start: `O(n)` time, `O(n)` space.

**Solve:** ([07-linked-list-cycle-ii.md](02-fast-slow-and-gap-pointers/07-linked-list-cycle-ii.md))
```python
def detectCycle(head):
    slow = fast = head
    while fast and fast.next:                # phase 1: find a meeting point inside the loop
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None                          # fast hit the end: no loop
    slow = head                              # phase 2: restart one walker at the head
    while slow != fast:                      # both move 1 step; they meet at the loop's start
        slow = slow.next
        fast = fast.next
    return slow
```

**Cost:** Phase 1 takes at most about `n` steps; phase 2 takes at most the distance from the head to the loop's start (less than `n`): `O(n)` time, `O(1)` space.
**Follow-up:** *Why does phase 2 work?* If `F` is the distance from the head to the loop's start and the meeting point is `a` steps into the loop, then `2(F + a) = F + a + m·C` (for a whole number `m` of laps of length `C`), so `F = m·C − a`: walking `F` steps from the meeting point lands on the start. *Length of the loop?* From the meeting point, count steps until you return. *Remove the cycle?* Find the node whose `next` is the start and set it to `None`.

**More scenarios on the same pattern**

**Variant A (crossover: where two chains meet, tracker #10)**
- **Question:** LC 160 Intersection of Two Linked Lists. Given the heads of two singly linked lists, return the node at which they intersect, or `null`. The lists must retain their original structure.
- **Scenario:** Two delivery routes end in the same final stretch of stops. Where do they first share a stop?
- **Pattern and cost:** Walk both pointers; when one reaches the end, **switch it to the other list's head**. Both then walk `m + n` steps in total and meet at the intersection (or both reach `None`). `O(m + n)` time, `O(1)` space. Alternatives: a set of one list's nodes (`O(m)` space), or measure both lengths and advance the longer list's pointer first. Not yet written up in the repo.

**Variant B (the cycle length)**
- **Question:** Given a linked list that contains a cycle, return the **length** of the cycle. (Classic follow-up of LC 141 / 142.)
- **Scenario:** The engineer now wants to know how many records are in the loop.
- **Pattern and cost:** After the pointers meet, keep one fixed and move the other until they meet again, counting steps. `O(n)` time, `O(1)` space.

---

### 8. Remove Nth Node From End of List (#8)

**Original question:** LC 19. Given the head of a linked list, remove the `n`-th node from the end of the list and return its head.

**Scenario:** A printer's job queue is a chain where each job knows the next. The operator must cancel the job that is `n`-th from the **back**, and the system can't afford to walk the queue twice.

**Ask first:**
1. Is `n` guaranteed to be at most the length? Is it 1-indexed (`n = 1` is the last)?
2. Can the first job be the one removed?

**Spot it:** "From the end" in **one pass**. If a second pointer starts `n` steps ahead, then when it reaches the end, the first pointer is right before the target. The first job might be removed, so use a dummy.

**Brute force:** Walk once to count the length, then walk to position `length - n`: two passes, `O(n)` time, `O(1)` space.

**Solve:** ([08-remove-nth-node-from-end-of-list.md](02-fast-slow-and-gap-pointers/08-remove-nth-node-from-end-of-list.md))
```python
def removeNthFromEnd(head, n: int):
    dummy = ListNode(0, head)
    slow, fast = dummy, head
    while n > 0 and fast:                    # open a gap of n
        fast = fast.next
        n -= 1
    while fast:                              # move both until fast falls off the end
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next               # slow is the node BEFORE the target
    return dummy.next
```

**Cost:** `fast` makes one pass and `slow` trails behind it: `O(n)` time, `O(1)` space.
**Follow-up:** *Why start `slow` on the dummy?* So that `slow` ends up *before* the target, and removing the head works. *Just find the n-th from the end, not delete?* The same gap, return `slow`'s successor. *Doubly linked with a tail pointer?* Walk back `n - 1` steps from the tail and unlink in `O(n)`, or `O(1)` for `n = 1` (Variant B). *Two passes is fine?* It is, but one pass is the expected answer.

**More scenarios on the same pattern**

**Variant A (the gap, no deletion)**
- **Question:** Return the `k`-th node from the end of a singly linked list in one pass. (Classic.)
- **Scenario:** A monitor shows the 3rd most recent entry of a log that is stored as a chain from oldest to newest.
- **Pattern and cost:** The same gap of `k` between two pointers; when `fast` reaches the end, `slow` is the answer. `O(n)` time, `O(1)` space. Handle `k` greater than the length.

**Variant B (crossover to a doubly linked list)**
- **Question:** Remove the `n`-th node from the end of a **doubly** linked list that keeps a `tail` pointer.
- **Scenario:** The same queue, but each job also knows the one before it and the queue knows its last job.
- **Pattern and cost:** No gap needed. Walk backward `n - 1` steps from the tail: `O(n)` time worst case, **`O(1)` for the last node**. Unlinking needs `prev.next = next` and `next.prev = prev` (update both). With the right structure, the trick disappears.

---

### 9. Reorder List (#9)

**Original question:** LC 143. You are given the head of a singly linked list `L0 → L1 → … → Ln-1 → Ln`. Reorder it to `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`. You may not modify the values in the nodes; only the nodes themselves may be changed.

**Scenario:** A playlist is a chain of tracks. A DJ wants the show to alternate: first track, last track, second track, second-to-last track, and so on, without copying any tracks.

**Ask first:**
1. Must I reuse the existing nodes (no new ones, no value swaps)? `O(1)` extra space?
2. What happens with an odd length (where does the middle track go)?

**Spot it:** I need **both ends at once**, but a chain can't walk backward. So: find the middle, **reverse the second half** (now I can walk it from the old end), and **weave** the two halves.

**Brute force:** Put all nodes in an array and re-link with two indices from both ends: `O(n)` time, `O(n)` space.

**Solve:** ([09-reorder-list.md](02-fast-slow-and-gap-pointers/09-reorder-list.md))
```python
def reorderList(head) -> None:
    if not head or not head.next:
        return
    slow, fast = head, head
    while fast and fast.next:                # 1) find the middle
        slow = slow.next
        fast = fast.next.next
    prev, curr = None, slow.next             # 2) reverse the second half
    slow.next = None                         #    cut the list into two halves
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    first, second = head, prev               # 3) weave: one from the front, one from the back
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
```

**Cost:** Three passes, each at most `n` steps (middle, reverse, weave): `O(n)` time, `O(1)` space.
**Follow-up:** *Array version?* Collect the nodes in a list and link with two indices: simpler, `O(n)` space (Variant B). *Why cut at `slow.next = None`?* Otherwise the first half still points into the second half and the weave creates a cycle. *Odd length?* The extra middle node stays in the first half and ends the list.

**More scenarios on the same pattern**

**Variant A (crossover: odd/even positions, no reversal)**
- **Question:** LC 328 Odd Even Linked List. Group all nodes at odd indices together followed by the nodes at even indices, keeping relative order, in `O(1)` space and `O(n)` time.
- **Scenario:** A conveyor reorders a chain of boxes: first all boxes in positions 1, 3, 5, ..., then those in positions 2, 4, 6, ....
- **Pattern and cost:** No reversal and no middle: two running tails (odd list and even list) built in one pass, then joined. `O(n)` time, `O(1)` space. The "two dummy lists" idea of #17.

**Variant B (crossover to an array)**
- **Question:** Reorder a linked list as in LC 143, but you may use `O(n)` extra space.
- **Scenario:** The DJ doesn't care about memory, only about getting it right quickly.
- **Pattern and cost:** Copy all nodes into an array; use `left, right` indices from both ends, setting `next` as you alternate and finishing with `None`. `O(n)` time, `O(n)` space. Say this first, then improve it. The array version is easier to get right.

---

### 11. Palindrome Linked List (#11)

**Original question:** LC 234. Given the head of a singly linked list, return `true` if it is a palindrome or `false` otherwise.

**Scenario:** A chain of records stores a code one symbol per record. Does the code read the same forward and backward? The records can only be walked forward, and memory is tight.

**Ask first:**
1. May I modify the list temporarily (reverse a half) if I restore it? Or must it stay untouched?
2. Is `O(1)` space required, or can I copy the values into an array?

**Spot it:** Comparing the front with the back needs the back reversed, and the **second half reversed** can be compared with the first half in order.

**Brute force:** Copy the values into an array and compare it with its reverse (or use two indices): `O(n)` time, `O(n)` space.

**Solve:** ([11-palindrome-linked-list.md](02-fast-slow-and-gap-pointers/11-palindrome-linked-list.md))
```python
def isPalindrome(head) -> bool:
    if not head or not head.next:
        return True
    slow, fast = head, head
    while fast and fast.next:                # 1) find the middle
        slow = slow.next
        fast = fast.next.next
    prev, curr = None, slow                  # 2) reverse from the middle
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    left, right = head, prev                 # 3) compare the first half with the reversed second half
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    return True
```

**Cost:** Three passes of at most `n` steps: `O(n)` time. Only pointers: `O(1)` space. (Copying into an array is `O(n)` space.)
**Follow-up:** *Restore the list?* Reverse the second half again after comparing. *Why compare until `right` runs out?* The reversed half is the same size or one smaller, so the comparison stops at the middle. *Doubly linked?* Two pointers from both ends, no reversal (Variant B).

**More scenarios on the same pattern**

**Variant A (middle + reverse, a different combine)**
- **Question:** LC 2130 Maximum Twin Sum of a Linked List. In a list of even length `n`, the `i`-th node (0-indexed) is the twin of node `n − 1 − i`. Return the maximum twin sum (the sum of a node and its twin).
- **Scenario:** Team members are lined up in a chain; each one is paired with the person who is the same distance from the other end. What's the largest combined score of a pair?
- **Pattern and cost:** The same middle-reverse-walk as #11, but instead of comparing you **add** pairs and track the maximum. `O(n)` time, `O(1)` space. Or copy to an array and use two indices (`O(n)` space).

**Variant B (crossover: doubly linked)**
- **Question:** Check whether a **doubly** linked list is a palindrome.
- **Scenario:** The same code check, but each record also knows the one before it, and the system also remembers which record is last.
- **Pattern and cost:** No reversal and no middle: two pointers, one from the head and one from the tail, moving inward. `O(n)` time, `O(1)` space. Again, a richer structure removes the need for the trick.

---

### 12. Find the Duplicate Number (#12)

**Original question:** LC 287. Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive, there is only one repeated number, but it could be repeated more than once. Return it. You must solve it **without modifying `nums`** and using only constant extra space.

**Scenario:** A badge scanner logged `n + 1` visits from `n` possible badge numbers, so some badge number was used twice. The log is read-only and the scanner has almost no spare memory. Which badge number was reused?

**Ask first:**
1. May I modify the log, sort it, or use a set? (The constraints say no.)
2. Can the repeated number appear more than twice?

**Spot it:** Each value is a valid *index* (`1..n`), so `i → nums[i]` is a chain. Since there are `n + 1` entries pointing into `n` slots, two entries point to the same slot, and that makes a **loop**. The duplicate is where the loop starts.

**Brute force:** A `set` of seen values: `O(n)` time, `O(n)` space (not allowed). Sorting: `O(n log n)` time but modifies the array. Compare all pairs: `O(n²)`.

**Solve:** ([12-find-the-duplicate-number.md](02-fast-slow-and-gap-pointers/12-find-the-duplicate-number.md))
```python
def findDuplicate(nums: list[int]) -> int:
    slow = fast = nums[0]
    while True:                                # phase 1: meet inside the loop
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]                             # phase 2: the loop's entrance is the duplicate
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
```

**Cost:** Phase 1 meets within about `n` steps; phase 2 takes at most that many again: `O(n)` time. Only `slow` and `fast`, array read-only: `O(1)` space.
**Follow-up:** *Why is there always a loop?* `n + 1` values in `1..n` means two indices point to the same value, so the "next" function is not one-to-one. *Why start at `nums[0]` and not index 0?* No value points to index 0 (values are 1 or more), so index 0 is outside every loop. *Binary search alternative?* Count how many values are `≤ mid`; `O(n log n)` time, `O(1)` space. *Find all duplicates?* Variant A.

**More scenarios on the same pattern**

**Variant A (crossover: sign marking, may mutate)**
- **Question:** LC 442 Find All Duplicates in an Array. Given an array of `n` integers in `1..n`, each appearing once or twice, return all values that appear twice in `O(n)` time and `O(1)` extra space.
- **Scenario:** A warehouse tally lists bin labels visited, each at most twice. Report the labels visited twice.
- **Pattern and cost:** Several duplicates break Floyd's single loop. Use the array as a hash: for each value `v`, flip the sign of `nums[v - 1]`; if it is already negative, `v` is a repeat. `O(n)` time, `O(1)` space, but it **mutates** the array (restore the signs if required).

**Variant B (crossover: cyclic sort)**
- **Question:** LC 41 First Missing Positive. Given an unsorted integer array, return the smallest missing positive integer in `O(n)` time and `O(1)` space.
- **Scenario:** A ticketing system issued ticket numbers in no particular order. What is the smallest positive ticket number never issued?
- **Pattern and cost:** Put each value `v` in `1..n` at index `v - 1` by repeated swaps (cyclic sort); the first index `i` with `nums[i] != i + 1` gives the answer `i + 1`. `O(n)` time, `O(1)` space; mutates the array. Not yet written up in the Arrays-Strings repo (#78).

---

### Topic 3. Merge, Split & Dummy-Node Construction

---

### 13. Merge Two Sorted Lists (#13)

**Original question:** LC 21. You are given the heads of two sorted linked lists `list1` and `list2`. Merge the two lists into one sorted list by splicing together the nodes of the first two lists. Return the head of the merged list.

**Scenario:** Two departments each keep their invoices as a chain, ordered by date, each invoice knowing only the next one. Combine them into one chain in date order, reusing the existing records.

**Ask first:**
1. Are both chains already in order (ascending), and can either be empty?
2. May I reuse the existing nodes (splice), or must I create new ones? On equal dates, which comes first?

**Spot it:** Two ordered chains: always take the **smaller front**. The head of the result isn't known until the first comparison, so use a **dummy** in front and a `tail` that grows the result.

**Brute force:** Put all values in an array, sort, and rebuild a list: `O((m + n) log (m + n))` time, `O(m + n)` space. It ignores that both inputs are already ordered.

**Solve:** ([13-merge-two-sorted-lists.md](03-merge-split-and-dummy-node/13-merge-two-sorted-lists.md))
```python
def mergeTwoLists(list1, list2):
    dummy = ListNode(0)
    curr = dummy
    while list1 and list2:
        if list1.val <= list2.val:        # <=, so equal values keep list1's first (stable)
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        curr = curr.next
    curr.next = list1 if list1 else list2  # attach whatever is left, in one step
    return dummy.next
```

**Cost:** Each loop step moves one node into the result, at most `m + n` steps; attaching the leftover is `O(1)`: `O(m + n)` time. Nodes are relinked, not copied: `O(1)` extra space.
**Follow-up:** *Recursively?* `O(m + n)` stack. *`k` lists?* #16. *Sort a whole list?* Variant B. *Descending order?* Flip the comparison. *Why the dummy?* The first node of the result is unknown until the first comparison.

**More scenarios on the same pattern**

**Variant A (crossover to arrays, fill from the back)**
- **Question:** LC 88 Merge Sorted Array. Merge `nums2` into `nums1` (which has spare space at the end), in place, both sorted.
- **Scenario:** Two daily logs are stored in arrays, and the first has empty room reserved at its end. Combine them without a third buffer.
- **Pattern and cost:** With arrays, shifting is expensive, so fill from the **back** with three indices. `O(m + n)` time, `O(1)` space. The list version needs no shifting, so it can merge from the front.

**Variant B (crossover: merge sort on a list, tracker #18)**
- **Question:** LC 148 Sort List. Given the head of a linked list, return the list after sorting it in ascending order, in `O(n log n)` time.
- **Scenario:** A chain of records is in random order. Sort it without copying the values into an array.
- **Pattern and cost:** Merge sort: find the middle (#5), cut the list in two, sort each half recursively, and merge with #13. `O(n log n)` time, `O(log n)` recursion space (bottom-up merge sort gets `O(1)`). Not yet written up in the repo.

---

### 14. Add Two Numbers (#14)

**Original question:** LC 2. You are given two non-empty linked lists representing two non-negative integers. The digits are stored in **reverse order**, and each node contains a single digit. Add the two numbers and return the sum as a linked list.

**Scenario:** Two large account numbers are stored as chains of digits, with the ones digit first. Produce their sum in the same format, so billing can read it from the ones digit upward.

**Ask first:**
1. Which end holds the least significant digit (the ones place)? Can the lists differ in length?
2. Can there be leading zeros, or a final carry (for example `5 + 5`)? May I create new nodes?

**Spot it:** Schoolbook addition: **column by column from the ones place**, carrying. With the ones digit at the head, the walk matches the arithmetic.

**Brute force:** Convert each list to an integer, add, and convert back. Fine in Python, but it overflows in fixed-width languages and misses the point (lists can be very long).

**Solve:** ([14-add-two-numbers.md](03-merge-split-and-dummy-node/14-add-two-numbers.md))
```python
def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0
    while l1 or l2 or carry:                  # `or carry`: a last carry needs its own node
        val1 = l1.val if l1 else 0            # a shorter list counts as 0 digits
        val2 = l2.val if l2 else 0
        total = val1 + val2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)
        curr = curr.next
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next
    return dummy.next
```

**Cost:** One step per column, at most `max(m, n) + 1` steps: `O(max(m, n))` time. The output has that many new nodes: `O(max(m, n))` space (apart from the output, only a few variables).
**Follow-up:** *Most significant digit first?* #1 Variant B (stack, or reverse). *Subtract?* More cases (borrow). *Three lists?* Add a third term, same loop. *Why `or carry`?* `999 + 1` needs a fourth digit.

**More scenarios on the same pattern**

**Variant A (crossover to strings)**
- **Question:** LC 67 Add Binary. Given two binary strings, return their sum as a binary string.
- **Scenario:** A hardware tool adds two long bit patterns stored as text.
- **Pattern and cost:** Two indices from the right with a carry; build the result in a list and reverse. `O(max(m, n))` time and space. The string version walks from the end by index; the list version walks naturally from the head.

**Variant B (crossover: the carry comes from the far end)**
- **Question:** LC 369 Plus One Linked List (premium). A non-negative integer is stored as a linked list of digits, most significant first. Add one to it.
- **Scenario:** An odometer is stored as a chain of digits with the biggest place first. Add one.
- **Pattern and cost:** The carry starts at the *end*, but you start at the front. Find the **last node that is not 9** (using a dummy with value 0 in front), increment it, and set every later node to 0. `O(n)` time, `O(1)` space. Or reverse, add, reverse.

---

### 15. Remove Duplicates from Sorted List II (#15)

**Original question:** LC 82. Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the sorted list.

**Scenario:** An ordered chain of IDs contains repeats. Any ID that occurs more than once is considered bad and must disappear entirely (every copy), leaving only IDs that appeared exactly once. The very first ID might be one of the bad ones.

**Ask first:**
1. Remove *all* copies of a repeated value (not keep one)? Can the list be empty?
2. Is the list guaranteed to be ordered, so equal values are neighbours?

**Spot it:** Because the data is ordered, repeats are **runs**. "All copies must go" means I can't decide about a node until I know its run, and the head might go: use a dummy and a `prev` that points at the last *kept* node.

**Brute force:** Count the values with a hash map, then rebuild a list of the values that appear once: `O(n)` time, `O(n)` space. It ignores the ordering.

**Solve:** ([15-remove-duplicates-from-sorted-list-ii.md](03-merge-split-and-dummy-node/15-remove-duplicates-from-sorted-list-ii.md))
```python
def deleteDuplicates(head):
    dummy = ListNode(0, head)
    prev = dummy                               # the last node we are sure to keep
    while head:
        if head.next and head.val == head.next.val:
            while head.next and head.val == head.next.val:
                head = head.next               # walk to the LAST node of the run
            prev.next = head.next              # skip the whole run
        else:
            prev = prev.next                   # head is unique: keep it, advance prev
        head = head.next
    return dummy.next
```

**Cost:** `head` only moves forward and the inner loop shares the same `head`, so each node is passed once: `O(n)` time, `O(1)` space.
**Follow-up:** *Keep one copy (not remove all)?* Variant A (no dummy needed). *Unsorted?* A hash map of counts, `O(n)` space. *Remove a specific value?* Variant B. *Why `prev` doesn't move when a run is skipped?* The node after the run may be part of another run, so it isn't confirmed yet.

**More scenarios on the same pattern**

**Variant A (keep one copy: no dummy needed)**
- **Question:** LC 83 Remove Duplicates from Sorted List. Delete duplicates so each element appears only once; return the sorted list.
- **Scenario:** The same ordered ID chain, but each repeated ID should survive once.
- **Pattern and cost:** The first node is always kept, so the head never changes and a dummy is unnecessary: `while curr.next: if equal, curr.next = curr.next.next; else curr = curr.next`. `O(n)` time, `O(1)` space. Contrast with #15 to show *why* #15 needs the dummy.

**Variant B (the dummy node, plainly)**
- **Question:** LC 203 Remove Linked List Elements. Remove all nodes with a given value `val`; return the new head.
- **Scenario:** A log chain contains entries marked with a banned code; delete them all, even if the first one is banned.
- **Pattern and cost:** The head may be removed, so use a dummy and a `curr` that checks `curr.next.val == val`. Unsorted data is fine. `O(n)` time, `O(1)` space. The cleanest demonstration of "why a dummy node".

---

### 16. Merge k Sorted Lists (#16)

**Original question:** LC 23. You are given an array of `k` linked lists, each sorted in ascending order. Merge all the linked lists into one sorted linked list and return it.

**Scenario:** `k` regional servers each keep their events as a chain in time order. Produce one global timeline, reusing the records.

**Ask first:**
1. How large can `k` be, and can some chains be empty?
2. May I reuse the nodes, and is `O(k)` extra space acceptable?

**Spot it:** #13 at scale. The next record of the answer is always the smallest of the `k` current fronts: a structure that returns the minimum of a changing set, namely a **min-heap**.

**Brute force:** Merge the lists one after another: `O(N · k)` (the growing result is re-walked each time). Or dump everything into an array and sort: `O(N log N)`, `O(N)` space.

**Solve:** ([16-merge-k-sorted-lists.md](03-merge-split-and-dummy-node/16-merge-k-sorted-lists.md))
```python
import heapq

def mergeKLists(lists):
    class HeapNode:                              # wrapper: heapq must compare something that never ties badly
        def __init__(self, node):
            self.node = node
        def __lt__(self, other):
            return self.node.val < other.node.val

    min_heap = []
    for l in lists:                              # one candidate per non-empty list
        if l:
            heapq.heappush(min_heap, HeapNode(l))
    dummy = ListNode(0)
    curr = dummy
    while min_heap:
        node = heapq.heappop(min_heap).node      # the smallest front overall
        curr.next = node
        curr = curr.next
        if node.next:                            # that list's next record becomes its new front
            heapq.heappush(min_heap, HeapNode(node.next))
    return dummy.next
```

**Cost:** Each of `N` nodes is pushed and popped once; the heap holds at most `k` nodes, so each operation is `O(log k)`: `O(N log k)` time. The heap holds at most one node per list: `O(k)` space (the result reuses the nodes).
**Follow-up:** *Without a heap?* Divide and conquer: merge lists in pairs, `log k` rounds each touching all `N` nodes: `O(N log k)` time (Variant B). *Why the wrapper?* A tuple `(val, node)` would compare nodes when values tie, and `ListNode` isn't comparable; use `(val, index, node)` or a wrapper. *Lists too big for memory?* Stream from each source with a heap of heads (external merge).

**More scenarios on the same pattern**

**Variant A (crossover: a heap plus a running maximum)**
- **Question:** LC 632 Smallest Range Covering Elements from K Lists. Given `k` sorted lists, find the smallest range that includes at least one number from each list.
- **Scenario:** `k` regional schedules, each in time order: what's the shortest time span that includes at least one show from every region?
- **Pattern and cost:** The same heap of fronts, but you also track the current **maximum** among them; the range is `[heap root, max]`. Pop the smallest, push its list's next, update the best range. `O(N log k)` time, `O(k)` space (Heap repo).

**Variant B (crossover: divide and conquer)**
- **Question:** Merge `k` sorted linked lists by repeatedly merging them in pairs (no heap).
- **Scenario:** The same global timeline, but the team is told not to use extra data structures.
- **Pattern and cost:** Round 1 merges lists `0+1, 2+3, ...`; round 2 merges the results, and so on, until one list remains. Each round touches all `N` nodes and there are `log k` rounds: `O(N log k)` time, **`O(1)` extra** (`O(log k)` if recursive). Same time as the heap, less memory, and it reuses #13 directly.

---

### 17. Partition List (#17)

**Original question:** LC 86. Given the head of a linked list and a value `x`, partition it so that all nodes less than `x` come before nodes greater than or equal to `x`. You should preserve the original relative order of the nodes in each of the two partitions.

**Scenario:** A chain of tasks has priorities. Reorder it so all tasks with a priority below a threshold come first, then the rest, keeping each group's original order.

**Ask first:**
1. Must the relative order inside each group be kept (stable)? What about values equal to the threshold (they go in the second group)?
2. May I relink nodes, or must I create new ones?

**Spot it:** A stable split into two groups: build **two chains**, one per group, each with its own dummy, then join them.

**Brute force:** Copy values to an array, split into two lists with a stable pass, and rebuild: `O(n)` time, `O(n)` space.

**Solve:** ([17-partition-list.md](03-merge-split-and-dummy-node/17-partition-list.md))
```python
def partition(head, x: int):
    less_head, greater_head = ListNode(0), ListNode(0)
    less, greater = less_head, greater_head
    curr = head
    while curr:
        if curr.val < x:
            less.next = curr
            less = less.next
        else:
            greater.next = curr
            greater = greater.next
        curr = curr.next
    greater.next = None                       # cut the tail, or the list may still point into the old chain (a cycle)
    less.next = greater_head.next             # join the two groups
    return less_head.next
```

**Cost:** One loop over `n` nodes, `O(1)` per node: `O(n)` time. Two dummies and a few pointers; nodes are relinked, not copied: `O(1)` space.
**Follow-up:** *Why `greater.next = None`?* The last node of the `greater` group may still point to a node that was moved to `less`, which would create a cycle. *Three groups (`<`, `==`, `>`)?* Variant B. *Array version?* Variant A. *Stable?* Yes: each group keeps its original order.

**More scenarios on the same pattern**

**Variant A (crossover to arrays, three-way partition)**
- **Question:** LC 75 Sort Colors. Sort an array of `0`s, `1`s and `2`s in place.
- **Scenario:** A belt carries crates tagged 0, 1 or 2; group them in one sweep.
- **Pattern and cost:** In an array you can swap in place with three pointers (`low`, `mid`, `high`), `O(n)` time, `O(1)` space, but it is **not stable**. The list version with dummies is stable and `O(1)` space too (Arrays-Strings repo, #21).

**Variant B (more groups)**
- **Question:** Partition a linked list into three groups: values less than `x`, equal to `x`, and greater than `x`, each in original order. (Natural extension of LC 86.)
- **Scenario:** The task chain now needs "below, at, above" the threshold.
- **Pattern and cost:** Three dummies and three tails, joined at the end (cut the last tail). `O(n)` time, `O(1)` space. Generalises to any fixed number of groups.

---

### Topic 4. Hash Map + List / Design

---

### 19. Copy List with Random Pointer (#19)

**Original question:** LC 138. A linked list of length `n` is given such that each node contains an additional `random` pointer, which could point to any node in the list, or `null`. Construct a **deep copy** of the list: `n` brand-new nodes whose `next` and `random` pointers point to the new nodes, so that none of the pointers in the new list point to nodes in the original list. Return the head of the copied list.

**Scenario:** A document is a chain of sections. Each section also holds a "see also" reference to any other section (or none). Duplicate the whole document so the copy's references point only inside the copy.

**Ask first:**
1. Can a `random` pointer point to the node itself, or be `null`? Can the list be empty?
2. Is `O(n)` extra space acceptable, or must it be `O(1)`?

**Spot it:** The new nodes' `random` links need to find **the copy of** some original node. That's a lookup "old → new", i.e. a hash map, or weaving each copy next to its original so the copy is found by `original.next`.

**Brute force:** For every node, walk the list to find the index of its random target, then walk the new list to that index: `O(n²)` time.

**Solve:** ([19-copy-list-with-random-pointer.md](04-hash-map-and-design/19-copy-list-with-random-pointer.md))
```python
def copyRandomList(head):                         # hash map: O(n) space
    old_to_copy = {None: None}                    # None -> None handles missing next / random
    cur = head
    while cur:                                    # pass 1: create the copies
        old_to_copy[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                                    # pass 2: wire next and random through the map
        copy = old_to_copy[cur]
        copy.next = old_to_copy[cur.next]
        copy.random = old_to_copy[cur.random]
        cur = cur.next
    return old_to_copy[head]

def copyRandomListInterleave(head):               # O(1) extra space
    if not head:
        return None
    cur = head
    while cur:                                    # pass 1: A -> A' -> B -> B'
        nxt = cur.next
        cur.next = Node(cur.val, nxt)
        cur = nxt
    cur = head
    while cur:                                    # pass 2: A'.random = A.random.next
        if cur.random:
            cur.next.random = cur.random.next
        cur = cur.next.next
    dummy = Node(0)                               # pass 3: unweave
    copy_curr, cur = dummy, head
    while cur:
        nxt = cur.next.next
        copy = cur.next
        copy_curr.next = copy
        copy_curr = copy
        cur.next = nxt                            # restore the original list
        cur = nxt
    return dummy.next
```

**Cost:** Map version: two passes, `O(1)` dict operations: `O(n)` time, `O(n)` space (the map; the copies themselves are the required output). Interleaving: three passes, `O(n)` time, `O(1)` extra space.
**Follow-up:** *`O(1)` space?* The interleaving version. *Why `{None: None}`?* So `cur.next` and `cur.random` can be `None` without a branch. *Must the original be restored?* Yes, the third pass does that. *Cycle in the list?* Variant A.

**More scenarios on the same pattern**

**Variant A (crossover to graphs)**
- **Question:** LC 133 Clone Graph. Given a reference to a node in a connected undirected graph, return a deep copy of the graph.
- **Scenario:** A social network wants to duplicate a user's connected neighbourhood, where each user has a list of friends and the links can form loops.
- **Pattern and cost:** The same "old → new" map, but you must **traverse** with DFS or BFS and create each copy once (visited = the map). `O(V + E)` time and space. A chain was a degenerate graph; the map idea generalises (Graphs repo).

**Variant B (crossover to trees)**
- **Question:** LC 1485 Clone Binary Tree With Random Pointer (premium). Each tree node also has a `random` pointer to any node in the tree (or `null`). Return a deep copy.
- **Scenario:** A site map is a tree where each page also has a "related page" link to any other page. Duplicate it.
- **Pattern and cost:** A map from old node to new node, built with DFS/BFS over `left` and `right`, then a second pass for `random`. `O(n)` time, `O(n)` space (the interleaving trick doesn't carry over cleanly to trees).

---

### 20. LRU Cache (#20)

**Original question:** LC 146. Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. Implement `LRUCache(capacity)`, `get(key)` (return the value if the key exists, otherwise `-1`) and `put(key, value)` (update the value if the key exists, otherwise add it; when the number of keys exceeds the capacity, evict the least recently used key). Both `get` and `put` must run in `O(1)` average time.

**Scenario:** A web service keeps its most recently used responses in a fixed-size memory cache. Reading an entry or storing a new one makes it "fresh"; when the cache is full, the entry that has gone unused the longest is thrown away. Lookups and updates must be near-instant.

**Ask first:**
1. Does a `get` count as a use? Does updating an existing key count as a use?
2. What are the capacity limits, and is thread safety required?

**Spot it:** Two needs at once: **find an entry by key in `O(1)`** (a hash map) and **move it to "most recent" and drop the "oldest" in `O(1)`** (a doubly linked list: unlinking a node needs its previous neighbour). Neither structure does both alone.

**Brute force:** A list of keys ordered by recency: `get` and `put` are `O(n)` (find and shift). Or an array with timestamps, scanning for the oldest on eviction: `O(n)`.

**Solve:** ([20-lru-cache.md](04-hash-map-and-design/20-lru-cache.md))
```python
class Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}                           # key -> Node
        self.head, self.tail = Node(), Node()     # dummy ends: LRU is right after head, MRU right before tail
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_tail(self, node: Node) -> None:   # the most-recently-used position
        last = self.tail.prev
        last.next = node
        node.prev = last
        node.next = self.tail
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)                        # a use makes it fresh
        self._add_to_tail(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])         # drop the old node for this key
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add_to_tail(new_node)
        if len(self.cache) > self.capacity:
            lru = self.head.next                  # the stalest entry
            self._remove(lru)
            del self.cache[lru.key]               # the node stores its key so it can be removed from the map
```

**Cost:** The dict lookup is `O(1)` average; `_remove` and `_add_to_tail` change a fixed number of pointers: `O(1)` for both `get` and `put`. At most `capacity` nodes and dict entries, plus two dummy nodes: `O(capacity)` space.
**Follow-up:** *Why doubly linked?* To unlink a node in `O(1)` without searching for its predecessor. *Why dummy head and tail?* No special cases for the first and last node. *Why does the node store its key?* On eviction you need the key to delete it from the map. *Python shortcut?* `collections.OrderedDict` with `move_to_end` and `popitem(last=False)`; know the manual version. *Thread safety?* A lock around each operation.

**More scenarios on the same pattern**

**Variant A (crossover: frequency, then recency)**
- **Question:** LC 460 LFU Cache. Design a Least Frequently Used cache with `get` and `put` in `O(1)`; when the capacity is exceeded, evict the least frequently used key, and among equals the least recently used.
- **Scenario:** The cache now evicts the entry used the *fewest times*, with age only as a tie-break.
- **Pattern and cost:** One list is not enough: keep a map `key → node` and a map `frequency → doubly linked list` of nodes with that frequency, plus the current `min_freq`. On each use, move the node to the next frequency's list. `O(1)` per operation, `O(capacity)` space. Listed as out of scope in the tracker; mention the idea if asked.

**Variant B (crossover to arrays)**
- **Question:** LC 1472 Design Browser History. Implement `visit(url)`, `back(steps)` and `forward(steps)` for a browser's history.
- **Scenario:** A browser tracks pages visited and lets the user step back or forward through them, discarding the forward pages whenever a new page is visited.
- **Pattern and cost:** A doubly linked list with a `current` pointer works (`back` and `forward` walk `steps`, `O(steps)`). An **array and an index** is simpler: `visit` truncates and appends, `back`/`forward` are `O(1)`. Choosing the array here is the better engineering; the tracker notes the array or stack versions are simpler.

---

## Part 5. Common traps to say out loud

Interviewers listen for these. Say the relevant one *before* you code it.

**Pointer bookkeeping**
- **Losing the rest of the list.** Always save `nxt = curr.next` *before* you overwrite `curr.next` (#1, #2, #3).
- **Forgetting to cut.** After moving nodes into new chains, set the last `next = None`, otherwise a stale link creates a **cycle** (#17 `greater.next = None`, #9 `slow.next = None`).
- **Updating pointers in the wrong order** (doubly linked): in `_remove` and `_add_to_tail`, set both directions (`prev.next` and `next.prev`) and don't overwrite a pointer you still need (#20).
- **Returning the wrong head.** After reversing, the head is `prev`, not `head`. With a dummy, return `dummy.next`, not `dummy`.
- **`None` dereferences.** `fast.next.next` crashes if `fast.next` is `None`. Guard with `while fast and fast.next` (#5, #6, #7, #9, #11).
- **Comparing nodes by value instead of identity.** For cycles and intersections compare `slow is fast` / `slow == fast` (same object), not `.val` (#6, #7, #160).

**The head and the boundaries**
- **Add a dummy node whenever the head can change:** removing the first node (#8, #15), reversing a range from position 1 (#2), merging (#13), partitioning (#17). Say it out loud.
- **Empty list, one node, two nodes.** Test all three by hand. `reverseBetween` with `left == right`, `rotateRight` with `k % length == 0`, `reverseKGroup` with `k > length`.
- **Off-by-one in the gap.** For "n-th from the end", `slow` must end up *before* the target, which is why it starts at the dummy (#8). For rotate, the new tail is at index `length - k - 1` (#4).
- **Even vs odd length.** Which node is "the middle"? The loop `while fast and fast.next` gives the second middle; `while fast.next and fast.next.next` gives the first (#5).
- **Not normalising `k`.** `k % length` for rotate (#4). Forgetting it times out for huge `k`.

**Technique-specific**
- **Reverse k-group:** count the length first so you never reverse a partial group (#3).
- **Reorder / palindrome:** cut the list at the middle before reversing the second half, or the first half still points into it (#9). Restore the list afterwards if the problem says not to modify it (#11).
- **Floyd phase 2:** reset *one* pointer to the head and move **both one step at a time** (#7, #12). Moving `fast` by two again is a bug.
- **Add Two Numbers:** keep looping while there is a carry; a missing digit counts as 0 (#14).
- **Remove Duplicates II:** advance `prev` only when the current node is *unique*; after skipping a run, don't move `prev` (#15).
- **Merge k lists:** a heap of `(val, index, node)` or a wrapper with `__lt__`, since `ListNode` objects aren't comparable and ties would raise `TypeError` (#16).
- **Copy with random pointer:** map `None → None`, restore the original list in the interleaving version (#19).
- **LRU:** a `put` on an existing key must refresh recency and replace the value; the node must store its key for eviction; `get` also counts as a use (#20).
- **Recursion:** `O(n)` stack and Python's limit near 1000. Prefer the loop, and say so (#1, #13).

**Python-specific**
- Comparing a node to `None` with `==` is fine but use `is None` where clarity matters; `if node:` treats any node as truthy unless you define `__bool__`.
- A custom class in a heap needs `__lt__` (or a tuple with a tie-breaker index).
- Don't mutate a list while iterating over it; for lists of nodes, build the new chain with a tail pointer instead.
- Printing a list with a cycle loops forever. Use a counter when debugging.

---

## Part 6. Known gaps: important linked-list problems this repo doesn't cover yet

**Planned in [problems.md](problems.md) but not written up yet** (the entries above cover them only as variants, so write them up properly):

| # | Problem | Technique | Why it matters |
|---|---|---|---|
| 10 | Intersection of Two Linked Lists (LC 160, Core) | Switch heads at the end, so both walk `m + n` | A distinct, frequently asked trick; the scenario "where do two chains share a stop" is this |
| 18 | Sort List (LC 148, Stretch) | Middle + split + merge | Combines #5 and #13; the standard `O(n log n)` list sort, with an `O(1)`-space bottom-up follow-up |

**Not in the tracker at all, and likely to be asked:**

| Problem | Technique | Why add it |
|---|---|---|
| Swap Nodes in Pairs (LC 24), Odd Even Linked List (LC 328) | Pointer rewiring | The tracker lists these as out of scope (variations); a very common warm-up |
| Remove Linked List Elements (LC 203), Remove Duplicates from Sorted List (LC 83) | Dummy node, simple scan | The easiest reps of "why a dummy" |
| Add Two Numbers II (LC 445), Plus One Linked List (LC 369) | Stack, or reverse, or last non-9 | The carry-from-the-end cases |
| Linked List Random Node (LC 382) | Reservoir sampling | Tests whether you know sampling from a stream |
| LFU Cache (LC 460) | Maps + frequency lists | The natural follow-up to #20; the tracker lists it as out of scope |
| Flatten a Multilevel Doubly Linked List (LC 430) | Explicit stack or recursion on child pointers | Doubly linked list handling; listed as out of scope |
| Delete the Middle Node (LC 2095), Maximum Twin Sum (LC 2130), Reverse Nodes in Even Length Groups (LC 2074) | Applications of #5, #11, #2 | Easy-medium reps of known moves |
| Design Browser History (LC 1472), Design Linked List (LC 707) | Doubly linked list or array design | The tracker says array/stack versions are simpler and covered elsewhere |
| Convert Sorted List to BST (LC 109) | Middle + recursion | Lives in the Trees repo |
| Insertion Sort List (LC 147) | Dummy + sorted insertion | A different sort approach on lists |
| Merge In Between Linked Lists (LC 1669), Split Linked List in Parts (LC 725) | Rewiring with counts | More cut-and-join practice |

**Notes on the repo's own write-ups** (so you can answer well if asked):
- **#12 Find the Duplicate Number** is in this repo because it is Floyd's algorithm on an array (`i → nums[i]`). Know the binary-search and sign-marking alternatives and why Floyd satisfies "read-only, `O(1)` space".
- **#13 and #16:** your write-up for #16 uses a `HeapNode` wrapper with `__lt__`. Know the alternative `(val, index, node)` tuple, and the `O(1)`-extra-space divide-and-conquer version.
- **#19** has both the map and the interleaving versions. Say which uses more space and which needs three passes.
- **#20** uses dummy head and tail nodes and stores the key in each node. Know why.
- **#4 Rotate List** closes the list into a ring and cuts; the array version uses three reversals. Mention both if asked.

**Confidence note:** the LeetCode numbers in the variants were written from memory, in the same spirit as the tracker's own caveat in [problems.md](problems.md). Before relying on a number, search the title on LeetCode. The techniques, costs and traps are the part to trust and rehearse.
