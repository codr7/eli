## Embedded Lisp Interpreter

## Introduction
`eli` represents the culmination of more than 15 years of research into designing and implementing embedded Lisp interpreters.

It all began with a craving for an embedded scripting language that didn't drive me mad, buit quickly evolved into one of the deepest rabbit holes I've had the pleasure of falling into.

I've written a ton of implementations in different languages over the years, each verifying and further refining the design.

## Implementations

The following projects implement `eli` in different languges, some are more complete than others. Most work currently happens in [eli-java](https://github.com/codr7/eli-java). The goal is to gradually consolidate into code compatible production ready implementations.


- [C](https://github.com/codr7/alisp)
- [C#](https://github.com/codr7/sharpl)
- [Common Lisp](https://github.com/codr7/claesp)
- [Go](https://github.com/codr7/gfun)
- [Java](https://github.com/codr7/eli-java)
- [Swift](https://github.com/codr7/sweet)

## Benchmarks
I decided early on that `python3` would make a reasonable performance target to aim for. While it has a definite head start by virtue of being implemented in a lower level language, it has a comparable level of dynamism and is very well known.

### Python
```
$ python3 benchmarks/run.py
```
```
fact 1.689405483
fib 0.634149815
```

## Language

### Branches
`if` may be used to conditionally evaluate a block of code.
```
(if T 1)
```
`1`

```
(if F 1)
```
`_`

`else` may be used to provide an alternative branch.
```
(if F 1 (else 2))
```
`2`

`else-if` may be used to reduce nesting.
```
(if F 1 (else-if F 2 3))
```
`3`

### Bindings
Values may be bound to identifiers at compile time using `var`.

```
(var foo 42)
foo
```
`42`

`let` may be used to create runtime bindings,

```
(let [foo 'bar]
  foo)
```
`'bar`

and locally override existing bindings.

```
(var foo 'foo)
foo
```
`'foo`

```
(^baz [] foo)
  
(let [foo 'bar] (baz))
```
`'bar`

```
foo
```
`'foo`

### Loops
`for` may be used to repeat a block of code for each item in a sequence.

```
(let [foo 0]
  (for [i [1 2 3]
    (inc foo i))
  (foo))
```
`6`

### Quoting
Any expression may be quoted by prefixing with `'`.
```
'(+ 1 2)
```
`'(+ 1 2)`

A quoted list becomes a list of quoted items.
```
'[foo bar baz]
```
`['foo 'bar 'baz]`

`,` may be used to unquote.
```
(let [foo '(+ 1 2)]
  ,foo)
```
`3`

### Methods
Methods may be defined using `^`.

```
(^foo [x] Int 
  x)
  
(foo 42)
```
`42`

#### Arguments
Methods may be made to accept a variable number of arguments by suffixing the final argument with `*`.
```
(^foo [x*] Int 
  (+ x*))
  
(foo 35 7)
```

Prefixing arguments with `'` automatically quotes and passes the expression without evaluating at compile time.
```
(^foo ['x] Expr 
  x)
  
(foo (+ 35 7))
```
`(+ 35 7)`

`,` may be used to unquote,
note that this results in `(+ 35 7)` being spliced into `foo`'s body at compile time.
```
(^foo ['x] Expr ,x)

(foo (+ 35 7))
```
`42`

#### Result
When a result type is specified; the value of the last evaluated form is returned,
otherwise ´_`.
```
(^foo [x] _ 
  x)
  
(foo 42)
```
`_`

#### Recursion
`recall` may be used to jump to the start of the current method.
```
(^fib [n a b] Int
  (if (> n 1) 
    (recall (- n 1) b (+ a b)) 
    (if (is n 0) a b)))

(fib 10 0 1)
```
`55`

#### Return
`return` evaluates its arguments and exits the current method.

```
(^foo [] Int 1 (return 2 3) 4)
(foo)
```
`3`

#### Lambdas
Method definitions return the defined method, leaving out the name avoids binding.

```
(^_ [] Int 42)
```
`(Method _)`

### Macros
There is no special support for macros, [quoted arguments](https://github.com/codr7/jx#arguments) + inlined direct calls = macros.

The following example implements [`else-if`](https://github.com/codr7/jx#branches) in user code.

Note that this would result in a compile error without quoted arguments,
since `else` is only defined inside `if`'s body.

```
(^my-else-if ['cond 'body*] Any
    (else (if ,cond ,body*)))

(if F (my-else-if T 42))
```
`42`

### IO
`say` prints its arguments followed by newline to standard output.
```
(say "35+7=" (+ 35 7))
```
```
35+7=42
```

### Tests
`check` may be used to validate that a block of code produces the expected value.
```
(check 1 2)
```
```
Error in REPL@1:1: Check failed; expected 1, actual: 2
```

When called with one argument, the expected value is assumed to be `T`.
```
(check (= 42 42))
```