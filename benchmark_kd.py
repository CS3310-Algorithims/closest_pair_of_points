"""
Benchmark program
"""
import copy
import matplotlib.pyplot as plt
import random
import time

from closest_pair_points import bf_closest_pair_kd, closest_pair_kd,\
    gen_unique_kd_points


class Benchmark(object):
    """
    Benchmark for Closest Pair of Points:
        - Bruteforce
        - Recursion
        - Recursion vertical points
        - Recursion optimized
        - Recursion optimized vertical points
        - Recursion normal vs optimized
        - Bruteforce vs Recursion vs Recursion Optimized
    """
    random.seed(time.time())

    def run(self, choice=-1):
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
            self.bruteforce,
            self.recursion,
            self.bf_vs_recursion
        ]

        # try to convert choice to int
        try:
            choice = int(choice)
        except:
            choice = -1

        # run benchmark methods
        if choice >= 1 and choice <= len(benchmarks):
            while True:
                try:
                    dimensions = int(input("\nWhat dimensions?\n"))
                    break
                except:
                    print("Dimensions must be a number")

            benchmarks[choice-1](dimensions, choice)
        else:
            return False

        # show graph and close afterwards
        plt.show()
        plt.close("all")

        return True

    def bruteforce(self, dim, fig=1):
        """
        Benchmarks bruteforce version of closest pair of points

        Parameters
        ----------
        fig (int): Figure number for plot
        """
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

    def recursion(self, dim, fig=2):
        """
        Benchmarks normal recursion of closest pair of points

        Parameters
        ----------
        fig (int): Figure number for plot
        """
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

    def bf_vs_recursion(self, dim, fig=3):
        """
        Benchmarks bruteforce vs recursion vs recursion optimized of
        closest pair of points

        Parameters
        ----------
        fig (int): Figure number for plot
        """
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
    menu = "\nCLOSEST PAIR OF POINTS\n"\
        "\nWhich task to benchmark?\n"\
        "1: Bruteforce\n"\
        "2: Recursion\n"\
        "3: Bruteforce vs. Recursion\n"\
        "X: Exit\n"

    while True:
        print(menu)
        choice = input()

        if choice != "X" and choice != "x":
            # run benchmark with choice number
            valid = Benchmark().run(choice)

            if not valid:
                print("Invalid choice")
        else:
            break

    print("Exiting benchmark...")
