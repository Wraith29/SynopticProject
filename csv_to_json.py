import csv
import json
import os


def csv_to_json(csv_path: str, out_path: str) -> None:
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)

        data = [row for row in reader]

    with open(out_path, "w") as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    """This `if` statement means it will only execute if this script is run"""
    csv_path = r"SDT Project C\SDT Project C Holiday Chat Agent - Data Set.csv"
    # The `csv_path` string is prefixed with `r` to tell it to be "raw"
    # This means it will ignore any escape sequences within the path
    out_path = os.path.join("app", "static", "data", "holidays.json")

    csv_to_json(csv_path, out_path)
