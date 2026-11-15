import pytest

from temporalmemory import Event, TemporalMemory


def test_event_basic():
    event = Event("login", 100.0)
    assert event.as_tuple() == (100.0, "login")


def test_event_rejects_empty_name():
    with pytest.raises(ValueError):
        Event("", 1.0)


def test_event_equality_and_hash():
    assert Event("a", 1.0) == Event("a", 1.0)
    assert hash(Event("a", 1.0)) == hash(Event("a", 1.0))
    assert Event("a", 1.0) != Event("a", 2.0)


def test_add_and_len():
    mem = TemporalMemory()
    assert mem.add_event("a", 1.0) is True
    assert mem.add_event("a", 1.0) is False
    assert len(mem) == 1


def test_timeline_sorted():
    mem = TemporalMemory()
    mem.add_event("late", 30.0)
    mem.add_event("early", 10.0)
    mem.add_event("mid", 20.0)
    assert [e.name for e in mem.timeline()] == ["early", "mid", "late"]


def test_events_between_inclusive():
    mem = TemporalMemory()
    mem.add_event("a", 10.0)
    mem.add_event("b", 20.0)
    mem.add_event("c", 30.0)
    assert [e.name for e in mem.events_between(10.0, 20.0)] == ["a", "b"]


def test_events_between_rejects_inverted():
    mem = TemporalMemory()
    with pytest.raises(ValueError):
        mem.events_between(20.0, 10.0)


def test_next_after():
    mem = TemporalMemory()
    mem.add_event("a", 10.0)
    mem.add_event("b", 20.0)
    assert mem.next_after(10.0).name == "b"
    assert mem.next_after(20.0) is None


def test_latest():
    mem = TemporalMemory()
    mem.add_event("a", 10.0)
    mem.add_event("b", 20.0)
    assert mem.latest().name == "b"


def test_latest_empty_raises():
    mem = TemporalMemory()
    with pytest.raises(ValueError):
        mem.latest()