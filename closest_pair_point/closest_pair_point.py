"""
Closest Pair of Point module
    -   Point class
"""

import math
import sys


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


def dist(point_a, point_b):
    """Return distance of two points"""
    return math.sqrt(
        math.pow(point_a.x - point_b.x, 2) +
        math.pow(point_a.y - point_b.y, 2)
    )


def bf_closest_pair(list):
    """
    Wrapper for bruteforce approach to get minimal distance of two points in list.

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
    if(low < high):
        min_dist = sys.maxsize
        min_pair = (list[0], list[1])

        for i in range(low, high + 1):
            for j in range(i + 1, high + 1):
                distance = dist(list[i], list[j])

                if(distance < min_dist):
                    min_dist = distance
                    min_pair = (list[i], list[j])

        return {"distance": min_dist, "pair": min_pair}
    else:
        raise IndexError()


def closest(list_x, low, high, list_y):
    """
    Recursively find closest pair of Point in list_x, sorted by x-coordinate
    and list_y, sorted by y-coordinate. Both list_x and list_y are identical
    except sorted by different coordinates.


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
        if(list_y[i].x < mid_point.x):
            list_y_left.append(list_y[i])
        else:
            list_y_right.append(list_y[i])

    # recurse
    min_pair_left = closest(list_x, low, mid, list_y_left)
    min_pair_right = closest(list_x, mid + 1, high, list_y_right)

    # get minimal pair of the two parts
    min_pair = min_of_pairs(min_pair_left, min_pair_right)

    # build array to find points smaller than min_dist
    strip = []
    for i in range(len(list_y)):
        if(abs(list_y[i].x - mid_point.x) < min_pair["distance"]):
            strip.append(list_y[i])

    # get strip's min pair
    strip_min_pair = strip_closest(strip, min_pair)

    # return min of (min_pair, strip_min_pair)
    return min_of_pairs(min_pair, strip_min_pair)


def min_of_pairs(pair_a, pair_b):
    """Return closest pair of Points of two pair of Points"""
    if(pair_a["distance"] < pair_b["distance"]):
        return pair_a
    else:
        return pair_b


def strip_closest(strip_list, min_pair):
    """
    Find closest pair in strip_list

    Parameters
    ----------
    strip_list (list): A strip of list of Points of distance from minimal pair
    min_pair (dict): Minimal distance of two Points

    Return
    ------
    dict of "distance" (float) and "pair" (tuple of Point):
        minimal distance and two Points
    """
    strip_min_pair = min_pair

    for i in range(len(strip_list)):
        for j in range(i + 1, len(strip_list)):
            # exit if y difference is not less than min pair's distance
            y_diff = abs(strip_list[j].y - strip_list[j].y)
            if(y_diff < min_pair["distance"]):
                break

            # find new strip min pair
            distance = dist(strip_list[i], strip_list[j])
            if(distance < strip_min_pair["distance"]):
                strip_min_pair = {"distance": distance,
                                  "pair": (strip_list[i], strip_list[j])}

    return min_pair


def closest_pair(list):
    """
    Find closest pair in list

    Return
    ------
    dict of "distance" (float) and "pair" (tuple of Point):
        minimal distance and two Points
    """
    # sort list by x and y into distance lists
    list_x = sorted(list, key=lambda e: e.x)
    list_y = sorted(list, key=lambda e: e.y)

    return closest(list_x, 0, len(list_x) - 1, list_y)
