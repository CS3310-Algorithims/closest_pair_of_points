"""
Group Project: Closest Pair of Points
"""
import os.path

from closest_pair_points import Point, bf_closest_pair, bf_pairs,\
    closest_pair, closest_pair_plt, closest_pair_opt


class Run(object):
    """
    Run project
    """
    menu = "\nOPTIONS\n"\
        "1: List points\n"\
        "2: Bruteforce\n"\
        "3. Recursion\n"\
        "4. Recursion optimized\n"\
        "5. Recursion with Matplotlib\n"\
        "6: Add points manually\n"\
        "7: Add points from file\n"\
        "8. Remove points\n"\
        "9. Remove all points\n"\
        "X: Exit"

    def __init__(self):
        self.points = []

    def setup(self):
        """Run setup"""
        print("\nSETUP\n-----")

        print("\nEnter items manually or from file?")
        print("1: Manually")
        print("2: From file as input.txt")
        choice = self.input()

        while choice != "1" and choice != "2":
            print("Invalid choice")
            choice = self.input()

        if choice == "1":
            print()
            self.add_manual()
        else:
            self.add_from_file("input.txt")

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

        if self.points:
            pairs = bf_pairs(self.points)
            pairs.sort(key=lambda tup: tup[2])
            self.print_pairs(pairs)
        else:
            print("Must have two or more points.")

    def recursion(self):
        """Print the closest pair via divide and conquer"""
        print("RECURSION\n")

        if self.points:
            result = closest_pair(self.points)
            point1, point2 = result['pair']
            dist = result['distance']
            self.print_pairs([(point1, point2, dist)])
        else:
            print("Must have two or more points.")

    def recursion_plt(self):
        """Matpotlib visual for divide and conquer"""
        subtitle = "RECURSION WITH MATPLOTLIB\n"
        print(subtitle)

        if self.points:
            pause_t = 1.5

            print("Recursion pause time (sec)?")
            while True:
                try:
                    pause_t = float(self.input())
                    break
                except:
                    print("Must be a number.")
                    continue

            self.clear_screen()
            print(subtitle)

            result = closest_pair_plt(self.points, pause_t)
            point1, point2 = result['pair']
            dist = result['distance']
            self.print_pairs([(point1, point2, dist)])
        else:
            print("Must have two or more points.")

    def recursion_opt(self):
        """Print the closest pair via divide and conquer"""
        print("RECURSION OPTIMIZED\n")

        if self.points:
            result = closest_pair_opt(self.points)
            point1, point2 = result['pair']
            dist = result['distance']
            self.print_pairs([(point1, point2, dist)])
        else:
            print("Must have two or more points.")

    def add_manual(self):
        """Add to self.points manually"""
        err_msg = ""

        while True:
            self.clear_screen()
            self.print_points(self.points, "POINTS")
            print("\nFormat: [X] [Y]\nEnter X to stop")

            if err_msg:
                print(err_msg)

            data = self.input()

            if data == "X" or data == "x":
                self.clear_screen()
                self.print_points(self.points, "POINTS")
                break

            try:
                x, y = self.sanitize_input(data)
                point = Point(x, y)

                if point in self.points:
                    raise ValueError("Duplicate point.")
                else:
                    self.points.append(Point(x, y))

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
                    x, y = self.sanitize_input(line)
                    point = Point(x, y)

                    if point in self.points:
                        raise ValueError("Duplicate point.")
                    else:
                        self.points.append(Point(x, y))
                except Exception as err:
                    err_msg += f"\nInvalid input at line {i}. " + str(err)

        self.clear_screen()
        self.print_points(self.points, "POINTS")

        if err_msg:
            print(err_msg)

    def sanitize_input(self, data):
        """Return valid weight, profit input. Else raises ValueError"""
        x, y = 0, 0
        data = data.split()

        if data:
            if len(data) < 2:
                raise ValueError("Missing x.")

            try:
                x, y = float(data[0]), float(data[1])
            except:
                raise ValueError("Value must be a number.")
        else:
            raise ValueError("Invalid input.")

        return x, y

    def remove_points(self):
        """Remove values in self.points manually"""
        err_msg = ""

        while True:
            self.clear_screen()
            self.print_points(self.points, "POINTS")
            print("\nFormat: [X] [Y]\nEnter X to stop")

            if err_msg:
                print(err_msg)

            data = self.input()

            if data == "X" or data == "x":
                self.clear_screen()
                self.print_points(self.points, "POINTS")
                break

            try:
                x, y = self.sanitize_input(data)
                point = Point(x, y)

                try:
                    self.points.remove(point)
                except:
                    pass

                err_msg = ""
            except Exception as err:
                err_msg = "Invalid input. " + str(err)

    def clear_points(self):
        self.points = []
        print("All points removed.")

    def print_points(self, points, title=None):
        """Print points in tabulated format"""
        if points:
            labels = ["X", "Y"]
            width = 7
            fmt_label = "{:>{w}} {:>{w}}"
            fmt_data = "{:>{w}.1f} {:>{w}.1f}"

            if title:
                print(title, end="\n\n")

            bar = [width*'-' for _ in range(len(labels))]
            print(fmt_label.format(*labels, w=width))
            print(fmt_label.format(*bar, w=width))

            for point in points:
                print(fmt_data.format(point.x, point.y, w=width))
        else:
            print("EMPTY")

    def print_pairs(self, pairs, title=None):
        """Print points in tabulated format"""
        if pairs:
            labels = ["X1", "Y1", "X2", "Y2", "DIST"]
            width = 7
            fmt_label = "{:>{w}} {:>{w}} {:>{w}} {:>{w}} {:>{w}}"
            fmt_data = "{:>{w}.1f} {:>{w}.1f} {:>{w}.1f} {:>{w}.1f} {:>{w}.1f}"

            if title:
                print(title, end="\n\n")

            bar = [width*'-' for _ in range(len(labels))]
            print(fmt_label.format(*labels, w=width))
            print(fmt_label.format(*bar, w=width))

            for p1, p2, dist in pairs:
                print(fmt_data.format(p1.x, p1.y, p2.x, p2.y, dist, w=width))
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
