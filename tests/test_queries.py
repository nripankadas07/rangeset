"""Tests for RangeSet query operations."""

import pytest
from rangeset import RangeSet, RangeSetError


class TestContains:
    """Test RangeSet.contains() operation."""

    def test_contains_empty_set(self) -> None:
        """Empty set should not contain any value."""
        rs = RangeSet()
        assert not rs.contains(0)
        assert not rs.contains(5)
        assert not rs.contains(100)

    def test_contains_single_range_inside(self) -> None:
        """Value inside range should be contained."""
        rs = RangeSet([(1, 10)])
        assert rs.contains(1)
        assert rs.contains(5)
        assert rs.contains(9)

    def test_contains_single_range_outside_left(self) -> None:
        """Value before range should not be contained."""
        rs = RangeSet([(1, 10)])
        assert not rs.contains(0)

    def test_contains_single_range_outside_right(self) -> None:
        """Value at or after range end should not be contained."""
        rs = RangeSet([(1, 10)])
        assert not rs.contains(10)
        assert not rs.contains(11)

    def test_contains_multiple_ranges(self) -> None:
        """Contains should work with multiple ranges."""
        rs = RangeSet([(1, 3), (5, 7), (9, 11)])
        assert rs.contains(1)
        assert rs.contains(2)
        assert not rs.contains(3)
        assert not rs.contains(4)
        assert rs.contains(5)
        assert rs.contains(6)
        assert not rs.contains(7)
        assert not rs.contains(8)
        assert rs.contains(9)
        assert rs.contains(10)
        assert not rs.contains(11)

    def test_contains_boundary_cases(self) -> None:
        """Test boundary values [start, end)."""
        rs = RangeSet([(5, 10)])
        assert rs.contains(5)  # start is included
        assert not rs.contains(10)  # end is excluded

    def test_contains_negative_numbers(self) -> None:
        """Contains should work with negative numbers."""
        rs = RangeSet([(-5, 5)])
        assert rs.contains(-5)
        assert rs.contains(0)
        assert rs.contains(4)
        assert not rs.contains(5)
        assert not rs.contains(-6)

    def test_contains_large_numbers(self) -> None:
        """Contains should work with large numbers."""
        rs = RangeSet([(1000000, 2000000)])
        assert rs.contains(1000000)
        assert rs.contains(1500000)
        assert not rs.contains(2000000)


class TestSpan:
    """Test RangeSet.span() operation."""

    def test_span_empty_set(self) -> None:
        """Span of empty set should be 0."""
        rs = RangeSet()
        assert rs.span() == 0

    def test_span_single_range(self) -> None:
        """Span of single range should be end - start."""
        rs = RangeSet([(1, 5)])
        assert rs.span() == 4

    def test_span_single_unit_range(self) -> None:
        """Span of [n, n+1) should be 1."""
        rs = RangeSet([(5, 6)])
        assert rs.span() == 1

    def test_span_multiple_ranges(self) -> None:
        """Span should sum all ranges."""
        rs = RangeSet([(1, 3), (5, 7), (9, 11)])
        assert rs.span() == 2 + 2 + 2  # 6

    def test_span_negative_ranges(self) -> None:
        """Span should work with negative ranges."""
        rs = RangeSet([(-10, -5)])
        assert rs.span() == 5

    def test_span_crossing_zero(self) -> None:
        """Span should work crossing zero."""
        rs = RangeSet([(-5, 5)])
        assert rs.span() == 10

    def test_span_large_range(self) -> None:
        """Span should work with large ranges."""
        rs = RangeSet([(0, 1000000)])
        assert rs.span() == 1000000

    def test_span_many_ranges(self) -> None:
        """Span should correctly sum many ranges."""
        ranges = [(i * 2, i * 2 + 1) for i in range(100)]
        rs = RangeSet(ranges)
        assert rs.span() == 100


class TestIsEmpty:
    """Test RangeSet.is_empty() operation."""

    def test_is_empty_empty_set(self) -> None:
        """Empty set should return True."""
        rs = RangeSet()
        assert rs.is_empty()

    def test_is_empty_non_empty_single(self) -> None:
        """Single range should return False."""
        rs = RangeSet([(1, 5)])
        assert not rs.is_empty()

    def test_is_empty_non_empty_multiple(self) -> None:
        """Multiple ranges should return False."""
        rs = RangeSet([(1, 3), (5, 7)])
        assert not rs.is_empty()

    def test_is_empty_after_operations(self) -> None:
        """After removing all ranges should be empty."""
        rs = RangeSet([(1, 5)])
        result = rs.remove(1, 5)
        assert result.is_empty()

    def test_is_empty_after_intersection_no_overlap(self) -> None:
        """Intersection with no overlap should be empty."""
        rs1 = RangeSet([(1, 3)])
        rs2 = RangeSet([(5, 7)])
        result = rs1.intersection(rs2)
        assert result.is_empty()
