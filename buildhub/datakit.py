"""datakit — a tiny data-processing toolkit.

YOUR JOB: implement every function below so it matches SPEC.md. Drive Claude Code
to help, but you must understand and be able to explain each line. Run the public
tests as you go:  pytest tests/public
"""
from __future__ import annotations

import csv
import json


def load_records(path):
    """Load a .csv or .json file into a list of dict rows.

    - .csv  -> use csv.DictReader (every value is a str)
    - .json -> a list of objects (returned as-is)
    - anything else -> raise ValueError
    """
    if path.endswith(".csv"):
        # newline="" is what the csv module expects so quoted newlines parse correctly
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    raise ValueError(f"Unsupported file type: {path!r} (expected .csv or .json)")


def filter_records(records, **criteria):
    """Return only the rows where, for every field=value pair passed as a keyword
    argument, str(row[field]) == str(value)."""
    # Compare as strings so CSV rows ("10") and JSON rows (10) match the same criteria.
    return [
        row
        for row in records
        if all(str(row[field]) == str(value) for field, value in criteria.items())
    ]


def summarize(records, group_by, value, agg, decimals=2):
    """Group rows by the `group_by` field and aggregate the numeric `value` field.

    agg is one of:
      "count" -> number of rows in the group (int)
      "sum"   -> sum of the values (float)
      "mean"  -> mean of the values, rounded to `decimals` places (float)
      "min"   -> smallest value (float)
      "max"   -> largest value (float)
    Return a dict mapping each group value to its aggregate. Unknown agg -> ValueError.
    """
    if agg not in ("count", "sum", "mean", "min", "max"):
        raise ValueError(f"Unknown agg: {agg!r}")

    # Bucket the rows by their group_by value, keeping first-seen order.
    groups = {}
    for row in records:
        groups.setdefault(row[group_by], []).append(row)

    result = {}
    for key, rows in groups.items():
        if agg == "count":
            result[key] = len(rows)
            continue
        # float() handles both CSV strings ("10") and JSON numbers (10).
        values = [float(row[value]) for row in rows]
        if agg == "sum":
            result[key] = sum(values)
        elif agg == "mean":
            result[key] = round(sum(values) / len(values), decimals)
        elif agg == "min":
            result[key] = min(values)
        else:  # "max"
            result[key] = max(values)
    return result


def top_n(records, key, n):
    """Return the `n` rows with the largest numeric `key`, sorted descending."""
    # float() so CSV strings sort numerically ("9" < "10"), not alphabetically.
    ranked = sorted(records, key=lambda row: float(row[key]), reverse=True)
    return ranked[:n]


def to_report(summary):
    """Render a {key: value} dict as lines 'key: value', one per line, sorted
    ascending by key, joined with '\\n' (no trailing newline)."""
    return "\n".join(f"{key}: {summary[key]}" for key in sorted(summary))
