"""Tests for RangeSet edge cases and error handling."""

import pytest
from rangeset import RangeSet, RangeSetError


class TestErrorHandling:
    """Test RangeSetError is raised appropriately."""

    def test_rangeset_error_is_exception(self) -> None:
        """RangeSetError should be an Exception."""
        assert issubclass(RangeSetError, Exception)

    def test_invalid_start_type_float(self) -> None:
        """Float start should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([(1.5, 5)])

    def test_invalid_end_type_float(self) -> None:
        """Float end should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([(1, 5.5)])

    def test_invalid_start_type_string(self) -> None:
        """String start should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([("a", 5)])

    def test_invalid_end_type_string(self) -> None:
        """String end should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([(1, "b")])

    def test_invalid_input_not_tuple(self) -> None:
        """Non-tuple input should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([(1, 2, 3)])

    def test_invalid_input_list(self) -> None:
        """List instead of tuple should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([[1, 5]])

    def test_invalid_range_equal_bounds(self) -> None:
        """Range with start == end should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([(5, 5)])

    def test_invalid_range_reversed(self) -> None:
        """Range with start > end should raise RangeSetError."""
        with pytest.raises(RangeSetError):
            RangeSet([(10, 5)])

    def test_add_invalid_bounds_equal(self) -> None:
        """Add with equal bounds should raise RangeSetError."""
        rs = RangeSet([(1, 5)])
        with pytest.raises(RangeSetError):
            rs.add(3, 3)

    def test_add_invalid_bounds_reversed(self) -> None:
        """Add with reversed bounds should raise RangeSetError."""
        rs = RangeSet([(1, 5)])
        with pytest.raises(RangeSetError):
            rs.add(7, 3)

    def test_remove_invalid_bounds_equal(self) -> None:
        """Remove with equal bounds should raise RangeSetError."""
        rs = RangeSet([(1, 5)])
        with pytest.raises(RangeSetError):
            rs.remove(2, 2)

    def test_remove_invalid_bounds_reversed(self) -> None:
        """Remove with reversed bounds should raise RangeSetError."""
        rs = RangeSet([(1, 5)])
        with pytest.raises(RangeSetError):
            rs.remove(7, 3)

    def test_complement_invalid_bounds_equal(self) -> None:
        """Complement with equal bounds should raise RangeSetError."""
        rs = RangeSet([(1, 5)])
        with pytest.raises(RangeSetError):
            rs.complement(5, 5)

    def test_complement_invalid_bounds_reversed(self) -> None:
        """Complement with reversed bounds should raise RangeSetError."""
        rs = RangeSet([(1, 5)])
        with pytest.raises(RangeSetError):
            rs.complement(10, 1)


class TestEdgeCasesNegativeNumbers:
    """Test edge cases with negative numbers."""

    def test_negative_range(self) -> None:
        """Ranges can span negative numbers."""
        rs = RangeSet([(-10, -5)])
        assert rs.ranges == ((-10, -5),)

    def test_negative_to_positive_range(self) -> None:
        """Range can cross zero."""
        rs = RangeSet([(-5, 5)])
        assert rs.ranges == ((-5, 5),)
        assert rs.contains(-5)
        assert rs.contains(0)
        assert rs.contains(4)
        assert not rs.contains(5)

    def test_negative_with_add(self) -> None:
        """Add should work with negative ranges."""
        rs = RangeSet([(-10, -5)])
        result = rs.add(-3, 0)
        assert result.ranges == ((-10, -5), (-3, 0))

    def test_negative_with_union(self) -> None:
        """Union should work with negative ranges."""
        rs1 = RangeSet([(-10, -5)])
        rs2 = RangeSet([(-7, -2)])
        result = rs1.union(rs2)
        assert result.ranges == ((-10, -2),)

    def test_negative_with_intersection(self) -> None:
        """Intersection should work with negative ranges."""
        rs1 = RangeSet([(-10, -2)])
        rs2 = RangeSet([(-5, 0)])
        result = rs1.intersection(rs2)
        assert result.ranges == ((-5, -2),)

    def test_negative_complement(self) -> None:
        """Complement should work with negative bounds."""
        rs = RangeSet([(-5, -1)])
        result = rs.complement(-10, 0)
        assert result.ranges == ((-10, -5), (-1, 0))


class TestEdgeCasesLargeNumbers:
    """Test edge cases with large numbers."""

    def test_large_range(self) -> None:
        """Large ranges should work without expansion."""
        rs = RangeSet([(0, 1000000)])
        assert rs.ranges == ((0, 1000000),)
        assert rs.span() == 1000000

    def test_large_number_contains(self) -> None:
        """Contains should work with large numbers."""
        rs = RangeSet([(1000000, 2000000)])
        assert rs.contains(1000000)
        assert rs.contains(1500000)
        assert not rs.contains(2000000)

    def test_very_large_spans(self) -> None:
        """Span calculation with large ranges."""
        rs = RangeSet([(0, 1000000), (2000000, 3000000)])
        assert rs.span() == 2000000


class TestEdgeCasesZero:
    """Test edge cases with zero values."""

    def test_range_starting_at_zero(self) -> None:
        """Range starting at zero."""
        rs = RangeSet([(0, 5)])
        assert rs.ranges == ((0, 5),)
        assert rs.contains(0)

    def test_range_not_including_zero(self) -> None:
        """Range after zero."""
        rs = RangeSet([(1, 5)])
        assert not rs.contains(0)

    def test_negative_to_zero_range(self) -> None:
        """Range ending at zero."""
        rs = RangeSet([(-5, 0)])
        assert rs.contains(-1)
        assert not rs.contains(0)

    def test_add_at_zero(self) -> None:
        """Add operations at zero."""
        rs = RangeSet([(0, 5)])
        result = rs.add(-2, 0)
        assert result.ranges == ((-2, 5),)


class TestEdgeCasesChaining:
    """Test chaining multiple operations."""

    def test_chain_adds(self) -> None:
        """Chaining multiple add operations."""
        rs = RangeSet()
        result = rs.add(1, 3).add(5, 7).add(3, 5)
        assert result.ranges == ((1, 7),)

    def test_chain_removes(self) -> None:
        """Chaining multiple remove operations."""
        rs = RangeSet([(0, 10)])
        result = rs.remove(1, 2).remove(3, 4).remove(8, 9)
        assert result.ranges == ((0, 1), (2, 3), (4, 8), (9, 10))

    def test_chain_union_then_intersection(self) -> None:
        """Chaining union then intersection."""
        rs1 = RangeSet([(1, 5)])
        rs2 = RangeSet([(3, 7)])
        rs3 = RangeSet([(4, 10)])
        result = rs1.union(rs2).intersection(rs3)
        assert result.ranges == ((4, 7),)

    def test_chain_operations_mixed(self) -> None:
        """Chaining mixed operations."""
        rs = RangeSet([(1, 10)])
        result = rs.add(11, 15).remove(3, 5).union(RangeSet([(0, 1)]))
        # (0, 1) union (1, 3) merges to (0, 3)
        assert result.ranges == ((0, 3), (5, 10), (11, 15))


class TestEdgeCasesDoubleOperations:
    """Test applying operations twice."""

    def test_double_add_same_range(self) -> None:
        """Adding the same range twice."""
        rs = RangeSet([(1, 5)])
        result = rs.add(1, 5)
        assert result.ranges == ((1, 5),)

    def test_double_remove_same_range(self) -> None:
        """Removing the same range twice."""
        rs = RangeSet([(1, 5)])
        result = rs.remove(1, 5).remove(1, 5)
        assert result.is_empty()

    def test_union_with_self(self) -> None:
        """Union with itself should be idempotent."""
        rs = RangeSet([(1, 5), (7, 9)])
        result = rs.union(rs)
        assert result.ranges == rs.ranges

    def test_intersection_with_self(self) -> None:
        """Intersection with itself should be idempotent."""
        rs = RangeSet([(1, 5), (7, 9)])
        result = rs.intersection(rs)
        assert result.ranges == rs.ranges
