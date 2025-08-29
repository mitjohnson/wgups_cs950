__doc__ = """
WGUPS Routing Program (traveling salesman)
Solution created by Mitchell Johnson for CS950 @ WGU.
Student ID: xxxxxxxxx
"""
from data import load_data
from classes import Truck, Package
from datetime import datetime

from typing import List, Dict


def load_trucks(
    trucks: List[Truck],
    packages: List[Package],
    special_cases: Dict,
    current_time: datetime,
) -> List:
    """
    method to handle truck loading logic

    Overall complexity: O(n log n), Δ(n).
    """

    # destruct packages that need grouped, O(1).
    grouped_packages: List = special_cases["must_be_grouped"]

    # destruct delayed packages, O(d)
    delayed_ids = []
    for time_str, package_ids in special_cases["delayed"].items():
        if datetime.fromisoformat(time_str) > current_time:
            delayed_ids.extend(package_ids)

    # filter out delayed packages
    # O(n log n) if we have delayed packages, O(1) otherwise.
    if len(delayed_ids) > 0:
        eligible_packages = sorted(
            [package for package in packages if package.id not in delayed_ids],
            key=lambda package: package.delivery_deadline,
        )
    else:
        eligible_packages = packages

    print(len(eligible_packages))

    # greedily load each truck.
    # prioritizing loading special cases first, then deadlines.
    # O(t + g + n) -> O(n)
    for truck in trucks:
        if truck.id in special_cases["specific_truck"]:
            needed_in_current_truck: List = special_cases["specific_truck"][
                truck.id
            ]
            for package in needed_in_current_truck:
                if truck.capacity > 0:
                    package.delivery_status = "en route"
                    truck.load_package(package)
                    needed_in_current_truck.remove(package)
            if len(grouped_packages) > 0 and truck.capacity >= len(
                grouped_packages
            ):
                for package in grouped_packages:
                    truck.load_package(package)
                    package.delivery_status = "en route"
                    grouped_packages.remove(package)

        while truck.capacity > 0 and eligible_packages:
            package = eligible_packages.pop(0)
            package.delivery_status = "en route"
            truck.load_package(package)

    # combine leftover packages into single list, O(g + d) -> O(n)
    eligible_packages.extend(
        grouped_packages.extend(delayed_ids or []) or []
    )
    return eligible_packages


def main() -> None:

    packages, distances = load_data()

    hub = distances.get_node(address="HUB")
    trucks = [Truck(id=x, current_location=hub) for x in range(0, 2)]

    special_cases: Dict = {
        "delayed": {
            "09:05": [6, 25, 28, 32],
        },
        "specific_truck": {
            2: [3, 18, 36],
        },
        "must_be_grouped": [13, 14, 15, 19],
        "address_change": [9],
    }

    leftover_packages = load_trucks(
        trucks, packages.values(), special_cases, current_time
    )

    print(f"Leftover packages: {len(leftover_packages)}")


if __name__ == "__main__":
    main()
