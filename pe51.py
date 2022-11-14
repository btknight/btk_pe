from itertools import count
from numpy import power
from primes import primesfrom2to
from typing import Set
import logging


MAXDIGITS = 6
lendigits = MAXDIGITS
primes = frozenset(primesfrom2to(power(10, MAXDIGITS + 1) - 1))
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def find_max_match(lendigits: int) -> Set[int]:
    """Finds the maximum length match of the prime digits."""
    logging.debug(f'find_max_match({lendigits})')
    global primes
    max_match = set()
    wc = (1 << lendigits - 1) - 1
    max_wc = wc
    while wc > 0:
        match_gen = gen_match_set(wc, max_wc)
        for match_set in match_gen:
            matches = primes & match_set
            if len(matches) > len(max_match):
                print(f'Found new maximum length match: {sorted(matches)}')
                max_match = matches
        wc -= 1
    return max_match


def gen_match_set(wc: int, max_wc: int):
    inv_wc = ~wc & max_wc
    start = 0
    if inv_wc & (2 ** (num_digits(max_wc) - 1)) > 0:
        start = power(10, num_digits(inv_wc) - 1)
    if num_digits(inv_wc) > 0:
        r = range(start, power(10, num_digits(inv_wc)) - 1)
        logging.debug(f'r: {r}')
        for n in range(start, power(10, num_digits(inv_wc)) - 1):
            n = str(n).zfill(num_digits(inv_wc))
            logging.debug(f'n: {n}')
            yield from gen_output_range(n, wc, max_wc)
    else:
        yield from gen_output_range('', wc, max_wc)


def gen_output_range(n: str, wc: int, max_wc: int):
    start = 0
    # If wildcard includes the first digit
    if wc & (2 ** (num_digits(max_wc) - 1)) > 0:
        # starting range for the wc digits is 1
        start = 1
    wc_range = {str(j) * num_digits(max_wc) for j in range(start, 10)}
    sub_range = {sub_digits(j, n, wc, max_wc) for j in wc_range}
    for j in range(1, 11, 2):
        output_range = {int(i + str(j)) for i in sub_range}
        yield output_range


def num_digits(bitmask: int):
    """Return the number of digits represented by bitmask."""
    num = 0
    while bitmask > 0:
        num += bitmask % 2
        bitmask >>= 1
    return num


def sub_digits(wc_str: str, sub_str: str, wc: int, max_wc: int):
    inv_wc = ~wc & max_wc
    logging.debug(f'sub_digits({wc_str}, {sub_str}, {wc}, {max_wc})')
    if len(wc_str) != num_digits(max_wc):
        raise ValueError('orig_str must be as large as max_wc indicates')
    if len(sub_str) != num_digits(inv_wc):
        raise ValueError('sub_str must be as large as wc indicates')
    map = digit_map(inv_wc, max_wc)
    logging.debug(f'digit_map({inv_wc}, {max_wc}) = {map}')
    output_str = ''
    for i in range(0, len(wc_str)):
        if i in map:
            output_str += sub_str[map[i]]
        else:
            output_str += wc_str[i]
    return output_str


def digit_map(wc: int, max_wc: int):
    next_digit = count(num_digits(wc) - 1, step=-1)
    map = {}
    r = [i for i in range(num_digits(max_wc) - 1, -1, -1)]
    for i in r:
        if wc % 2 == 1:
            map[i] = next(next_digit)
        wc >>= 1
    return map


if __name__ == '__main__':
    for digits in range(2, MAXDIGITS + 1):
        max_match = find_max_match(digits)
        print(f'max_match found: {sorted(max_match)}')
