__doc__ = """
WGUPS Routing Program (traveling salesman)
Solution created by Mitchell Johnson for CS950 @ WGU.
Student ID: xxxxxxxxx
"""
from data import load_data
from classes import Truck, Package
from datetime import time

from typing import List, Tuple, Dict


def load_trucks(
    trucks: List[Truck], packages_to_deliver: List[Package], current_time: time
) -> Tuple[List, List, List]:
    """method to handle truck loading logic"""

    # sort packages by deadline to get them out the door.
    packages_by_deadline: List[Package] = sorted(
        packages_to_deliver, key=lambda pkg: pkg.delivery_deadline
    )

    # TODO: Look at knapsack problem again.
    special_cases: Dict[str, List[int]] = {
        "must be on truck 2": [3, 18, 36],
        "delayed until 09:05": [6, 25, 28, 32],
        "must be grouped together": [13, 14, 15, 19],
    }


def main() -> None:

    packages, distances = load_data()

    current_time = time(8, 00)
    hub = distances.get_node(address="HUB")
    trucks = [Truck(id=x, current_location=hub) for x in range(0, 2)]

    load_trucks(trucks, packages.values(), current_time)


if __name__ == "__main__":
    main()
