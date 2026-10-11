"""buildhub CLI.  Implement so:  python -m buildhub summarize <file> --group-by G --value V --agg A
and:  python -m buildhub top <file> --key K --n N   both work (see SPEC.md)."""
import argparse
import sys

from buildhub import datakit


def build_parser():
    parser = argparse.ArgumentParser(prog="buildhub", description="Small data-processing toolkit.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    summarize = subparsers.add_parser("summarize", help="group rows and aggregate a numeric field")
    summarize.add_argument("file", help="path to a .csv or .json file")
    summarize.add_argument("--group-by", required=True, help="field to group rows by")
    summarize.add_argument("--value", required=True, help="numeric field to aggregate")
    summarize.add_argument(
        "--agg", required=True, choices=["count", "sum", "mean", "min", "max"], help="aggregation to apply"
    )

    top = subparsers.add_parser("top", help="show the rows with the largest numeric field")
    top.add_argument("file", help="path to a .csv or .json file")
    top.add_argument("--key", required=True, help="numeric field to rank rows by")
    top.add_argument("--n", required=True, type=int, help="number of rows to show")

    return parser


def main(argv=None):
    # argv=None makes argparse read sys.argv[1:]; tests can pass a list instead.
    args = build_parser().parse_args(argv)
    records = datakit.load_records(args.file)

    if args.command == "summarize":
        summary = datakit.summarize(records, args.group_by, args.value, args.agg)
        print(datakit.to_report(summary))
    else:  # "top"
        for row in datakit.top_n(records, args.key, args.n):
            print(row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
