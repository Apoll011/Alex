from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Self

from core.musiclib import config
from core.musiclib.interval import AbstractInterval
from core.musiclib.util.cache import Cached

class IntervalSet(Cached):
    def __init__(self, intervals: frozenset[AbstractInterval]) -> None:
        if not isinstance(intervals, frozenset):
            raise TypeError(f'expected frozenset, got {type(intervals)}')
        if any(not isinstance(interval, AbstractInterval) for interval in intervals):
            raise TypeError('expected AbstractInterval items')
        self.intervals = intervals
        self.intervals_ascending = tuple(sorted(intervals))
        self.bits = ''.join('1' if AbstractInterval(i) in intervals else '0' for i in range(12))
        self.names: frozenset[str] = config.intervals_to_names.get(intervals, frozenset())
        self.name_kinds = {name: config.kinds[name] for name in self.names}

    @classmethod
    def from_name(cls: type[Self], name: str) -> Self:
        return cls(config.name_to_intervals[name])

    @classmethod
    def from_bits(cls, bits: str) -> IntervalSet:
        return cls(frozenset(AbstractInterval(i) for i, v in enumerate(bits) if int(v)))

    @classmethod
    def from_base12(cls, intervals: frozenset[str]) -> IntervalSet:
        return cls(frozenset(AbstractInterval.from_str(i) for i in intervals))

    @property
    def inverse(self) -> IntervalSet:
        return IntervalSet(frozenset(-i for i in self.intervals))

    def __len__(self) -> int:
        return len(self.intervals)

    def __iter__(self) -> Iterator[AbstractInterval]:
        return iter(self.intervals_ascending)

    def __getnewargs__(self) -> tuple[frozenset[AbstractInterval]]:
        return (self.intervals,)

    def __str__(self) -> str:
        return '_'.join(str(i) for i in self.intervals_ascending)
