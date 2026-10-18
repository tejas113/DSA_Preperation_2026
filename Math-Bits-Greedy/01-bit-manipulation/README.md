# Topic 1 — Bit Manipulation

## The pattern

Treat a number as a row of bits, and use a few operators to do in one step what a loop would do slowly.

```python
a ^ a == 0             # equal values cancel out   → Single Number, Missing Number
a ^ 0 == a
n & (n - 1)            # clears the lowest set bit → count set bits, test for a power of two
(n >> i) & 1           # reads bit i
a ^ b                  # sum WITHOUT carry
(a & b) << 1           # the carry                 → add two numbers with no "+"

# Add without "+":
while b:
    a, b = a ^ b, (a & b) << 1     # in Python, mask to 32 bits to imitate overflow: & 0xFFFFFFFF
```

## How to spot this topic

* The question mentions **bits**, **binary**, **`XOR`**, or says **"without using `+`"**, or wants **`O(1)` extra space** on a problem that a hash set would otherwise solve.
* Words to look for: **"every element appears twice except one"**, **"number of 1 bits"**, **"reverse bits"**, **"missing number"**, **"binary string"**.
* Quick test: *would pairs of equal values cancel out, or can I build the answer one bit at a time?* If yes, it's this topic.

**Not this topic if:** you're enumerating subsets with a bitmask (→ that's bitmask DP or Backtracking, out of scope here).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 1 | Single Number | XOR every element; pairs cancel, the single value is left |
| 2 | Number of 1 Bits | Repeat `n &= n - 1` and count until `n` is zero |
| 3 | Counting Bits | `bits[i] = bits[i >> 1] + (i & 1)` — reuse the answer for `i` shifted right |
| 4 | Reverse Bits | Loop 32 times: shift the result left, add the lowest bit of `n`, shift `n` right |
| 5 | Missing Number | XOR all indices `0..n` with all values; what's left is the missing one |
| 6 | Sum of Two Integers | XOR is the sum without carry; `(a & b) << 1` is the carry; repeat until no carry |
| 7 | Single Number II | For each bit position, count set bits across all numbers; take the count `mod 3` |
| 8 | Add Binary | Walk both strings from the right with a carry, like adding on paper |
| 9 | Bitwise AND of Numbers Range | The answer is the common binary prefix of `left` and `right` |
