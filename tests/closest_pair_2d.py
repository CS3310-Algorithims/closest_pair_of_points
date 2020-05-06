"""
Unit tests
"""
import copy
import unittest

from closest_pair import Point, bf_closest_pair_2d, closest_pair_2d,\
    closest_pair_2d_opt


class TestClosestPairPlanar(unittest.TestCase):
    """
    Tests for cloest pair of points in XY plane
    """
    # class attributes

    def setUp(self):
        """
        Test setup
        """

    def test_list_invalid_raise_exception(self):
        """0 or 1 point should raise exeption"""
        list_one = [Point(1, 1)]

        with self.assertRaises(IndexError):
            bf_closest_pair_2d([])
            bf_closest_pair_2d(list_one)
            closest_pair_2d([])
            closest_pair_2d(list_one)

    def test_list_two(self):
        """Match 2 points hardcoded list"""
        list_two = [Point(0, 1), Point(1, 0)]

        min_answer = {"distance": Point.distance(
            list_two[0], list_two[1]), "pair": (list_two[0], list_two[1])}
        bf_min = bf_closest_pair_2d(list_two)
        re_min = closest_pair_2d(list_two)
        re_opt_min = closest_pair_2d_opt(list_two)

        self.assertEqual(bf_min, min_answer)
        self.assertEqual(re_min, min_answer)
        self.assertEqual(re_opt_min, min_answer)

    def test_list_three(self):
        """Match 3 points hardcoded list"""
        list_three = [Point(0, 1), Point(2, 3), Point(1, 0)]

        min_answer = {"distance": Point.distance(
            list_three[0], list_three[2]), "pair": (list_three[0], list_three[2])}
        bf_min = bf_closest_pair_2d(list_three)
        re_min = closest_pair_2d(list_three)
        re_opt_min = closest_pair_2d_opt(list_three)

        self.assertEqual(bf_min, min_answer)
        self.assertEqual(re_min, min_answer)
        self.assertEqual(re_opt_min, min_answer)

    def test_list_four(self):
        """Match 4 points hardcoded list"""
        list_four = [Point(0, 1), Point(2, 3), Point(4, 5), Point(1, 0)]

        min_answer = {"distance": Point.distance(
            list_four[0], list_four[3]), "pair": (list_four[0], list_four[3])}
        bf_min = bf_closest_pair_2d(list_four)
        re_min = closest_pair_2d(list_four)
        re_opt_min = closest_pair_2d_opt(list_four)

        self.assertEqual(bf_min, min_answer)
        self.assertEqual(re_min, min_answer)
        self.assertEqual(re_opt_min, min_answer)

    def test_list_duplicate_points(self):
        """Match 4 points with duplicate point hardcoded list"""
        list_dup = [Point(0, 1), Point(2, 3), Point(4, 5), Point(0, 1)]

        min_answer = {"distance": Point.distance(
            list_dup[0], list_dup[3]), "pair": (list_dup[0], list_dup[3])}
        bf_min = bf_closest_pair_2d(list_dup)
        re_min = closest_pair_2d(list_dup)
        re_opt_min = closest_pair_2d_opt(list_dup)

        self.assertEqual(bf_min["distance"], 0)
        self.assertEqual(re_min["distance"], 0)
        self.assertEqual(re_opt_min["distance"], 0)
        self.assertEqual(bf_min, min_answer)
        self.assertEqual(re_min, min_answer)
        self.assertEqual(re_opt_min, min_answer)

    def test_bruteforce_matches_recursion(self):
        """Points size n from 2 to 100"""
        # gen list of lists
        for i in range(5, 100):
            bf_list = Point.get_unique_points(i)
            re_list = copy.deepcopy(bf_list)
            re_opt_list = copy.deepcopy(bf_list)

            bf_min = bf_closest_pair_2d(bf_list)
            re_min = closest_pair_2d(re_list)
            re_opt_min = closest_pair_2d_opt(re_opt_list)

            self.assertNotEqual(bf_min["distance"], 0)
            self.assertEqual(bf_min["distance"], re_min["distance"])
            self.assertEqual(bf_min["distance"], re_opt_min["distance"])

    def test_bruteforce_matches_recursion_w_dups(self):
        """Points size n from 2 to 100 with duplicate point"""
        # gen list of lists
        for i in range(5, 100):
            bf_list = Point.get_unique_points(i)
            bf_list.append(copy.deepcopy(bf_list[0]))  # add duplicate point
            re_list = copy.deepcopy(bf_list)

            bf_min = bf_closest_pair_2d(bf_list)
            re_min = closest_pair_2d(re_list)

            self.assertEqual(bf_min["distance"], 0)
            self.assertEqual(re_min["distance"], 0)

    def test_bruteforce_matches_recursion_n100(self):
        """Points of size n=100 reapeating 100 times"""
        n = 100
        repeat = 100

        # gen list of lists
        for i in range(repeat):
            bf_list = Point.get_unique_points(n)
            re_list = copy.deepcopy(bf_list)
            re_opt_list = copy.deepcopy(bf_list)

            bf_min = bf_closest_pair_2d(re_list)
            re_min = closest_pair_2d(re_list)
            re_opt_min = closest_pair_2d_opt(re_opt_list)

            self.assertNotEqual(bf_min["distance"], 0)
            self.assertEqual(bf_min["distance"], re_min["distance"])
            self.assertEqual(bf_min["distance"], re_opt_min["distance"])

    def test_bruteforce_matches_recursion_vertical_n100(self):
        """Vertical points of size n=100 reapeating 100 times"""
        n = 100
        repeat = 100

        # gen list of lists
        for i in range(repeat):
            bf_list = Point.get_unique_points(n)
            for point in bf_list:
                point.x = 0

            re_list = copy.deepcopy(bf_list)
            re_opt_list = copy.deepcopy(bf_list)

            bf_min = bf_closest_pair_2d(re_list)
            re_min = closest_pair_2d(re_list)
            re_opt_min = closest_pair_2d_opt(re_opt_list)

            self.assertNotEqual(bf_min["distance"], 0)
            self.assertEqual(bf_min["distance"], re_min["distance"])
            self.assertEqual(bf_min["distance"], re_opt_min["distance"])


if __name__ == "__main__":
    unittest.main()
