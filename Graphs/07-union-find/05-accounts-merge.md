# Accounts Merge  ·  LeetCode 721  ·  Medium

Group 07 — Union-Find  ·  the "real-world" DSU problem: elements are **email
strings**, not integers, so you remap them to ids first — then it's ordinary
component-finding.

Prereqs: `concepts/08-union-find.md` (especially §7, "non-integer elements"),
`03-number-of-connected-components.md`.

---

## 1. Problem

`accounts[i]` is a list: `accounts[i][0]` is a person's **name**, and the rest
`accounts[i][1:]` are **emails** on that account.

Two accounts belong to the **same person** if they share **at least one common
email**. A person may have any number of accounts, but all their accounts carry
the same name (different people can share a name).

**Merge the accounts.** Return, for each person, `[name, sorted_email_1,
sorted_email_2, ...]` (emails in sorted order, name first). Order of the returned
accounts doesn't matter.

Constraints:
- `1 <= accounts.length <= 1000`, `2 <= accounts[i].length <= 10`.
- `1 <= accounts[i][j].length <= 30`.

Example:

```
accounts = [
  ["John","johnsmith@mail.com","john_newyork@mail.com"],
  ["John","johnsmith@mail.com","john00@mail.com"],
  ["Mary","mary@mail.com"],
  ["John","johnnybravo@mail.com"],
]

output = [
  ["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
  ["John","johnnybravo@mail.com"],
  ["Mary","mary@mail.com"],
]
```

The first two Johns share `johnsmith@mail.com` → merged. The third "John"
(`johnnybravo`) shares no email → stays separate. Mary is alone.

---

## 2. Explain Like I'm 5

Think of every **email address** as a person on an island. If two emails ever
appear together on the *same account row*, tie a string between them — they're on
the same island (same real person).

Once all the strings are tied, look at each island of emails. Sort the emails on
that island, stick the person's name in front, and that's one merged account.

The person's name? Just read it off any account row that email came from — every
email remembers which name it was listed under.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "Merge things that **share** something" | ✅ accounts sharing an email |
| Elements are **strings**, not `0..n-1` | ✅ → remap to integer ids |
| Final answer is "group by which cluster, then format" | ✅ → group by DSU root |

**Reduce it to:** *"DSU over email ids. Within each account, union all its emails.
Then bucket emails by root, sort each bucket, prepend the name."*

**Look-alikes:**
- Number of Connected Components — same "count/find clusters," but here you also
  **materialize** the clusters and format them, and elements are strings.
- Friend circles / "group anagrams together" / "merge overlapping intervals by
  shared endpoint" — all "union things that share a key."

---

## 4. Intuition

1. The real connection isn't "account ↔ account" — it's **"email ↔ email, when
   they co-occur on some account."** Two accounts merge *because* they have an
   email in common, so make the **emails** the graph nodes.
2. Within one account row, every email belongs to the same person → union them
   all together. The simplest way: union `emails[0]` with each of `emails[1:]`.
   (Unioning consecutive pairs works too; unioning all to the first is cleanest.)
3. After processing every account, emails that are transitively connected (share
   a chain of accounts) all land in the **same DSU component**.
4. DSU needs integers, so first pass: assign each distinct email a fresh integer
   id (`email_id`), and also record `email_name[email]` (any name it appeared
   under — they're all the same person, so it doesn't matter which).
5. Final pass: group emails by `find(email_id[email])`. For each group: sort the
   emails, prepend `email_name[any email in the group]`, emit.

---

## 5. Approach (primary): remap emails → ids, union per account, group by root

1. **Pass 1 — build the maps.** For each account `[name, *emails]`, for each
   `email`: if new, `email_id[email] = len(email_id)`; set
   `email_name[email] = name`.
2. `dsu = DSU(len(email_id))`.
3. **Pass 2 — union.** For each account, let `emails = account[1:]`; for each `e`
   in `emails[1:]`: `dsu.union(email_id[emails[0]], email_id[e])`.
4. **Pass 3 — group.** `groups = defaultdict(list)`; for each `email, eid` in
   `email_id.items()`: `groups[dsu.find(eid)].append(email)`.
5. **Pass 4 — format.** For each group's email list: `sorted(emails)` with
   `email_name[emails[0]]` prepended. Collect into the result.

Builds on: `concepts/08` §7 (string → id remapping) + idiom for grouping by root.

---

## 6. Pseudocode

