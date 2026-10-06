# 994. Rotting Oranges

**LC 994** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Multi-source BFS, level by level (one level = one minute)

---

## 1. Intuition

Every rotten orange infects its fresh neighbours each minute, all at the same time. That's a multi-source BFS
where each **BFS level is one minute**. Keep a count of fresh oranges. When it reaches 0 you have the
answer. If the rot can't spread any further and some fresh oranges are left, they can never rot.

* **All rotten oranges start together:** step 1 pushes every `(i, j)` with `grid[i][j] == 2`. That's minute 0 for all of them.
* **`fresh_count` is the finish line:** it's counted once at the start and drops by 1 each time `grid[nr][nc] = 2` rots an orange. At the end, `fresh_count == 0` decides between `time` and `-1`.
* **One loop pass = one minute:** `for _ in range(len(queue))` pops only the oranges that were rotten *at the start* of this minute. Oranges rotted during this minute are pushed and wait for the next pass.
* **No off-by-one:** `while queue and fresh_count > 0` stops as soon as the last fresh orange rots. That way `time` isn't increased for an extra "empty" minute that would only pop the last oranges and find nothing.

**Recall:** Push all `2`s and count the `1`s. Each level is `time += 1`, rotting the neighbours with `fresh_count -= 1`. Return `time` if `fresh_count == 0`, otherwise `-1`.

## 2. Approach

* **Idea:** Multi-source BFS from every rotten orange, done level by level so the number of levels is the number of minutes.
* **Graph representation:** implicit **grid** graph, undirected and unweighted. Moves go in **4 directions**, from `directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]` (down, up, right, left). Empty cells (`0`) block the spread.
* **Data structure / pointers:**
  * `queue` (`deque`): the oranges that will spread rot in the next minute. The `len(queue)` snapshot is taken at the start of each pass and marks where one minute ends and the next begins.
  * `fresh_count`: the number of oranges still fresh.
  * `time`: the number of minutes that have passed (completed BFS levels).
  * `grid` is the visited marker: setting a cell from `1` to `2` marks it **when it is pushed**, so an orange is rotted and queued only once.
  * Out-of-bounds is checked with `0 <= nr < rows and 0 <= nc < columns` before `grid[nr][nc]` is read.
* **Invariant:** at the start of pass number `time + 1`, `queue` holds exactly the oranges that went rotten at minute `time`, and every orange within `time` steps of a starting rotten orange is already rotten.
* **Edge cases:**
  * No fresh oranges at the start (including a grid of only `0`s, or only `2`s): `fresh_count > 0` fails right away, so it returns `0`.
  * No rotten oranges but some fresh ones: `queue` is empty, the loop never runs, and `fresh_count > 0`, so it returns `-1`.
  * A fresh orange cut off by empty cells or the edge: the queue runs empty while `fresh_count > 0`, so it returns `-1`.
  * A 1×1 grid: `[[0]]` → 0, `[[2]]` → 0, `[[1]]` → -1.
  * An empty grid isn't possible (LC guarantees `m, n ≥ 1`). With `[]`, `grid[0]` would raise `IndexError`.
  * It changes `grid` in place (fresh oranges become `2`). It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import deque


class Solution:

    def orangesRotting(self, grid: list[list[int]]) -> int:
        rows = len(grid)
        columns = len(grid[0])

        fresh_count = 0
        queue = deque()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Step 1: Collect all rotten oranges in the queue and count fresh ones
        for i in range(rows):
            for j in range(columns):
                if grid[i][j] == 2:
                    queue.append((i, j))
                elif grid[i][j] == 1:
                    fresh_count += 1

        time = 0

        # Step 2: Level-by-level Multi-Source BFS
        # Process level-by-level while there are rotten oranges and fresh oranges left
        while queue and fresh_count > 0:
            time += 1

            # Process all rotten oranges for the current minute level
            for _ in range(len(queue)):
                r, c = queue.popleft()

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc

                    # If adjacent cell is within bounds and contains a fresh orange
                    if (
                        0 <= nr < rows
                        and 0 <= nc < columns
                        and grid[nr][nc] == 1
                    ):
                        grid[nr][nc] = 2  # Rot the fresh orange
                        fresh_count -= 1  # Decrement fresh orange count
                        queue.append((nr, nc))  # Enqueue for next minute level

        # If fresh oranges remain that couldn't be reached, return -1
        return time if fresh_count == 0 else -1
```

## 4. Dry Run

Input (LC Example 1):

```text
r0:  2  1  1
r1:  1  1  0
r2:  0  1  1
```

Start: `queue = [(0,0)]`, `fresh_count = 6`, `time = 0`. Neighbours are tried in the order **down, up, right, left**.

| Minute (`time`) | Pops this pass | Rotted (`1` → `2`), in order | `fresh_count` | `queue` after the pass |
| --- | --- | --- | --- | --- |
| 1 | `(0,0)` | `(1,0)` (down), `(0,1)` (right) | 4 | `(1,0) (0,1)` |
| 2 | `(1,0)`, `(0,1)` | `(1,1)` (right of `(1,0)`), `(0,2)` (right of `(0,1)`) | 2 | `(1,1) (0,2)` |
| 3 | `(1,1)`, `(0,2)` | `(2,1)` (down from `(1,1)`). `(0,2)` has no fresh neighbours | 1 | `(2,1)` |
| 4 | `(2,1)` | `(2,2)` (right) | 0 | `(2,2)` |
| — | loop stops because `fresh_count == 0` (`(2,2)` is never popped) | — | 0 | — |

Returns **`time = 4`**.

## 5. Complexity

* **Time: O(rows × columns)**
  Think of it as: each orange is pushed and popped at most once. The starting rotten oranges go in during the first scan, and each fresh orange goes in only at the moment it changes from `1` to `2`, which can happen only once. Each pop checks 4 neighbours, a fixed amount of work. So the first scan plus the BFS together grow with the number of cells.
* **Space: O(rows × columns)**
  Think of it as: the only extra memory is `queue`. In the worst case (for example, a grid that is all rotten oranges at the start), it holds nearly every cell at once. There's no separate visited set, because changing `1` to `2` in `grid` does that job.

## 6. Recall (30 seconds)

* Multi-source BFS from all the `2`s. **`for _ in range(len(queue))` = one minute**, and `time += 1` once per pass.
* Count `fresh_count` first and decrease it each time you rot an orange. The loop runs `while queue and fresh_count > 0`, so there's no extra minute at the end.
* Return `time` if `fresh_count == 0`, otherwise `-1`. O(R·C) time and O(R·C) queue.
