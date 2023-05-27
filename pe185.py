"""
https://projecteuler.net/problem=185

The game Number Mind is a variant of the well known game Master Mind.

Instead of coloured pegs, you have to guess a secret sequence of digits. After each guess you're only told in how many places you've guessed the correct digit. So, if the sequence was 1234 and you guessed 2036, you'd be told that you have one correct digit; however, you would NOT be told that you also have another digit in the wrong place.

For instance, given the following guesses for a 5-digit secret sequence,

90342 ;2 correct
70794 ;0 correct
39458 ;2 correct
34109 ;1 correct
51545 ;2 correct
12531 ;1 correct

The correct sequence 39542 is unique.

Based on the following guesses,

5616185650518293 ;2 correct
3847439647293047 ;1 correct
5855462940810587 ;3 correct
9742855507068353 ;3 correct
4296849643607543 ;3 correct
3174248439465858 ;1 correct
4513559094146117 ;2 correct
7890971548908067 ;3 correct
8157356344118483 ;1 correct
2615250744386899 ;2 correct
8690095851526254 ;3 correct
6375711915077050 ;1 correct
6913859173121360 ;1 correct
6442889055042768 ;2 correct
2321386104303845 ;0 correct
2326509471271448 ;2 correct
5251583379644322 ;2 correct
1748270476758276 ;3 correct
4895722652190306 ;1 correct
3041631117224635 ;3 correct
1841236454324589 ;3 correct
2659862637316867 ;2 correct

Find the unique 16-digit secret sequence.
"""


from collections import defaultdict
from itertools import cycle
from functools import reduce
import re
from pprint import pprint
from time import time

DIGIT_LEN = 16


def gen_possible_nums(guess_l):
    possible_num_l = []
    for j in range(0, len(guess_l[0][0])):
        def zero():
            return 0
        possible_num_l.append(defaultdict(zero))
    # Me fail English? That's unpossible!
    for guess, count in sorted(guess_l, key=lambda x: -x[1]):
        for i in range(0, len(guess)):
            digit = guess[i]
            if count == 0:
                del possible_num_l[i][digit]
            else:
                possible_num_l[i][digit] += 1
    digits_to_try_l = []
    for j in range(0, len(guess_l[0][0])):
        digits_to_try_l.append([])
        for digit, occ_n in sorted(possible_num_l[j].items(), key=lambda x: -x[1]):
            digits_to_try_l[j].append(digit)
    return digits_to_try_l


class BitmappedCounter(object):
    def __init__(self, bitmap, repeat=False):
        self.bitmap = bitmap
        self.repeat = repeat
        if repeat:
            self.counter = cycle(range(0, 2**self.bitlen))
        else:
            self.counter = (i for i in range(0, 2**self.bitlen))

    @property
    def bitlen(self):
        bitlen = 0
        bitmap = self.bitmap
        while bitmap > 0:
            if bitmap % 2 == 1:
                bitlen += 1
            bitmap >>= 1
        return bitlen

    def map_counter_to_bitmap(self, ctr):
        mapped_ctr = 0
        bit_pos = []
        bitmap = self.bitmap
        i = 0
        while bitmap > 0:
            if bitmap % 2 == 1:
                bit_pos.append(i)
            bitmap >>= 1
            i += 1
        for i in bit_pos:
            mapped_ctr += (ctr % 2) * 2**i
            ctr >>= 1
        return mapped_ctr

    def __iter__(self):
        self.counter = (i for i in range(0, 2**self.bitlen))
        return self

    def __next__(self):
        return self.map_counter_to_bitmap(next(self.counter))


class BMCounterList(object):
    def __init__(self, bitmap_m, length):
        self.length = length
        self.bitmap_m = bitmap_m
        self._init_ctrs()

    def _init_ctrs(self):
        self.ctr_m = []
        self.initial_sent = False
        for i in range(0, len(self.bitmap_m)):
            repeat = i + 1 < len(self.bitmap_m)
            self.ctr_m.append(BitmappedCounter(self.bitmap_m[i], repeat=repeat))
        self.counter_l = [next(bmc) for bmc in self.ctr_m]
        self.counter_l.insert(0, 2 ** self.length - 1)

    def __iter__(self):
        self._init_ctrs()
        return self

    def __next__(self):
        if self.initial_sent:
            self.increment()
        else:
            self.initial_sent = True
        return self.counter_l.copy()

    def increment(self, i: int = 0):
        ctr_val = None
        if i > 0:
            def is_masked_by_next_val(ctr_val):
                if i + 1 == len(self.counter_l):
                    return False
                return reduce(lambda x, y: x | y, self.counter_l[i + 1:]) & ctr_val > 0

            while ctr_val is None or is_masked_by_next_val(ctr_val):
                ctr_val = next(self.ctr_m[i - 1])
                if ctr_val == 0 and i + 1 < len(self.ctr_m):
                    self.increment(i + 1)
        else:
            self.increment(i + 1)
            ctr_val = (2 ** self.length - 1) ^ reduce(lambda x, y: x | y, self.counter_l[i + 1:])
        self.counter_l[i] = ctr_val


def combinator(guess_m):
    pos_m = []
    for j in range(0, len(guess_m)):
        pos_m.append((0, len(guess_m[j])))
    bitmap_m = []
    for i in range(1, max([x[1] for x in pos_m])):
        bitmap = 0
        for start, end in pos_m:
            bitmap <<= 1
            if start <= i < end:
                bitmap += 1
        bitmap_m.append(bitmap)
    bmcl = BMCounterList(bitmap_m, len(pos_m))
    while True:
        bitmap_counter_l = next(bmcl)
        guess = ''
        for i in range(len(guess_m) - 1, -1, -1):
            for k in range(0, len(bitmap_counter_l)):
                if bitmap_counter_l[k] % 2 == 1:
                    guess = guess_m[i][k] + guess
                bitmap_counter_l[k] >>= 1
        yield guess


def num_matches(str1, str2):
    if len(str1) != len(str2):
        raise ValueError(f'str1 and str2 not same length')
    c = 0
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            c += 1
    return c


def main():
    guess_l = []
    for line in __doc__.split('\n'):
        guess_m = re.match(r'^ *(\d{%d}) ;(\d) correct' % DIGIT_LEN, line)
        if guess_m:
            guess = (guess_m.group(1), int(guess_m.group(2)))
            guess_l.append(guess)
    pprint(guess_l)
    guess_m = gen_possible_nums(guess_l)
    pprint(guess_m)
    combos = 1
    for row in guess_m:
        combos *= len(row)
    print(f'Combinations: {combos}')
    cmb = combinator(guess_m)
    while True:
        gen_guess = next(cmb)
        if all([num_matches(gen_guess, g) == c for g, c in guess_l if c > 0]):
            print(f'Found the value: {gen_guess}')
            return


if __name__ == '__main__':
    t_0 = time()
    main()
    print(f'Time: {time() - t_0}')