```
function accountsMerge(accounts):
    email_id = {}          # email -> integer id
    email_name = {}        # email -> owner's name
    for [name, *emails] in accounts:
        for email in emails:
            if email not in email_id:
                email_id[email] = size(email_id)
            email_name[email] = name

    dsu = DSU(size(email_id))
    for [name, *emails] in accounts:
        for e in emails[1:]:
            union(email_id[emails[0]], email_id[e])

    groups = defaultdict(list)
    for email, eid in email_id.items():
        groups[find(eid)].append(email)

    result = []
    for emails in groups.values():
        result.append([email_name[emails[0]]] + sorted(emails))
    return result
```

---

## 7. Dry Run

```
accounts = [
  ["John","a@x.com","b@x.com"],
  ["John","b@x.com","c@x.com"],
  ["Mary","m@x.com"],
]
```

**Pass 1:** `email_id = {a:0, b:1, c:2, m:3}`. `email_name = {a:John, b:John,
c:John, m:Mary}`.

**Pass 2 — union:**

| account | unions |
|---|---|
| `["John", a, b]` | `union(0, 1)` → `parent[1]=0` |
| `["John", b, c]` | `union(1, 2)` → `find(1)=0`, `find(2)=2` → `parent[2]=0` |
| `["Mary", m]` | `emails[1:]` is empty → no union |

**Pass 3 — group by root:** `find(0)=0, find(1)=0, find(2)=0, find(3)=3`.

```
groups = { 0: ["a@x.com","b@x.com","c@x.com"],  3: ["m@x.com"] }
```

**Pass 4 — format:**
- Group `0`: `sorted([a,b,c])` = `[a@x.com, b@x.com, c@x.com]`; name =
  `email_name["a@x.com"]` = `John` → `["John","a@x.com","b@x.com","c@x.com"]`.
- Group `3`: `["Mary","m@x.com"]`.

Result: `[["John","a@x.com","b@x.com","c@x.com"], ["Mary","m@x.com"]]`. ✅

---

## 8. Python Code (primary — DSU over email ids)

```python
from collections import defaultdict
from typing import List


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        email_id = {}                        # email -> integer id
        email_name = {}                      # email -> owner's name

        for account in accounts:
            name = account[0]
            for email in account[1:]:
                if email not in email_id:
                    email_id[email] = len(email_id)
                email_name[email] = name

        dsu = DSU(len(email_id))
        for account in accounts:
            emails = account[1:]
            for e in emails[1:]:
                dsu.union(email_id[emails[0]], email_id[e])

        groups = defaultdict(list)
        for email, eid in email_id.items():
            groups[dsu.find(eid)].append(email)

        return [[email_name[emails[0]]] + sorted(emails) for emails in groups.values()]


if __name__ == "__main__":
    sol = Solution()

    out = sol.accountsMerge([
        ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
        ["John", "johnsmith@mail.com", "john00@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "johnnybravo@mail.com"],
    ])
    assert sorted(out) == sorted([
        ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
        ["John", "johnnybravo@mail.com"],
        ["Mary", "mary@mail.com"],
    ])

    # no merges at all
    out2 = sol.accountsMerge([["A", "a@x.com"], ["B", "b@x.com"]])
    assert sorted(out2) == sorted([["A", "a@x.com"], ["B", "b@x.com"]])

    # chain merge: 1-2 share, 2-3 share => all one person
    out3 = sol.accountsMerge([
        ["X", "1@x.com", "2@x.com"],
        ["X", "2@x.com", "3@x.com"],
        ["X", "3@x.com", "4@x.com"],
    ])
    assert sorted(out3) == sorted([["X", "1@x.com", "2@x.com", "3@x.com", "4@x.com"]])

    # same name, different people
    out4 = sol.accountsMerge([["Bob", "b1@x.com"], ["Bob", "b2@x.com"]])
    assert sorted(out4) == sorted([["Bob", "b1@x.com"], ["Bob", "b2@x.com"]])

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Build an email graph, then BFS/DFS the components

```python
from collections import defaultdict, deque
from typing import List


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        graph = defaultdict(set)
        email_name = {}

        for name, *emails in accounts:
            for e in emails:
                email_name[e] = name
                graph[emails[0]].add(e)      # link every email to the first
                graph[e].add(emails[0])

        seen = set()
        result = []
        for email in graph:
            if email in seen:
                continue
            q = deque([email])
            seen.add(email)
            component = []
            while q:
                cur = q.popleft()
                component.append(cur)
                for nei in graph[cur]:
                    if nei not in seen:
                        seen.add(nei)
                        q.append(nei)
            result.append([email_name[email]] + sorted(component))
        return result
