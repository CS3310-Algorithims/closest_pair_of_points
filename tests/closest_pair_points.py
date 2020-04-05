"""
Unit tests
"""
import copy
import unittest

from closest_pair_points import Point, bf_closest_pair, closest_pair


class TestClosestPairPoints(unittest.TestCase):
    """
    Tests for cloest pair of points
    """
    # class attributes

    def setUp(self):
        """
        Test setup
        """

    def test_list_invalid_raise_exception(self):
        """
        Test empty list and list of one Point
        """
        list_one = [Point(1, 1)]

        with self.assertRaises(IndexError):
            bf_closest_pair([])
            bf_closest_pair(list_one)
            closest_pair([])
            closest_pair(list_one)

    def test_list_two(self):
        list_two = [Point(0, 1), Point(1, 0)]

        min_answer = {"distance": Point.distance(
            list_two[0], list_two[1]), "pair": (list_two[0], list_two[1])}
        bf_min = bf_closest_pair(list_two)
        re_min = closest_pair(list_two)

        self.assertEqual(bf_min, min_answer)
        self.assertEqual(re_min, min_answer)

    def test_list_three(self):
        list_three = [Point(0, 1), Point(2, 3), Point(1, 0)]

        min_answer = {"distance": Point.distance(
            list_three[0], list_three[2]), "pair": (list_three[0], list_three[2])}
        bf_min = bf_closest_pair(list_three)
        re_min = closest_pair(list_three)

        self.assertEqual(bf_min, min_answer)
        self.assertEqual(re_min, min_answer)

    def test_list_four(self):
        list_four = [Point(0, 1), Point(2, 3), Point(4, 5), Point(1, 0)]

        min_answer = {"distance": Point.distance(
            list_four[0], list_four[3]), "pair": (list_four[0], list_four[3])}
        bf_min = bf_closest_pair(list_four)
        re_min = closest_pair(list_four)

        self.assertEqual(bf_min, min_answer)
        self.assertEqual(re_min, min_answer)

    def test_list_duplicate_points(self):
        list_dup = [Point(0, 1), Point(2, 3), Point(4, 5), Point(0, 1)]

        min_answer = {"distance": Point.distance(
            list_dup[0], list_dup[3]), "pair": (list_dup[0], list_dup[3])}
        bf_min = bf_closest_pair(list_dup)
        re_min = closest_pair(list_dup)

        self.assertEqual(bf_min["distance"], 0)
        self.assertEqual(re_min["distance"], 0)
        self.assertEqual(bf_min, min_answer)
        self.assertEqual(re_min, min_answer)

    def test_bruteforce_matches_recursion(self):
        # gen list of lists
        for i in range(5, 100):
            bf_list = Point.get_unique_points(i)
            re_list = copy.deepcopy(bf_list)

            bf_min = bf_closest_pair(re_list)
            re_min = closest_pair(re_list)

            self.assertNotEqual(bf_min["distance"], 0)
            self.assertEqual(bf_min["distance"], re_min["distance"])

    def test_bruteforce_matches_recursion_w_dups(self):
        # gen list of lists
        for i in range(5, 100):
            bf_list = Point.get_unique_points(i)
            bf_list.append(copy.deepcopy(bf_list[0]))  # add duplicate point
            re_list = copy.deepcopy(bf_list)

            bf_min = bf_closest_pair(re_list)
            re_min = closest_pair(re_list)

            self.assertEqual(bf_min["distance"], 0)
            self.assertEqual(re_min["distance"], 0)

    def test_bruteforce_matches_recursion_n1000(self):
        n = 1000
        repeat = 100

        # gen list of lists
        for i in range(repeat):
            bf_list = Point.get_unique_points(n)
            re_list = copy.deepcopy(bf_list)

            bf_min = bf_closest_pair(re_list)
            re_min = closest_pair(re_list)

            self.assertNotEqual(bf_min["distance"], 0)
            self.assertEqual(bf_min["distance"], re_min["distance"])


if __name__ == "__main__":
    unittest.main()
