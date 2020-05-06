"""
Benchmark program
"""
import copy
import os
import random
import time
import sys
import matplotlib.pyplot as plt

from closest_pair import Point, bf_closest_pair_2d, closest_pair_2d,\
    closest_pair_2d_opt, bf_closest_pair_kd, closest_pair_kd,\
    gen_unique_kd_points


class Benchmark(object):
    """
    Benchmark for Closest Pair of Points
    """
    random.seed(time.time())
    tasks = [
        "2D Bruteforce",
        "2D Recursion",
        "2D Recursion Vertical",
        "2D Recursion Optimized",
        "2D Recursion Optimized Vertical",
        "2D Recursion Normal VS Optimized",
        "2D Bruteforce VS Recursion",
        "K-D Bruteforce",
        "K-D Recursion",
        "K-D Bruteforce vs Recursion"
    ]

    def menu(self):
        exit_cmd = "X"
        menu = "\nCLOSEST PAIR OF POINTS BENCHMARKS\n"\
            "\nWhich task to benchmark?\n"
        pad = len(str(len(self.tasks)))

        for i, title in enumerate(self.tasks, start=1):
            menu += f"{i:>{pad}}: " + title + "\n"
        menu += f"{exit_cmd:>{pad}}: Exit"

        return menu

    def run(self):
        """
        Run benchmark function by choice option and show graph(s)

        Parameters
        ----------
        choice (int): Benchmark number. -1 to run all benchmarks.

        Return
        ------
        False if invalid choice, else True.
        """
        # array of benchmark methods
        benchmarks = [
            self.bruteforce_2d,
            self.recursion_2d,
            self.recursion_2d_vertical,
            self.recursion_2d_opt,
            self.recursion_2d_opt_vertical,
            self.re_2d_vs_re_2d_opt,
            self.bf_2d_vs_recursion_2d,
            self.bruteforce_kd,
            self.recursion_kd,
            self.bf_kd_vs_recursion_kd
        ]
        menu = self.menu()

        while True:
            try:
                print(menu)
                choice = input("> ")

                if choice == "X" or choice == "x":
                    break

                # try to convert choice to int
                try:
                    choice = int(choice)
                except:
                    choice = -1

                # run benchmark methods
                if choice >= 1 and choice <= len(benchmarks):
                    benchmarks[choice-1](choice)

                    # show graph and close afterwards
                    plt.show()
                    plt.close("all")
            except KeyboardInterrupt:
                print('Interrupted')

    def bruteforce_2d(self, fig=1):
        """
        Benchmarks bruteforce version of closest pair of points

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_bruteforce = []
        lists_bf = []

        # generate lists of lists
        for i in range(sample_size):
            # generate list of unique Points
            unique_points = Point.get_unique_points(n[i])

            # add to benchmarking lists
            lists_bf.append(unique_points)

        # headings variables
        heading1 = "n input"
        heading2 = "timings (seconds)"
        pad_size = len(heading1) if len(
            str(n[-1])) < len(heading1) else len(str(n[-1]))
        sep = "-"

        # benchmark bruteforce via lists
        print("\nBRUTEFORCE\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_bf)):
            # benchmarking
            start_time = time.perf_counter()
            answer = bf_closest_pair_2d(lists_bf[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_bruteforce.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_bruteforce, label="Bruteforce")
        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title('Growth Rates: Bruteforce')
        plt.legend()  # show legend

    def recursion_2d(self, fig=2):
        """
        Benchmarks recursion version of closest pair of points

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_recursion = []
        lists_re = []

        # generate lists of lists
        for i in range(sample_size):
            # generate list of unique Points
            unique_points = Point.get_unique_points(n[i])

            # add to benchmarking lists
            lists_re.append(unique_points)

        # headings variables
        heading1 = "n input"
        heading2 = "timings (seconds)"
        pad_size = len(heading1) if len(
            str(n[-1])) < len(heading1) else len(str(n[-1]))
        sep = "-"

        # benchmark recursion via lists_copy
        print("\nRECURSION\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_re)):
            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair_2d(lists_re[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_recursion.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_recursion, label="Recursion")
        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title('Growth Rates: Recursion')
        plt.legend()  # show legend

    def recursion_2d_vertical(self, fig=3):
        """
        Benchmarks recursion version of closest pair of points with
        vertical points only, ie all points have same x-coord.

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_recursion = []
        lists_re = []

        # generate lists of lists
        for i in range(sample_size):
            # generate list of unique Points
            unique_points = Point.get_unique_points(n[i])

            for point in unique_points:
                point.x = 0

            # add to benchmarking lists
            lists_re.append(unique_points)

        # headings variables
        heading1 = "n input"
        heading2 = "timings (seconds)"
        pad_size = len(heading1) if len(
            str(n[-1])) < len(heading1) else len(str(n[-1]))
        sep = "-"

        # benchmark recursion via lists_copy
        print("\nRECURSION VERTICAL POINTS\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_re)):
            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair_2d(lists_re[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_recursion.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_recursion, label="Recursion Vertical Points")
        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title('Growth Rates: Recursion Vertical Points')
        plt.legend()  # show legend

    def recursion_2d_opt(self, fig=4):
        """
        Benchmarks recursion optimized version of closest pair of points

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_recursion = []
        lists_re = []

        # generate lists of lists
        for i in range(sample_size):
            # generate list of unique Points
            unique_points = Point.get_unique_points(n[i])

            # add to benchmarking lists
            lists_re.append(unique_points)

        # headings variables
        heading1 = "n input"
        heading2 = "timings (seconds)"
        pad_size = len(heading1) if len(
            str(n[-1])) < len(heading1) else len(str(n[-1]))
        sep = "-"

        # benchmark recursion via lists_copy
        print("\nRECURSION OPTIMIZED\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_re)):
            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair_2d_opt(lists_re[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_recursion.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_recursion, label="Recursion Optimized")
        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title('Growth Rates: Recursion Optimized')
        plt.legend()  # show legend

    def recursion_2d_opt_vertical(self, fig=5):
        """
        Benchmarks recursion optimized version of closest pair of points with
        vertical points only, ie all points have same x-coord.

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_recursion = []
        lists_re = []

        # generate lists of lists
        for i in range(sample_size):
            # generate list of unique Points
            unique_points = Point.get_unique_points(n[i])

            for point in unique_points:
                point.x = 0

            # add to benchmarking lists
            lists_re.append(unique_points)

        # headings variables
        heading1 = "n input"
        heading2 = "timings (seconds)"
        pad_size = len(heading1) if len(
            str(n[-1])) < len(heading1) else len(str(n[-1]))
        sep = "-"

        # benchmark recursion via lists_copy
        print("\nRECURSION OPTIMIZED VERTICAL POINTS\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_re)):
            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair_2d_opt(lists_re[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_recursion.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_recursion,
                 label="Recursion Optimized Vertical Points")
        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title('Growth Rates: Recursion Optimized Vertical Points')
        plt.legend()  # show legend

    def re_2d_vs_re_2d_opt(self, fig=6):
        """
        Benchmarks recursion normal vs recursion optimized

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_bruteforce = []
        timings_recursion = []
        lists_re = []
        lists_re_opt = []
        re_answers = []
        re_opt_answers = []

        # generate lists of lists
        print("\nRECURSION VS RECURSION OPTIMIZED\n\n")
        for i in range(sample_size):
            # generate list of unique Points
            unique_points = Point.get_unique_points(n[i])

            # add to benchmarking lists
            lists_re.append(unique_points)
            lists_re_opt.append(copy.deepcopy(unique_points))

        # headings variables
        heading1 = "n input"
        heading2 = "timings (seconds)"
        pad_size = len(heading1) if len(
            str(n[-1])) < len(heading1) else len(str(n[-1]))
        sep = "-"

        # benchmark bruteforce via lists
        print("\nRECURSION\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_re)):
            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair_2d(lists_re[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_bruteforce.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

            # add answer to list
            re_answers.append(answer)

        # benchmark recursion via lists_copy
        print("\nRECURSION OPTIMIZED\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_re_opt)):
            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair_2d_opt(lists_re_opt[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_recursion.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

            # add answer to list
            re_opt_answers.append(answer)

        # verify bruteforce and recursion has same answer
        print("\nChecking pair distances matches from normal against "
              "optimized...")

        answer_dist_matches = True
        for i in range(len(re_answers)):
            if re_answers[i]["distance"] != re_opt_answers[i]["distance"]:
                answer_dist_matches = False
                break

        print(f"All answers match? {answer_dist_matches}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_bruteforce, label="Recursion")
        plt.plot(n, timings_recursion, label="Recursion Optimized")
        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title('Growth Rates: Recursion vs Recursion Optimized')
        plt.legend()  # show legend

    def bf_2d_vs_recursion_2d(self, fig=7):
        """
        Benchmarks bruteforce vs recursion vs recursion optimized of
        closest pair of points

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_bruteforce = []
        timings_recursion = []
        timings_recursion_opt = []
        lists_bf = []
        lists_re = []
        lists_re_opt = []
        bf_answers = []
        re_answers = []
        re_opt_answers = []

        # generate lists of lists
        print("\nBRUTEFORCE VS RECURSION VS RECURSION OPTIMIZED\n\n")
        for i in range(sample_size):
            # generate list of unique Points
            unique_points = Point.get_unique_points(n[i])

            # add to benchmarking lists
            lists_bf.append(unique_points)
            lists_re.append(copy.deepcopy(unique_points))
            lists_re_opt.append(copy.deepcopy(unique_points))

        # headings variables
        heading1 = "n input"
        heading2 = "timings (seconds)"
        pad_size = len(heading1) if len(
            str(n[-1])) < len(heading1) else len(str(n[-1]))
        sep = "-"

        # benchmark bruteforce via lists
        print("\nBRUTEFORCE\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_bf)):
            # benchmarking
            start_time = time.perf_counter()
            answer = bf_closest_pair_2d(lists_bf[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_bruteforce.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

            # add answer to list
            bf_answers.append(answer)

        # benchmark recursion via lists_copy
        print("\nRECURSION\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_re)):
            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair_2d(lists_re[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_recursion.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

            # add answer to list
            re_answers.append(answer)

        # benchmark recursion via lists_copy
        print("\nRECURSION OPTIMIZED\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_re_opt)):
            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair_2d_opt(lists_re[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_recursion_opt.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

            # add answer to list
            re_opt_answers.append(answer)

        # verify bruteforce and recursion has same answer
        print("\nChecking pair distances matches from bruteforce against "
              "recursion...")

        answer_dist_matches = True
        for i in range(len(bf_answers)):
            if bf_answers[i]["distance"] != re_answers[i]["distance"] and\
                    bf_answers[i]["distance"] != re_opt_answers[i]["distance"]:
                answer_dist_matches = False
                break

        print(f"All answers match? {answer_dist_matches}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_bruteforce, label="Bruteforce")
        plt.plot(n, timings_recursion, label="Recursion")
        plt.plot(n, timings_recursion_opt, label="Recursion Optimized")
        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title('Growth Rates: Bruteforce vs Recursion'
                  'vs Recursion Optimized')
        plt.legend()  # show legend

    def bruteforce_kd(self, fig=8):
        """
        Benchmarks bruteforce version of closest pair of points

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        dim = None
        print("\nWhat dimension?")
        while True:
            try:
                dim = int(input("> "))
                break
            except:
                print("Dimensions must be a number")

        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_bf = []

        # headings variables
        heading1 = "n input"
        heading2 = "timings (seconds)"
        pad_size = len(heading1) if len(
            str(n[-1])) < len(heading1) else len(str(n[-1]))
        sep = "-"

        # benchmark bruteforce via lists
        print(f"\nBRUTEFORCE {dim}D\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        # generate lists of lists
        for i in range(sample_size):
            # create list of points
            points = gen_unique_kd_points(n[i], dim)

            # benchmarking
            start_time = time.perf_counter()
            answer = bf_closest_pair_kd(points)
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_bf.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_bf, label=f"Bruteforce {dim}D")

        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title(f'Growth Rates: Bruteforce {dim}D')
        plt.legend()  # show legend

    def recursion_kd(self, fig=9):
        """
        Benchmarks normal recursion of closest pair of points

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        dim = None
        print("\nWhat dimension?")
        while True:
            try:
                dim = int(input("> "))
                break
            except:
                print("Dimensions must be a number")

        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_recur = []

        # headings variables
        heading1 = "n input"
        heading2 = "timings (seconds)"
        pad_size = len(heading1) if len(
            str(n[-1])) < len(heading1) else len(str(n[-1]))
        sep = "-"

        # benchmark recursion via lists
        print(f"\nRECURSION {dim}D\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        # generate lists of lists
        for i in range(sample_size):
            # create list of points
            points = gen_unique_kd_points(n[i], dim)

            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair_kd(points)
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_recur.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_recur, label=f"Recursion {dim}D")
        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title(f'Growth Rates: Recursion {dim}D')
        plt.legend()  # show legend

    def bf_kd_vs_recursion_kd(self, fig=10):
        """
        Benchmarks bruteforce vs recursion vs recursion optimized of
        closest pair of points

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        dim = None
        print("\nWhat dimension?")
        while True:
            try:
                dim = int(input("> "))
                break
            except:
                print("Dimensions must be a number")

        print(f"\nBRUTEFORCE VS RECURSION {dim}D")

        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_bf = []
        timings_recur = []
        lists_bf = []
        lists_re = []
        bf_answers = []
        re_answers = []
        re_opt_answers = []

        for i in range(sample_size):
            # generate list of unique Points
            points = gen_unique_kd_points(n[i], dim)

            # add to benchmarking lists
            lists_bf.append(points)
            lists_re.append(copy.deepcopy(points))

        # headings variables
        heading1 = "n input"
        heading2 = "timings (seconds)"
        pad_size = len(heading1) if len(
            str(n[-1])) < len(heading1) else len(str(n[-1]))
        sep = "-"

        # benchmark bruteforce via lists
        print(f"\nBRUTEFORCE {dim}D\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_bf)):
            # benchmarking
            start_time = time.perf_counter()
            answer = bf_closest_pair_kd(lists_bf[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_bf.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

            # add answer to list
            bf_answers.append(answer)

        # benchmark recursion via lists_copy
        print(f"\nRECURSION {dim}D\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_re)):
            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair_kd(lists_re[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_recur.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

            # add answer to list
            re_answers.append(answer)

        # verify bruteforce and recursion has same answer
        print("\nChecking pair distances matches from bruteforce against "
              "recursion...")

        answer_dist_matches = True
        for i in range(len(bf_answers)):
            if bf_answers[i]["distance"] != re_answers[i]["distance"] and\
                    bf_answers[i]["distance"] != re_opt_answers[i]["distance"]:
                answer_dist_matches = False
                break

        print(f"All answers match? {answer_dist_matches}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_bf, label=f"Bruteforce {dim}D")
        plt.plot(n, timings_recur, label=f"Recursion {dim}D")
        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title(f'Growth Rates: Bruteforce vs Recursion {dim}D')
        plt.legend()  # show legend


if __name__ == "__main__":
    Benchmark().run()
