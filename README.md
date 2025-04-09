# eli

## Introduction
`eli` represents the culmination of more than 15 years of designing and implementing embedded Lisp interpreters in various languages.

It all began with wishing for a nice language to script a personal project, but evolved into one of the deepest rabbit holes I've had the pleasure of falling into.

## Implementations

The following projects implement `eli` in different languges, some are more complete than others. Most work currently happens in [eli-java](https://github.com/codr7/eli-java).

- [C](https://github.com/codr7/alisp)
- [C#](https://github.com/codr7/sharpl)
- [Go](https://github.com/codr7/gfun)
- [Java](https://github.com/codr7/eli-java)
- [Swift](https://github.com/codr7/sweet)

I'm also working on bringing some `eli` magic to [Common Lisp](https://github.com/codr7/cl-eli).

## Performance
I decided early on that Python would make a reasonable performance target to aim for, since it's mostly interpreted and well known.

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
Immutable sequences of characters.
`"abc"`

String literals support the following escapes: `\n` for line break, `"` for double quote, and `\\` for backslash.

#### Sym (Any Comparable)
Quoted identifiers.
`'foo`

#### Time (Any)
Durations of time.

#### Timestamp (Any)
Points in time.
`(now)`

### Truthiness
All types have `Bit` representations, most unconditionally evaluate to `T`; such values are referred to as truthy. Notable exceptions besides `F` are `[]`, `{}` and `_`.

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

Quoted lists become lists of quoted items.

```
'[foo bar baz]
```
`['foo 'bar 'baz]`


Quoted maps only quote the keys.

```
'{a:(+ 1 2) b:(+ 3 4)}
```
`{'a:3 'b:7}`

Courtesy of pairs behaving the same way.

```
'foo:(+ 1 2)
```
`'foo:3`

`,` unquotes the succeding form.

```
(let [foo '(+ 1 2)]
  ,foo)
```
`3`

### Bindings
`var` binds values to identifiers, the value is evaluated at compile time.

```
(var foo 42)
foo
```
`42`

`let` may be used to create scoped runtime bindings,

```
(let [foo 'bar]
  foo)
```
`'bar`

and to locally override existing `var` bindings.

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

`set` updates the value of existing bindings.

```
(let [foo 1 bar 2]
  (set foo 3 bar 4)
  foo:bar)
```
`3:4`

### Value vs. Identity
`=` returns `T` if specified arguments have equal values.

```
(= [1 2 3:4] [1 2 3:4])
```
`T`

While `is` returns `T` only if specified arguments have equal identities.

```
(is [1 2 3:4] [1 2 3:4])
```
`F`

```
(let [foo [1 2 3:4]]
  (is foo foo))
```
`T`

### Sequences
`head` returns the first item in a sequence, or `_` if empty.

```
(head "foo")
```
`\f`

`tail` returns the tail of a sequence, or `_` if empty.

```
(tail '{a:1 b:2 c:3})
```
`{'b:2 'c:3}`

`count` returns the number of items in a sequence, `#` may be used as shorthand.

```
  #7:35:42
```
`3`

### Loops
`loop` repeats its body indefinitely.

```
(let [foo 0]
  (loop
    (if (= (inc foo) 10) (break foo))))
```
`10`

`for` repeats its body with variables bound to successive items from an iterable.
```
(let [foo 0]
  (iter/for [i [1 2 3]
    (inc foo i))
  foo)
```
`6`

Multiple sequences may be iterated in parallel.
```
(let [foo 0 bar 0]
  (iter/for [i [1 2 3]
             j [4 5]]
    (inc foo i)
    (inc bar j))

  foo:bar)
```
`6:9`

`break` evaluates its arguments and jumps to the end of the loop.
```
(let [foo 0]
  (loop T
    (if (= (inc foo) 10)
      (break (* foo 2)))))
```
`20`

`next` evaluates its arguments and jumps to the start of next iteration.
```
(let [foo 0]
  (loop
    (if (< (inc foo) 10)
      (next))
      
    (break (* foo 2))))
```
`20`

### Iterators
`get` may be used to acquire an iterator for any iterable value. `pop` returns the next item or `_`.

```
(let [i (iter/get '[foo bar baz])]
  (iter/pop i))
```
`'foo`

#### Pipelines
`all` returns `T` if all items from a set of iterables pass the predicate, otherwise `F`.
```
(iter/all < [1 2] [3 4])
```
`T`

`any` returns `T` if any items from a set of iterables pass the predicate, otherwise `F`.
```
(iter/any > [1 2 5] [3 4 5])
```
`F`

`comb` returns an iterator for all combinations of items in an iterable.
```
[(iter/comb [1 2 3])*]
```
`[[1] [2] [1 2] [3] [1 3] [2 3] [1 2 3]]`

`cross` returns an iterator for the cross product of two iterables.
```
[(iter/cross + [1 2] [3 4])*]
```
`[4 5 5 6]`

`concat` returns a concatenated iterator for a set of iterables.

```
[(iter/concat [1 2 3] 4:5)*]
```
`[1 2 3 4 5]`

`fold` folds an iterable into a single value using the specified binary operation and seed value.
```
(^my-sum [in*]
  (iter/fold + in 0))

(my-sum 1 2 3)
```
`6`

`map` returns an iterator to a method mapped over a set of iterables.
```
[(iter/map + [1 3] [5 7 11])*]
```
`[6 10]`

`where` returns an iterator to items matching a predicate from a set of iterables.
```
[(iter/where > [1 5 2 6] [1 2 3 4])*]
```
`[5:2 6:4]`

`unzip` splits an iterable of pairs into a pair of lists.
```
(iter/unzip [1:2 3:4])
```
`[1 3]:[2 4]`

`zip` transforms a set of iterables into a pair iterator.
```
[(iter/zip 'foo:'bar:'baz [1 2 3] "abc")*]
```
`['foo:1:\a 'bar:2:\b 'baz:3:\c]`

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

Suffixing the last argument with `*` makes the method accept a variable number of arguments.

```
(^foo [x*] 
  (+ x*))
  
(foo 35 7)
```
`42`

#### Result
By default, the last value is returned.

```
(^foo [x] 
  x)
  
(foo 42)
```
`42`

`return` evaluates its arguments and jumps to the end of the method.

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

#### Overloading
Methods support overloading. When called; the most specific, most recent, matching definition is chosen.

```
(^foo [x]
  (say "x 1"))

(^foo [x y]
  (say "x y"))

(foo 1)

(^foo [x]
  (say "x 2"))

(foo 1)
(foo 1 2)
```
```
x 1
x 2
x y
```

#### Lambdas
Lambdas may be created by leaving out the method name.

```
(^[] 42)
```
`(^repl@1:1 [])`

### Destructuring
All bindings; `let`, `var` and method arguments; support in place destructuring of pairs and maps.

```
(var i:j 1:2)
i:j
```
`1:2`

Maps support two forms; one with implicit keys,

```
(var {foo baz} '{foo:1 bar:2 baz:3})
foo:baz
```
`1:3`

and the other explicit.

```
(var {f:foo b:baz} '{foo:1 bar:2 baz:3})
f:b
```

### Spreading
Lists, maps and method calls support expanding iterable values in place by suffixing with `*`.

```
["abc"*]
```
`[\a \b \c]`

Maps require pair values.

```
(let [foo "abc"]
  {(iter/map (^[i] i:(foo i)) (range 0 3 1))*})
```
`{0:\a 1:\b 2:\c}`

### Type Checking
Expressions may be suffixed with `@` to type check.

```
(+ 35 7)@Numeric
```
`42`

An error is signalled if types aren't compatible.

```
42@String

Error in REPL@1:3: Type check failed, expected String: 42
```

Bindings are supported.

```
(let [foo@Int 42]
  foo]
```
`42`

As well as method arguments, where more specifically typed arguments have higher priority in overload resolution.

```
(^foo [x@Int]
  x)

(foo 42)
```
`42`

### IO
`say` prints its arguments followed by newline to standard output.

```
(say "35+7=" (+ 35 7))

35+7=42
```

### Libraries
`lib` defines/extends namespaces.
```
(lib foo
  (var bar 42))

foo/bar
```
`42`

`import` pulls external bindings into the current namespace.
```
(import f/bar)
bar
```
`42`

The target id may be overridden.
```
(import foo:f)
f/bar
```
`42`

### Loading
test.eli:
```
42
```

`include` emits the content of external files at compile time.

```
(include "test.eli")
```
`42`

`load` evaluates the content of external files at run time.

```
(load "test.eli")
```
`42`

### Debugging
`dump` converts its arguments to readable strings.

```
(dump ['foo "bar" 42])
```
`"['foo \"bar\" 42]"`

### Testing
`check` signals an error if its body doesn't produce the specified result.

```
(check 1 2)
```
```
Error in REPL@1:1: Check failed; expected 1, actual: 2
```

### Work
Should you find yourself involved in a software project with interesting non-GenAI challenges and in need of a creative developer/tech/team lead with 26 years experience, don't hesitate to get in [touch](mailto:codr7@protonmail.com).