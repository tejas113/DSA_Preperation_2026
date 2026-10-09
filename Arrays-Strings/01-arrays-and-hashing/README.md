# Topic 1 — Arrays & Hashing

## The pattern

Walk through the input once, and remember what you've seen in a `set` or a `dict`. Every later question ("have I seen this?", "what's the count?", "where was it?") is then a quick lookup instead of another scan.

```python
seen = {}                          # value -> index, or value -> count, or key -> list of items
for i, x in enumerate(nums):
    need = target - x              # what would complete the answer (Two Sum style)
    if need in seen:               # check BEFORE storing, so an element can't pair with itself
        return [seen[need], i]
    seen[x] = i                    # remember x for the elements that come later
```

The same shape changes only in **what you store**: a set (duplicates), a count (anagrams, top k), a canonical key (grouping), or a value ↔ value mapping (isomorphic strings).

## How to spot this topic

* The question is about **duplicates, counts, groups, pairs, or "have I seen this before?"**.
* Words to look for: **"duplicate"**, **"anagram"**, **"frequency"**, **"group by"**, **"pair that sums to"**, **"top k"**, **"consecutive"**, **"maps one to another"**, **"O(1) insert / delete / random"**.
* Quick test: *if I could remember everything I've already seen, would the answer be one quick check per element?* If yes, it's this topic.

**Not this topic if:** the array is sorted and you must use `O(1)` extra space (→ Topic 2), or the answer is a contiguous chunk (→ Topics 3 and 4).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 1 | Contains Duplicate | Seen-set: if it's already there, it's a duplicate |
| 2 | Valid Anagram | Count the letters of both strings and compare |
| 3 | Two Sum | Store each value's index; look up `target - x` |
| 4 | Group Anagrams | Use the sorted word (or a 26-count tuple) as the dict key |
| 5 | Top K Frequent Elements | Count, then bucket values by their frequency |
| 6 | Longest Consecutive Sequence | Put all numbers in a set; count up only from a number with no `x - 1` |
| 7 | Encode and Decode Strings | Length-prefix each string (`5#hello`) so any character is safe |
| 8 | Insert Delete GetRandom O(1) | Dict for lookup + list for random pick; delete by swapping with the last item |
| 9 | Isomorphic Strings | Keep a mapping in both directions; each side must map to one thing |
| 10 | Ransom Note | Frequency count, like Valid Anagram, but one-directional |
| 11 | Word Pattern | Isomorphic Strings, but on words |
| 12 | Contains Duplicate II | Map each value to its last index; check the gap |
| 13 | Happy Number | Seen-set to detect that the digit-square sequence has entered a loop |
