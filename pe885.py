"""<p>
For a positive integer $d$, let $f(d)$ be the number created by sorting the digits of $d$ in ascending order, removing any zeros. For example, $f(3403) = 334$.</p>

<p>
Let $S(n)$ be the sum of $f(d)$ for all positive integers $d$ of $n$ digits or less. You are given $S(1) = 45$ and $S(5) = 1543545675$.</p>

<p>
Find $S(18)$. Give your answer modulo $1123455689$.</p>"""
from math import log, ceil
from functools import reduce, partial
from time import perf_counter
from typing import Iterator, List


def sum_mod(mod: int, x: int, y: int):
    return (x + y) % mod


def as_digits(n: int, ge: int = 0, le: int = 9, base: int = 10) -> Iterator[int]:
    """Returns individual digits of a number."""
    if n == 0 and ge <= n <= le:
        yield 0
        return
    while n > 0:
        next_n = n % base
        if ge <= next_n <= le:
            yield next_n
        n = n // base


def f(n: int, mod: int) -> int:
    """Function as described in the problem. Breaks apart a number into """
    if n < 10:
        return n
    result = 0
    for d in sorted(as_digits(n, ge=1)):
        result *= 10
        result += d
    return result % mod


def main():
    n = 8
    mod = 1123455689
    sum_mod_112 = partial(sum_mod, mod)
    t0 = perf_counter()
    print(f'S({n}) = ', reduce(sum_mod_112, (f(i, mod) for i in range(1, 10**n))))
    #print(f'S({n}) = ', sum((f(i, mod) for i in range(1, 10**n))))
    tf = perf_counter()
    print('Time taken:', tf - t0)


if __name__ == '__main__':
    main()
