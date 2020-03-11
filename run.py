"""
Group Project - Closest Pair of Points
"""

from closest_pair_points import Point, bf_closest_pair, closest_pair


class Run(object):
    """
    Run closest pair of points program
    """

    def closest_pair(self):
        """Run closest pair of points
        """
        points = [Point(5, 2), Point(3, 2), Point(7, 1), Point(
            5, 7), Point(3, 5), Point(6, 7), Point(5, 5), Point(3, 1)]

        print(f"list of points\n{points}\n")

        bf_min_pair = bf_closest_pair(points)
        re_min_pair = closest_pair(points)

        print(f"Bruteforce solution: {bf_min_pair}")
        print(f"Recursive solution: {re_min_pair}")


if __name__ == "__main__":
    Run().closest_pair()
