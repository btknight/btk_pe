"""https://projecteuler.net/problem=145

Some positive integers n have the property that the sum [ n + reverse(n) ] consists entirely of odd (decimal) digits.
For instance, 36 + 63 = 99 and 409 + 904 = 1313. We will call such numbers reversible; so 36, 63, 409, and 904 are
reversible. Leading zeroes are not allowed in either n or reverse(n).

There are 120 reversible numbers below one-thousand.

How many reversible numbers are there below one-billion (10^9)?
"""


found_numbers = set()


def one_odd_one_even(a: int, b: int):
    if a % 2 == 1 and b % 2 == 0:
        return True
    if a % 2 == 0 and b % 2 == 1:
        return True
    return False


def reversible_num():
    global found_numbers
    for j in range(1, 9):
        i_0 = pow(10, j) + 2
        i_f = pow(10, j + 1) - 1
        print(f'10^{j}: range({i_0}, {i_f})')
        for i in range(i_0, i_f):
            i_len = len(str(i))
            if i not in found_numbers and i % 10 > 0 and one_odd_one_even(i % 10, i // pow(10, i_len - 1)):
                yield i


def reverse_int(num: int):
    rev_int = 0
    while num > 0:
        rev_int *= 10
        rev_int += num % 10
        num = num // 10
    return rev_int


def all_digits_odd(num: int):
    while num > 0:
        if num % 2 == 0:
            return False
        num = num // 10
    return True


def main():
    global found_numbers
    for i in reversible_num():
        rev_i = reverse_int(i)
        if all_digits_odd(i + rev_i):
            #print(f'Found ({i}, {rev_i})')
            found_numbers.add(i)
            found_numbers.add(rev_i)
    print(f'Reversible numbers below 10^9: {len(found_numbers)}')


if __name__ == '__main__':
    main()
