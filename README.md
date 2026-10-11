### INF601 - Advanced Programming in Python
### Rachel White
### Mini Project 4


# Project Title

Buildhub data processing toolkit.

Track: B

## Description

This project is a toolkit that reads a table of data from a CSV or JSON file and answers questions about it. It uses only the standard Python library so it should be able to be used from Python code or the command line.

It provides five functions in `buildhub/datakit.py`:

* `load_records` - read a `.csv` or `.json` file into a list of rows
* `filter_records` - keep only the rows that match given field values
* `summarize` - group rows and compute a count, sum, mean, min or max per group
* `top_n` - return the `n` rows with the largest value in a column
* `to_report` - turn a summary into sorted `key: value` lines of text

## Getting Started

### Dependencies

* Python 3 (the toolkit itself uses only the standard library)
* pytest, for running the tests:
```
pip install -r requirements.txt
```

### Installing

* Clone the repository and open the folder:
```
git clone https://github.com/rachelr801/miniproject4RachelWhite.git
cd miniproject4RachelWhite
```

### Executing program

* Run these from the repository root.
* Summarize a column by group (`--agg` can be `count`, `sum`, `mean`, `min` or `max`; `--decimals` is optional and defaults to 2):
```
python -m buildhub summarize fixtures/sample.csv --group-by team --value points --agg mean --decimals 2
```
* Show the top rows by a numeric column:
```
python -m buildhub top fixtures/sample.csv --key points --n 3
```
* To test the program:
```
pytest
python -m pytest
```

## Help

* Add `--help` to any command to see its options:
```
python -m buildhub summarize --help
```
* `No module named buildhub` - run the command from the repository root and include `-m`.
* `KeyError` - a column name is misspelled; names are case-sensitive.
* `could not convert string to float` - `--value` and `--key` need a numeric column.

## AI Usage

I used prompts to have Claude write all of the code. I reviewed and tested the code after prompting to implement each function and concluded that Claude had accurately generated the code to successfully pass the tests so I did not make any changes to the Claude generated code.

* [REPORT.md](REPORT.md) - technical report, including what the agent did vs. what I did
* [TRANSCRIPT.md](TRANSCRIPT.md) - transcript of the Claude Code session

## Authors

Rachel White
r_white4@fhsu.edu

## Version History

* 1.0
    * All five `datakit` functions and the `summarize` / `top` CLI
    * Added the `--decimals` option required by the spec
    * See the [commit history](https://github.com/rachelr801/miniproject4RachelWhite/commits/main)

## Acknowledgments

* Starter files and specification from INF601 - Advanced Programming in Python, Mini Project 4
* Built with [Claude Code](https://claude.com/claude-code)
