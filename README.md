# RangeSet

Manage sets of non-overlapping integer ranges with merge, intersection, and complement.

## Installation

```bash
pip install .
```

## Quick Start

```python
from rangeset import RangeSet

# Create a RangeSet from ranges
rs = RangeSet([(1, 5), (10, 15)])

# Add a range (returns new instance)
rs2 = rs.add(3, 12)  # Merges overlapping ranges
# rs2.ranges == ((1, 15),)

# Remove a range
rs3 = rs.remove(3, 7)
# rs3.ranges == ((1, 3), (10, 15))

# Union of two sets
rs4 = rs.union(RangeSet([(20, 25)]))
# rs4.ranges == ((1, 5), (10, 15), (20, 25))

# Intersection
rs5 = rs.intersection(RangeSet([(4, 12)]))
# rs5.ranges == ((4, 5), (10, 12))

# Check membership
rs.contains(3)  # True
rs.contains(7)  # False

# Get total span
rs.span()  # 5 + 5 = 10

# Check if empty
rs.is_empty()  # False

# Complement within bounds
rs.complement(0, 20)
# RangeSet([(0, 1), (5, 10), (15, 20)])
```

## API Reference

### `RangeSet(ranges: Iterable[tuple[int, int]] = ())`

Create a RangeSet from an iterable of (start, end) tuples (half-open intervals: [start, end)).
Automatically merges overlapping and adjacent ranges.

**Parameters:**
- `ranges`: Iterable of (start, end) tuples. Defaults to empty.

**Raises:**
- `RangeSetError`: If ranges are invalid (non-integer bounds, start >= end, etc.)

### `RangeSet.add(start: int, end: int) -> RangeSet`

Add a range to the set, merging with overlapping ranges. Returns a new RangeSet.

**Parameters:**
- `start`: Start of range (inclusive)
- `end`: End of range (exclusive)

**Returns:** New RangeSet instance with the added range.

**Raises:** `RangeSetError` if the range is invalid.

### `RangeSet.remove(start: int, end: int) -> RangeSet`

Remove a range from the set, splitting existing ranges if needed. Returns a new RangeSet.

**Parameters:**
- `start`: Start of range to remove (inclusive)
- `end`: End of range to remove (exclusive)

**Returns:** New RangeSet instance with the removed range.

**Raises:** `RangeSetError` if the range is invalid.

### `RangeSet.union(other: RangeSet) -> RangeSet`

Return the set union of this RangeSet and another.

**Parameters:**
- `other`: Another RangeSet instance

**Returns:** New RangeSet containing all ranges from both sets.

### `RangeSet.intersection(other: RangeSet) -> RangeSet`

Return the set intersection of this RangeSet and another.

**Parameters:**
- `other`: Another RangeSet instance

**Returns:** New RangeSet containing only overlapping ranges.

### `RangeSet.complement(lower: int, upper: int) -> RangeSet`

Return the complement of this set within the range [lower, upper).

**Parameters:**
- `lower`: Lower bound (inclusive)
- `upper`: Upper bound (exclusive)

**Returns:** New RangeSet containing the complement.

**Raises:** `RangeSetError` if bounds are invalid.

### `RangeSet.contains(value: int) -> bool`

Check if an integer value is contained in any range.

**Parameters:**
- `value`: Integer to check

**Returns:** True if the value is in the set, False otherwise.

### `RangeSet.span() -> int`

Return the total number of integers covered by all ranges.

**Returns:** Sum of all range sizes (end - start).

### `RangeSet.is_empty() -> bool`

Check if the RangeSet is empty.

**Returns:** True if no ranges exist, False otherwise.

### `RangeSet.ranges -> tuple[tuple[int, int], ...]`

Property that returns all ranges as an immutable tuple of (start, end) pairs, sorted.

**Returns:** Tuple of (start, end) ranges in ascending order.

### `RangeSetError`

Exception raised for invalid operations (non-integer bounds, start >= end, etc.).

## Running Tests

Install test dependencies:
```bash
pip install pytest pytest-cov
```

Run tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ -v --cov=src/rangeset --cov-report=term-missing
```

## Design

- **Immutable API**: All mutation operations return new RangeSet instances, leaving the original unchanged.
- **Automatic Merging**: Overlapping and adjacent ranges are automatically merged during construction.
- **Half-Open Intervals**: All ranges use [start, end) notation where start is inclusive and end is exclusive.
- **Integer-Only**: Supports all integers (positive, negative, zero) but not floats or unbounded ranges.
- **Efficient Storage**: No expansion to individual integers; ranges are stored as tuples.

## License

MIT License - See LICENSE file for details.
