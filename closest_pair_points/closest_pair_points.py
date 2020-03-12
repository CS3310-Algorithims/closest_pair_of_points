"""
Closest Pair of Point module
    - Point class
    - Bruteforce closest pair of points
    - Recursive closest pair of points
    - Util to generate a list of random and unique Points
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

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y

    def __ne__(self, o):
        return self.x != o.x or self.y != o.y

    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Point(self.x - o.x, self.y - o.y)

    def __mul__(self, o):
        return Point(self.x * o.x, self.y * o.y)

    def __floordiv__(self, o):
        return Point(self.x // o.x, self.y // o.y)

    def __truediv__(self, o):
        return Point(self.x / o.x, self.y / o.y)

    @staticmethod
    def two_pairs_equal(pairs_a, pairs_b):
        """
        Compare if two tuple of Points are equal.

        Parameters
        ----------
        pairs_a (tuple of Points): First tuple of Points
        pairs_b (tuple of Points): Second tuple of Points
        """
        return pairs_a[0] == pairs_b[0] or pairs_a[0] == pairs_b[1]


def dist(point_a, point_b):
    """Return distance of two points"""
    return math.sqrt(
        math.pow(point_a.x - point_b.x, 2) +
        math.pow(point_a.y - point_b.y, 2)
    )


def bf_closest_pair(list):
    """
    Wrapper for bruteforce approach to get minimal distance of two points in
    list.

    list (list): List of Points

    Return
    ------
    dict of "distance" (float) and "pair" (tuple of Point):
        minimal distance and two Points
    """
    return bf_closest(list, 0, len(list) - 1)


def bf_closest(list, low, high):
    """
    Bruteforce approach to get minimal distance of two points in list.
    Minumum size is 2 (high - low >= 1), else exception IndexError is raised.

    Time Complexity: O(n^2)

    Parameters
    ----------
    list (list): List of Points
    low (int): Start index (inclusive)
    high (int): End index (inclusive)

    Return
    ------
    dict of "distance" (float) and "pair" (tuple of Point):
        minimal distance and two Points
    """
    # raise exception if list is less than 2 elements (high is inclusive)
    if(high - low <= 0):
        raise IndexError()

    # set minimal pair as the first two elements
    min_dist = dist(list[low], list[low + 1])
    min_pair = (list[low], list[low + 1])

    # iterate if list has more than 2 elements
    if(high - low > 1):
        for i in range(low, high):  # skip last element compare b/c redundant
            for j in range(i + 1, high + 1):
                distance = dist(list[i], list[j])

                if(distance < min_dist):
                    min_dist = distance
                    min_pair = (list[i], list[j])

    return {"distance": min_dist, "pair": min_pair}


def closest_pair(list):
    """
    Find closest pair in list.

    Timsort: O(nlogn)
    Closest: O(nlogn)
    Time Complexity: O(nlogn)

    Return
    ------
    dict of "distance" (float) and "pair" (tuple of Point):
        minimal distance and two Points
    """
    # sort list by x and y into distance lists via python's Timsort: O(nlogn)
    list_x = sorted(list, key=lambda e: e.x)
    list_y = sorted(list, key=lambda e: e.y)

    return closest(list_x, 0, len(list_x) - 1, list_y)


def closest(list_x, low, high, list_y):
    """
    Recursively find closest pair of Point in list_x, sorted by x-coordinate
    and list_y, sorted by y-coordinate. Both list_x and list_y are identical
    except sorted by different coordinates.

    Recurrence relation: T(n) = 2T(n/2) + n
    Time Complexity: O(nlogn)

    Parameters
    ----------
    list_x (list): List of Points sorted by x-coordinate
    low (int): Start index for list_x (inclusive)
    high (int): End index for list_x (inclusive)
    list_y: List of Points sorted by y-coordinate

    Return
    ------
    dict of "distance" (float) and "pair" (tuple of Point):
        minimal distance and two Points
    """
    # base case: use brute force on size 3 or less
    if(high - low + 1 <= 3):
        return bf_closest(list_x, low, high)

    # initializations
    mid = (low + high) // 2
    mid_point = list_x[mid]
    list_y_left = []
    list_y_right = []

    # split list_y by middle of list_x's midpoint
    for i in range(len(list_y)):
        if(list_y[i].x <= mid_point.x):
            list_y_left.append(list_y[i])
        else:
            list_y_right.append(list_y[i])

    # recurse
    min_pair_left = closest(list_x, low, mid, list_y_left)
    min_pair_right = closest(list_x, mid + 1, high, list_y_right)

    # get minimal pair of the two parts
    min_pair = min_of_pairs(min_pair_left, min_pair_right)

    # build strip array to find points smaller than delta
    delta = min_pair["distance"]
    strip = []
    for i in range(len(list_y)):
        if(abs(list_y[i].x - mid_point.x) < delta):
            strip.append(list_y[i])

    # get strip's min pair
    strip_min_pair = strip_closest(strip, min_pair)

    # return min of (min_pair, strip_min_pair)
    return min_of_pairs(min_pair, strip_min_pair)


def min_of_pairs(pair_a, pair_b):
    """Return closest pair of Points of two pair of Points"""
    return pair_a if pair_a["distance"] <= pair_b["distance"] else pair_b


def strip_closest(strip_list, min_pair):
    """
    Find closest pair in strip_list

    Recurrence relation: T(n) = 7n
    Time Complexity: O(n)

    Parameters
    ----------
    strip_list (list): A strip of list of Points of distance from minimal pair
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
     d high |_1_|_2_|_3_|_4_|
     ___ ___|_5_|_X_|_6_|_7_|___ ___ x-coord
            .       |       .
            .<-- 2d wide -->.

    Return
    ------
    dict of "distance" (float) and "pair" (tuple of Point):
        minimal distance and two Points
    """
    strip_min_pair = min_pair

    for i in range(len(strip_list) - 1):  # skip last element compare
        for j in range(i + 1, min(i + 7, len(strip_list))):
            # find new strip min pair
            distance = dist(strip_list[i], strip_list[j])

            if(distance < strip_min_pair["distance"]):
                strip_min_pair = {"distance": distance,
                                  "pair": (strip_list[i], strip_list[j])}

    return strip_min_pair


def get_unique_list_points(size):
    """
    Generate list of random and unique points

    Parameters
    ----------
    size (int): size of desired list

    Return
    ------
    list of unique Points
    """
    # generate unique list of size twice of size using random.sample()
    unique_list = random.sample(range(0, 3 * size), 2 * size)
    mid = len(unique_list) // 2

    return [Point(unique_list[i], unique_list[mid + i]) for i in range(size)]
