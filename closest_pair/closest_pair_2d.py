"""
Closest Pair of Points XY Plane
    - closest_pair_2d: Divide and Conquer in xy plane
    - bf_closest_pair_2d: Brute force in xy plane
"""
import math
import random

from .utils import min_of_pairs


class Point(object):
    """
    Point class of 2d: x and y
    """

    def __init__(self, x, y, *args):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError()

    def __len__(self):
        return 2

    @staticmethod
    def distance(point_a, point_b):
        """Return dist of two points"""
        return math.sqrt((point_a.x - point_b.x)**2 +
                         (point_a.y - point_b.y)**2)

    @staticmethod
    def get_unique_points(size):
        """Generate list of random and unique points"""
        x = random.sample(range(-size*10, size*10), size)
        y = random.sample(range(-size*10, size*10), size)
        return [Point(a, b) for a, b in zip(x, y)]


def bf_closest_pair_2d(points):
    """
    Wrapper for bruteforce approach to get minimal distance of two points.

    Parameters
    ----------
    points (list): List of Point

    Return
    ------
    {"distance": float, "pair": Point}
    """
    return bf_closest_2d(points, 0, len(points) - 1)


def bf_closest_2d(points, low, high):
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


def closest_pair_2d(points):
    """
    Find closest_2d pair in points using divide and conquer.

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

    return closest_2d(points_xsorted, 0, len(points_xsorted) - 1, points_ysorted)


def closest_2d(points_xsorted, low, high, points_ysorted):
    """
    Recursively find the closest_2d pair of points in points_xsorted and with
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
        return bf_closest_2d(points_xsorted, low, high)

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
    min_pair_left = closest_2d(points_xsorted, low, mid, points_yleft)
    min_pair_right = closest_2d(points_xsorted, mid + 1, high, points_yright)

    # get the smaller of the two local minimal pairs
    min_pair = min_of_pairs(min_pair_left, min_pair_right)

    # build strip array to find points smaller than delta from x-coord to mid
    delta = min_pair["distance"]
    strip = [p for p in points_ysorted if abs(p.x - mid_point.x) < delta]

    # return min_pair or smaller if found in strip
    return strip_closest_2d(strip, min_pair)


def strip_closest_2d(strip, min_pair):
    """
    Find closest_2d pair in strip. Sparsity geneeralization by Jon Louis Bentley
    and Michael Ian Shamos.

    Time Complexity: O(7n)

    Parameters
    ----------
    strip (list): A strip of list of Points around median within delta
    min_pair (dict): Minimal distance of two Points

    Correctness Proof
    -----------------
    Need to only compare at most 7 comparisons per point by correctness proof

    Let a list be bisected into two halves.
    Let d = delta, the closest_2d pair's distance of two halves in the list.
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


def closest_pair_2d_opt(points):
    """
    Find closest_2d pair in points using divide and conquer using optimized strip
    calculation.
    Optimized version does not consider duplicate points.

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

    return closest_opt(points_xsorted, 0, len(points_xsorted) - 1, points_ysorted)


