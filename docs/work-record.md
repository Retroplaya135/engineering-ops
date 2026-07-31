# Work records

A work record describes one outcome and its supporting evidence. The
[schema](../schemas/work-record.schema.json) defines these required fields:

- `id` identifies the record; keep it stable within the repository.
- `summary` states the reviewable outcome.
- `owner` identifies the person accountable for the next action.
- `risk` selects the review depth.
- `evidence` is a non-empty list of objects, each containing a `claim` and a `reference`.
- `decision` states what was accepted, rejected, or blocked.
- `stop_condition` says when work must pause instead of guessing.

The [checker](../tools/check-record.py) rejects missing or unknown fields, invalid
risk values, empty strings, and malformed evidence entries. It does not check
ID uniqueness or inspect the referenced evidence.
