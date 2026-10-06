# 787. Cheapest Flights Within K Stops

**LC 787** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Bellman-Ford limited to K + 1 rounds (shortest path that uses at most K + 1 edges)

---

## 1. Intuition

"At most K stops" means "at most K + 1 flights". Bellman-Ford fits this perfectly: after round 1 you know
the cheapest price to every city using **1 flight**, after round 2 using **at most 2 flights**, and so on.
So run exactly `k + 1` rounds and read off `dst`. The one trap is that inside a round, each update must use
the prices from the **previous** round. Otherwise one round could chain several flights together.

* **`prices[x]` = the cheapest cost to reach `x` using at most (rounds done) flights.** It starts with `prices[src] = 0` and everything else `inf`.
* **One round = one more flight allowed:** `for _ in range(k + 1)`, and inside it, every flight `u → v` tries `prices[u] + price`.
* **`temp` is the key line:** each round reads from `prices` (last round's values) and writes to `temp = list(prices)`. A city improved in this round can't be used again until the next round, so round `i` never builds paths longer than `i` flights.
* **Skip cities you can't reach yet:** `if prices[u] == float('inf'): continue`.
* **The answer:** after `k + 1` rounds, `prices[dst]` is the cheapest route using at most `k + 1` flights. If it's still `inf`, return `-1`.

**Recall:** `prices[src] = 0`. Repeat `k + 1` times: copy `prices` to `temp`, relax every flight reading from `prices` and writing to `temp`, then `prices = temp`. Return `prices[dst]`, or `-1`.

## 2. Approach

* **Idea:** Bellman-Ford with a **limited number of rounds**. Normal Bellman-Ford runs V − 1 rounds to find shortest paths of any length. Here the number of rounds is the limit on flights, so stopping after `k + 1` rounds gives the cheapest path that uses at most `k + 1` edges.
* **Graph representation:** **edge list** (`flights = [[u, v, price], ...]`). **Directed** and **weighted** (`price`). It's used directly, with no adjacency list built.
* **Data structure / pointers:**
  * `prices`: the best known cost to each city using at most `r` flights, after `r` rounds. This is the round's **read-only** snapshot.
  * `temp`: a copy that this round **writes** into. It starts equal to `prices`, so a city's cost never goes up.
  * Each flight tries one "relax": `if prices[u] + price < temp[v]: temp[v] = prices[u] + price`.
  * There's no visited set. Bellman-Ford doesn't "finish" a node; it just keeps improving numbers round by round.
* **Invariant:** after round `r` (r = 1 … k+1), `prices[x]` is exactly the cheapest cost from `src` to `x` using **at most `r` flights**, or `inf` if no such route exists.
* **Edge cases:**
  * `dst` unreachable within `k + 1` flights (or at all): `prices[dst]` stays `inf`, so it returns `-1`.
  * `k = 0`: one round, so only direct flights `src → dst` count.
  * A cheaper route that needs too many stops is correctly **ignored**. That's exactly what `temp` guarantees (see the dry run).
  * Cycles (for example `0 → 1 → 2 → 0`): no problem, because there are only `k + 1` rounds and a loop can't run forever.
  * Several flights between the same two cities: each is relaxed, so the cheapest one wins.
  * Disconnected cities: they stay `inf` and are skipped by the `continue`.
  * Negative prices: not allowed on LC (`price ≥ 1`), but the code would still be correct, because the round limit stops negative cycles from running forever. (Dijkstra could **not** handle that.)
  * `src == dst`: not allowed on LC, but would return `0`.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
class Solution:
    def findCheapestPrice(self, n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
        prices = [float('inf')] * n
        prices[src] = 0

        # Relax edges exactly k + 1 times
        for _ in range(k + 1):
            temp = list(prices)
            for u, v, price in flights:
                if prices[u] == float('inf'):
                    continue
                if prices[u] + price < temp[v]:
                    temp[v] = prices[u] + price
            prices = temp

        return prices[dst] if prices[dst] != float('inf') else -1
```

## 4. Dry Run

Input (LC Example 1): `n = 4`, `src = 0`, `dst = 3`, `k = 1`, so there are **2 rounds**.

```text
flights:  0 →(100) 1    1 →(100) 2    2 →(100) 0    1 →(600) 3    2 →(200) 3
```

Start: `prices = [0, inf, inf, inf]`

| Round | Reads `prices` | Flight relaxations (in list order) | `prices` after the round |
| --- | --- | --- | --- |
| 1 | `[0, inf, inf, inf]` | `0→1`: 0 + 100 = **100** < inf, so `temp[1] = 100`. All other flights start at an `inf` city, so skip. | `[0, 100, inf, inf]` |
| 2 | `[0, 100, inf, inf]` | `0→1`: 100, not < 100. `1→2`: 100 + 100 = **200**, so `temp[2] = 200`. `2→0`: `prices[2]` is still `inf` (old snapshot), so skip. `1→3`: 100 + 600 = **700**, so `temp[3] = 700`. `2→3`: `prices[2]` is still `inf`, so **skip**. | `[0, 100, 200, 700]` |

It returns **`700`** (route `0 → 1 → 3`, 1 stop).

**Why `temp` matters here:** in round 2, `temp[2]` became `200` *before* the flight `2 → 3` was checked. If the code read from the array it was writing to, it would compute `200 + 200 = 400` in the same round. That's the route `0 → 1 → 2 → 3`, which uses **2 stops** when only `k = 1` is allowed, so it's wrong.

## 5. Complexity

Let **E** = `len(flights)` and **n** = the number of cities.

* **Time: O(k × (n + E))**, often written O(k × E)
  Think of it as: there are `k + 1` rounds, and each round does two things. It copies the `n`-length `prices` list into `temp`, and it looks at every one of the E flights once with a quick check. So the work is (number of rounds) × (n + E).
* **Space: O(n)**
  Think of it as: only two lists of length `n` exist at a time, `prices` and `temp`. The flight list is read directly, with no adjacency list built.

## 6. Recall (30 seconds)

* At most K stops means at most **K + 1 edges**, so run Bellman-Ford for exactly **`k + 1` rounds**.
* Every round: `temp = list(prices)`, **read from `prices` and write to `temp`**, then swap. Without the copy, one round can chain several flights and break the stop limit.
* O(k·(n + E)) time and O(n) space. `inf` at the end → `-1`. Unlike Dijkstra, it works with negative prices.
