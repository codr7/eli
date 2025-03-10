## Embedded Lisp Interpreter

## Introduction
`eli` represents the culmination of more than 15 years of designing and implementing embedded Lisp interpreters in various languages.

It all began with a craving an embedded Lisp for personal projects, but evolved into one of the deepest rabbit holes I've had the pleasure of falling into.

## Implementations

The following projects implement `eli` in different languges, some are more complete than others. Most work currently happens in [eli-java](https://github.com/codr7/eli-java). The goal is to gradually consolidate into code compatible production ready implementations.


- [C](https://github.com/codr7/alisp)
- [C#](https://github.com/codr7/sharpl)
- [Common Lisp](https://github.com/codr7/claesp)
- [Go](https://github.com/codr7/gfun)
- [Java](https://github.com/codr7/eli-java)
- [Swift](https://github.com/codr7/sweet)

## Performance
I decided early on that Python would make a reasonable performance target to aim for since it's mostly interpreted and very well known.

```
$ python3 benchmarks/run.py
```
```
fact 1.689405483
fib  0.634149815
```

## [Java](https://github.com/codr7/eli-java)

```
$ java -jar eli.jar benchmarks/run.eli
```
```
fact 1.682860949
fib  1.568288647
```

## Language

### Types

#### Any
The root of all types.

#### Bit (Any)
Bits are either true or false.

`T` `F`

#### Callable
The root of callable types.

#### Comparable
The root of comparable types.

#### Countable
The root of countable types.

#### Char (Any)
Characters.

`\a`

#### Expr (Any)
Quoted expressions.

`'(+ 1 2)`

#### Float (Any Numeric)
Floating point values with absolute precision.

`1.23`

#### Int (Any Numeric)
64 bit integers.

`42`

#### Iter (Any Iterable)
Root of iterator types.

#### Iterable
Root of iterable types.

#### Lib (Any)
Type of libraries.

#### List (Any Callable Comparable Countable Iterable Sequential)
Mutable, random access sequences of values.

`[1 2 3]`

#### Macro (Any Callable)
Type of macros.

#### Map (Any Callable Comparable Countable Iterable Sequential)
Mutable, ordered mappings between values.

`{1:2 3:4}`

#### Maybe (Any Nil)
Optional values.

#### Meta (Any)
Type of types.

#### Method (Any Callable)
Type of methods.

#### Nil
Missing values.

`_`

#### Numeric (Any Comparable)
Root of numeric types.

#### Pair (Any Comparable Countable Iterable Sequential)
Pairs of values.

`1:2`

#### Sequential
Root of values with heads and tails.

#### String (Any Callable Comparable Countable Iterable Sequential)
Sequences of characters.

`"abc"`

#### Sym (Any Comparable)
Quoted identifiers.

`'foo`

#### Time (Any)
Durations of time.

#### Timestamp (Any)
Points in time.

`(now)`

### Truthiness
All values have `Bit` representations, most evaluate to `T`; Such values are referred to as truthy. Notable exceptions besides `F` are empty strings, lists; `0` and `_`.

### Branches
`if` evaluates its body if the specified condition is truthy.

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

`,` unquotes the succeding form.
```
(let [foo '(+ 1 2)]
  ,foo)
```
`3`

### Bindings
Values may be bound to identifiers indefinitely using `var`.

```
(var foo 42)
foo
```
`42`

`let` may be used to create scoped bindings,

```
(let [foo 'bar]
  foo)
```
`'bar`

or override existing bindings inside its body.

```
(var foo 1)
foo
```
`1`

```
(^baz [] foo)
  
(let [foo 2] (baz))
```
`2`

```
foo
```
`1`

Both `let` and `var` support pair destructuring.

```
(let [i:j 1:2]
  i:j)
```
`1:2`

`set` may be used to replace the value of existing bindings.

```
(let [foo 1 bar 2]
  (set foo 2 bar 3)
  foo:bar)
```
`3:4`

### Loops
#### for
`for` repeats its body with variables bound to successive items.

```
(let [foo 0]
  (for [i [1 2 3]
    (inc foo i))
  foo)
```
`6`

Multiple sequences may be iterated in parallel.

```
(let [foo 0 bar 0]
  (for [i [1 2 3]
        j [4 5]]
    (inc foo i)
    (inc bar j))

  (say "foo: " foo " bar: " bar))

foo: 6 bar: 9
```

#### while
`while` repeats its body as long as the specified condition is truthy.

```
(let [foo 0]
  (while (< foo 10)
    (inc foo))
  foo)
```

#### break
`break` evaluates its arguments and jumps to the end of the loop.

```
(let [foo 0]
  (while T
    (if (= (inc foo) 10)
      (break
	(say 'break)
	(* foo 2)))))

break
```
`20`

#### next
`next` evaluates its arguments and jumps to the start of next iteration.

```
(let [foo 0]
  (while T
    (if (< (inc foo) 3)
      (next (say 'next)))
      
    (break
      (say 'break)
      (* foo 2))))

next
next
break
```
`20`


### Iterators
`reduce` may be used to transform any iterable into a single value using the specified binary operation and seed value.

```
(^my-sum [in*]
  (iter/reduce + in 0))

(my-sum 1 2 3)
```
`6`

`unzip` may be used to split any iterable of pairs into a pair of lists.

```
(iter/unzip [1:2 3:4])
```
`[1 3]:[2 4]`

### Methods
Methods may be defined using `^`.

```
(^foo [x] 
  x)
  
(foo 42)
```
`42`

#### Arguments
Final arguments suffixed with `?` are optional.

```
(^foo [x y?]
  (say x " " y))

(foo 1 2)
(foo 3)
```
```
1 2
3 _
```

Suffixing the last argument with `*` enables the method to accept a variable number of arguments.

```
(^foo [x*] 
  (+ x*))
  
(foo 35 7)
```

#### Result
By default, the value of the last form is returned.

```
(^foo [x] 
  x)
  
(foo 42)
```
`42`

`return` evaluates its arguments and jumps to the end of the current method.

```
(^foo [] 1 (return 2 3) 4)

(foo)
```
`3`

Methods returning pairs support call site destructuring.

```
(^foo []
  1:2:3)
```

```
(foo:_)
```
`1`

```
(_:_:foo)
```
`3`

```
(_:foo)
```
`2:3`

#### Lambdas
Lambdas may be created by leaving out the method name.

```
(^[] 42)
```
`(Method REPL@1:1)`

### IO
`say` prints its arguments followed by newline to standard output.

```
(say "35+7=" (+ 35 7))

35+7=42
```

### Libraries
`lib` may be used to define/extend namespaces.
```
(lib foo
  (var bar 42))

foo/bar
```
`42`

`import` may be used to pull external bindings into the current namespace.
```
(import f/bar)
bar
```
`42`

The target id may be specified.
```
(import foo:f)
f/bar
```
`42`

### Loading
`include` may be used to emit the content of external files at compile time.

test.eli:
```
42
```
```
(include "test.eli")
```
`42`

`load` may be used to evaluate the content of external files at run time.

test.eli:
```
42
```
```
(load "test.eli")
```
`42`

### Tests
`check` validates that its body produces the specified result.

```
(check 1 2)
```
```
Error in REPL@1:1: Check failed; expected 1, actual: 2
```

### Work
Should you find yourself involved in a software project with interesting non-GenAI challenges and in need of a creative developer/tech/team lead with 40 years of solid experience from different technologies/roles/companies/countries, don't hesitate to get in [touch](mailto:codr7@protonmail.com).