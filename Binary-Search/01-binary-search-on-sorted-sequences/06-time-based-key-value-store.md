# 981. Time Based Key-Value Store

**LC 981** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Boundary search over timestamps (floor lookup)

---

## 1. Intuition

`set` calls for a given key always arrive with strictly increasing timestamps, so `self.store[key]` is a sorted list "for free" just by appending. `get(key, timestamp)` then just needs "the latest value recorded at or before `timestamp`" — a floor lookup, done with binary search.

- `values[mid][0] <= timestamp` → this timestamp is a valid candidate, so remember it (`res = values[mid][1]`) and keep looking right (`left = mid + 1`) for an even later valid one.
- `values[mid][0] > timestamp` → too far in the future, discard it and look left (`right = mid - 1`).
- `res` starts at `""` and is only overwritten when a valid candidate is found — so "never updated" and "key/timestamp not found" naturally both resolve to `""`.
- This is the same "record + keep pushing" trick as [#3 Find First and Last Position](03-find-first-and-last-position-of-element-in-sorted-array.md), just biased toward the last valid value instead of a duplicate run.

**Recall:** `set` = append (order is free); `get` = binary search for the floor, recording the best match as you push right.

## 2. Approach

* **Idea:** `set` is `O(1)` append into a hashmap of lists; `get` is exact-match-style binary search (Form 1) per key, where "match" means "`<= timestamp`" rather than "`== target`".
* **Data structure / pointers:** `self.store` is a `dict[str, list[tuple[int, str]]]`, one sorted-by-timestamp list per key; `left`/`right` bound the search within that one key's list; `res` holds the best value found so far.
* **Invariant:** every time `values[mid][0] <= timestamp`, `res` is updated to the most recent such value seen; the loop keeps pushing `left` right to see if a later valid timestamp beats it.
* **Edge cases:**
  - Key never `set` → `self.store.get(key, [])` is `[]`, loop never runs, returns `""`.
  - `timestamp` before the earliest recorded value → every candidate fails the `<=` check, `res` stays `""`.
  - Exact timestamp match → updates `res` immediately; since timestamps are strictly increasing per key, no duplicate-timestamp ambiguity is possible.

## 3. Code

```python
from collections import defaultdict


class TimeMap:

    def __init__(self):
        # Map each key to a list of (timestamp, value) tuples
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # Appending preserves strictly increasing timestamp order
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        res = ""
        values = self.store.get(key, [])
        left, right = 0, len(values) - 1

        while left <= right:
            mid = (left + right) // 2

            # Valid candidate: record value and look for a larger timestamp <= target
            if values[mid][0] <= timestamp:
                res = values[mid][1]
                left = mid + 1
            else:
                right = mid - 1

        return res


# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
```

## 4. Dry Run

```
set("foo", "bar", 1)    -> store["foo"] = [(1, "bar")]
get("foo", 1)           -> mid=0: 1<=1, res="bar", left=1 -> ends, return "bar"
get("foo", 3)           -> mid=0: 1<=3, res="bar", left=1 -> ends, return "bar"
set("foo", "bar2", 4)   -> store["foo"] = [(1, "bar"), (4, "bar2")]
get("foo", 4)           -> mid=0: 1<=4, res="bar", left=1
                            mid=1: 4<=4, res="bar2", left=2 -> ends, return "bar2"
get("foo", 5)           -> mid=0: 1<=5, res="bar", left=1
                            mid=1: 4<=5, res="bar2", left=2 -> ends, return "bar2"
```

## 5. Complexity

* **Time:** `set` is `O(1)` (amortized list append). `get` is `O(log K)`, where `K` is the number of timestamps recorded for that key.
* **Space:** `O(N)` total, where `N` is the number of `set` calls across all keys — every `set` adds one tuple.

## 6. Recall (30 seconds)

- Strictly increasing timestamps per key means appending already gives you a sorted list — no extra sorting needed.
- `get` is a floor lookup: binary search where a hit means "keep looking for something later," not "stop."
- `res = ""` as the default handles both "unknown key" and "timestamp before anything recorded" with no special-casing.
