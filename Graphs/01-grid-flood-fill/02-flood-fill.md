# Flood Fill  ·  LeetCode 733  ·  Easy

Group 01 — Grid Flood-Fill  ·  the simplest member of the pattern. One flood, no
outer loop. This is the "paint bucket" tool in an image editor.

Prereqs: `concepts/02` (grid as a graph), `concepts/04` (DFS on a grid). Nothing
new — this is Number of Islands with the outer loop removed.

---

## 1. Problem

You are given an image as an `m x n` grid of integers, where `image[r][c]` is the
color of that pixel. You are also given a starting pixel `(sr, sc)` and a new
`color`.

**Flood fill:** starting from `(sr, sc)`, change the color of that pixel and every
pixel **4-directionally connected** to it that has the **same original color** as
`(sr, sc)`. Then keep spreading from the newly-colored pixels. Return the modified
image.

Constraints:
- `1 <= m, n <= 50`.
- `0 <= image[r][c], color < 2^16`.
- `0 <= sr < m`, `0 <= sc < n` (the start pixel is always valid).

Example 1:

```
image = [[1,1,1],
         [1,1,0],
         [1,0,1]]
sr = 1, sc = 1, color = 2

start pixel (1,1) has color 1. Recolor every 1 connected to it → 2.

result = [[2,2,2],
          [2,2,0],
          [2,0,1]]
```

The bottom-right `1` at `(2,2)` stays `1` — it's walled off by `0`s, so it is not
connected to `(1,1)` through same-colored pixels.

Example 2 (the tricky one):

```
image = [[0,0,0],
         [0,0,0]]
sr = 0, sc = 0, color = 0

start color is already 0. Nothing changes. result = [[0,0,0],[0,0,0]]
```

---

## 2. Explain Like I'm 5

You have a coloring book page. You dip your paintbrush in **blue** and touch one
square. That square was **white**. So you paint it blue, and then paint every
white square touching it blue, and every white square touching *those* blue, and
so on — but you stop at any square that was already a different color (say red);
you don't cross those.

One special rule: if you dip in **white** paint and touch a square that is
**already white**, just... don't. There's nothing to do, and if you tried to
"spread white onto white forever" you'd never stop. That's Example 2.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| 2D grid of colors/values | ✅ |
| "starting from this cell, spread to connected same-value cells" | ✅ |
| Only **one** starting point, no "count the groups" | ✅ → **no outer loop** |
| You **modify** cells as you go | ✅ → the recolor doubles as the "visited" mark |
| No shortest-path / distance ask | ✅ plain flood |

**Reduce it to:** *"Single-source flood fill on a grid; the target test is `cell ==
start_color`, and writing `color` is what marks a cell done."*

**Look-alikes:**
- Number of Islands — same flood, but wrapped in a loop over all cells to *count*
  regions. Flood Fill has **no** loop; you're given the start.
- Surrounded Regions — flood, but seeded from the border.
- Word Search — grid DFS, but you **un-mark** on the way back (backtracking).
  Flood Fill never un-marks.

---

## 4. Intuition

1. The start pixel has some `start_color`. Every pixel we recolor must currently
   equal `start_color`.
2. When we set a pixel to the new `color`, it **no longer equals `start_color`**.
   So if we ever revisit it, the test `image[r][c] == start_color` is now `False`
   and we stop. **The recolor is the visited mark** — we don't need a separate
   `visited` set.
3. Wait — that only works if `color != start_color`. If they're equal, recoloring
   changes nothing, the test never turns `False`, and DFS loops forever. So: if
   `start_color == color`, return immediately.
4. Read `start_color` **once, before** we recolor anything. The moment we write to
   `image[sr][sc]`, reading it again would give the wrong original color.

That's the whole problem: flood from one seed, recolor = visited, and the one-line
guard for the equal-color case.

---

## 5. Approach (primary): DFS

1. `m, n = len(image), len(image[0])`.
2. `start_color = image[sr][sc]` — capture it now.
3. If `start_color == color`: return `image` unchanged (guard).
4. Define `dfs(r, c)`:
   - Off the board → return.
   - `image[r][c] != start_color` → return (wrong color, or already recolored).
   - `image[r][c] = color`.
   - Recurse into all 4 neighbors.
5. Call `dfs(sr, sc)`.
6. Return `image`.

Builds on: `concepts/04` grid-DFS template.

---

## 6. Pseudocode

```
function floodFill(image, sr, sc, color):
    m, n = rows, cols
    start = image[sr][sc]
    if start == color: return image          # guard: nothing to do / avoid infinite loop

    function dfs(r, c):
        if r,c off board: return
        if image[r][c] != start: return
        image[r][c] = color
        dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)

    dfs(sr, sc)
    return image
