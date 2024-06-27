"""<p>The proper divisors of a number are all the divisors excluding the number itself. For example, the proper divisors of $28$ are $1$, $2$, $4$, $7$, and $14$. As the sum of these divisors is equal to $28$, we call it a perfect number.</p>
<p>Interestingly the sum of the proper divisors of $220$ is $284$ and the sum of the proper divisors of $284$ is $220$, forming a chain of two numbers. For this reason, $220$ and $284$ are called an amicable pair.</p>
<p>Perhaps less well known are longer chains. For example, starting with $12496$, we form a chain of five numbers:
$$12496 \to 14288 \to 15472 \to 14536 \to 14264 (\to 12496 \to \cdots)$$</p>
<p>Since this chain returns to its starting point, it is called an amicable chain.</p>
<p>Find the smallest member of the longest amicable chain with no element exceeding one million.</p>"""

from time import perf_counter
from math import ceil, sqrt
from typing import List, Iterator, Optional, Tuple
from primes import primes_from_2_to


MAX_NUM = 10**6


def find_proper_divisors(n: int) -> Iterator[int]:
    """Generate list of proper divisors of n."""
    if n < 1:
        return
    yield 1
    for i in range(2, ceil(sqrt(n)) + 1):
        if n % i == 0:
            yield i
            yield n // i


def find_depth(matrix: List[Optional[int]], i: int) -> Optional[Tuple[int, int]]:
    """Find an amicable chain starting at i. If none exists, return None."""
    chain = []
    # Compute sums of divisors until we encounter an entry already populated.
    while not matrix[i]:
        chain.append(i)
        matrix[i] = sum([j for j in find_proper_divisors(i)])
        if matrix[i] > MAX_NUM:
            break
        i = matrix[i]
    # Learned that a chain can be "entered" via another number.
    # For example, 9464 -> 12496, the starting point for the amicable chain given as an example.
    # A chain list is used to record values of i encountered. We can then find the length of the chain, even if we did
    # not start with that number.
    if i in chain and len(chain) > 1:
        return i, len(chain) - chain.index(i)
    return None


def main():
    #
    # Create matrix of the sums of divisors.
    t0 = perf_counter()
    matrix: List[Optional[int]] = [None] * 10**6
    matrix[0] = 0
    matrix[1] = 0
    min_i = None
    max_depth = None
    #
    # Populate the prime numbers.
    for p in primes_from_2_to(MAX_NUM):
        matrix[p] = 1
    for i in range(2, MAX_NUM):
        if matrix[i]:
            continue
        result = find_depth(matrix, i)
        if result is None:
            continue
        minimum, depth = result
        if max_depth is None or depth > max_depth:
            print('New maximum found:', (minimum, depth))
            min_i = minimum
            max_depth = depth
    tf = perf_counter()
    print('Minimum number found:', min_i, '; max depth:', max_depth)
    print('Time taken:', tf - t0)


if __name__ == '__main__':
    main()
