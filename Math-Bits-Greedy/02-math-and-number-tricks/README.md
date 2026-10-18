# Topic 2 — Math & Number Tricks

## The pattern

A short piece of arithmetic or number theory replaces a slow loop. Most of the difficulty is in the **edge cases**: overflow, negative numbers, zero, and the last digit.

```python
# Peel digits
while x:
    digit = x % 10
    x //= 10

# Fast exponentiation — O(log n)
result = 1
while n:
    if n & 1:
        result *= x            # this bit of the exponent is set: multiply it in
    x *= x                     # square the base
    n >>= 1                    # halve the exponent
# negative n: compute x ** abs(n) and return 1 / result

# Sieve of Eratosthenes
is_prime = [True] * n
for p in range(2, int(n ** 0.5) + 1):
    if is_prime[p]:
        for multiple in range(p * p, n, p):
            is_prime[multiple] = False
```

**Rejection sampling** (Rand10 from Rand7): combine two rolls into one bigger uniform number (`(rand7() - 1) * 7 + rand7()` is uniform on `1..49`), throw away the values `41..49`, and map the rest with `% 10 + 1`.

## How to spot this topic

* The input is **a number**, and the naive approach is a loop over every value up to it.
* Words to look for: **"reverse the integer"**, **"palindrome number"**, **"x to the power n"**, **"count primes"**, **"trailing zeroes"**, **"uniform random"**.
* Quick test: *is there a short formula or a fast standard routine for this number?* If yes, it's this topic.

**Not this topic if:** the number is a **string of digits to parse** (→ Arrays-Strings, Topic 9).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 10 | Reverse Integer | Peel digits and rebuild; return 0 if the result leaves the 32-bit range |
| 11 | Palindrome Number | Negatives are never palindromes; reverse only the second half and compare |
| 12 | Pow(x, n) | Fast exponentiation; for a negative `n`, invert at the end |
| 13 | Count Primes | Sieve of Eratosthenes, starting each crossing-out at `p * p` |
| 14 | Implement Rand10() Using Rand7() | Rejection sampling over a `1..49` range, keeping only `1..40` |
| 15 | Factorial Trailing Zeroes | Count factors of 5: `n // 5 + n // 25 + n // 125 + …` |
| 16 | Max Points on a Line | For each point, hash the reduced slope (`dy / gcd`, `dx / gcd`) to every other point |
| 17 | Detect Squares | Hash map of point counts; for each diagonal point, look up the other two corners |
