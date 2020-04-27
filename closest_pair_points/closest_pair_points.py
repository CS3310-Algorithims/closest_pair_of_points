"""
Closest Pair of Point module
    - Point class
    - Bruteforce closest pair of points
    - Recursive closest pair of points
"""
import math
import random


class Point(object):
    """
    Point class of 2d: x and y
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y

    @staticmethod
    def distance(point_a, point_b):
        """Return dist of two points"""
        return math.sqrt((point_a.x - point_b.x)**2 +
                         (point_a.y - point_b.y)**2)

    @staticmethod
    def is_two_pairs_equal(pairs_a, pairs_b):
        """
        Compare if two tuple of Points are equal.

        Parameters
        ----------
        pairs_a (tuple of Points): First tuple of Points
        pairs_b (tuple of Points): Second tuple of Points
        """
        return (pairs_a[0] == pairs_b[0] and pairs_a[1] == pairs_b[1]) or \
            (pairs_a[0] == pairs_b[1] and pairs_a[1] == pairs_b[0])

    @staticmethod
    def get_unique_points(size):
        """Generate list of random and unique points"""
        # generate unique list of size twice of size using random.sample()
        uniques = random.sample(range(0, 3 * size), 2 * size)
        mid = len(uniques) // 2

        return [Point(uniques[i], uniques[mid + i]) for i in range(size)]


def bf_closest_pair(points):
    """
    Wrapper for bruteforce approach to get minimal distance of two points.

    points (list): List of Point

    Return
    ------
    {"distance": float, "pair": Point}
    """
    return bf_closest(points, 0, len(points) - 1)


def bf_closest(points, low, high):
    """
    Bruteforce approach to get minimal distance of two points.
    Minumum size is 2 (high - low >= 1), else exception IndexError is raised.

    Time Complexity: O(n^2)

    Parameters
    ----------
    points (list): List of Point
    low (int): Start index (inclusive)
    high (int): End index (inclusive)

    Return
    ------
    {"distance": float, "pair": Point}
    """
    # raise exception if points is less than 2 elements (high is inclusive)
    if high - low <= 0:
        raise IndexError()

    # set minimal pair as the first two elements
    min_dist = Point.distance(points[low], points[low + 1])
    min_points = (points[low], points[low + 1])

    # iterate if points has more than 2 elements
    if high - low > 1:
        for i in range(low, high):  # skip last element compare b/c redundant
            for j in range(i + 1, high + 1):
                dist = Point.distance(points[i], points[j])

                if dist < min_dist:
                    min_dist = dist
                    min_points = (points[i], points[j])

    return {"distance": min_dist, "pair": min_points}


def bf_pairs(points):
    """
    Creates a permutation list of all pairs of points with distance
    Return [(Point, Point, float)]
    """
    return _bf_pairs(points, 0, len(points) - 1)


def _bf_pairs(points, low, high):
    """
    Creates a permutation list of all pairs of points with distance
    Return [(Point, Point, float)]
    """
    # raise exception if points is less than 2 elements (high is inclusive)
    if high - low <= 0:
        raise IndexError()

    pairs = []

    # iterate if points has more than 2 elements
    if high - low > 1:
        for i in range(low, high):  # skip last element compare b/c redundant
            for j in range(i + 1, high + 1):
                dist = Point.distance(points[i], points[j])
                pairs.append((points[i], points[j], dist))

    return pairs


def closest_pair(points):
    """
    Find closest pair in points using divide and conquer.

    Timsort: O(nlogn)
    Closest: O(nlogn)
    Time Complexity: O(nlogn)

    Return
    ------
    {"distance": float, "pair": Point}
    """
    # sort points by x and y via python's Timsort: O(nlogn)
    points_xsorted = sorted(points, key=lambda point: point.x)
    points_ysorted = sorted(points, key=lambda point: point.y)

    return closest(points_xsorted, 0, len(points_xsorted) - 1, points_ysorted)


def closest(points_xsorted, low, high, points_ysorted):
    """
    Recursively find the closest pair of points in points_xsorted and with
    points_ysorted for the strip in the middle.

    Recurrence relation: T(n) = 2T(n/2) + n
    Time Complexity: O(nlogn)

    Parameters
    ----------
    points_xsorted (list): List of Point sorted by x-coordinate
    low (int): Start index for points_xsorted (inclusive)
    high (int): End index for points_xsorted (inclusive)
    points_ysorted (list): List of Point sorted by y-coordinate

    Return
    ------
    {"distance": float, "pair": Point}
    """
    # base case: use brute force on size 3 or less
    if high - low + 1 <= 3:
        return bf_closest(points_xsorted, low, high)

    # initializations
    mid = (low + high) // 2
    mid_point = points_xsorted[mid]
    points_yleft, points_yright = [], []

    # split points_ysorted by middle of points_xsorted's midpoint
    for point in points_ysorted:
        if point.x <= mid_point.x:
            points_yleft.append(point)
        else:
            points_yright.append(point)

    # recurse to find local minimal pairs on left and right
    min_pair_left = closest(points_xsorted, low, mid, points_yleft)
    min_pair_right = closest(points_xsorted, mid + 1, high, points_yright)

    # get the smaller of the two local minimal pairs
    min_pair = min_of_pairs(min_pair_left, min_pair_right)

    # build strip array to find points smaller than delta from x-coord to mid
    delta = min_pair["distance"]
    strip = []
    for point in points_ysorted:
        if abs(point.x - mid_point.x) < delta:
            strip.append(point)

    # try to find a pair that's smaller than min_pair in the strip
    strip_min_pair = strip_closest(strip, min_pair)

    # return the smaller of min_pair and strip_min_pair
    return min_of_pairs(min_pair, strip_min_pair)


def min_of_pairs(pair_a, pair_b):
    """Return closest pair of Points of two pair of Points"""
    return pair_a if pair_a["distance"] <= pair_b["distance"] else pair_b


def strip_closest(strip, min_pair):
    """
    Find closest pair in strip.

    Recurrence relation: T(n) = 7n
    Time Complexity: O(n)

    Parameters
    ----------
    strip (list): A strip of list of Point of distance from minimal pair
    min_pair (dict): Minimal distance of two Points

    Correctness Proof
    -----------------
    Need to only compare at most 7 comparisons per point by correctness proof

    Let a list be bisected into two halves.
    Let d = delta, the closest pair's distance of two halves in the list.
    Then create a strip from the middle to delta distance on either side.
    This strip has been pre-sorted by y-coordinate.
    Populate points where x-coord from middle to within delta distance.

    Because the points are within d, then in a d x 2d rectangle, there can only
    be 1 point per d/2 x d/2 square.

    Therefore, a point can have at most 7 points to compare to find a new pair
    that's less than delta wide. Points larger than delta wide are irrelevant.
    Because the strip has already been sorted by y-coordinate, you only need
    to iterate a point to 7 other sequential point comparisons.

    Illustration
    ------------
    Let's consider a rectangle of d by 2d in the strip along the middle.
    Let's compare point X to every other point in the rectangle, which is at
    most 7 points.

                  y-coord
                    |
            . . . . | . . . .      
            .       |       .
            .       |       .   <--- strip
            .___ ___|___ ___.   
     d high |_4_|_5_|_6_|_7_|
     ___ ___|_X_|_1_|_2_|_3_|___ ___ x-coord
            .       |       .
            .<-- 2d wide -->.

    Return
    ------
    {"distance": float, "pair": Point}
    """
    strip_min_dist = min_pair["distance"]
    strip_min_points = min_pair["pair"]

    for i in range(len(strip) - 1):  # skip last element compare
        for j in range(i + 1, min(i + 7, len(strip))):
            dist = Point.distance(strip[i], strip[j])

            if dist < strip_min_dist:
                strip_min_dist = dist
                strip_min_points = (strip[i], strip[j])

    return {"distance": strip_min_dist, "pair": strip_min_points}
