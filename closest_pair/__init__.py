"""
Closest Pair of Points
    XY Plane
    --------
    - closest_pair: Divide and Conquer in xy plane
    - bf_closest_pair: Brute force in xy plane

    Kth Dimensions
    --------------
    - closest_pair_kd: Divide and Conquer in kth dimensions
    - bf_closest_pair_kd: Brute force in kth dimensions

    Point class
    -----------
    Point: A point structure for XY planar implementation
    Point.distance: Calculate distance between two Point objects
    Point.get_unique_points: Generate list of Point in XY plane

    Utilities
    ---------
    distance: Calculate distance between two tuple of the same kth dimensions
    gen_unique_kd_points: Generate tuple points of size n in kth dimensions
"""
from .closest_pair_2d import bf_pairs_2d
from .closest_pair_2d import bf_closest_pair_2d
from .closest_pair_2d import closest_pair_2d
from .closest_pair_2d import closest_pair_2d_opt
from .closest_pair_2d import closest_pair_2d_opt_plt
from .closest_pair_2d import Point

from .closest_pair_kd import bf_pairlist_kd
from .closest_pair_kd import bf_closest_pair_kd
from .closest_pair_kd import closest_pair_kd

from .utils import distance
from .utils import gen_unique_kd_points
