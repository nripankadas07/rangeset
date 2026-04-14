"""Tests for RangeSet set operations (union, intersection, complement)."""

import pytest
from rangeset import RangeSet, RangeSetError


class TestUnion:
    """Test RangeSet.union() operation."""

    def test_union_two_empty(self) -> None:
        """Union of two empty sets should be empty."""
        rs1 = RangeSet()
        rs2 = RangeSet()
        result = rs1.union(rs2)
        assert result.is_empty()

    def test_union_empty_with_non_empty(self) -> None:
        """Union with empty should return copy of other."""
        rs1 = RangeSet()
        rs2 = RangeSet([(1, 5)])
        result = rs1.union(rs2)
        assert result.ranges == ((1, 5),)

    def test_union_non_empty_with_empty(self) -> None:
        """Union of non-empty with empty should return copy of first."""
        rs1 = RangeSet([(1, 5)])
        rs2 = RangeSet()
        result = rs1.union(rs2)
        assert result.ranges == ((1, 5),)

    def test_union_non_overlapping(self) -> None:
        """Union of non-overlapping should preserve both."""
        rs1 = RangeSet([(1, 3)])
        rs2 = RangeSet([(5, 7)])
        result = rs1.union(rs2)
        assert result.ranges == ((1, 3), (5, 7))

    def test_union_overlapping(self) -> None:
        """Union of overlapping should merge."""
        rs1 = RangeSet([(1, 5)])
        rs2 = RangeSet([(3, 7)])
        result = rs1.union(rs2)
        assert result.ranges == ((1, 7),)

    def test_union_adjacent(self) -> None:
        """Union of adjacent should merge."""
        rs1 = RangeSet([(1, 3)])
        rs2 = RangeSet([(3, 5)])
        result = rs1.union(rs2)
        assert result.ranges == ((1, 5),)

    def test_union_multiple_ranges(self) -> None:
        """Union with multiple ranges should merge appropriately."""
        rs1 = RangeSet([(1, 3), (7, 9)])
        rs2 = RangeSet([(2, 5), (8, 11)])
        result = rs1.union(rs2)
        assert result.ranges == ((1, 5), (7, 11))

    def test_union_immutability(self) -> None:
        """Union should return new instance."""
        rs1 = RangeSet([(1, 5)])
        rs2 = RangeSet([(3, 7)])
        result = rs1.union(rs2)
        assert rs1.ranges == ((1, 5),)
        assert rs2.ranges == ((3, 7),)
        assert rs1 is not result
        assert rs2 is not result

    def test_union_returns_rangeset(self) -> None:
        """Union should return RangeSet instance."""
        rs1 = RangeSet([(1, 5)])
        rs2 = RangeSet([(3, 7)])
        result = rs1.union(rs2)
        assert isinstance(result, RangeSet)


