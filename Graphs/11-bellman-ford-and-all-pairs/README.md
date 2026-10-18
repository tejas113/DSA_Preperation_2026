# Group 11 — Bellman-Ford / All-Pairs Shortest Path

> 🔁 **Whole group flagged for revision.** On Day 5, re-derive both problems from
> scratch — don't recite. The two things that must click:
> 1. **Cheapest Flights:** "K stops" = "K+1 flights" = K+1 Bellman-Ford rounds;
>    the `snapshot` copy is what forces *exactly one* new flight per round (you
>    spend the fares that existed at the **start** of the round).
> 2. **Find the City:** Floyd-Warshall = "for each intermediate city `k`, can
>    `i → k → j` beat `i → j`?" — `k` **outermost**. Then it's just a count over
>    the finished distance matrix.

## What this pattern is

Shortest paths when Dijkstra doesn't apply or isn't the right shape:

- **Bellman-Ford** — negative edge weights, or a **limit on the number of
  edges/stops**, or negative-cycle detection. `O(V·E)`.
- **Floyd-Warshall** — *all-pairs* shortest paths in `O(V³)`, for small `V` when
  you need many arbitrary-pair queries.

Full mechanics: `concepts/11-bellman-ford.md`, `concepts/12-floyd-warshall.md`.

## How to recognize it

- "Cheapest / shortest path" **+** a cap like "at most `K` stops / moves / edges"
  → **hop-limited Bellman-Ford** (`K` rounds against a frozen `dist` copy).
- Negative weights anywhere → Bellman-Ford (Dijkstra is invalid).
- "For every pair..." / "the city with the fewest reachable within distance `D`"
  → **Floyd-Warshall** (if `V` is small).

## The decision tree (say this out loud)

```
unweighted?                       -> BFS                     (concepts/03)
weighted, non-negative, no cap?   -> Dijkstra                (concepts/10)
weighted + hop/stop cap?          -> Bellman-Ford, K rounds  (concepts/11)
negative weights?                 -> Bellman-Ford            (concepts/11)
all pairs, small V?               -> Floyd-Warshall          (concepts/12)
```

## Complexity

- Bellman-Ford: `O(V·E)` time (`O(K·E)` for a `K`-hop limit), `O(V)` space.
- Floyd-Warshall: `O(V³)` time, `O(V²)` space.

## Problems

1. `01-cheapest-flights-within-k-stops.md` — the hop-limited Bellman-Ford
   pattern: cheapest `src → dst` using **at most `K` stops** (LeetCode 787).
   **Start here.**
2. `02-find-the-city-smallest-neighbors.md` *(supplementary)* — all-pairs
   shortest paths (Floyd-Warshall), then a per-city count (LeetCode 1334).
