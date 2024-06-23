"""<p>All square roots are periodic when written as continued fractions and can be written in the form:</p>

$\displaystyle \quad \quad \sqrt{N}=a_0+\frac 1 {a_1+\frac 1 {a_2+ \frac 1 {a3+ \dots}}}$

<p>For example, let us consider $\sqrt{23}:$</p>
$\quad \quad \sqrt{23}=4+\sqrt{23}-4=4+\frac 1 {\frac 1 {\sqrt{23}-4}}=4+\frac 1  {1+\frac{\sqrt{23}-3}7}$

<p>If we continue we would get the following expansion:</p>

$\displaystyle \quad \quad \sqrt{23}=4+\frac 1 {1+\frac 1 {3+ \frac 1 {1+\frac 1 {8+ \dots}}}}$

<p>The process can be summarised as follows:</p>
<p>
$\quad \quad a_0=4, \frac 1 {\sqrt{23}-4}=\frac {\sqrt{23}+4} 7=1+\frac {\sqrt{23}-3} 7$<br>
$\quad \quad a_1=1, \frac 7 {\sqrt{23}-3}=\frac {7(\sqrt{23}+3)} {14}=3+\frac {\sqrt{23}-3} 2$<br>
$\quad \quad a_2=3, \frac 2 {\sqrt{23}-3}=\frac {2(\sqrt{23}+3)} {14}=1+\frac {\sqrt{23}-4} 7$<br>
$\quad \quad a_3=1, \frac 7 {\sqrt{23}-4}=\frac {7(\sqrt{23}+4)} 7=8+\sqrt{23}-4$<br>
$\quad \quad a_4=8, \frac 1 {\sqrt{23}-4}=\frac {\sqrt{23}+4} 7=1+\frac {\sqrt{23}-3} 7$<br>
$\quad \quad a_5=1, \frac 7 {\sqrt{23}-3}=\frac {7 (\sqrt{23}+3)} {14}=3+\frac {\sqrt{23}-3} 2$<br>

$\quad \quad a_6=3, \frac 2 {\sqrt{23}-3}=\frac {2(\sqrt{23}+3)} {14}=1+\frac {\sqrt{23}-4} 7$<br>
$\quad \quad a_7=1, \frac 7 {\sqrt{23}-4}=\frac {7(\sqrt{23}+4)} {7}=8+\sqrt{23}-4$<br>
</p>

<p>It can be seen that the sequence is repeating. For conciseness, we use the notation $\sqrt{23}=[4;(1,3,1,8)]$, to indicate that the block (1,3,1,8) repeats indefinitely.</p>

<p>The first ten continued fraction representations of (irrational) square roots are:</p>
<p>
$\quad \quad \sqrt{2}=[1;(2)]$, period=$1$<br>
$\quad \quad \sqrt{3}=[1;(1,2)]$, period=$2$<br>
$\quad \quad \sqrt{5}=[2;(4)]$, period=$1$<br>
$\quad \quad \sqrt{6}=[2;(2,4)]$, period=$2$<br>
$\quad \quad \sqrt{7}=[2;(1,1,1,4)]$, period=$4$<br>
$\quad \quad \sqrt{8}=[2;(1,4)]$, period=$2$<br>
$\quad \quad \sqrt{10}=[3;(6)]$, period=$1$<br>
$\quad \quad \sqrt{11}=[3;(3,6)]$, period=$2$<br>
$\quad \quad \sqrt{12}=[3;(2,6)]$, period=$2$<br>
$\quad \quad \sqrt{13}=[3;(1,1,1,1,6)]$, period=$5$
</p>
<p>Exactly four continued fractions, for $N \le 13$, have an odd period.</p>
<p>How many continued fractions for $N \le 10\,000$ have an odd period?</p>
"""
from time import perf_counter
from math import sqrt
from typing import Iterator


def gen_continued_fraction(x: int) -> Iterator[int]:
    """Generates the integers of the continued fraction of the square root of x.
    Original code that does not give the correct answer."""
    if sqrt(x) - int(sqrt(x)) == 0:
        yield int(sqrt(x))
        return
    i = sqrt(x)
    while True:
        i_int = int(i)
        yield i_int
        i = 1.0 / (i - i_int)


def gen_continued_fraction_ind(x: int) -> Iterator[int]:
    """Generates the integers of the continued fraction of the square root of x. Derived from Pascal's algorithm posted
    at https://math.stackexchange.com/questions/265690/continued-fraction-of-a-square-root."""
    if sqrt(x) - int(sqrt(x)) == 0:
        yield int(sqrt(x))
        return
    a = a0 = int(sqrt(x))
    r = 0
    s = 1
    while True:
        yield a
        r = a * s - r
        s = (x - pow(r, 2)) // s
        a = (r + a0) // s


def cf_period(x: int):
    """Given a number, computes the periodicity of the continued fraction of its square root."""
    period = -1     # ignore first term
    period_end = 2 * int(sqrt(x))
    for i in gen_continued_fraction_ind(x):
        period += 1
        if i == period_end and period > 0:
            break
    return period


def main():
    limit = 10000
    t0 = perf_counter()
    s = sum([1 for i in map(cf_period, range(2, limit + 1)) if i & 1 == 1])
    tf = perf_counter()
    print('Number of square roots with odd periods in their continued fractions:', s)
    print('Time taken:', tf - t0)


if __name__ == '__main__':
    main()
