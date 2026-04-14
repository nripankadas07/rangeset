"""Core RangeSet implementation."""

from typing import Iterable, Tuple
from .errors import RangeSetError

Range = Tuple[int, int]


class RangeSet:
    """Manage sets of non-overlapping integer ranges with merge, intersection, and complement."""

    def __init__(self, ranges: Iterable[Range] = ()) -> None:
        """
        Create a RangeSet from an iterable of (start, end) pairs.

        Args:
            ranges: Iterable of (start, end) tuples (half-open intervals: [start, end))

        Raises:
            RangeSetError: If ranges are invalid or not properly formatted.
        """
        self._ranges: Tuple[Range, ...] = self._merge_ranges(ranges)

    def _validate_range(self, start: int, end: int) -> None:
        """
        Validate that a range is valid (both integers, start < end).

        Args:
            start: Start of range
            end: End of range

        Raises:
            RangeSetError: If range is invalid.
        """
        if not isinstance(start, int) or not isinstance(end, int):
            raise RangeSetError("Range bounds must be integers")
        if start >= end:
            raise RangeSetError("Range start must be less than end")

    def _validate_and_parse_ranges(
        self, ranges: Iterable[Range]
    ) -> list[Range]:
        """
        Parse and validate ranges from input.

        Args:
            ranges: Iterable of (start, end) tuples

        Returns:
            List of validated ranges

        Raises:
            RangeSetError: If any range is invalid.
        """
        result: list[Range] = []
        for r in ranges:
            if not isinstance(r, tuple) or len(r) != 2:
                raise RangeSetError("Each range must be a (start, end) tuple")
            start, end = r
            self._validate_range(start, end)
            result.append((start, end))
        return result

    def _merge_ranges(self, ranges: Iterable[Range]) -> Tuple[Range, ...]:
        """
        Merge overlapping and adjacent ranges.

        Args:
            ranges: Iterable of (start, end) tuples

        Returns:
            Sorted tuple of non-overlapping ranges.
        """
        parsed = self._validate_and_parse_ranges(ranges)
        if not parsed:
            return ()

        sorted_ranges = sorted(parsed)
        merged: list[Range] = []

        for start, end in sorted_ranges:
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))

        return tuple(merged)

    @property
    def ranges(self) -> Tuple[Range, ...]:
        """
        Return tuple of (start, end) pairs in sorted order.

        Returns:
            Immutable tuple of ranges.
        """
        return self._ranges

    def add(self, start: int, end: int) -> "RangeSet":
        """
        Add a range, merging overlaps.

        Args:
            start: Start of range to add
            end: End of range to add

        Returns:
            New RangeSet instance with the added range.

        Raises:
            RangeSetError: If the range is invalid.
        """
        self._validate_range(start, end)
        new_ranges = list(self._ranges) + [(start, end)]
        return RangeSet(new_ranges)

    def remove(self, start: int, end: int) -> "RangeSet":
        """
        Remove a range, splitting as needed.

        Args:
            start: Start of range to remove
            end: End of range to remove

        Returns:
            New RangeSet instance with the removed range.

        Raises:
            RangeSetError: If the range is invalid.
        """
        self._validate_range(start, end)
        new_ranges: list[Range] = []

        for r_start, r_end in self._ranges:
            if end <= r_start or start >= r_end:
                new_ranges.append((r_start, r_end))
            else:
                if r_start < start:
                    new_ranges.append((r_start, start))
                if r_end > end:
                    new_ranges.append((end, r_end))

        return RangeSet(new_ranges)

    def union(self, other: "RangeSet") -> "RangeSet":
        """
        Set union of two RangeSets.

        Args:
            other: Another RangeSet instance

        Returns:
            New RangeSet containing all ranges from both sets.
        """
        all_ranges = list(self._ranges) + list(other._ranges)
        return RangeSet(all_ranges)

    def intersection(self, other: "RangeSet") -> "RangeSet":
        """
        Set intersection of two RangeSets.

        Args:
            other: Another RangeSet instance

        Returns:
            New RangeSet containing only overlapping ranges.
        """
        result: list[Range] = []

        for s_start, s_end in self._ranges:
            for o_start, o_end in other._ranges:
                overlap_start = max(s_start, o_start)
                overlap_end = min(s_end, o_end)
                if overlap_start < overlap_end:
                    result.append((overlap_start, overlap_end))

        return RangeSet(result)

    def complement(self, lower: int, upper: int) -> "RangeSet":
        """
        Complement within [lower, upper).

        Args:
            lower: Lower bound (inclusive)
            upper: Upper bound (exclusive)

        Returns:
            New RangeSet containing the complement.

        Raises:
            RangeSetError: If bounds are invalid.
        """
        self._validate_range(lower, upper)
        result: list[Range] = []
        current = lower

        for r_start, r_end in self._ranges:
            if r_start <= lower:
                current = max(current, r_end)
            elif current < r_start:
                result.append((current, r_start))
                current = r_end
            else:
                current = r_end

        if current < upper:
            result.append((current, upper))

        return RangeSet(result)

    def contains(self, value: int) -> bool:
        """
        Check if a value is contained in the RangeSet.

        Args:
            value: Integer to check

        Returns:
            True if value is in any range, False otherwise.
        """
        for start, end in self._ranges:
            if start <= value < end:
                return True
        return False

    def span(self) -> int:
        """
        Return total number of integers covered.

        Returns:
            Sum of all range sizes.
        """
        return sum(end - start for start, end in self._ranges)

    def is_empty(self) -> bool:
        """
        Check if the RangeSet is empty.

        Returns:
            True if no ranges exist, False otherwise.
        """
        return len(self._ranges) == 0
