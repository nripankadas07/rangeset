"""Tests for RangeSet add and remove operations."""

import pytest
from rangeset import RangeSet, RangeSetError


class TestAdd:
    """Test RangeSet.add() operation."""

    def test_add_to_empty(self) -> None:
        """Adding to empty set should create range."""
        rs = RangeSet()
        result = rs.add(1, 5)
        assert result.ranges == ((1, 5),)

    def test_add_non_overlapping(self) -> None:
        """Adding non-overlapping range should append."""
        rs = RangeSet([(1, 3)])
        result = rs.add(5, 7)
        assert result.ranges == ((1, 3), (5, 7))

    def test_add_overlapping_left(self) -> None:
        """Adding overlapping on left should merge."""
        rs = RangeSet([(5, 10)])
        result = rs.add(3, 7)
        assert result.ranges == ((3, 10),)

    def test_add_overlapping_right(self) -> None:
        """Adding overlapping on right should merge."""
        rs = RangeSet([(1, 5)])
        result = rs.add(3, 7)
        assert result.ranges == ((1, 7),)

    def test_add_adjacent_merge(self) -> None:
        """Adding adjacent range should merge."""
        rs = RangeSet([(1, 3)])
        result = rs.add(3, 5)
        assert result.ranges == ((1, 5),)

    def test_add_contained(self) -> None:
        """Adding contained range should not change anything."""
        rs = RangeSet([(1, 10)])
        result = rs.add(3, 7)
        assert result.ranges == ((1, 10),)

    def test_add_contains(self) -> None:
        """Adding range that contains existing should expand."""
        rs = RangeSet([(3, 7)])
        result = rs.add(1, 10)
        assert result.ranges == ((1, 10),)

    def test_add_multiple_merges(self) -> None:
        """Adding range that bridges two ranges should merge all."""
        rs = RangeSet([(1, 3), (5, 7)])
        result = rs.add(2, 6)
        assert result.ranges == ((1, 7),)

    def test_add_invalid_range(self) -> None:
        """Adding invalid range should raise RangeSetError."""
        rs = RangeSet([(1, 5)])
        with pytest.raises(RangeSetError):
            rs.add(5, 5)

    def test_add_immutability(self) -> None:
        """Add should return new instance."""
        rs1 = RangeSet([(1, 5)])
        rs2 = rs1.add(3, 7)
        assert rs1.ranges == ((1, 5),)
        assert rs2.ranges == ((1, 7),)
        assert rs1 is not rs2

    def test_add_returns_rangeset(self) -> None:
        """Add should return RangeSet instance."""
        rs = RangeSet()
        result = rs.add(1, 5)
        assert isinstance(result, RangeSet)


class TestRemove:
    """Test RangeSet.remove() operation."""

    def test_remove_from_empty(self) -> None:
        """Removing from empty set should be empty."""
        rs = RangeSet()
        result = rs.remove(1, 5)
        assert result.is_empty()

    def test_remove_non_overlapping(self) -> None:
        """Removing non-overlapping range should not change."""
        rs = RangeSet([(1, 3)])
        result = rs.remove(5, 7)
        assert result.ranges == ((1, 3),)

    def test_remove_exact_match(self) -> None:
        """Removing exact match should remove range."""
        rs = RangeSet([(1, 5)])
        result = rs.remove(1, 5)
        assert result.is_empty()

    def test_remove_from_left(self) -> None:
        """Removing from left should shrink range."""
        rs = RangeSet([(1, 5)])
        result = rs.remove(1, 3)
        assert result.ranges == ((3, 5),)

    def test_remove_from_right(self) -> None:
        """Removing from right should shrink range."""
        rs = RangeSet([(1, 5)])
        result = rs.remove(3, 5)
        assert result.ranges == ((1, 3),)

    def test_remove_from_middle_split(self) -> None:
        """Removing from middle should split range."""
        rs = RangeSet([(1, 10)])
        result = rs.remove(4, 6)
        assert result.ranges == ((1, 4), (6, 10))

    def test_remove_partial_overlap_left(self) -> None:
        """Removing with partial left overlap."""
        rs = RangeSet([(3, 10)])
        result = rs.remove(1, 5)
        assert result.ranges == ((5, 10),)

    def test_remove_partial_overlap_right(self) -> None:
        """Removing with partial right overlap."""
        rs = RangeSet([(1, 5)])
        result = rs.remove(3, 10)
        assert result.ranges == ((1, 3),)

    def test_remove_multiple_ranges(self) -> None:
        """Removing should affect multiple ranges."""
        rs = RangeSet([(1, 3), (5, 7), (9, 11)])
        result = rs.remove(2, 10)
        assert result.ranges == ((1, 2), (10, 11))

    def test_remove_invalid_range(self) -> None:
        """Removing invalid range should raise RangeSetError."""
        rs = RangeSet([(1, 5)])
        with pytest.raises(RangeSetError):
            rs.remove(5, 3)

    def test_remove_immutability(self) -> None:
        """Remove should return new instance."""
        rs1 = RangeSet([(1, 10)])
        rs2 = rs1.remove(3, 7)
        assert rs1.ranges == ((1, 10),)
        assert rs2.ranges == ((1, 3), (7, 10))
        assert rs1 is not rs2

    def test_remove_returns_rangeset(self) -> None:
        """Remove should return RangeSet instance."""
        rs = RangeSet([(1, 5)])
        result = rs.remove(1, 5)
        assert isinstance(result, RangeSet)
