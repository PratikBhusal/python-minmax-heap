from comparable import Comparable
from min_max_heap import MinMaxHeap


if __name__ == "__main__":
    fizz = MinMaxHeap([9, 28, 40, 12, 30, 19, 34])
    print(fizz._arr)  # [9, 30, 40, 12, 28, 19, 34]
    fizz.push(1)
    print(fizz._arr)  # [1, 30, 40, 9, 28, 19, 34, 12]
    print()

    buzz = MinMaxHeap([34, 12, 28, 9, 30, 19, 1, 40])
    print(buzz._arr)  # [1, 40, 34, 9, 30, 19, 28, 12]
    print(buzz.pop_max())
    print(buzz._arr)  # [1, 30, 34, 9, 12, 19, 28]
