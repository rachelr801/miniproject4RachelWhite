# Technical Report: buildhub

**Author:** Rachel White
**Course:** INF601 - Advanced Programming in Python, Mini Project 4 (Track B)
**Repository:** https://github.com/rachelr801/miniproject4RachelWhite

---

## 1. What I built and why

`buildhub` is a small data-processing toolkit written using only the Python
standard library. It loads a table of records from a CSV or JSON file and answers
simple questions about it: filtering rows, grouping and aggregating a numeric
column, finding the top rows by a column, and printing a sorted text report.

It has two parts:

| Part | File | Purpose |
|---|---|---|
| Library | `buildhub/datakit.py` | Five functions: `load_records`, `filter_records`, `summarize`, `top_n`, `to_report` |
| CLI | `buildhub/__main__.py` | `python -m buildhub summarize ...` and `python -m buildhub top ...` |

Example, using the provided sample data:

```bash
python -m buildhub summarize fixtures/sample.csv --group-by team --value points --agg mean
```

```text
blue: 32.5
red: 31.67
```

The goal of the project was to implement a fixed specification (`SPEC.md`) by
directing an AI coding agent (Claude Code), while understanding every line well
enough to explain it. A hidden autograder checks the implementation with
parameters derived from my `BUILD_SEED` (467), so the code had to be general
rather than tuned to the public tests.

## 2. Design decisions

**Standard library only.** The spec requires it. The toolkit imports only `csv`,
`json`, `argparse` and `sys`, so it runs on any Python 3 installation with nothing
to install. `pytest` is used only for testing.

**`load_records`: choose the format by file extension.** The function checks
`path.endswith(".csv")` or `.json` and raises `ValueError` for anything else.
CSV files are opened with `newline=""`, which is what the `csv` module documents
as correct, and read with `csv.DictReader`, so every value is a string. JSON values
keep their original types. Both files are opened with `with` blocks so they are
always closed.

**Compare and compute in a type-neutral way.** Because CSV gives strings (`"10"`)
and JSON gives numbers (`10`), the same data can arrive in two forms. Each
function handles this explicitly:

- `filter_records` compares `str(row[field]) == str(value)`, so `points=10` and
  `points="10"` match both file types.
- `summarize` and `top_n` convert values with `float(...)` before doing math or
  sorting. This matters for sorting in particular: as strings, `"9"` sorts after
  `"10"`.

**`filter_records`: a single list comprehension with `all(...)`.** `all()` of an
empty sequence is `True`, so calling it with no criteria returns every row without
any special-case code.

**`summarize`: validate first, then group, then aggregate.** An unknown `agg`
raises `ValueError` before any work is done, even if there are no records. Rows
are grouped with `dict.setdefault`, which keeps groups in the order they first
appear. `count` uses `len(rows)` and never converts values, so it returns an
`int` and works on non-numeric columns. Only `mean` is rounded, to `decimals`
places, as the spec states. I used `sum(values) / len(values)` rather than
`statistics.mean` because it is simple and needs no import.

**`top_n`: `sorted(..., reverse=True)` then slice.** `sorted` returns a new list,
so the caller's data is not changed. Python's sort is stable, so rows with equal
values stay in their original file order. Slicing with `[:n]` safely handles an
`n` larger than the number of rows.

**`to_report`: one expression.** `"\n".join(f"{key}: {summary[key]}" for key in
sorted(summary))` sorts by key, formats each line with `str(value)`, and puts
newlines only between lines, so there is no trailing newline.

**CLI: `argparse` with subcommands.** `summarize` and `top` are subparsers.
`--agg` uses `choices`, so a typo such as `median` gets a clear error listing the
valid options. `--n` and `--decimals` use `type=int`, so they arrive as numbers.
`main(argv=None)` reads the real command line by default but can also be called
with a list, which makes it testable. It returns `0`, which `sys.exit(main())`
turns into the exit code.

## 3. What the agent did vs. what I did

I used Claude Code agentically for the whole build. The full session is in
[`TRANSCRIPT.md`](TRANSCRIPT.md).

**What I did:**

