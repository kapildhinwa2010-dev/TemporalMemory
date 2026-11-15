# TemporalMemory

[![CI](https://github.com/kapildhinwa2010-dev/TemporalMemory/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/TemporalMemory/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kapildhinwa2010-dev/TemporalMemory/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/TemporalMemory/actions/workflows/codeql.yml)


Timestamped event memory: sorted timelines, range queries, next-after, latest.

**Part of the [Kapildhinwa2010-dev Toolkit](https://github.com/kapildhinwa2010-dev/Kapildhinwa2010-dev).**

## What it does

Unlike the sibling fact memories, TemporalMemory stores TIME-STAMPED
events (name + numeric timestamp) and answers temporal queries:
sorted timeline, inclusive range queries, first event strictly after
a time, and the latest event. HONEST LIMITATION (also in the
docstring): timestamps are plain numbers on any monotone clock you
choose; no wall-clock parsing, no persistence.

## Install

```bash
pip install -r requirements.txt
```

## Quick start

```python
from temporalmemory import TemporalMemory

mem = TemporalMemory()
mem.add_event("boot", 0.0)
mem.add_event("login", 1.5)
print(mem.events_between(0.0, 2.0))
print(mem.next_after(0.0).name)  # "login"
```

## API

- add_event(name, timestamp) - False if the (name, time) pair exists
- timeline() - events sorted by (timestamp, name)
- events_between(start, end) - inclusive range
- next_after(timestamp) / latest()

## Honest results and limitations

- Timestamps are floats, not datetimes: no units, no timezone, no
  parsing - you own the clock.
- In-memory only; nothing is saved to disk.
- No event deletion or update.

## License

MIT - see [LICENSE](LICENSE).
