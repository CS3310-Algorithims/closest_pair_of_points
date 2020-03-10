"""
Group Project - Closest Pair of Points
"""

from closest_pair_point import Point, bf_closest_pair, closest_pair


class Run(object):
    """
    Run closest pair of points program
    """

    def closest_pair(self):
        """Run closest pair of points
        """
        a = Point(2, 3)
        b = Point(12, 30)
        c = Point(40, 50)
        d = Point(5, 1)
        e = Point(12, 10)
        f = Point(3, 4)
        points = [a, b, c, d, e, f]

        print(f"list of points\n{points}\n")

        bf_min_pair = bf_closest_pair(points)
        re_min_pair = closest_pair(points)

        print(f"Bruteforce solution: {bf_min_pair}")
        print(f"Recursive solution: {re_min_pair}")


if __name__ == "__main__":
    Run().closest_pair()
