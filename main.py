import argparse
import csv
import sys

from tabulate import tabulate

from reports import REPORTS


def parse_args():
    parser = argparse.ArgumentParser(description="Student session reports")
    parser.add_argument("--files", nargs="+", required=True, help="CSV files to process")
    parser.add_argument("--report", required=True, choices=REPORTS, help="Report name")
    return parser.parse_args()


def read_rows(file_paths):
    rows = []
    for path in file_paths:
        try:
            with open(path, newline="", encoding="utf-8") as f:
                rows.extend(csv.DictReader(f))
        except FileNotFoundError:
            print(f"Error: file not found: {path}", file=sys.stderr)
            sys.exit(1)
    return rows


def main():
    args = parse_args()
    rows = read_rows(args.files)
    data = REPORTS[args.report](rows)
    print(tabulate(data, headers="keys", tablefmt="outline"))


if __name__ == "__main__":
    main()
