"""
https://projecteuler.net/problem=167

For two positive integers a and b, the Ulam sequence U(a,b) is defined by U(a,b)1 = a, U(a,b)2 = b and for k > 2,
U(a,b)k is the smallest integer greater than U(a,b)(k-1) which can be written in exactly one way as the sum of two
distinct previous members of U(a,b).

For example, the sequence U(1,2) begins with
1, 2, 3 = 1 + 2, 4 = 1 + 3, 6 = 2 + 4, 8 = 2 + 6, 11 = 3 + 8;
5 does not belong to it because 5 = 1 + 4 = 2 + 3 has two representations as the sum of two previous members, likewise
7 = 1 + 6 = 3 + 4.

Find ∑ U(2,2n+1)k for 2 ≤ n ≤10, where k = 10^11.
"""


from collections import defaultdict, namedtuple
from typing import Dict
from time import time


UlamParm = namedtuple('UlamParm', ['diff', 'period'])
max_j = 1
start = time()

def zero():
    return 0


class Ulam2n(object):
    """
    Represents a Ulam(2, 2n + 1) sequence.
    n: As described above
    evens: List of even terms in the sequence. For these sequences, there are only two.
    period_start: Zero-based index start of the periodicity in the terms.
    sum_ctr: Dict of a tally of sums. Keys are the prior sums, Value is the number of times the sum has been
            encountered.
    _seq: The sequence stored as a list.
    """
    # From Finch, On The Regularity of Certain 1-Additive Sequences, Table 1
    ulam_parms: Dict[int, UlamParm] = {
        5: UlamParm(126, 32),
        7: UlamParm(126, 26),
        9: UlamParm(1778, 444),
        11: UlamParm(6510, 1628),
        13: UlamParm(23622, 5906),
        15: UlamParm(510, 80),
        17: UlamParm(507842, 126960),
        19: UlamParm(1523526, 380882),
        21: UlamParm(8388606, 2097152),
        23: UlamParm(4194302, 1047588),
    }

    def __init__(self, n: int):
        super().__init__()
        self.n = n
        self._seq = [2, self.v, 2 + self.v]
        self.evens = [2]
        self.period_start = 0
        self.sum_ctr: Dict[int, int] = defaultdict(zero)

    @property
    def v(self):
        """The "v" term for U(u, v), 2n + 1."""
        return self.n * 2 + 1

    @property
    def diff(self):
        """Difference in sums for successive periods."""
        return self.ulam_parms[self.v].diff

    @property
    def period(self):
        """Period length of the repeating terms."""
        return self.ulam_parms[self.v].period

    @property
    def periodic_terms(self):
        """List of periodic terms."""
        if len(self._seq) < self.period_start:
            return []
        return self._seq[self.period_start:]

    def __getitem__(self, index: int):
        """Ulam number for this sequence at a particular position.

        index: 1-based index of the number
        """
        k = index - 1   # convert to zero-based index
        k_pd = k - self.period_start
        if self.period_start == 0 or k_pd < self.period:
            # Compute the sequence to the desired length
            self._ulam_compute(k)
            # Return result from sequence
            return self._seq[k]
        else:
            # We are in the period
            # Compute the sequence up to the point in the period corresponding to the desired value
            self._ulam_compute((k_pd % self.period) + self.period_start)
            # Use Finch's period and diff values to compute the product
            periodic_product = (k_pd // self.period) * self.diff
            # Then find the base periodic term
            seq_add = self.periodic_terms[k_pd % self.period]
            # And add it to the product
            retval = periodic_product + seq_add
            return retval

    def _ulam_compute(self, i: int):
        """Computes the Ulam sequence up to the zero-based index i."""
        # While the sequence is shorter than the desired length
        while i >= len(self._seq):
            # Get the last term added
            b = self._seq[-1]
            # If we have both even numbers, follow an optimization
            if len(self.evens) == 2:
                if b % 2 == 1:
                    # For an odd b, add only the two even numbers
                    for a in self.evens:
                        self.sum_ctr[a + b] += 1
                else:
                    # For an even b, add only the odd numbers gleaned so far
                    odds = [i for i in self._seq if i % 2 == 1]
                    for a in odds:
                        self.sum_ctr[a + b] += 1
            else:
                # If we do not have both even numbers, just add the last number to all previous
                for a in self._seq[:-1]:
                    self.sum_ctr[a + b] += 1
            # The next value is the smallest of the sums with only one instance encountered.
            new_val = min([k for k, val in self.sum_ctr.items() if val == 1])
            self._seq.append(new_val)
            # Get a list of values larger than new_val from the sum counter, prep for deletion
            sum_ctr_deletes = [k for k in self.sum_ctr.keys() if k <= new_val]
            if new_val % 2 == 0:
                # Found the second even number.
                self.evens.append(new_val)
                # Periodicity starts after this number's index in the sequence.
                self.period_start = len(self._seq)
                # No more even numbers will be found in the sequence or will be computed, so add these to the list for
                # removal.
                sum_ctr_deletes.extend([k for k in self.sum_ctr.keys() if k > new_val and k % 2 == 0])
            # Delete the values from the sum counter.
            for k in sum_ctr_deletes:
                del self.sum_ctr[k]


def main():
    sum = 0
    for n in range(2, 11):
        print(f'Ulam(2, {2 * n + 1})')
        ul = Ulam2n(n)
        print(f'  diff = {ul.diff}, period = {ul.period}')
        print(f'  Need up to {(10**11 - 6) % ul.period} computes in Ulam seq')
        first_sixty = [ul[i] for i in range(1, 62)]
        print(f'  seq: {first_sixty}')
        val = ul[10**11]
        print(f'  U(2, {ul.v})[10**11] = {val}')
        sum += val
    print(f'sum = {sum}')
    print(f'Time taken = {time()-start} sec')


if __name__ == '__main__':
    main()
