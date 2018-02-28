import unittest

from super_simple_stocks import my_insort_left, my_bisect_left


class TestInsortAndBisect(unittest.TestCase):

    def test_my_insort_left(self):
        ls = [1, 3, 4, 6, 8]

        my_insort_left(ls, 0)
        my_insort_left(ls, 2)
        my_insort_left(ls, 9)

        expected_ls = [0, 1, 2, 3, 4, 6, 8, 9]
        self.assertEqual(ls, expected_ls)

    def test_my_bisect_left(self):
        ls = [1, 3, 4, 6, 8]

        position_1 = my_bisect_left(ls, 0)
        position_2 = my_bisect_left(ls, 2)
        position_3 = my_bisect_left(ls, 9)

        self.assertEqual(position_1, 0)
        self.assertEqual(position_2, 1)
        self.assertEqual(position_3, 5)