def closest_opt(points_xsorted, low, high, points_ysorted):
    """
    Recursively find the closest_2d pair of points in points_xsorted and with
    points_ysorted for the strip in the middle.
    Uses optimized strip calculation.

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
        return bf_closest_2d(points_xsorted, low, high)

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
    min_pair_left = closest_opt(points_xsorted, low, mid, points_yleft)
    min_pair_right = closest_opt(points_xsorted, mid + 1, high, points_yright)

    # get the smaller of the two local minimal pairs
    min_pair = min_of_pairs(min_pair_left, min_pair_right)

    # build strip array to find points smaller than delta from x-coord to mid
    delta = min_pair["distance"]
    strip_left = [p for p in points_yleft if abs(p.x - mid_point.x) < delta]
    strip_right = [p for p in points_yright if abs(p.x - mid_point.x) < delta]

    # return min_pair or smaller if found in strip
    return strip_closest_opt(strip_left, strip_right, min_pair)


def strip_closest_opt(strip_left, strip_right, min_pair):
    """
    Find closest_2d pair in strip using hopscotch approach by Jose C. Pereira
    and Fernando G. Lobo.

    Time Complexity: O(2n)

    Parameters
    ----------
    strip_left (list): A strip of Points left side of median within delta.
    strip_right (list): A strip of Points right side of median within delta.
    min_pair (dict): Minimal distance of two Points

    Correctness Proof
    -----------------
    Because each side of median do not need to compare itself, then points
    on each side need only compare points on the opposite side.

    Let d = delta and in a d x 2d box where left is d x d and right is d x d.
    Suppose the left side has a point X of interest and the right side has a
    maximum of 4 points of interest. Then, point X need only to compare the
    closest_2d 2/4 points. The other farther 2 points are larger than delta.
    Similarly, the same reasoning can be applied when right has 3 points.
    Therefore, only 2 comparisons are needed per point on either side.

    Illustration
    ------------
    Let left = {X}, right = {1, 2, 3, 4}.
    Point X to point 1 and point 2 are within delta distance.
    Point X to point 3 and point 4 are larger than delta distance.
    Therefore, X need only compare to point 1 and point 2.

                  y-coord
                    |
            . . . . | . . . .
            .       |       .
            .       |       .   <--- strip
            .___ ___|___ ___.
     d high |___|___|_2_|_3_|
     ___ ___|___|_X_|_1_|_4_|___ ___ x-coord
            .       |       .
            .<-- 2d wide -->.

    NOTE
    ----
    Worse Case Scenario:
    When all points are on the same axis, such as all vertical points
    where x=C for some constant C, then strip_right is empty.
    Because the strip is already by y-coord, then there only need one for loop
    of n comparisons on strip_left.
    Therefore, time complexity is O(n).

    Return
    ------
    {"distance": float, "pair": Point}
    """
    strip_min_dist = min_pair["distance"]
    strip_min_points = min_pair["pair"]

    # if strip_left and strip_right is not empty
    if strip_left and strip_right:
        # init left and right indices
        l, r = 0, 0

        # while there are still points in strip_left or strip_right
        while l < len(strip_left) and r < len(strip_right):
            left, right = strip_left[l], strip_right[r]

            dist = Point.distance(left, right)
            if dist < strip_min_dist:
                strip_min_dist = dist
                strip_min_points = (left, right)

            # if left is lower than or same level as right
            if left.y <= right.y:
                # when there's still point on the otherside
                if r + 1 < len(strip_right):
                    right = strip_right[r+1]

                    dist = Point.distance(left, right)
                    if dist < strip_min_dist:
                        strip_min_dist = dist
                        strip_min_points = (left, right)
                l += 1
            # else right is lower than left
            else:
                # when there's still point on the other side
                if l + 1 < len(strip_left):
                    left = strip_left[l+1]

                    dist = Point.distance(left, right)
                    if dist < strip_min_dist:
                        strip_min_dist = dist
                        strip_min_points = (left, right)
                r += 1
    # else there is only strip_left
    elif strip_left and not strip_right:
        for i in range(len(strip_left) - 1):  # skip last element compare
            dist = Point.distance(strip_left[i], strip_left[i+1])
            if dist < strip_min_dist:
                strip_min_dist = dist
                strip_min_points = (strip_left[i], strip_left[i+1])

    return {"distance": strip_min_dist, "pair": strip_min_points}


# -------------------------------------------
# METHODS BELOW FOR VISUALIZATION RUN PROGRAM
# -------------------------------------------

def bf_pairs_2d(points):
    """
    Creates a permutation list of all pairs of points with distance.
    Used for visual run program.
    Return [(Point, Point, float)]
    """
    return _bf_pairs_2d(points, 0, len(points) - 1)


def _bf_pairs_2d(points, low, high):
    """
    Creates a permutation list of all pairs of points with distance.
    Used for visual run program.
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


def closest_pair_2d_opt_plt(points, pause_t):
    """
    Matplotlib version to show how middle points are selected.
    Used for visual run program.

    Parameters
    pause_t (float): Number of seconds to pause at each recursion
    """
    from matplotlib import pyplot as plt
    from matplotlib.patches import Rectangle, Patch

    # presort points by x-coord and y-coord
    points_xsorted = sorted(points, key=lambda point: point.x)
    points_ysorted = sorted(points, key=lambda point: point.y)

    # matplotlib
    plt.ion()
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.73, 0.75])  # add space for legend

    # add title and legend
    ax.set_title("Divide and Conquer")
    left_patch = Patch(color="aqua", label="Left")
    right_patch = Patch(color="lime", label="Right")
    strip_patch = Patch(color="tomato", label="Strip")
    mid_patch = Patch(color="violet", label="Middle")
    ax.legend(handles=[left_patch, right_patch, strip_patch, mid_patch],
              bbox_to_anchor=(1, 1), loc="upper left", frameon=False)

    # prepare x, y arrays for plot
    plt_x, plt_y = [], []
    for point in points:
        plt_x.append(point.x)
        plt_y.append(point.y)

    # add plot line with scatter style
    ax.plot(plt_x, plt_y, linestyle="None", marker="o", c="black")

    # preadd empty plot line (scatter style) for marking min_pair
    ax.plot([], [], linestyle="None", marker="o", c="black")

    # preadd invis vertical line
    ax.axvline(x=0, linewidth=0, c="violet")

    # preadd invis rectangle to plot
    rect_h = points_ysorted[-1].y - points_ysorted[0].y
    rect = Rectangle(xy=(0, points_ysorted[0].y), width=0, height=rect_h,
                     linewidth=0, color='aqua', fill=False)
    ax.add_patch(rect)

    # do closest_2d pair of points with matplotlib
    min_pair = closest_2d_opt_plt(points_xsorted, 0, len(points_xsorted) - 1,
                                  points_ysorted, ax, pause_t)

    # show plot after recursion
    plt.show(block=True)

    return min_pair