```

---

## 7. Dry Run

```
image = [[1,1,1],
         [1,1,0],
         [1,0,1]]
sr=1, sc=1, color=2
start_color = image[1][1] = 1     (1 != 2, so we proceed)
```

Trace `dfs`, showing the image after each recolor:

| call | image[r][c] | == start(1)? | action | image now |
|---|---|---|---|---|
| dfs(1,1) | 1 | yes | set (1,1)=2 | row1 = [1,2,0] |
| dfs(2,1) | 0 | no | return | — |
| dfs(0,1) | 1 | yes | set (0,1)=2 | row0 = [1,2,1] |
| ↳ dfs(1,1) | 2 | no (already recolored) | return | — |
| ↳ dfs(-1,1) | off board | — | return | — |
| ↳ dfs(0,2) | 1 | yes | set (0,2)=2 | row0 = [1,2,2] |
| ↳↳ dfs(1,2) | 0 | no | return | — |
| ↳↳ dfs(0,1) | 2 | no | return | — |
| ↳ dfs(0,0) | 1 | yes | set (0,0)=2 | row0 = [2,2,2] |
| ↳↳ dfs(1,0) | 1 | yes | set (1,0)=2 | row1 = [2,2,0] |
| ↳↳↳ dfs(2,0) | 1 | yes | set (2,0)=2 | row2 = [2,0,1] |
| ↳↳↳ (its neighbors: (2,1)=0, (1,0)=2, off board) | — | — | return | — |
| back up: dfs(1,2) from dfs(1,1) | 0 | no | return | — |
| dfs(1,0) from dfs(1,1) | 2 | no | return | — |

Final image:

```
[[2,2,2],
 [2,2,0],
 [2,0,1]]
```

`(2,2)` was never reached — `1`, but cut off by `0`s. ✅

---

## 8. Python Code (primary — DFS)

```python
from typing import List


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int,
                  color: int) -> List[List[int]]:
        m, n = len(image), len(image[0])
        start_color = image[sr][sc]

        if start_color == color:            # nothing to do; also avoids infinite recursion
            return image

        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

        def dfs(r: int, c: int) -> None:
            if not (0 <= r < m and 0 <= c < n):     # off the board
                return
            if image[r][c] != start_color:          # wrong color OR already recolored
                return
            image[r][c] = color                     # recolor == mark visited
            for dr, dc in DIRS:
                dfs(r + dr, c + dc)

        dfs(sr, sc)
        return image


if __name__ == "__main__":
    sol = Solution()

    assert sol.floodFill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2) == \
        [[2, 2, 2], [2, 2, 0], [2, 0, 1]]

    # start color already equals target -> unchanged (the infinite-loop guard)
    assert sol.floodFill([[0, 0, 0], [0, 0, 0]], 0, 0, 0) == [[0, 0, 0], [0, 0, 0]]

    # single pixel
    assert sol.floodFill([[5]], 0, 0, 9) == [[9]]

    # isolated start pixel (neighbors differ)
    assert sol.floodFill([[1, 2, 1], [2, 1, 2], [1, 2, 1]], 1, 1, 7) == \
        [[1, 2, 1], [2, 7, 2], [1, 2, 1]]

    # whole grid one color -> all recolored
    assert sol.floodFill([[3, 3], [3, 3]], 0, 0, 4) == [[4, 4], [4, 4]]

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. BFS (use when recursion depth could blow — big single-color image)

