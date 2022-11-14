import unittest
from pe51 import *


class PE51Test(unittest.TestCase):
    def test_num_digits(self):
        self.assertEqual(0, num_digits(-1))
        self.assertEqual(0, num_digits(0))
        self.assertEqual(3, num_digits(7))
        self.assertEqual(4, num_digits(15))
        self.assertEqual(4, num_digits(30))
        self.assertEqual(5, num_digits(31))
        self.assertEqual(6, num_digits(63))
        self.assertEqual(7, num_digits(127))
        self.assertEqual(8, num_digits(255))

    def test_digit_map(self):
        self.assertEqual({0: 0, 1: 1, 2: 2, 3: 3}, digit_map(15, 15))
        self.assertEqual({0: 0, 1: 1, 2: 2}, digit_map(14, 15))
        self.assertEqual({0: 0, 1: 1, 3: 2}, digit_map(13, 15))
        self.assertEqual({0: 0, 1: 1}, digit_map(12, 15))
        self.assertEqual({1: 0, 2: 1}, digit_map(6, 15) )

    def test_sub_digits(self):
        self.assertEqual('1993', sub_digits('9999', '13', 6, 15))
        self.assertEqual('9139', sub_digits('9999', '13', 9, 15))

    def test_gen_output_range(self):
        g3 = gen_output_range('', 3, 3)
        g2 = gen_output_range('6', 2, 3)
        self.assertEqual({i for i in range(111, 992, 110)}, next(g3))
        self.assertEqual({i for i in range(161, 962, 100)}, next(g2))

    def test_gen_match_set(self):
        g1 = gen_match_set(1, 3)
        g2 = gen_match_set(2, 3)
        g4 = gen_match_set(1, 31)
        self.assertEqual({i for i in range(101, 912, 100)}, next(g2))
        self.assertEqual({i for i in range(103, 914, 100)}, next(g2))
        self.assertEqual({i for i in range(105, 916, 100)}, next(g2))
        self.assertEqual({i for i in range(101, 192, 10)}, next(g1))
        self.assertEqual({i for i in range(103, 194, 10)}, next(g1))
        self.assertEqual({i for i in range(100001, 100092, 10)}, next(g4))

    def test_find_max_match(self):
        self.assertEqual({13, 23, 43, 53, 73, 83}, find_max_match(2))
        self.assertEqual({56003, 56113, 56333, 56443, 56663, 56773, 56993}, find_max_match(5))
