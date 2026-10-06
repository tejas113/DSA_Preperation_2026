# Topic 3 — Expression Evaluation

## The pattern

Scan the tokens left to right. Keep a stack of **operands**, so each operator can be applied at the right moment. The three problems add one difficulty each: no precedence, then precedence, then parentheses.

```python
# Reverse Polish Notation: every operator applies to the two most recent operands
stack = []
for token in tokens:
    if token in "+-*/":
        b, a = stack.pop(), stack.pop()        # b is on top — pop order matters for - and /
        stack.append(apply(a, b, token))
    else:
        stack.append(int(token))

# Basic Calculator II (precedence): apply * and / immediately, push + and - as signed numbers
#   at the end: sum(stack)
# Basic Calculator (parentheses): on "(" push the running result and sign, restart at 0;
#   on ")" pop them and combine
```

## How to spot this topic

* The input is an **arithmetic expression** (or its tokens), and you must **evaluate** it.
* Words to look for: **"evaluate"**, **"calculator"**, **"reverse Polish"**, **"operator precedence"**, **"parentheses"**.
* Quick test: *am I applying operators to operands in the right order?* If yes, it's this topic.

**Not this topic if:** you only match brackets without computing anything (→ Topic 1).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 9 | Evaluate Reverse Polish Notation | Pop two operands, apply, push; division truncates toward zero |
| 10 | Basic Calculator II | Remember the last operator; on `*` or `/` combine with the stack top, on `+` or `-` push `±num` |
| 11 | Basic Calculator | Track `result` and `sign`; on `(` push both and restart, on `)` pop and combine |
