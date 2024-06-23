# https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n/3035188#3035188
import numpy


def primes_from_2_to(n: int) -> numpy.array:
    if not n > 1:
        raise ValueError('n must be greater than 1')
    if n < 7:
        return [i for i in [2, 3, 5] if i <= n]
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = numpy.ones(n // 3 + (n % 6 == 2), dtype=bool)
    for i in range(1, int(n**0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[           k * k // 3         ::2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False
    return numpy.r_[2, 3, ((3 * numpy.nonzero(sieve)[0][1:] + 1) | 1)]
