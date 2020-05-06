"""
Unit tests
"""
import copy
import random
import unittest

from closest_pair_points import bf_closest_pair_kd, closest_pair_kd,\
    gen_unique_kd_points
from closest_pair_points.utils import distance


class TestClosestPairKD(unittest.TestCase):
    """
    Tests for cloest pair of points for kth dimensions
    """
    random.seed(0)

    def setUp(self):
        """
        Test setup
        """
        self.dimensions = 3

    def test_list_invalid_raise_exception(self):
        """0 or 1 point should raise exception"""
        for dim in range(1, self.dimensions + 1):
            list_one = gen_unique_kd_points(1, dim)

            with self.assertRaises(IndexError):
                bf_closest_pair_kd([])
                bf_closest_pair_kd(list_one)
                closest_pair_kd([])
                closest_pair_kd(list_one)

    def test_bruteforce_matches_recursion(self):
        """Dimension=1, 2, 3 for points size n from 2 to 100"""
        min_n, max_n = 2, 100
        for dim in range(1, self.dimensions + 1):
            # gen list of lists
            for n in range(min_n, max_n + 1):
                bf_list = gen_unique_kd_points(n, dim)
                re_list = copy.deepcopy(bf_list)

                bf_min = bf_closest_pair_kd(bf_list)
                re_min = closest_pair_kd(re_list)

                self.assertNotEqual(bf_min["distance"], 0)
                self.assertEqual(bf_min["distance"], re_min["distance"])

    def test_bruteforce_matches_recursion_w_dups(self):
        """Dimension=1, 2, 3 for points size n from 2 to 100 with dups"""
        min_n, max_n = 2, 100

        for dim in range(1, self.dimensions + 1):
            # gen list of lists
            for n in range(min_n, max_n + 1):
                bf_list = gen_unique_kd_points(n, dim)
                bf_list.append(copy.deepcopy(bf_list[0]))  # add dup point
                re_list = copy.deepcopy(bf_list)

                bf_min = bf_closest_pair_kd(bf_list)
                re_min = closest_pair_kd(re_list)

                self.assertEqual(bf_min["distance"], 0)
                self.assertEqual(re_min["distance"], 0)

    def test_bruteforce_matches_recursion_n100(self):
        """Dimension=1, 2, 3 for points size n=100 reapeating 100 times"""
        n = 100
        repeat = 100
        for dim in range(1, self.dimensions + 1):
            # gen list of lists
            for i in range(repeat):
                bf_list = gen_unique_kd_points(n, dim)
                re_list = copy.deepcopy(bf_list)

                bf_min = bf_closest_pair_kd(re_list)
                re_min = closest_pair_kd(re_list)

                self.assertNotEqual(bf_min["distance"], 0)
                self.assertEqual(bf_min["distance"], re_min["distance"])


if __name__ == "__main__":
    unittest.main()
