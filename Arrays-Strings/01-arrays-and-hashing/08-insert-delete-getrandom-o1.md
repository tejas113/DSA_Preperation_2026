# 380. Insert Delete GetRandom O(1)

**LC 380** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Hash map + array, remove by overwriting with the last element

---

## 1. Intuition

You need three things in `O(1)`: add, delete, and pick a random element. A hash set is fast at the first
two but cannot pick a random one. A list can pick a random one by index, but deleting from the middle
shifts everything (`O(n)`). So use both: the list holds the values, and a dict remembers each value's
position in the list. To delete, don't shift — copy the last element into the hole and pop the end.

* `self.nums` is the list of values. `random.choice(self.nums)` picks by index, so every element is equally likely.
* `self.numMap[val] = len(self.nums)` records where `val` will sit *before* `append` puts it at the end.
* `if val in self.numMap` answers "is it already there?" in `O(1)`, for both `insert` and `remove`.
* `self.nums[idx] = last_val` fills the hole left by `val` with the last element, so nothing shifts.
* `self.numMap[last_val] = idx` fixes the moved element's recorded position.
* `self.nums.pop()` then drops the now-duplicate last slot, and `del self.numMap[val]` forgets the removed value.

**Recall:** list for random pick, dict for value → index; delete by copying the last element into the hole, then `pop()`.

---

## 2. Approach

* **Idea:** keep a list (fast random access, fast append/pop at the end) and a dict (fast lookup, and the index of each value in the list). Removal moves the last element into the removed slot so the list stays packed.
* **Data structure / pointers:** `nums` is the list of current values. `numMap` maps value → its index in `nums`. `idx` is the slot being freed, and `last_val` is the element that fills it.
* **Invariant:** `nums` holds each value exactly once, and for every value `v` in `numMap`, `nums[numMap[v]] == v`. Because each value appears once, `random.choice` is uniform.
* **Edge cases:**
  * `insert` of a value already present → `False`, and nothing changes.
  * `remove` of a value that is not present → `False`.
  * Removing the last element itself (`val == last_val`) → still correct: it copies itself to its own slot, then `pop()` and `del` remove it.
  * Removing the only element → both `nums` and `numMap` end up empty.
  * Re-inserting a value after removing it → works, it is appended at the end again.
  * `getRandom` on an empty set would raise an error; the problem guarantees there is at least one element when it is called.

---

## 3. Code

```python
import random

class RandomizedSet:

    def __init__(self):
        self.numMap = {}
        self.nums = []

    def insert(self, val: int) -> bool:
        if val in self.numMap:
            return False

        self.numMap[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.numMap:
            return False

        last_val = self.nums[-1]
        idx = self.numMap[val]
        
        # Swap target element with last element
        self.nums[idx] = last_val
        self.numMap[last_val] = idx
        
        # Remove target element
        self.nums.pop()
        del self.numMap[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)


if __name__ == "__main__":
    def check_invariant(rs: RandomizedSet) -> None:
        assert len(rs.nums) == len(rs.numMap)
        for value, index in rs.numMap.items():
            assert rs.nums[index] == value

    # Example from the problem statement
    rs = RandomizedSet()
    assert rs.insert(1) is True
    assert rs.remove(2) is False
    assert rs.insert(2) is True
    assert rs.getRandom() in (1, 2)
    assert rs.remove(1) is True
    assert rs.insert(2) is False
    assert rs.getRandom() == 2
    check_invariant(rs)

    # Remove from the middle, then the last element, then the only element
    rs = RandomizedSet()
    for value in (10, 20, 30):
        assert rs.insert(value) is True
    assert rs.remove(10) is True
    assert rs.nums == [30, 20] and rs.numMap == {20: 1, 30: 0}
    check_invariant(rs)
    assert rs.remove(20) is True
    check_invariant(rs)
    assert rs.remove(30) is True
    assert rs.nums == [] and rs.numMap == {}
    assert rs.insert(30) is True
    check_invariant(rs)

    print("All tests passed")
```

---

## 4. Dry Run

`remove(10)` when `nums = [10, 20, 30]` and `numMap = {10: 0, 20: 1, 30: 2}`. Here `idx = 0` and `last_val = 30`.

| Step | Operation | `self.nums` | `self.numMap` |
| --- | --- | --- | --- |
| **Start** | before removing `10` | `[10, 20, 30]` | `{10: 0, 20: 1, 30: 2}` |
| **1** | `self.nums[idx] = last_val` (copy `30` into slot `0`) | `[30, 20, 30]` | `{10: 0, 20: 1, 30: 2}` |
| **2** | `self.numMap[last_val] = idx` (`30` now lives at `0`) | `[30, 20, 30]` | `{10: 0, 20: 1, 30: 0}` |
| **3** | `self.nums.pop()` and `del self.numMap[10]` | `[30, 20]` | `{20: 1, 30: 0}` |

**Return:** `True`

---

## 5. Complexity

* **Time:** `O(1)` average for `insert`, `remove` and `getRandom` — each is a few dict lookups and list operations at the end or at a known index; `random.choice` picks by index. Nothing shifts, because `remove` overwrites and then `pop()`s.
* **Space:** `O(n)` — `nums` and `numMap` each hold the `n` current values.

---

## 6. Recall (30 seconds)

* **Two structures:** list `nums` for random pick by index, dict `numMap` for value → index.
* **Removal:** copy the last element into the removed slot → update its index in `numMap` → `pop()` the list → `del` the key.
* **Last-element case:** works when `val == last_val`, because `numMap[last_val] = idx` runs before the `del`.
