import timeit
from typing import Generator, Tuple


# shamelessly klepped from Wikipedia https://en.wikipedia.org/wiki/Farey_sequence
def farey_sequence(n: int, descending: bool = False) -> Generator[Tuple[int, int], None, None]:
    """Print the n'th Farey sequence. Allow for either ascending or descending."""
    (a, b, c, d) = (0, 1, 1, n)
    if descending:
        (a, c) = (1, n - 1)
    yield a, b
    while (c <= n and not descending) or (a > 0 and descending):
        k = (n + b) // d
        (a, b, c, d) = (c, d, k * c - a, k * d - b)
        yield a, b


def sbtree_search(max_q: int, p: int, q: int):
    level = 1
    a, b = (0, 1)
    c, d = (1, 0)
    while True:
        m = a + c
        n = b + d
        if m/n < p/q:
            a, b = (m, n)
        if m/n >= p/q:
            c, d = (m, n)
        if m/n == p/q:
            return level, a, b
        level += 1


def main():
    level = 8
    p, q = (3, 7)
    level, m, n = sbtree_search(level, p, q)
    print(f'level: {level}, {m}/{n}')


if __name__ == '__main__':
    main()
