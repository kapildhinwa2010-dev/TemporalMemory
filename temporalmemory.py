# TemporalMemory - Timestamped event memory with time-range queries
# Part of the Kapildhinwa2010-dev Toolkit.

"""Temporal event memory: events ordered by timestamp.

Lineage: reserv.dean-part-2 (HELIX). Unlike the sibling fact memories,
this repo stores TIME-STAMPED events and answers temporal queries:
sorted timelines, range queries, next-after and latest.

HONEST LIMITATION: timestamps are plain numbers (any monotone clock you
choose); there is no wall-clock parsing and no persistence.
"""

from __future__ import annotations

__all__ = ["Event", "TemporalMemory"]


class Event:
    """A single named event at a numeric timestamp."""

    __slots__ = ("name", "timestamp")

    def __init__(self, name: str, timestamp: float) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        self.name = name
        self.timestamp = float(timestamp)

    def as_tuple(self):
        return (self.timestamp, self.name)

    def __eq__(self, other) -> bool:
        return isinstance(other, Event) and self.as_tuple() == other.as_tuple()

    def __hash__(self) -> int:
        return hash(self.as_tuple())

    def __repr__(self) -> str:
        return "Event({!r}, t={})".format(self.name, self.timestamp)


class TemporalMemory:
    """Event log with sorted-timeline temporal queries."""

    def __init__(self) -> None:
        self._events: set = set()

    def add_event(self, name: str, timestamp: float) -> bool:
        """Add an event; returns False if the (name, time) pair exists."""
        event = Event(name, timestamp)
        if event in self._events:
            return False
        self._events.add(event)
        return True

    def timeline(self) -> list:
        """All events sorted by (timestamp, name)."""
        return sorted(self._events, key=lambda e: e.as_tuple())

    def events_between(self, start: float, end: float) -> list:
        """Events with start <= timestamp <= end (inclusive)."""
        if start > end:
            raise ValueError("start must be <= end")
        return [e for e in self.timeline() if start <= e.timestamp <= end]

    def next_after(self, timestamp: float):
        """First event strictly after ``timestamp``, or None."""
        for e in self.timeline():
            if e.timestamp > timestamp:
                return e
        return None

    def latest(self):
        """The most recent event; ValueError if empty."""
        if not self._events:
            raise ValueError("memory is empty")
        return self.timeline()[-1]

    def __len__(self) -> int:
        return len(self._events)