```

Same `O(N·K·log(N·K))` (the sort dominates). DSU vs graph-BFS is a real choice
here — DSU avoids building an explicit adjacency list; BFS avoids the id-remap.

### The BFS↔DFS answer the interviewer wants

> "The connection is between emails that co-occur on an account. DSU over email
> ids is clean — remap strings to ints, union each account's emails, group by
> root. A graph-BFS version skips the remap but builds an adjacency list. Both
> are dominated by the final `O(total emails · log)` sort of each group."

---

## 10. Complexity — derived step by step

Let `N` = number of accounts, `K` = max emails per account, so total emails
`E ≤ N·K` (with duplicates across accounts; distinct emails `D ≤ E`).

**Time:**
- Pass 1 (build maps): touch every email once → `O(E)`.
- Pass 2 (union): `O(E · α(D))` ≈ `O(E)`.
- Pass 3 (group): one `find` per distinct email → `O(D · α(D))` ≈ `O(D)`.
- Pass 4 (format): sorting each group; summed over all groups, `O(D log D)`.
- **Total: `O(E + D log D)`** — the per-group sort dominates.

**Space:**
- `email_id`, `email_name`, `groups`: `O(D)`.
- DSU `parent` + `rank`: `O(D)`.
- **Total: `O(D)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| An account with exactly one email | `emails[1:]` is empty → no `union` → it's its own group |
| Same email under two different-name accounts (contradictory input) | not possible per problem statement (shared email ⟹ same person ⟹ same name); `email_name` just keeps the last-seen name |
| Two accounts, same name, no shared email | two separate groups — name is not a merge key, only shared emails are |
| Duplicate email within one account | `email_id` dedupes; `union` with itself is a no-op |
| Chain merges (`A∩B`, `B∩C` but `A∩C = ∅`) | transitivity via DSU → all one group |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Unioning accounts by name.** Name is *not* a connector — different people
      share names. Only a **shared email** merges accounts.
- [ ] **Forgetting to record `email_name`** (or overwriting it in a way that
      matters) — you need the name back when formatting each group. Any name the
      email appeared under is correct (all the same person).
- [ ] **Grouping by `email_id[email]` instead of `find(email_id[email])`** —
      groups by *original* id, not by component. Every email ends up in its own
      "group."
- [ ] **Not sorting each group's emails** — the output requires sorted emails
      after the name.
- [ ] **Sorting the whole row including the name** — the name goes first
      unconditionally; only the emails are sorted.
