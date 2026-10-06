# 733. Flood Fill

**LC 733** · **Source:** [+] Claude · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Single-source flood fill on a grid (DFS recolour in place)

---

## 1. Intuition

It's the paint-bucket tool. Click one pixel, and every pixel connected to it that has the *same starting
colour* gets the new colour. This is Number of Islands for one island only: start at `(sr, sc)`, spread
in 4 directions, and stop at any pixel that's a different colour.

* **What counts as "land":** a pixel with `image[r][c] == original_colour`. That's the colour the clicked pixel had *before* anything changed.
* **Recolouring is the visited set:** `image[r][c] = color` changes the pixel, so it fails the `!= original_colour` check if any neighbour tries to visit it again.
* **Why the `original_colour == color` guard matters:** if the new colour is the same as the old one, recolouring a pixel changes nothing. The pixel still matches `original_colour`, so neighbours would keep calling `dfs` on each other forever. That ends in infinite recursion, which Python reports as `RecursionError`. Returning `image` straight away avoids it, and it's correct because nothing needs to change.
* **Only one component:** `dfs(sr, sc)` is called once, so pixels with the same colour that aren't connected to the start (like `(2, 2)` in the dry run) stay as they are.

**Recall:** Save `original_colour`. If it already equals `color`, return. Otherwise DFS from `(sr, sc)` and recolour every connected pixel that matches.

## 2. Approach

* **Idea:** DFS from the start pixel through 4-directional neighbours that still have `original_colour`, recolouring each one on the way.
* **Graph representation:** implicit **grid** graph, undirected and unweighted. Moves go in **4 directions**: `(r, c±1)`, `(r±1, c)`.
* **Data structure / pointers:**
  * `rows`, `columns`: image size.
  * `original_colour`: the colour of `image[sr][sc]` before any change. This decides which pixels belong to the region.
  * `image` itself is the visited marker. A pixel is marked **when `dfs` enters it** (`image[r][c] = color`), and after that it no longer equals `original_colour`.
  * Out-of-bounds is checked first in `dfs` (`not (0 <= r < rows and 0 <= c < columns)`), before the code reads `image[r][c]`.
* **Invariant:** every pixel already set to `color` was connected to `(sr, sc)` through pixels that had `original_colour`. Since `color != original_colour`, no pixel is processed twice.
* **Edge cases:**
  * `color == original_colour`: the guard returns `image` unchanged. Without it, you get infinite recursion.
  * A 1×1 image: recolours that one pixel and returns.
  * An isolated start pixel: only `(sr, sc)` changes, and every neighbour fails the colour check.
  * Same colour but not connected: stays the same (`(2, 2)` in the dry run).
  * An empty image isn't possible (LC guarantees `m, n ≥ 1`). With `[]`, `image[0]` would raise `IndexError`.
  * Recursion depth: a 50×50 image of one colour (the LC maximum) makes `dfs` go up to about 2,500 calls deep. That's above Python's default limit of 1,000, so it raises `RecursionError` when you run it locally. An iterative BFS or stack version avoids this.
  * The input is changed in place, and the same `image` object is returned.

## 3. Code

```python
class Solution:

    def floodFill(
        self, image: list[list[int]], sr: int, sc: int, color: int
    ) -> list[list[int]]:
        rows = len(image)
        columns = len(image[0])
        original_colour = image[sr][sc]

        # Guard against infinite recursion when starting pixel is already the target color
        if original_colour == color:
            return image

        def dfs(r: int, c: int) -> None:
            # Base case: Out of bounds check
            if not (0 <= r < rows and 0 <= c < columns):
                return

            # Base case: Pixel color doesn't match the original starting color
            if image[r][c] != original_colour:
                return

            # Recolour current pixel
            image[r][c] = color

            # Recursively fill 4-directional neighbors
            dfs(r, c + 1)  # Right
            dfs(r, c - 1)  # Left
            dfs(r + 1, c)  # Down
            dfs(r - 1, c)  # Up

        dfs(sr, sc)
        return image
```

## 4. Dry Run

Input: `image = [[1,1,1],[1,1,0],[1,0,1]]`, `sr = 1`, `sc = 1`, `color = 2`, so `original_colour = 1`.
The table lists pixels in the order the DFS actually recolours them. Each call tries right, left, down, up, in that order.

| Order | Pixel `(r, c)` | Reached from | What happens | `image` after |
| --- | --- | --- | --- | --- |
| 1 | `(1, 1)` | start | recolour; right `(1,2)` is `0`, so it returns | `[[1,1,1],[1,2,0],[1,0,1]]` |
| 2 | `(1, 0)` | left of `(1,1)` | recolour; right is now `2`, left is out of bounds | `[[1,1,1],[2,2,0],[1,0,1]]` |
| 3 | `(2, 0)` | down from `(1,0)` | recolour; right `(2,1)` is `0`, down is out of bounds, up is already `2` | `[[1,1,1],[2,2,0],[2,0,1]]` |
| 4 | `(0, 0)` | up from `(1,0)` | recolour | `[[2,1,1],[2,2,0],[2,0,1]]` |
| 5 | `(0, 1)` | right of `(0,0)` | recolour | `[[2,2,1],[2,2,0],[2,0,1]]` |
| 6 | `(0, 2)` | right of `(0,1)` | recolour; down `(1,2)` is `0` | `[[2,2,2],[2,2,0],[2,0,1]]` |
| — | `(2, 2)` | never reached | its neighbours `(1,2)` and `(2,1)` are `0`, so it stays `1` | — |

After this, `(1,1)` tries down `(2,1)`, which is `0`, and up `(0,1)`, which is already `2`, so the DFS ends. It returns **`[[2,2,2],[2,2,0],[2,0,1]]`**.

## 5. Complexity

* **Time: O(rows × columns)**
  Think of it as: each pixel is recoloured at most once, and after that it fails the colour check. A pixel can be *called* up to 4 times (once from each neighbour), but every call after the first returns at once. So the work per pixel is fixed, and the worst case is when the whole image is one colour and every pixel gets painted.
* **Space: O(rows × columns)** in the worst case
  Think of it as: there's no extra visited set, because the image itself is the marker. The only cost is the recursion stack. If the region is one long winding path, `dfs` goes one call deeper per pixel before it returns.

## 6. Recall (30 seconds)

* Save `original_colour = image[sr][sc]`. **If it equals `color`, return right away**, or the DFS never ends.
* DFS in 4 directions, and stop at out-of-bounds or `image[r][c] != original_colour`. Recolouring a pixel marks it as visited.
* O(R·C) time and O(R·C) worst-case recursion depth. This is Number of Islands for a single component.
