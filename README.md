# TemporalMemory

TemporalMemory is a small Python module for storing named events with numeric timestamps and querying them in time order. It keeps all events in memory; it does not parse calendar dates or persist data.

## Status

The repository contains a single-module implementation and a focused unit-test suite. The supported behavior is limited to adding events and querying the stored set; this is not a database, service, or command-line application.

## Features

- Store an event as a non-empty string name and a timestamp converted to `float`.
- Reject duplicate `(name, timestamp)` pairs; the same name at a different timestamp is allowed.
- Return all events ordered by `(timestamp, name)`.
- Query an inclusive timestamp range with `events_between(start, end)`; reversed bounds raise `ValueError`.
- Find the first event strictly after a timestamp with `next_after(timestamp)`, or receive `None` if no such event exists.
- Get the latest event with `latest()`; an empty memory raises `ValueError`.
- Check the number of stored events with `len(memory)`.

## Requirements and use

Python 3.9 or later is declared in the project metadata. The repository includes `requirements.txt` for its declared dependencies and tests. There is no command-line interface. Run Python from the repository root to import the module:

```bash
python -m pip install -r requirements.txt
python
```

```python
from temporalmemory import TemporalMemory

memory = TemporalMemory()
memory.add_event("boot", 0.0)
memory.add_event("login", 1.5)

print(memory.events_between(0.0, 2.0))
print(memory.next_after(0.0).name)  # login
```

The timestamp is just a number: this module assigns no units, clock, timezone, or date interpretation to it.

## Tests and CI

Run the tests from the repository root with:

```bash
python -m pytest -q
```

At the checked-out repository commit, this command completed with **10 tests passed**. A direct import and example-query smoke check also passed locally. The checked-in CI workflow is configured to run pytest, byte-compilation, and an import smoke test on Python 3.10, 3.11, and 3.12; this README does not claim a separate GitHub Actions run result.

## Limitations

- Events are held only in process memory and are lost when the process ends.
- Timestamps are numeric values, not parsed dates or datetimes; there is no timezone or unit handling.
- There are no methods for deleting or updating events.
- The implementation provides no persistence, storage backend, service/API, or CLI.

## License

The repository includes an MIT License. See [LICENSE](LICENSE) for its terms and copyright notice.