```python
from collections import deque
from typing import List


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int,
                  color: int) -> List[List[int]]:
        m, n = len(image), len(image[0])
        start_color = image[sr][sc]
        if start_color == color:
            return image

        DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
        q = deque([(sr, sc)])
        image[sr][sc] = color                       # recolor on enqueue

        while q:
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and image[nr][nc] == start_color:
                    image[nr][nc] = color
                    q.append((nr, nc))
        return image
```

### The BFS↔DFS answer the interviewer wants

> "Both are `O(m*n)` time and `O(m*n)` space, visiting each pixel of the connected
> region once. The recolor itself is the visited mark, so neither needs an extra
> `visited` set. DFS is shorter; BFS avoids Python's recursion limit if the region
> could be ~10^6 pixels. I'd pick DFS and mention the switch."

### 9b. Iterative DFS (explicit stack) — same shape as BFS but `pop()` from the end

```python
stack = [(sr, sc)]
image[sr][sc] = color
while stack:
    r, c = stack.pop()
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < m and 0 <= nc < n and image[nr][nc] == start_color:
            image[nr][nc] = color
            stack.append((nr, nc))
```

---

## 10. Complexity — derived step by step

**V and E:** node = a pixel, `V = m * n`. Edge = adjacency between 4-neighbor
pixels, `E ≈ 2mn = O(m*n)`.

**Time:**
- The guard and setup are `O(1)` (plus `O(1)` to read `start_color`).
- `dfs`/BFS touches each pixel of the connected region **once** — the `!=
  start_color` test stops repeats, because a recolored pixel no longer matches.
- Worst case the whole image is one color → all `m*n` pixels visited, each doing
  `O(1)` work + 4 child calls → `O(m*n)`.
- **Total: `O(m * n)`** (`= O(V + E)`; more tightly `O(size of the region)`).

**Space:**
- No `visited` set — the image *is* the visited structure. `O(1)` extra there.
- Recursion stack (DFS) / queue (BFS): worst case a snake-shaped single-color
  region → `O(m*n)`.
- Output: we return the same `image` object, no copy → `O(1)` if not counted.
- **Total: `O(m * n)`** worst case, from the call stack / queue alone.

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `start_color == color` | the guard → return immediately (without it: `RecursionError` / TLE) |
| Single-pixel image `[[x]]` | `dfs(0,0)` recolors it, all neighbors off-board |
| Start pixel isolated (all neighbors differ) | only `(sr,sc)` changes |
| Whole grid same color | entire grid recolored |
| Region split by other colors | only the connected part changes |
| `color` is a value already elsewhere in the grid (e.g. `2` exists) | fine — we only ever compare against `start_color`, never against `color` |
| Start pixel on an edge/corner | bounds check handles missing neighbors |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Missing the `start_color == color` guard.** The #1 bug. Symptom:
      `RecursionError: maximum recursion depth exceeded` or "Time Limit Exceeded".
      Because recoloring to the same color never makes the match test `False`.
- [ ] **Reading `start_color` too late** — after `dfs` has already changed
      `image[sr][sc]`. Capture it in a local variable *before* calling `dfs`.
- [ ] **Comparing against `color` instead of `start_color`** in the match test.
      Fills the wrong pixels (or nothing).
- [ ] **Bounds check after indexing** `image[r][c]` → `IndexError`, or `image[-1]`
      wraps to the last row (silent wrong answer).
- [ ] **Adding a `visited` set and forgetting to also check the color** — then a
      neighboring different-colored pixel gets recolored because "it wasn't
      visited". You need `image[r][c] == start_color`, not just "unvisited".
- [ ] Returning `None` instead of `image` (the flood mutates in place, but the
      function must still `return image`).

**Narrate to the interviewer:** "It's hanging on the all-zeros test with
`color = 0`. That means the recursion never terminates — the base case
`image[r][c] != start_color` can never become true when I'm painting the color
onto itself. I need an early return when `start_color == color`."

