from timeit import Timer

def benchmark(reps, setup, test):
    Timer(test, setup).timeit(reps)
    return Timer(test, setup).timeit(reps)


print('fact', benchmark(10000, '''
def fact(acc, n):
  return acc if n == 1 else fact(n * acc, n - 1)
''',
'fact(1, 900)'))

print('fib ', benchmark(100000, '''
def fib(n, a, b):
  return a if n == 0 else b if n == 1 else fib(n-1, b, a+b)
''',
'fib(80, 0, 1)'))