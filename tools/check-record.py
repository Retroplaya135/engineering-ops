#!/usr/bin/env python3
"""Validate the dependency-free subset of the work-record contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = ("id", "summary", "owner", "risk", "evidence", "decision", "stop_condition")
RISKS = {"routine", "elevated", "blocked"}


def validate(record: object) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    errors: list[str] = []
    unknown = sorted(set(record) - set(REQUIRED))
    if unknown:
        errors.append(f"unknown fields: {', '.join(unknown)}")
    for field in REQUIRED:
        if field not in record:
            errors.append(f"missing field: {field}")
    for field in ("id", "summary", "owner", "decision", "stop_condition"):
        if field in record and (not isinstance(record[field], str) or not record[field].strip()):
            errors.append(f"{field} must be a non-empty string")
    if record.get("risk") not in RISKS:
        errors.append("risk must be routine, elevated, or blocked")
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence must be a non-empty list")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict) or set(item) != {"claim", "reference"}:
                errors.append(f"evidence[{index}] must contain claim and reference")
                continue
            for field in ("claim", "reference"):
                if not isinstance(item[field], str) or not item[field].strip():
                    errors.append(f"evidence[{index}].{field} must be a non-empty string")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", type=Path, nargs="+")
    args = parser.parse_args()
    failed = False
    for path in args.records:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            print(f"{path}: {error}")
            failed = True
            continue
        errors = validate(record)
        if errors:
            failed = True
            for error in errors:
                print(f"{path}: {error}")
        else:
            print(f"{path}: valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
