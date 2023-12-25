from comparable import Comparable
from typing import Iterator, Iterable, Callable
from math import floor, log2
from functools import partial
from operator import lt, gt


class MinMaxHeap:
    _arr: list[Comparable]

    def __init__(
        self, value: Iterator[Comparable] | Iterable[Comparable] | None = None
    ) -> None:
        self._arr = [] if value is None else list(value)

        self.heapify()

    def heapify(self) -> None:
        for i in range(len(self._arr) // 2, -1, -1):
            self._push_down(i)

    def push(self, value: Comparable) -> None:
        if not self._arr:
            self._arr.append(value)
            return
        self._arr.append(value)
        self._push_up(len(self._arr) - 1)

    def min(self) -> Comparable:
        if not self._arr:
            raise IndexError("heap has no elements")
        return self._arr[0]

    def max(self) -> Comparable:
        match len(self._arr):
            case 0:
                raise IndexError("heap has no elements")
            case 1:
                return self._arr[0]
            case 2:
                return self._arr[1]
            case other:
                return max(self._arr[1], self._arr[2])

    def pop_min(self) -> Comparable:
        if not self._arr:
            raise IndexError("pop from empty heap")

        length: int = len(self._arr)
        if len(self._arr) == 1:
            return self._arr.pop()

        self._arr[0], self._arr[length - 1] = self._arr[length - 1], self._arr[0]
        min_value: Comparable = self._arr.pop()
        self._push_down(0)
        return min_value

    def pop_max(self) -> Comparable:
        if not self._arr:
            raise IndexError("pop from empty heap")

        length: int = len(self._arr)
        if len(self._arr) == 1:
            return self._arr.pop()

        max_index: int = self._arr.index(self.max())

        self._arr[max_index], self._arr[length - 1] = (
            self._arr[length - 1],
            self._arr[max_index],
        )
        max_value: Comparable = self._arr.pop()
        self._push_down(max_index)

        return max_value

    def _left_child_index(self, i: int) -> int:
        return 2 * i + 1

    def _parent_index(self, i: int) -> int:
        return (i - 1) // 2

    def _grandparent_index(self, i: int) -> int:
        return (i - 3) // 4

    def _has_grandparent(self, i: int) -> bool:
        return i > 2

    def _on_max_depth(self, i: int) -> bool:
        return bool(floor(log2(i + 1)) & 1)

    def _leftmost_grandchild_index(self, i: int) -> int:
        return 4 * i + 3

    def _has_children(self, i: int) -> bool:
        return self._left_child_index(i) < len(self._arr)

    def _has_grandchildren(self, i: int) -> bool:
        return self._leftmost_grandchild_index(i) < len(self._arr)

    def _get_grandchildren_indexes(self, i: int) -> range:
        bounded_min: Callable[[int], int] = lambda x: min(x, len(self._arr))

        return range(
            bounded_min(self._leftmost_grandchild_index(i)),
            bounded_min(self._leftmost_grandchild_index(i) + 4),
        )

    def _push_up(self, i: int) -> None:
        if i == 0:
            return

        def push_up(i: int, not_invariant: Callable[[Comparable, Comparable], bool]):
            while self._has_grandparent(i) and not_invariant(
                self._arr[i], self._arr[grandparent_index := self._grandparent_index(i)]
            ):
                self._arr[i], self._arr[grandparent_index] = (
                    self._arr[grandparent_index],
                    self._arr[i],
                )
                i = grandparent_index

        parent_index = self._parent_index(i)
        parent_value = self._arr[parent_index]
        if self._on_max_depth(i):
            if self._arr[i] < self._arr[parent_index]:
                self._arr[i], self._arr[parent_index] = (
                    self._arr[parent_index],
                    self._arr[i],
                )
                push_up(parent_index, lt)
            else:
                push_up(i, gt)
        else:
            if self._arr[i] > self._arr[parent_index]:
                self._arr[i], self._arr[parent_index] = (
                    self._arr[parent_index],
                    self._arr[i],
                )
                push_up(parent_index, gt)
            else:
                push_up(i, lt)

    def _push_down(self, i: int) -> None:
        def push_down_optimal(i: int, is_min: bool = True) -> int:
            invariant: Callable[[Comparable, Comparable], bool] = lt if is_min else gt

            optimal_index: int = self._left_child_index(i)

            # Right child more optimal
            if optimal_index + 1 < len(self._arr) and invariant(
                self._arr[optimal_index + 1], self._arr[optimal_index]
            ):
                optimal_index += 1

            if not self._has_grandchildren(i):
                if invariant(self._arr[optimal_index], self._arr[i]):
                    self._arr[optimal_index], self._arr[i] = (
                        self._arr[i],
                        self._arr[optimal_index],
                    )
                raise StopIteration("No grandchildren")

            get_optimal_val = min if is_min else max
            optimal_index = get_optimal_val(
                optimal_index,
                get_optimal_val(
                    self._get_grandchildren_indexes(i),
                    key=self._arr.__getitem__,
                    default=optimal_index,
                ),
                key=self._arr.__getitem__,
            )

            if invariant(self._arr[i], self._arr[optimal_index]):
                raise StopIteration(
                    f"i={i} already optimal where {is_min=},{optimal_index=}"
                )

            self._arr[optimal_index], self._arr[i] = (
                self._arr[i],
                self._arr[optimal_index],
            )

            if optimal_index < self._left_child_index(i) + 2:  # Smallest index is child
                raise StopIteration("Grandchildren not optimal")

            optimal_index_parent: int = self._parent_index(optimal_index)
            not_invariant: Callable[[Comparable, Comparable], bool] = (
                gt if is_min else lt
            )

            if not_invariant(self._arr[optimal_index], self._arr[optimal_index_parent]):
                self._arr[optimal_index], self._arr[optimal_index_parent] = (
                    self._arr[optimal_index_parent],
                    self._arr[optimal_index],
                )

            return optimal_index

        try:
            while self._has_children(i):
                if self._on_max_depth(i):
                    i = push_down_optimal(i, False)
                else:
                    i = push_down_optimal(i)
        except StopIteration as e:
            pass