class TestIntersection:
    """Test RangeSet.intersection() operation."""

    def test_intersection_two_empty(self) -> None:
        """Intersection of two empty sets should be empty."""
        rs1 = RangeSet()
        rs2 = RangeSet()
        result = rs1.intersection(rs2)
        assert result.is_empty()

    def test_intersection_empty_with_non_empty(self) -> None:
        """Intersection with empty should be empty."""
        rs1 = RangeSet()
        rs2 = RangeSet([(1, 5)])
        result = rs1.intersection(rs2)
        assert result.is_empty()

    def test_intersection_non_overlapping(self) -> None:
        """Intersection of non-overlapping should be empty."""
        rs1 = RangeSet([(1, 3)])
        rs2 = RangeSet([(5, 7)])
        result = rs1.intersection(rs2)
        assert result.is_empty()

    def test_intersection_complete_overlap(self) -> None:
        """Intersection with complete overlap should return overlap."""
        rs1 = RangeSet([(1, 5)])
        rs2 = RangeSet([(1, 5)])
        result = rs1.intersection(rs2)
        assert result.ranges == ((1, 5),)

    def test_intersection_partial_overlap(self) -> None:
        """Intersection with partial overlap."""
        rs1 = RangeSet([(1, 5)])
        rs2 = RangeSet([(3, 7)])
        result = rs1.intersection(rs2)
        assert result.ranges == ((3, 5),)

    def test_intersection_contained(self) -> None:
        """Intersection where one is contained in other."""
        rs1 = RangeSet([(1, 10)])
        rs2 = RangeSet([(3, 7)])
        result = rs1.intersection(rs2)
        assert result.ranges == ((3, 7),)

    def test_intersection_multiple_ranges(self) -> None:
        """Intersection with multiple ranges."""
        rs1 = RangeSet([(1, 5), (7, 11)])
        rs2 = RangeSet([(3, 9)])
        result = rs1.intersection(rs2)
        assert result.ranges == ((3, 5), (7, 9))

    def test_intersection_multiple_both_sides(self) -> None:
        """Intersection with multiple ranges on both sides."""
        rs1 = RangeSet([(1, 3), (5, 7), (9, 11)])
        rs2 = RangeSet([(2, 6), (8, 10)])
        result = rs1.intersection(rs2)
        assert result.ranges == ((2, 3), (5, 6), (9, 10))

    def test_intersection_immutability(self) -> None:
        """Intersection should return new instance."""
        rs1 = RangeSet([(1, 5)])
        rs2 = RangeSet([(3, 7)])
        result = rs1.intersection(rs2)
        assert rs1.ranges == ((1, 5),)
        assert rs2.ranges == ((3, 7),)
        assert rs1 is not result
        assert rs2 is not result

    def test_intersection_returns_rangeset(self) -> None:
        """Intersection should return RangeSet instance."""
        rs1 = RangeSet([(1, 5)])
        rs2 = RangeSet([(3, 7)])
        result = rs1.intersection(rs2)
        assert isinstance(result, RangeSet)


class TestComplement:
    """Test RangeSet.complement() operation."""

    def test_complement_empty_set(self) -> None:
        """Complement of empty set should return full range."""
        rs = RangeSet()
        result = rs.complement(1, 10)
        assert result.ranges == ((1, 10),)

    def test_complement_full_range(self) -> None:
        """Complement of full range should be empty."""
        rs = RangeSet([(1, 10)])
        result = rs.complement(1, 10)
        assert result.is_empty()

    def test_complement_partial_left(self) -> None:
        """Complement leaving gap on left."""
        rs = RangeSet([(5, 10)])
        result = rs.complement(1, 10)
        assert result.ranges == ((1, 5),)

    def test_complement_partial_right(self) -> None:
        """Complement leaving gap on right."""
        rs = RangeSet([(1, 5)])
        result = rs.complement(1, 10)
        assert result.ranges == ((5, 10),)

    def test_complement_with_gap_in_middle(self) -> None:
        """Complement revealing gap in middle."""
        rs = RangeSet([(1, 3), (7, 10)])
        result = rs.complement(1, 10)
        assert result.ranges == ((3, 7),)

    def test_complement_multiple_gaps(self) -> None:
        """Complement with multiple gaps."""
        rs = RangeSet([(2, 4), (6, 8)])
        result = rs.complement(1, 10)
        assert result.ranges == ((1, 2), (4, 6), (8, 10))

    def test_complement_partial_range_overlap(self) -> None:
        """Complement with range partially outside bounds."""
        rs = RangeSet([(0, 5)])
        result = rs.complement(1, 10)
        assert result.ranges == ((5, 10),)

    def test_complement_range_inside_bounds(self) -> None:
        """Complement with range completely inside bounds."""
        rs = RangeSet([(3, 7)])
        result = rs.complement(1, 10)
        assert result.ranges == ((1, 3), (7, 10))

    def test_complement_invalid_bounds(self) -> None:
        """Complement with invalid bounds should raise RangeSetError."""
        rs = RangeSet([(1, 5)])
        with pytest.raises(RangeSetError):
            rs.complement(10, 1)

    def test_complement_immutability(self) -> None:
        """Complement should return new instance."""
        rs1 = RangeSet([(1, 3), (7, 10)])
        rs2 = rs1.complement(1, 10)
        assert rs1.ranges == ((1, 3), (7, 10))
        assert rs2.ranges == ((3, 7),)
        assert rs1 is not rs2

    def test_complement_returns_rangeset(self) -> None:
        """Complement should return RangeSet instance."""
        rs = RangeSet([(1, 5)])
        result = rs.complement(1, 10)
        assert isinstance(result, RangeSet)