- Set up the repository and virtual environment from the starter files.
- Broke the work into steps, giving the agent one function at a time.
- Reviewed each implementation and the agent's line-by-line explanation before
  moving on.
- Decided when each piece was done and told the agent to commit and push, which
  gave one commit per function.
- Asked whether the project used my build seed. That question led the agent to
  find the full `SPEC.md` and catch a missing CLI option (see below).

**What the agent did:**

- Wrote all of the code in `datakit.py` and `__main__.py`.
- Ran the public tests after each function, plus extra manual checks (Section 4).
- Explained each implementation and pointed out edge cases the spec left open,
  such as missing fields and negative `n`.
- Ran the git commands to create the repository, commit and push.
- Produced the readable transcript from the session export.

**A mistake that was caught.** The agent first worked from the docstrings in the
starter `datakit.py` rather than `SPEC.md`, which was one folder above my repo.
As a result, the first version of the CLI was missing the `--decimals` option
that the spec requires for `summarize`. When I asked about the build seed, the
agent read `SPEC.md`, noticed the gap, and added the option in a separate commit.
This is the parameter the autograder varies with the seed, so the miss could have
cost points. The lesson for me is to give the agent the full spec up front rather
than one piece at a time.

I initially had some difficulty copying the starter files into my repo. I'm not sure what I was doing wrong but once I moved the starter files and my repo files into the same folder on my computer everything seemed to work much better and I successfully copied the files. I learned that Claude is fairly adept at writing the code with very little prompting but it is good to double check that the code actually conforms to what the assignment is specifying.

## 4. How I tested it

**Public tests.** `python -m pytest` runs the 7 tests in `tests/public`. They were
run after every function, and all 7 pass on the final code.

**Manual checks** run by the agent during the session, beyond the public tests:

| Area | What was checked | Result |
|---|---|---|
| `load_records` | `.txt` file | raises `ValueError` |
| `filter_records` | no criteria; `points=10` vs `points="10"` on CSV and JSON | all rows; both match both formats |
| `summarize` | all five aggs on CSV and JSON | identical results for both formats |
| `summarize` | `decimals=0`, grouping by `level`, `agg="median"` | rounds correctly; works; raises `ValueError` |
| `top_n` | `n=0`, `n=99`, ties, `"9"` vs `"10"` | `[]`; all rows; file order kept; numeric order |
| `to_report` | empty summary | `""` |
| CLI | both subcommands, `--decimals 0/1/3`, bad `--agg`, no subcommand | correct output; clear argparse errors |

Because the autograder varies `decimals` and `n` by seed, I paid particular
attention to checking several values of each rather than only the ones in the
public tests.

## 5. Limitations and next steps

**Limitations**

- **Missing fields raise `KeyError`.** The spec defines filtering as `row[field]`,
  so a row without that field is an error rather than a non-match.
- **Negative `n` in `top_n`** follows Python slicing, so `n=-1` returns every row
  except the last instead of an empty list.
- **Empty or non-numeric values** (for example a blank CSV cell) make
  `float(...)` raise `ValueError` in `summarize` and `top_n`.
- **Extensions are case-sensitive.** `data.CSV` is rejected.
- **Group keys keep their file type.** Grouping CSV data by `level` gives string
  keys (`"3"`); grouping JSON data gives integers (`3`). A summary that mixed both
  types would make `to_report`'s sort fail.
- **CSV files saved by Excel with a byte-order mark** would have a first column
  name like `"\ufeffname"` (an invisible character before `name`). Opening with `encoding="utf-8-sig"` would fix this.
- **`top` prints rows as Python dicts**, which is readable but not easy for
  another program to parse.
- **No tests of my own.** Only the public tests are saved in the repo; the extra
  checks above were run by hand.

**Next steps**

- Add a `tests/test_datakit.py` file that turns the manual checks above into
  permanent tests, including several `decimals` and `n` values and CLI tests that
  call `main([...])`.
- Decide and document behavior for missing fields, blank values and negative `n`.
- Add an option to print `top` results as JSON or CSV.
- Accept upper-case extensions and BOM-encoded CSV files.