- [ ] **Assuming emails are unique across accounts** — the *same* email string
      appears in multiple accounts (that's the whole point); `email_id` must
      dedupe.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **DSU on non-integer elements = remap to ids first.** Build `element -> id`
   (and any side-maps like `element -> name`) in one pass, size the DSU to the id
   count, translate.
2. **Choose the right node.** The accounts don't connect *directly*; the emails
   do. Picking emails (not accounts) as the graph nodes makes the merge trivial.
3. **"Materialize the clusters":** group elements by `find(id)` into a dict of
   lists, then format each cluster. This "bucket by root" step is how DSU
   problems produce a *listing*, not just a count.
4. **`union` within a group of things that belong together** (all emails on one
   account) — a common shape ("union all items in each row/set/window").

| Problem | How this transfers |
|---|---|
| Number of Connected Components | count-only version; here you also materialize + format |
| "Group strings that share a character / anagram key" | remap keys to ids, union within groups, bucket by root |
| Sentence similarity with transitivity (LC 737) | union word pairs, then check `find(a) == find(b)` |
| "Merge user records that share any of {email, phone, device id}" | same — union on *any* shared attribute |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Also merge accounts that share a **phone number** or a **device id**, not just an email."

- **(b) Pattern:** same DSU, more attribute types as connectors.
- **(c) Adapt:** give every *attribute value* (email, phone, device id — namespaced
  so `"phone:555..."` can't collide with `"email:..."`) an id. For each account,
  union all of its attribute-value ids together. Group by root as before; when
  formatting, filter each group back to just the emails (or whatever the output
  wants). Complexity unchanged in shape.
- **(d) Say:** "Any number of shared-attribute types is still one DSU — just
  make every distinct attribute value a node and union all of an account's
  attributes together."

### Scenario 2 — "Accounts stream in continuously (millions). Report merged identities on demand."

- **(b) Pattern:** DSU is online — perfect fit.
- **(c) Adapt:** maintain the `email_id`/`email_name` maps and the DSU across the
  stream; process each incoming account's unions as it arrives (`O(K · α)`). A
  "who is this person?" query is `find(email_id[email])` then a lazy group
  lookup. Only re-sort a group's emails when actually asked for that group.
- **(d) Say:** "Streaming account ingestion is `O(α)` per email; keep the group
  formatting lazy so you only pay the sort when a specific identity is
  requested."

### Scenario 3 — "An account was entered by mistake and must be **removed** — un-merge if it was the only link between two clusters."

- **(b) Pattern:** DSU **can't un-merge**.
- **(c) Adapt:** if all operations are known upfront, process offline in reverse.
  Otherwise, rebuild the DSU from scratch without that account (`O(E α)` — a full
  recompute), or maintain a dynamic-connectivity structure. For a moderate stream
  with rare deletions, periodic full rebuilds are the pragmatic choice.
- **(d) Say:** "Deletions aren't DSU's model — offline-reverse if possible, else
  a full rebuild without the bad record, since accounts data usually tolerates a
  periodic recompute."

### Scenario 4 — "Two accounts with the **same name** and a shared email is a normal merge; two accounts with **different names** sharing an email is a data-quality alert — flag those pairs instead of merging."

- **(b) Pattern:** same DSU, plus a conflict check during union.
- **(c) Adapt:** before unioning two emails' components, if
  `email_name[e1] != email_name[e2]`, record the pair as a conflict and **skip**
  the union (or union anyway but emit the alert — decide with the interviewer).
  Track a `name_of_component[root]`; on a successful union, if the two components
  had different names, that's the flag.
- **(d) Say:** "Attach the name to each component; a union that would merge two
  differently-named components is the data-quality signal — flag it and decide
  the merge policy explicitly."

### Scenario 5 — "Return the merged accounts **sorted by number of emails descending**, then by name."

- **(b) Pattern:** same algorithm, sort the final list.
- **(c) Adapt:** after building each `[name, *sorted_emails]` row, sort the
  result list with key `(-len(emails), name)`. `O(G log G)` extra where `G` =
  number of merged accounts.
- **(d) Say:** "Output ordering is a final sort on the formatted rows — doesn't
  touch the merge logic."

### Scenario 6 — "`D` (distinct emails) is `10^8`. Optimize memory."

- **(b) Pattern:** the maps and DSU arrays are all `O(D)` — that's the floor,
  but shrink the constants.
- **(c) Adapt:** hash each email to a 64-bit id instead of storing the full
  string as a dict key where possible; use array-backed `parent`/`rank`; stream
  accounts rather than holding all of them. If even `O(D)` in RAM is too much,
  shard emails by hash across machines and union within shards, then reconcile
  cross-shard links (like the parallel Number-of-Islands scenario). Time stays
  `O(E + D log D)`.
- **(d) Say:** "At `10^8` distinct emails I'd hash to fixed-width ids, use flat
  arrays, and if needed shard by email hash and reconcile boundary unions across
  shards."

---

## 15. Flashcards

**Q:** What are the graph nodes in Accounts Merge — accounts or emails?
**A:** **Emails.** Two accounts merge *because* they share an email, so union the
emails; accounts connect only transitively.

**Q:** How do you use DSU on strings?
**A:** One pass to assign each distinct string an integer id (and any side-maps
like `email -> name`); size the DSU to the id count; translate.

**Q:** The 4 passes?
**A:** (1) build `email_id` + `email_name`; (2) union each account's emails to
its first email; (3) group emails by `find(id)`; (4) sort each group, prepend the
name.

**Q:** The bug where every email ends up in its own group?
**A:** Grouping by `email_id[email]` instead of `find(email_id[email])` — you
must bucket by *component root*, not original id.

**Q:** Why is unioning by name wrong?
**A:** Different people can share a name. Only a shared email connects accounts.

**Q:** Time and space?
**A:** `O(E + D log D)` time (the per-group sort dominates; `E` = total emails,
`D` = distinct), `O(D)` space.

**Q:** Also merge on shared phone/device id — what changes?
**A:** Make every distinct attribute value (namespaced) a node; union all of an
account's attribute ids together. Same DSU.

**Q:** "Bucket by root" — why does it matter beyond this problem?
**A:** It's how any DSU problem produces a *listing* of its clusters (not just a
count): `groups[find(x)].append(x)` for every element, then format each bucket.
