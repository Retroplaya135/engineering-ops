<div align="center">
  <img src="docs/cover.png" alt="Engineering Ops" width="100%">
  <h3>Evidence-led technical reviews and handoffs.</h3>
  <p>
    <img alt="Status: focused toolkit" src="https://img.shields.io/badge/status-focused%20toolkit-334155">
    <img alt="Python 3.11 or newer" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
    <img alt="Dependencies: standard library" src="https://img.shields.io/badge/dependencies-standard%20library-64748b">
    <img alt="JSON Schema 2020-12" src="https://img.shields.io/badge/JSON%20Schema-2020--12-000000?logo=json&logoColor=white">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-16a34a">
  </p>
  <p>
    <a href="#overview">Overview</a> ·
    <a href="#work-record-model">Record model</a> ·
    <a href="#quick-start">Quick start</a> ·
    <a href="#review-flow">Review flow</a> ·
    <a href="#boundaries">Boundaries</a>
  </p>
</div>

## Overview

Engineering Ops is a small, dependency-free toolkit for recording technical work so another engineer can review it or take ownership without reconstructing an entire conversation. It provides a work-record contract, a deterministic Python checker, examples at three risk levels, and concise templates for handoffs and reviewer decisions.

The unit of work is deliberately narrow: one outcome that can be accepted, rejected, returned with a specific request, or stopped. Each record names the accountable owner, the evidence supporting the result, the decision reached, the risk level, and the condition that prohibits further execution.

This is not a project-management system or an activity log. It is a portable review contract for code changes, investigations, migrations, operational tasks, and other work where “done” needs evidence and a clear ownership boundary.

## Work-record model

| Field | Meaning |
| --- | --- |
| `id` | Stable identifier within the repository or workstream |
| `summary` | The reviewable outcome, stated as a result rather than a list of actions |
| `owner` | Person or role accountable for the next decision or action |
| `risk` | `routine`, `elevated`, or `blocked` |
| `evidence` | One or more claim/reference pairs that a reviewer can inspect |
| `decision` | What was accepted, rejected, deferred, or prohibited |
| `stop_condition` | The condition under which work must pause instead of guessing |

The [JSON Schema](schemas/work-record.schema.json) defines the complete record shape. The standard-library [checker](tools/check-record.py) enforces the same required fields, rejects unknown fields, validates risk values, requires non-empty strings, and checks the exact evidence-entry shape.

The checker does not execute the JSON Schema file. It implements the dependency-free validation subset directly so it can run anywhere Python is available. If you use a separate JSON Schema validator, keep its results and the checker results aligned when the contract changes.

## What is included

| Surface | Purpose |
| --- | --- |
| Schema | Machine-readable Draft 2020-12 contract for work records |
| Checker | Deterministic local validation with no installed packages |
| Routine example | Low-impact, reversible documentation change |
| Elevated example | Signing-key rotation requiring independent review and rollback evidence |
| Blocked example | Export stopped because redistribution rights are unresolved |
| Selection guide | Helps split broad work into independently reviewable outcomes |
| Risk guide | Maps impact and reversibility to minimum review depth |
| Handoff contract | Defines the evidence and decisions a receiving engineer needs |
| Templates | Provides compact handoff and reviewer-response starting points |

The examples are synthetic and intentionally small. They demonstrate how the same record shape changes as risk rises without exposing customer data, credentials, incident details, or internal links.

## Quick start

Engineering Ops requires Python 3.11 or newer and installs no packages. From the repository root:

```bash
python3 tools/check-record.py \
  examples/routine.json \
  examples/elevated.json \
  examples/blocked.json
```

Each valid file is reported by path. Invalid files produce one line per finding and a non-zero exit status, which makes the checker suitable for local hooks and continuous-integration steps.

To create a record, copy the example closest to the work's risk level. Replace every synthetic value, keep references stable, then run the checker before requesting review.

## Review flow

