# 310. Minimum Height Trees

**LC 310** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Peeling leaves layer by layer (Kahn's algorithm with degree instead of indegree) to find the tree's centre

---

## 1. Intuition

Picture a tree as a blob. Cut off all the leaves at once, then cut off the new leaves, and keep going.
It's like peeling an onion. The best roots are in the **middle** of the longest path, because rooting there
keeps every branch short. Peeling from the outside in always ends at that middle: either **one centre node**
or **two neighbouring centre nodes**.

* **Leaves are nodes with exactly one neighbour:** step 1 puts every `i` with `len(graph[i]) == 1` into `leaves`. That's the outer layer.
* **Cut a whole layer at a time:** `leaves_count = len(leaves)` takes a snapshot of the current layer, and `remaining_nodes -= leaves_count` removes it from the count **before** the layer is processed.
* **Cutting a leaf can create a new leaf:** `neighbor = graph[leaf].pop()` and `graph[neighbor].remove(leaf)` delete the edge. If `len(graph[neighbor]) == 1`, the neighbour is now on the outside, so it joins the next layer.
* **Stop at 1 or 2 nodes:** `while remaining_nodes > 2`. A tree can have at most 2 centres. Whatever is left in `leaves` at the end is the answer.

**Recall:** Queue every node with degree 1, then peel layer by layer (`remaining -= len(leaves)`), cutting edges and queueing new degree-1 nodes, until at most 2 nodes remain. Return what's left in the queue.

## 2. Approach

* **Idea:** A root gives a minimum-height tree exactly when it's a centre of the tree (the middle of its longest path). Peeling leaves in layers is a BFS from all the leaves inward, and the last 1 or 2 nodes reached are the centres.
* **Graph representation:** **adjacency sets** (`defaultdict(set)`) built from the edge list. **Undirected**, unweighted, and guaranteed to be a **tree** (connected, `n - 1` edges, no cycles).
* **Data structure / pointers:**
  * `graph[x]`: the set of `x`'s neighbours that are **still in** the tree. `len(graph[x])` is `x`'s current degree. Using a set makes `remove(leaf)` fast.
  * `leaves` (`deque`): the current layer of leaves. A node is pushed **once**, at the moment its degree drops to `1`, which is the visited rule.
  * `remaining_nodes`: how many nodes haven't been peeled yet.
  * `leaves_count`: the size of the layer being peeled, so new leaves wait for the next pass.
* **Invariant:** after each full pass, `graph` describes the tree with all peeled layers removed, `leaves` holds exactly its current leaves, and that smaller tree still has the **same centre(s)** as the original.
* **Edge cases:**
  * `n == 1` (`edges = []`): the early return gives `[0]`. **This check is required.** A single node has degree 0, not 1, so it would never go into `leaves`, and the code would wrongly return `[]`.
  * `n == 2`: both nodes are centres, so the early return gives `[0, 1]`. (Without the check this case would still work, because `remaining_nodes > 2` is already false.)
  * A path of odd length, for example `0-1-2`: the single middle node `[1]`.
  * A path of even length, for example `0-1-2-3`: the two middle nodes `[1, 2]`.
  * A star (one hub): one pass removes all `n - 1` leaves, so it returns `[hub]`.
  * The input is guaranteed to be a tree. A graph with a cycle or more than one component isn't valid input, and the code doesn't check for it.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import defaultdict, deque
from typing import List

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        # Edge case: 2 or fewer nodes are already MHT roots
        if n <= 2:
            return [i for i in range(n)]

        # Build undirected graph adjacency set
        graph = defaultdict(set)
        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)

        # Step 1: Find initial outer leaves (nodes with degree == 1)
        leaves = deque()
        for i in range(n):
            if len(graph[i]) == 1:
                leaves.append(i)

        remaining_nodes = n

        # Step 2: Trim leaves layer-by-layer until at most 2 centroid nodes remain
        while remaining_nodes > 2:
            leaves_count = len(leaves)
            remaining_nodes -= leaves_count

            for _ in range(leaves_count):
                leaf = leaves.popleft()
                
                # Remove connection between leaf and its neighbor
                neighbor = graph[leaf].pop()
                graph[neighbor].remove(leaf)

                # If the neighbor becomes a new leaf, add it to queue
                if len(graph[neighbor]) == 1:
                    leaves.append(neighbor)

        # Step 3: Remaining nodes in queue are the MHT roots
        return list(leaves)
```

## 4. Dry Run

Input (LC Example 2): `n = 6`, `edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]`

```text
0   1   2
 \  |  /
    3
    |
    4
    |
    5
```

`graph`: `3:{0,1,2,4}`, `0:{3}`, `1:{3}`, `2:{3}`, `4:{3,5}`, `5:{4}`. The first scan finds `leaves = [0, 1, 2, 5]`.

**Pass 1:** `remaining_nodes = 6 > 2`. `leaves_count = 4`, so `remaining_nodes = 6 - 4 = 2`.

| Pop `leaf` | `neighbor` | Neighbour's degree after the cut | New leaf? | `leaves` after |
| --- | --- | --- | --- | --- |
| `0` | `3` | 3 (`{1,2,4}`) | no | `[1, 2, 5]` |
| `1` | `3` | 2 (`{2,4}`) | no | `[2, 5]` |
| `2` | `3` | 1 (`{4}`) | **yes**, push 3 | `[5, 3]` |
| `5` | `4` | 1 (`{3}`) | **yes**, push 4 | `[3, 4]` |

The loop checks `remaining_nodes = 2 > 2`, which is false, so it stops. It returns **`[3, 4]`**. Rooting at 3 or at 4 gives height 2, and any other root gives height 3 or more.

## 5. Complexity

* **Time: O(n)**
  Think of it as: every node is peeled once, and every edge is cut once. A tree has `n - 1` edges, so building `graph` is O(n). The first leaf scan looks at each node once. In the peeling loop, each node is pushed and popped at most once, and each pop does a fixed amount of work: one `pop()`, one `remove()` and one length check, each a quick set operation. So the total grows with n.
* **Space: O(n)**
  Think of it as: `graph` stores each of the `n - 1` edges twice (once from each end), and `leaves` holds at most one entry per node.

## 6. Recall (30 seconds)

* The answer is the **centre** of the tree, which is always 1 or 2 nodes. Peel the leaves (degree 1) from the outside in, one whole layer at a time.
* `remaining -= len(leaves)` before each pass. Cut each leaf's edge, and if its neighbour's degree drops to 1, queue it for the next pass.
* Stop when `remaining <= 2` and return the queue. Handle `n <= 2` first. O(n) time and space.
