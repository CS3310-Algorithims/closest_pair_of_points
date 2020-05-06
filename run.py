"""
Group Project: Closest Pair of Points
"""
import os.path

from closest_pair import bf_pairlist_kd, closest_pair_kd,\
    Point, closest_pair_2d_opt_plt


class Run(object):
    """
    Run project
    """
    menu = "\nK-D IMPLEMENTATION\n"\
        "1: List points\n"\
        "2: K-D Bruteforce\n"\
        "3. K-D Recursion\n"\
        "4. 2D Planar matplotlib recursion\n"\
        "5: Change points manually\n"\
        "6: Reduce dimensions\n"\
        "7: Add points from file\n"\
        "8. Remove all points\n"\
        "X: Exit"

    def __init__(self):
        self.dim = 1
        self.points = []

    def setup(self):
        """Run setup"""
        print("\nSETUP\n-----")
        filename = "input.txt"

        print("\nEnter items manually or from file?")
        print("1: Manually")
        print(f"2: From file {filename}")
        print(f"3: From specific file")

        while True:
            choice = self.input()

            if choice == "1":
                print()
                self.change_points()
            elif choice == "2":
                self.add_from_file(filename)
            elif choice == "3":
                self.add_from_file()
            else:
                print("Invalid choice")
                continue
            break

    def start(self):
        """Run user interactive mode"""
        self.setup()

        while True:
            print(self.menu, end="\n")
            choice = self.input()

            if choice == "X" or choice == "x":
                break

            self.clear_screen()

            if choice == "1":
                self.print_points(self.points, "POINTS")
            elif choice == "2":
                self.bruteforce_kd()
            elif choice == "3":
                self.recursion_kd()
            elif choice == "4":
                self.recursion_plt()
            elif choice == "5":
                self.change_points()
            elif choice == "6":
                self.reduce_points()
            elif choice == "7":
                clear = self.input("Clear previous points? (Y/N)")
                if clear == "Y" or clear == "y":
                    self.clear_points()
                self.add_from_file()
            elif choice == "8":
                self.clear_points()
            else:
                self.print_points(self.points, "POINTS")
                pass

    def bruteforce_kd(self):
        """Print all pair combinations via brute force"""
        print("BRUTE FORCE\n")

        if len(self.points) > 1:
            pairs = bf_pairlist_kd(self.points)
            pairs.sort(key=lambda tup: tup[2])
            self.print_pairs(pairs)
        else:
            print("Must have two or more points.")

    def recursion_kd(self):
        """Print the closest pair via divide and conquer"""
        print("RECURSION\n")

        if len(self.points) > 1:
            result = closest_pair_kd(self.points)
            point1, point2 = result['pair']
            dist = result['distance']
            self.print_pairs([(point1, point2, dist)])
        else:
            print("Must have two or more points.")

    def recursion_plt(self):
        """Print the closest pair via divide and conquer"""
        subtitle = "RECURSION WITH MATPLOTLIB\n"
        print(subtitle)

        if len(self.points) > 1:
            # dimension check
            if self.dim != 2:
                print("Dimensions must be 2 for for planar visualizaiton")
                return

            # pause input
            print("Recursion pause time (sec)?")
            pause_t = 1.5
            while True:
                try:
                    pause_t = float(self.input())
                    break
                except:
                    print("Must be a number.")
                    continue

            self.clear_screen()
            print(subtitle)

            # convert self.points to list of Point objects
            plt_points = []
            for point in self.points:
                plt_points.append(Point(*point))

            try:
                result = closest_pair_2d_opt_plt(plt_points, pause_t)
                point1, point2 = result['pair']
                dist = result['distance']
                self.print_pairs([(point1, point2, dist)])
            except:
                print("Matpotlib prematurely closed.")
        else:
            print("Must have two or more points.")

    def sanitize_input(self, data):
        """Return valid float input. Else raises ValueError"""
        if data:
            try:
                data = tuple(map(float, data.split()))
            except:
                raise ValueError("Value must be a number.")
        else:
            raise ValueError("No input.")

        return data

    def pad_point(self, point, dim):
        """Pad a point with 0 up to specified dimension"""
        point_dim = len(point)
        for d in range(point_dim, dim):
            point += (0,)

        return point

    def pad_points(self, points, dim):
        """Pad a list of points with 0 up to specified dimension"""
        for i in range(len(points)):
            points[i] = self.pad_point(points[i], dim)

    def add_point(self, point):
        """Add a point to points"""
        point_dim = len(point)

        # pad point tuple if dimension is less
        if point_dim < self.dim:
            point = self.pad_point(point, self.dim)
        # pad all self.points if new point has greater dimensions
        elif point_dim > self.dim:
            self.pad_points(self.points, point_dim)
            self.dim = point_dim

        if point in self.points:
            raise ValueError("Duplicate point.")
        else:
            self.points.append(point)

    def remove_point(self, point):
        """Remove a point from self.points"""
        try:
            self.points.remove(point)
        except:
            pass

    def change_points(self):
        """Change points manually"""
        err_msg = ""

        while True:
            self.clear_screen()
            self.print_points(self.points, "POINTS")
            print("\nAdd   : A [N] [N] ... [N]"
                  "\nRemove: R [N] [N] ... [N]"
                  "\nEnter X to stop")

            if err_msg:
                print(err_msg)

            data = self.input()

            if data == "X" or data == "x":
                self.clear_screen()
                self.print_points(self.points, "POINTS")
                break
            try:
                point = self.sanitize_input(data[1:])

                if data[0] == "A" or data[0] == "a":
                    self.add_point(point)
                elif data[0] == "R" or data[0] == "r":
                    self.remove_point(point)

                err_msg = ""
            except Exception as err:
                err_msg = "Invalid input. " + str(err)

    def reduce_point(self, point, dim):
        """Reduce a point to specified dimension"""
        return point[:dim] if dim < len(point) else point

    def reduce_points(self):
        """"Reduce all points to specified dimension"""
        # get dimension input
        print("What dimension to reduce to?")
        while True:
            try:
                dim = int(self.input())
                break
            except:
                print("Must be a number.")
                continue

        # reduce all points
        if dim < self.dim:
            for i in range(len(self.points)):
                self.points[i] = self.reduce_point(self.points[i], dim)
                self.dim = dim

        self.clear_screen()
        self.print_points(self.points, "POINTS")

    def add_from_file(self, filename=None):
        """Add to self.points from file"""
        err_msg = ""

        if not filename:
            filename = self.input("Enter file name")

        while not os.path.exists(filename):
            print("Path does not exist.")
            filename = self.input()

        with open(filename) as file:
            print()
            for i, line in enumerate(file):
                try:
                    point = self.sanitize_input(line)
                    if point:
                        self.add_point(point)
                except Exception as err:
                    err_msg += f"\nInvalid input at line {i}. " + str(err)

        self.clear_screen()
        self.print_points(self.points, "POINTS")

        if err_msg:
            print(err_msg)

    def remove_points(self):
        """Remove values in self.points manually"""
        err_msg = ""

        while True:
            self.clear_screen()
            self.print_points(self.points, "POINTS")
            print("\nFormat: [A] [B] ... [N]\nEnter X to stop")

            if err_msg:
                print(err_msg)

            data = self.input()

            if data == "X" or data == "x":
                self.clear_screen()
                self.print_points(self.points, "POINTS")
                break

            try:
                point = self.sanitize_input(data)
                try:
                    self.points.remove(point)
                except:
                    pass
            except Exception as err:
                err_msg = "Invalid input. " + str(err)

    def clear_points(self):
        self.dim = 1
        self.points = []
        print("All points removed.")

    def print_points(self, points, title=None):
        """Print points in tabulated format"""
        if points:
            dim = len(points[0])

            labels = [f"{d+1}D" for d in range(dim)]
            width = 7
            fmt_label = "{:>{w}} " * dim
            fmt_data = "{:>{w}.1f} " * dim

            if title:
                print(title, end="\n\n")

            bar = [width*'-' for _ in range(len(labels))]
            print(fmt_label.format(*labels, w=width))
            print(fmt_label.format(*bar, w=width))

            for point in points:
                print(fmt_data.format(*point, w=width))
        else:
            print("EMPTY")

    def print_pairs(self, pairs, title=None):
        """Print points in tabulated format"""
        if pairs:
            dim = len(pairs[0][0])
            labels = [f"P{p+1}.{d+1}D" for p in range(2) for d in range(dim)]
            labels += ["DIST"]
            width = 7
            fmt_label = "{:>{w}} " * ((2*dim) + 1)
            fmt_data = "{:>{w}.1f} " * ((2*dim) + 1)

            if title:
                print(title, end="\n\n")

            bar = [width*'-' for _ in range(len(labels))]
            print(fmt_label.format(*labels, w=width))
            print(fmt_label.format(*bar, w=width))

            for p1, p2, dist in pairs:
                print(fmt_data.format(*p1, *p2, dist, w=width))
        else:
            print("EMPTY")

    def clear_screen(self):
        import os
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')

    def input(self, msg=None, end="\n"):
        if msg:
            print(msg, end=end)
        return input("> ")


if __name__ == "__main__":
    Run().start()
