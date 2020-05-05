"""
Group Project: Closest Pair of Points
"""
import os.path

from closest_pair_points import bf_pairlist_kd, closest_pair_kd


class Run(object):
    """
    Run project
    """
    menu = "\nK-D IMPLEMENTATION\n"\
        "1: List points\n"\
        "2: Bruteforce\n"\
        "3. Recursion\n"\
        "6: Add points manually\n"\
        "7: Add points from file\n"\
        "8. Remove points\n"\
        "9. Remove all points\n"\
        "X: Exit"

    def __init__(self):
        self.dim = 1
        self.points = []

    def setup(self):
        """Run setup"""
        print("\nSETUP\n-----")
        filename = "input_kd.txt"

        print("\nEnter items manually or from file?")
        print("1: Manually")
        print(f"2: From file {filename}")
        choice = self.input()

        while choice != "1" and choice != "2":
            print("Invalid choice")
            choice = self.input()

        if choice == "1":
            print()
            self.add_manual()
        else:
            self.add_from_file(filename)

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
                self.bruteforce()
            elif choice == "3":
                self.recursion()
            elif choice == "4":
                self.recursion_opt()
            elif choice == "5":
                self.recursion_plt()
            elif choice == "6":
                self.add_manual()
            elif choice == "7":
                clear = self.input("Clear previous points? (Y/N)")
                if clear == "Y" or clear == "y":
                    self.clear_points()
                self.add_from_file()
            elif choice == "8":
                self.remove_points()
            elif choice == "9":
                self.clear_points()
            else:
                self.print_points(self.points, "POINTS")
                pass

    def bruteforce(self):
        """Print all pair combinations via brute force"""
        print("BRUTE FORCE\n")

        if len(self.points) > 1:
            pairs = bf_pairlist_kd(self.points)
            pairs.sort(key=lambda tup: tup[2])
            self.print_pairs(pairs)
        else:
            print("Must have two or more points.")

    def recursion(self):
        """Print the closest pair via divide and conquer"""
        print("RECURSION\n")

        if len(self.points) > 1:
            result = closest_pair_kd(self.points)
            point1, point2 = result['pair']
            dist = result['distance']
            self.print_pairs([(point1, point2, dist)])
        else:
            print("Must have two or more points.")

    def pad_point(self, point, dim):
        point_dim = len(point)
        for d in range(point_dim, dim):
            point += (0,)

        return point

    def pad_points(self, points, dim):
        for i in range(len(points)):
            points[i] = self.pad_point(points[i], dim)

    def add_point(self, point):
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

    def add_manual(self):
        """Add to self.points manually"""
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
                self.add_point(point)
                err_msg = ""
            except Exception as err:
                err_msg = "Invalid input. " + str(err)

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
                    if point in self.points:
                        raise ValueError("Duplicate point.")
                    else:
                        self.points.append(point)
                except Exception as err:
                    err_msg += f"\nInvalid input at line {i}. " + str(err)

        self.clear_screen()
        self.print_points(self.points, "POINTS")

        if err_msg:
            print(err_msg)

    def sanitize_input(self, data):
        """Return valid float input. Else raises ValueError"""
        if data:
            try:
                data = tuple(map(float, data.split()))
            except:
                raise ValueError("Value must be a number.")
        else:
            raise ValueError("Invalid input.")

        return data

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
