# DP Patterns — base cases, combine rules and complexity

A 2-minute read before any DP problem. Every rule below comes from problems in this repo.

---

## Ask 3 questions before you code

1. **What am I computing?** Count, min, max, or yes/no?
2. **What does a valid end return?** (success base)
3. **What does a dead end return?** (failure base)

Answer these and you already have your base cases and how to combine states. The recurrence comes after.

---

## The one table to remember

| Question asks for | Valid end returns | Dead end returns | Combine states with |
|---|---|---|---|
| **Count** the ways | `1` | `0` | `+` |
| **Min** cost / steps | `0` | `inf` | `min` |
| **Max** value / length | `0` | `-inf` | `max` |
| **Is it possible?** | `True` | `False` | `or` |

- **Count:** Climbing Stairs, Decode Ways, Coin Change II, Target Sum, Distinct Subsequences
- **Min:** Coin Change, Min Cost Climbing Stairs, Edit Distance
- **Max:** House Robber, LIS, LCS
- **Possible:** Word Break, Partition Equal Subset Sum, Interleaving String

**Intuition:**
- **Count** — reaching the end is *one* way, so return `1`. Then add up the ways from each choice.
- **Min / Max** — at the end there is *nothing left* to pay or gain, so return `0`. Each step adds its own cost or gain on the way back up.
- **Possible** — reaching the end means *it worked*, so return `True`. One working choice is enough.

---

## The dead end returns whatever the combine ignores

| Combine | Ignores | So a dead end returns |
|---|---|---|
| `+` | `0` | `0` |
| `min` | `inf` | `inf` |
| `max` | `-inf` | `-inf` |
| `or` | `False` | `False` |

**Why it matters:** in Coin Change, overshooting must return `inf`. If it returned `0`, `min` would pick the dead end as the "best" answer.

**House Robber can use `0`** because "skip" is always allowed, so there's no real dead end.

---

## The end base isn't always 0

The real rule: **return what it costs to finish from here.**

```python
# Edit Distance: word1 is used up, but word2 still has characters left
if i == len(word1):
    return len(word2) - j      # you still have to insert them
```

Most of the time that cost is `0`, but not always.

---

## `or` vs `and`

- **`or` joins choices.** One working option is enough.
- **`and` joins requirements.** Every part of one option must hold.

```python
dp(state) = (condition_1 and dp(next_1)) or (condition_2 and dp(next_2))
#            one option: ALL needed          another option
```

Interleaving String:

```python
match_s1 = (i < len(s1) and s1[i] == s3[i + j]) and dp(i + 1, j)
match_s2 = (j < len(s2) and s2[j] == s3[i + j]) and dp(i, j + 1)
return match_s1 or match_s2
```

**Use `and` to:**
- **Guard a move:** only recurse if this step is legal (`s1[i] == s3[i + j] and dp(...)`).
- **Check bounds first:** `i < len(s1) and s1[i] == ...` so you never index past the end.
- **Need every piece:** a palindrome needs matching ends **and** a palindrome inside.

**Put the cheap check first.** `and` stops at the first `False`, so the recursion only runs when the check passes.

**Say it out loud:** "this **or** that" → `or`. "this **and** that" → `and`.

---

## `or` / `and` when counting

| Yes/no | Count | Meaning |
|---|---|---|
| `or` | `+` | separate choices: add the ways |
| `and` | `×` | independent parts, all needed: multiply the ways |

Pick + skip in Coin Change II → `+`. A left part with 3 ways and a right part with 4 ways → `3 × 4 = 12` (Unique BSTs, LC 96).

---

## Pick: stay or move on?

| Can an item be reused? | On a pick, go to | Example |
|---|---|---|
| **Yes** (unbounded) | stay on `i` | Coin Change I & II: `dp(i, sum + coins[i])` |
| **No** (0/1) | `i + 1` | Partition, Target Sum: `dp(i + 1, sum + nums[i])` |

Skip always moves to `i + 1`.

---

## Combinations vs permutations (count problems)

- **Index `i` in the state** (pick / skip, go through items in order) → **combinations**. `[1, 2]` and `[2, 1]` count **once**. *Coin Change II.*
- **No index** (try every item at every step) → **permutations**. `[1, 2]` and `[2, 1]` count **twice**. *Combination Sum IV, LC 377.*

Same base cases, different answer. Read the question carefully.

---

## Where is the answer?

| The best answer... | Return |
|---|---|
| starts at the beginning | `dp(0)` or `dp(0, 0)` |
| can start or end at **any** cell | call `dp` on every cell and keep the max |

Any-cell examples: Maximal Square, Longest Increasing Path, the two palindrome problems.

---

## Time and space: it's not always O(n)

> **Time = (number of states) × (work per state)**
> **Space = (number of states, for the memo) + (recursion depth)**

The **number of states** is how many different keys your memo can hold. Look at what goes into the key.

| Memo key | States | Work per state | Time | Space | Examples |
|---|---|---|---|---|---|
| `dp(i)` | `n` | O(1) | **O(n)** | O(n) | Climbing Stairs, House Robber, Decode Ways |
| `dp(i)` with a loop inside | `n` | O(words × word length) | **O(n · m · k)** | O(n) | Word Break |
| `dp(i, j)` over two strings | `m × n` | O(1) | **O(m × n)** | O(m × n) | LCS, Edit Distance, Distinct Subsequences |
| `dp(r, c)` over a grid | `m × n` | O(1) | **O(m × n)** | O(m × n) | Unique Paths, Maximal Square, Longest Increasing Path |
| `dp(i, current_sum)` | `n × amount` | O(1) | **O(n × amount)** | O(n × amount) | Coin Change I & II, Partition, Target Sum |
| `dp(idx, prev_idx)` | `n × n` | O(1) | **O(n²)** | O(n²) | LIS |
| `dp(i, j)` + loop over a split `k` | `n²` | O(n) | **O(n³)** | O(n²) | Burst Balloons |

**Work it out in 4 steps:**
1. **Count the key's parts.** One index → about `n` states. Two indexes → `n × m`. Index + running sum → `n × target`.
2. **Look inside the function.** No loop → O(1) per state. A loop over `k` choices → O(k) per state.
3. **Multiply** them → time.
4. **Space** = the memo (every state) + the recursion stack (usually `n` deep, or `m + n` for two strings).

**Remember:**
- **Memo and table have the same time.** The table can save space: if a row only reads the row before it, keep one row (Edit Distance O(m × n) → O(n); House Robber O(n) → O(1)).
- **A running sum in the key is expensive.** Coin Change with `amount = 10,000` and 12 coins is 120,000 states, even though the input is only 12 numbers.

**O(n) only when the key is one index and the function has no loop.**

---

## 10-second recall

- **Count:** `1` / `0` / `+`. **Min:** `0` / `inf` / `min`. **Max:** `0` / `-inf` / `max`. **Possible:** `True` / `False` / `or`.
- A dead end returns what the combine ignores.
- `or` = choices, `and` = requirements (`+` and `×` when counting).
- Reuse → stay on `i`; use once → `i + 1`.
- Index in the state → combinations; no index → permutations.
- Time = states × work per state; space = states + recursion depth.