def closest_2d_opt_plt(points_xsorted, low, high, points_ysorted, ax, pause_t):
    """
    Matplotlib version to show minimal pair at each recursion level.
    Used for visual run program.

    Parameters
    ----------
    plt_x (array): 1D array of x values
    plt_y (array): 1D array of y values
    pause_t (float): Number of seconds to pause at each recursion
    rect_y (float): Rectangle lower y coordinate for boundary
    rect_h (float): Rectangle height for boundary
    """
    from matplotlib import pyplot as plt

    # base case: use brute force on size 3 or less
    if high - low + 1 <= 3:
        return bf_closest_2d(points_xsorted, low, high)

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

    # recurse to find local minimal pairs on left
    min_pair_left = closest_2d_opt_plt(points_xsorted, low, mid,
                                       points_yleft, ax, pause_t)

    # get last plot line and rectangle
    line = ax.get_lines()[-2]
    vline = ax.get_lines()[-1]
    rect = ax.patches[-1]

    # plot minimal pair on the left
    min_points = min_pair_left['pair']
    x = [min_points[0].x, min_points[1].x]
    y = [min_points[0].y, min_points[1].y]
    plt.pause(pause_t)
    ax.set_title(f"Midpoint: ({mid_point.x}, {mid_point.y})\n"
                 f"Min left: {min_pair_left['distance']:.2f}\n")
    line.set_data(x, y)
    line.set_color("aqua")

    # draw rectangle boundary
    rect.set_xy((points_xsorted[low].x, rect.get_y()))
    rect.set_linewidth(1)
    rect.set_width(abs(mid_point.x - points_xsorted[low].x))
    rect.set_color("aqua")

    # change vertical line position and make visible
    vline.set_xdata([mid_point.x])
    vline.set_linewidth(1)

    # recurse to find local minimal pairs on right
    min_pair_right = closest_2d_opt_plt(points_xsorted, mid + 1, high,
                                        points_yright, ax, pause_t)

    # plot minimal pair on the right
    min_points = min_pair_right['pair']
    x = [min_points[0].x, min_points[1].x]
    y = [min_points[0].y, min_points[1].y]
    plt.pause(pause_t)
    ax.set_title(f"Midpoint: ({mid_point.x}, {mid_point.y})\n"
                 f"Min right: {min_pair_right['distance']:.2f}\n")
    line.set_data(x, y)
    line.set_color("lime")

    # draw rectangle boundary
    rect.set_xy((mid_point.x, rect.get_y()))
    rect.set_width(abs(mid_point.x - points_xsorted[high].x))
    rect.set_color("lime")

    # change vertical line position
    vline.set_xdata([mid_point.x])

    # get the smaller of the two local minimal pairs
    min_pair = min_of_pairs(min_pair_left, min_pair_right)

    # build strip array to find points smaller than delta from x-coord to mid
    delta = min_pair["distance"]
    strip_left = [p for p in points_yleft if abs(p.x - mid_point.x) < delta]
    strip_right = [p for p in points_yright if abs(p.x - mid_point.x) < delta]

    # try to find a pair that's smaller than min_pair in the strip
    min_pair = strip_closest_opt(strip_left, strip_right, min_pair)

    # plot minimal pair
    min_points = min_pair['pair']
    x = [min_points[0].x, min_points[1].x]
    y = [min_points[0].y, min_points[1].y]
    plt.pause(pause_t)
    ax.set_title(f"Midpoint: ({mid_point.x}, {mid_point.y})\n"
                 f"Combined min: {min_pair['distance']:.2f}\n"
                 f"Delta: {delta:.2f}")
    line.set_data(x, y)
    line.set_color("tomato")

    # draw rectangle boundary
    rect.set_xy((mid_point.x - delta, rect.get_y()))
    rect.set_width(2*delta)
    rect.set_color("tomato")

    # return the smaller of min_pair and strip_min_pair
    return min_pair