---

## 13. Learnings & Transfer

**Reusable ideas from this problem:**
1. **Mutation-as-visited-mark.** When the write you perform makes a cell stop
   matching the target test, you don't need a separate `visited` set. (Only valid
   when the new value ≠ the matched value — hence the guard.)
2. **Capture the key value before you start mutating.** A discipline that recurs in
   in-place matrix problems, linked-list reversal, Game of Life, "rotate image".
3. **Guard against the self-referential no-op** that turns a loop infinite. General
   defensive habit: "what if the new state equals the old state?"
4. **Single-source flood vs loop-and-flood.** You're handed the seed → no outer
   loop. Recognize which one the problem needs.

| Problem | How this transfers |
|---|---|
| Number of Islands | same flood + an outer loop to count regions |
| Max Area of Island | same flood, returns a size instead of `None` |
| Surrounded Regions | flood, but seeded from the border; two-color logic |
| Rotting Oranges / 01 Matrix | grid flood becomes multi-source BFS for distances |
| Word Search | grid DFS but you **un-mark** cells on the way back (backtracking) — contrast with flood fill which never un-marks |
| Game of Life | "capture before mutate" — use a temp encoding to read old + write new |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Build the paint-bucket tool for our image editor, but add a **tolerance** slider: fill pixels whose color is within distance `t` of the clicked pixel's original color, not exactly equal."

- **(b) Pattern:** still single-source grid flood — only the *match test* changes.
- **(c) Adapt:** replace `image[r][c] == start_color` with
  `abs(image[r][c] - start_color) <= t`. **But** the mutation-as-visited trick now
  breaks: after recoloring, a pixel might *still* be within `t` of a neighbor's
  original color, causing re-visits or infinite loops. So **reintroduce an explicit
  `visited` set** and test `(r, c) not in visited and abs(...) <= t`. Compare each
  pixel to the *original* `start_color`, using a copy of the row if you're worried
  about read-after-write.
- **(d) Say:** "When the write no longer guarantees the match test flips to false,
  you must bring back an explicit visited set."

### Scenario 2 — "The image is 100,000 × 100,000. A fill could touch billions of pixels. Make it not crash and not hang the UI."

- **(b) Pattern:** same flood; the concerns are recursion depth and responsiveness.
- **(c) Adapt:** (1) use **iterative BFS/stack** — no recursion limit. (2) Process
  in **chunks**: pop a bounded number of pixels per animation frame, yield control,
  resume — a coroutine/generator. (3) If pixels live on disk in tiles, flood
  tile-by-tile, queueing cross-tile boundary pixels. Complexity stays `O(region
  size)` but memory for the frontier can be capped with a scanline approach.
- **(d) Say:** "Huge floods become iterative + incremental (frame-budgeted) + tiled
  along memory boundaries."

### Scenario 3 — "The fill must be **undoable**. After a fill, the user can press Ctrl+Z to restore exactly what was there."

- **(b) Pattern:** flood + **record the diff** during traversal.
- **(c) Adapt:** `dfs` appends `(r, c)` to a `changed` list right before recoloring
  (all had `start_color`). Undo = set every listed cell back to `start_color`.
  Store `(start_color, color, changed)` on the undo stack. Memory `O(region size)`.
- **(d) Say:** "Reversible mutations: collect the change-set during the traversal;
  the inverse operation replays it backward."

### Scenario 4 — "A user rapidly clicks 200 times. Keep the editor at 60 fps."

- **(b) Pattern:** many independent single-source floods.
- **(c) Adapt:** each fill is `O(region)`; total is the sum of region sizes, which
  can't be avoided if all regions are distinct. Optimizations: (1) **coalesce**
  clicks landing in a region that a queued fill will already recolor — check a
  pending map. (2) Run fills on a worker thread, double-buffer the image. (3) If
  many clicks hit the *same* region with the *same* color, dedupe to one.
