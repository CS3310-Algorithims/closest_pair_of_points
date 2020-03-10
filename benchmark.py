"""
Benchmark program
"""
import copy
import matplotlib.pyplot as plt
import random
import time

from closest_pair_point import Point, bf_closest_pair, closest_pair


class Benchmark(object):
    """
    Benchmark class:
        - Sorting benchmark
        - Tower of Hanoi benchmark
        - Matrix multiplication benchmark
    """
    random.seed(0)

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
        benchmarks = [self.closest_pair_points]

        # try to convert choice to int
        try:
            choice = int(choice)
        except:
            choice = -1 if choice == "A" or choice == "a" else 0

        # run benchmark methods
        if(choice == -1):
            for i in range(len(benchmarks)):
                benchmarks[i](i + 1)
        elif(choice >= 1 and choice <= len(benchmarks)):
            benchmarks[choice-1](choice)
        else:
            return False

        # show graph and close afterwards
        plt.show()
        plt.close("all")

        return True

    def closest_pair_points(self, fig=1):
        """
        Benchmarks sorting functions

        Parameters
        ----------
        fig (int): Figure number for plot
        """
        sample_size = 13

        # x and y cooardinates for graphs
        n = [2**(i + 1) for i in range(sample_size)]
        timings_bruteforce = []
        timings_recursive = []
        lists_bf = []
        lists_re = []
        bf_answers = []
        re_ansewrs = []

        # generate lists of lists
        print("\nGenerating unique, identical lists for bruteforce and "
              "recursion...")
        for i in range(sample_size):
            # generate unique list of size twice of n[i] using random.sample()
            unique_list = random.sample(range(0, 3 * n[i]), 2 * n[i])
            mid = len(unique_list) // 2

            # generate list of unique Points
            unique_points = [Point(unique_list[i], unique_list[mid + i])
                             for i in range(n[i])]

            # add to benchmarking lists
            lists_bf.append(unique_points)
            lists_re.append(copy.deepcopy(unique_points))

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
            answer = bf_closest_pair(lists_bf[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_bruteforce.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

            # add answer to list
            bf_answers.append(answer)

        # benchmark recursive via lists_copy
        print("\nRECURSIVE\n\n"
              f"{heading1:<{pad_size}} {heading2}\n"
              f"{sep * pad_size:<{pad_size}} {sep * len(heading2)}")

        for i in range(len(lists_re)):
            # benchmarking
            start_time = time.perf_counter()
            answer = closest_pair(lists_re[i])
            end_time = time.perf_counter()

            # add time diff to timings
            duration = end_time - start_time
            timings_recursive.append(duration)

            print(f"{n[i]:<{pad_size}} {duration}")

            # add answer to list
            re_ansewrs.append(answer)

        # verify bruteforce and recursion has same answer
        print("\nChecking pair distances matches from bruteforce against "
              "recursion..")

        answer_dist_matches = True
        for i in range(len(bf_answers)):
            if(bf_answers[i]["distance"] != re_ansewrs[i]["distance"]):
                answer_dist_matches = False
                break

        print(f"All answers match? {answer_dist_matches}")

        # graph results
        plt.figure(fig)
        plt.plot(n, timings_bruteforce, label="Bruteforce")
        plt.plot(n, timings_recursive, label="Recursive")
        plt.xlabel('input size (n)')
        plt.ylabel('timings (seconds)')
        plt.title('Growth Rates: Bruteforce vs Recursion')
        plt.legend()  # show legend


if __name__ == "__main__":
    menu = "\nWhich task to benchmark?\n"\
        "1: Closest Pair of Points\n"\
        "A: Run all benchmarks\n"\
        "X: Exit\n"

    while(True):
        print(menu)
        choice = input()

        if(choice != "X" and choice != "x"):
            # run benchmark with choice number
            valid = Benchmark().run(choice)

            if(not valid):
                print("Invalid choice")
        else:
            break

    print("Exiting benchmark...")
