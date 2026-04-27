"""RangeSet: Manage sets of non-overlapping integer ranges."""

from .core import RangeSet
from .errors import RangeSetError

__all__ = ["RangeSet", "RangeSetError"]
__version__ = "0.1.0"