- **(d) Say:** "Batch of point operations → dedupe overlapping work, move off the
  UI thread, double-buffer."

### Scenario 5 — "Only perform the fill if the clicked region is **fully enclosed** — it must not touch the image border. Otherwise do nothing."

- **(b) Pattern:** flood + a **border-touch flag** — a mini version of Surrounded
  Regions (Group 03).
- **(c) Adapt:** during the flood, collect all region cells into a list and set
  `touches_border = True` if any cell has `r in (0, m-1)` or `c in (0, n-1)`. After
  the flood: if `touches_border`, do nothing (don't recolor — or roll back using
  the collected list); else recolor all collected cells.
- **(d) Say:** "‘Only if not touching the boundary’ = flood to gather the region,
  check any cell against the border, then commit or abort."

### Scenario 6 — "The canvas is a sphere: the left edge connects to the right edge, and the top row to the bottom row (a torus). Flood fill on that."

- **(b) Pattern:** same flood, **wrapped neighbor function**.
- **(c) Adapt:** neighbors become `((r + dr) % m, (c + dc) % n)` and you **drop the
  bounds check** entirely (every index is valid after the modulo). Everything else
  is identical. Complexity unchanged, `O(m*n)`.
- **(d) Say:** "Wrapped/toroidal grids: replace bounds-checking with modular
  arithmetic in the neighbor generator; the traversal is untouched."

---

## 15. Flashcards

**Q:** What makes Flood Fill the *simplest* member of Group 01?
**A:** You're given the seed pixel → **no outer loop**. It's just one flood.

**Q:** Why doesn't Flood Fill need a `visited` set?
**A:** Recoloring a pixel to `color` makes it stop matching `start_color`, so the
match test `image[r][c] == start_color` doubles as the visited check.

**Q:** The #1 bug in Flood Fill, and its symptom?
**A:** Forgetting the `start_color == color` guard → infinite recursion
(`RecursionError` / TLE), because painting a color onto itself never ends.

**Q:** Why capture `start_color` before calling `dfs`?
**A:** The first recolor changes `image[sr][sc]`; reading it later gives the wrong
original color.

**Q:** Time and space?
**A:** `O(m*n)` time (each region pixel visited once), `O(m*n)` space worst case
for the recursion stack / BFS queue. No extra visited structure.

**Q:** Tolerance version ("fill colors within `t`") — what breaks and how to fix?
**A:** Mutation no longer guarantees the match test flips false → reintroduce an
explicit `visited` set; compare to the *original* start color.

**Q:** How does Flood Fill relate to Number of Islands?
**A:** Same grid flood. Number of Islands wraps it in a loop over all cells to
count regions; Flood Fill has no loop.

**Q:** Contrast Flood Fill with Word Search's grid DFS.
**A:** Flood Fill never un-marks a cell. Word Search **un-marks** on the way back
(backtracking) so cells can be reused by other paths.

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. Recursive DFS, `O(m*n)` time and space — matches
the primary solution.

```python
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int,
                  color: int) -> List[List[int]]:

        rows = len(image)
        columns = len(image[0])

        original_colour = image[sr][sc]

        if original_colour == color:
            return image

        def dfs(sr, sc):
            if not (0 <= sr < rows and 0 <= sc < columns):
                return

            if image[sr][sc] != original_colour:
                return

            image[sr][sc] = color

            dfs(sr, sc + 1)
            dfs(sr, sc - 1)
            dfs(sr + 1, sc)
            dfs(sr - 1, sc)

        dfs(sr, sc)
        return image
```

**Correct.** All three key points are there: the `original_colour == color` guard,
capturing `original_colour` before mutating, and the parenthesised bounds check.

**One style note (not a bug):** the inner `dfs(sr, sc)` reuses the names `sr, sc`
from the outer parameters. It works here only because the outer `sr, sc` are not
needed after the single `dfs(sr, sc)` call. Prefer distinct names — `dfs(r, c)` —
so the two scopes can't be confused, especially in a longer function or if you
later add code that still expects the *original* `sr, sc`.
