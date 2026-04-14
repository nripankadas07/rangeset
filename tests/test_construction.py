"""Tests for RangeSet construction and initialization."""

import pytest
from rangeset import RangeSet, RangeSetError


class TestConstruction:
    """Test RangeSet initialization."""

    def test_empty_construction(self) -> None:
        """Empty RangeSet should have no ranges."""
        rs = RangeSet()
        assert rs.ranges == ()
        assert rs.is_empty()

    def test_single_range(self) -> None:
        """Construct with a single range."""
        rs = RangeSet([(1, 5)])
        assert rs.ranges == ((1, 5),)

    def test_multiple_non_overlapping_ranges(self) -> None:
        """Multiple non-overlapping ranges should be kept separate."""
        rs = RangeSet([(1, 3), (5, 7)])
        assert rs.ranges == ((1, 3), (5, 7))

    def test_overlapping_ranges_merge(self) -> None:
        """Overlapping ranges should merge."""
        rs = RangeSet([(1, 5), (3, 7)])
        assert rs.ranges == ((1, 7),)

    def test_adjacent_ranges_merge(self) -> None:
        """Adjacent ranges [1,3) and [3,5) should merge to [1,5)."""
        rs = RangeSet([(1, 3), (3, 5)])
        assert rs.ranges == ((1, 5),)

    def test_contained_ranges_merge(self) -> None:
        """Contained ranges should merge."""
        rs = RangeSet([(1, 10), (3, 5)])
        assert rs.ranges == ((1, 10),)

    def test_unsorted_input_sorted_output(self) -> None:
        """Unsorted input should be sorted in output."""
        rs = RangeSet([(5, 7), (1, 3)])
        assert rs.ranges == ((1, 3), (5, 7))

    def test_ranges_property_immutable(self) -> None:
        """Ranges property should return tuple (immutable)."""
        rs = RangeSet([(1, 5)])
        ranges = rs.ranges
        assert isinstance(ranges, tuple)

    def test_invalid_range_start_equal_end(self) -> None:
        """Range with start >= end should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([(5, 5)])

    def test_invalid_range_start_greater_end(self) -> None:
        """Range with start > end should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([(5, 3)])

    def test_non_integer_start(self) -> None:
        """Non-integer start should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([("1", 5)])

    def test_non_integer_end(self) -> None:
        """Non-integer end should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([(1, 5.5)])

    def test_non_tuple_input(self) -> None:
        """Non-tuple input should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([[1, 5]])

    def test_complex_merge_scenario(self) -> None:
        """Multiple overlaps should merge into single range."""
        rs = RangeSet([(1, 3), (2, 5), (4, 8)])
        assert rs.ranges == ((1, 8),)

    def test_many_ranges_preserved(self) -> None:
        """Many non-overlapping ranges should be preserved."""
        ranges = [(i, i + 1) for i in range(0, 20, 2)]
        rs = RangeSet(ranges)
        assert len(rs.ranges) == 10
