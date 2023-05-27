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


from itertools import product
import re
from pprint import pprint
from time import time

DIGIT_LEN = 16


def gen_possible_nums(guess_l):
    possible_num_l = []
    # Me fail English? That's unpossible!
    unpossible_num_l = [v for v, c in guess_l if c == 0]
    for i in range(0, DIGIT_LEN):
        unpossible_digit_l = [v[i] for v in unpossible_num_l]
        digits = ''
        for digit in [str(i) for i in range(1 if i == 0 else 0, 10) if str(i) not in unpossible_digit_l]:
            digits += digit
        possible_num_l.append(digits)
    def product_as_str():
        p = product(*possible_num_l[:])
        for digit_t in p:
            digits = ''
            for digit in digit_t:
                digits += digit
            yield digits
    return product_as_str()


def digits_match_guesses(digits, nz_guess_l):
    for v, c in nz_guess_l:
        if count_matches(digits, v) != c:
            return False
    return True


def count_matches(digits, guess):
    matches = 0
    for i in range(len(digits)):
        if digits[i] == guess[i]:
            matches += 1
    return matches


def main():
    guess_l = []
    for line in __doc__.split('\n'):
        guess_m = re.match(r'^ *(\d{%d}) ;(\d) correct' % DIGIT_LEN, line)
        if guess_m:
            guess = (guess_m.group(1), int(guess_m.group(2)))
            guess_l.append(guess)
    pprint(guess_l)
    nz_guess_l = [(v, c) for v, c in guess_l if c > 0]
    product = gen_possible_nums(guess_l)
    for n in product:
        if digits_match_guesses(n, nz_guess_l):
            print(f'Found match: {n}')
            return


if __name__ == '__main__':
    t_0 = time()
    main()
    print(f'Time: {time() - t_0}')
