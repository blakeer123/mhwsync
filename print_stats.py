import pstats
from pstats import SortKey
from sys import argv

if __name__ == "__main__":  
    if len(argv) == 3:
        p = pstats.Stats(argv[1])
        p.sort_stats(SortKey.CUMULATIVE).print_stats(int(argv[2]))

        exit(0)

    else:
        print("usage: print_stats.py <file> <rowcount>")
        exit(1)