1. **Select one outcome.** Use [the selection guide](docs/selection.md) to split work when ownership, risk, verification, or stopping rules differ.
2. **Choose the risk level.** Apply [the risk guide](docs/risk-and-review.md) based on impact and reversibility, not effort or line count.
3. **Record evidence.** Pair each material claim with a stable repository path or authorized URL that a reviewer can inspect.
4. **State the decision.** Record what is accepted, rejected, pending, or blocked. Avoid descriptions that merely say work occurred.
5. **Set the stop condition.** Name the missing authority, information, rollback proof, or safety condition that prevents further execution.
6. **Validate and review.** Run the checker, then apply human judgment at the depth required by the risk level.
7. **Hand over ownership.** Use the [handoff template](templates/handoff.md) and [handoff contract](docs/handoff-contract.md) when another person becomes responsible.

The checker verifies structure. It does not decide whether evidence is convincing or whether the named owner has authority. That distinction is intentional: deterministic validation should reject malformed records, while accountable reviewers decide whether the result is acceptable.

## Practical usage

### Pull-request evidence

Use one record for the outcome a pull request claims to deliver. References can point to targeted tests, a migration rehearsal, a benchmark result, or a specific design decision. An elevated change should name its independent reviewer and include failure-path or rollback evidence in the authorized system where that evidence belongs.

### Investigation handoff

Record the observed outcome, the evidence already gathered, the current decision, and the exact condition that blocks further diagnosis. The next engineer can then continue from a bounded state instead of replaying chat history or assuming unverified conclusions.

### Operational work

Use `blocked` when credentials, destructive authority, customer-data approval, redistribution rights, or rollback evidence are missing. A blocked record is a valid outcome: it preserves why execution stopped and who can remove the constraint.

## Verification

```bash
python3 tools/check-record.py examples/*.json
python3 -m unittest discover -s tests -v
```

The current tests verify that every included example is valid, every required field is enforced, and malformed evidence entries are rejected. The checker also rejects unknown fields, invalid risks, empty required strings, unreadable files, and invalid JSON during normal CLI execution.

Because the project has no package manifest or external dependency, runtime compatibility is governed by the Python features used in the checker and tests. The documented target is Python 3.11 or newer.

## Repository map

| Path | Contents |
| --- | --- |
| `schemas/` | Work-record JSON Schema |
| `tools/` | Dependency-free checker |
| `tests/` | Checker contract tests |
| `examples/` | Routine, elevated, and blocked synthetic records |
| `docs/` | Field reference, selection, risk, and handoff guidance |
| `templates/` | Handoff and reviewer-response templates |

## Boundaries

Engineering Ops does not store records, host a workflow, assign reviewers, inspect evidence links, prove claims, verify authorization, enforce decisions, or execute stop conditions. It does not check identifier uniqueness across a repository. Those concerns remain with the surrounding repository, review process, and authorized systems of record.

Keep sensitive evidence where access is already controlled. A public work record should reference authorized evidence without copying credentials, customer information, private incident data, or internal documents into the repository.

The schema and checker are two implementations of the same contract. Changes should update both, along with field documentation, synthetic examples, and tests. Consumers that need formal JSON Schema validation should run their chosen validator in addition to this project's checker.

## Documentation

- [Work-record reference](docs/work-record.md)
- [Selecting a work unit](docs/selection.md)
- [Risk and review](docs/risk-and-review.md)
- [Handoff contract](docs/handoff-contract.md)
- [JSON Schema](schemas/work-record.schema.json)
- [Handoff template](templates/handoff.md)
- [Reviewer-response template](templates/reviewer-response.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)

## Contributing, security, and license

When changing the contract, explain which decision the field supports and update the schema, checker, documentation, examples, and tests together. Use synthetic records only.

Report suspected vulnerabilities privately as described in [SECURITY.md](SECURITY.md). Do not place sensitive evidence in public issues or pull requests.

Engineering Ops is available under the [MIT License](LICENSE).
