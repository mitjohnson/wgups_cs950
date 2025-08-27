import csv
from pathlib import Path


def load_package_data(
    path=Path(__file__).parent / "WGUPS_Package_File.csv",
):
    """Loads the CSV file of packages to deliver."""

    with open(path, newline="", encoding="utf-8") as package_data:
        for row in csv.DictReader(package_data):
            yield row


def load_distance_data(
    path=Path(__file__).parent / "WGUPS_Distance_Table.csv",
):
    """Loads the CSV file of delivery distances."""

    with open(path, newline="", encoding="utf-8") as distance_data:
        return list(csv.reader(distance_data))
