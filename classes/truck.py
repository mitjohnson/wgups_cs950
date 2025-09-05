from .package import Package
from .graph import Node
from .simulation_manager import SimulationManager

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict


@dataclass
class Truck:
    id: int
    current_location: Node
    speed: int = 18
    capacity: int = 16
    contents: List = field(default_factory=list)
    truck_time: datetime = datetime(2025, 8, 24, 8)

    def load_package(self, package: Package) -> None:
        """Load packages into the truck"""

        if self.capacity > 0:
            package.delivry_status = "en route"
            package.loading_time = self.truck_time
            self.contents.append(package)
            self.capacity -= 1

    def deliver_package(self, node: Node, distance: float) -> timedelta:
        """
        removes a package and reports travel time to a node

        Overall complexity: O(p)
        """

        travel_time = SimulationManager.calculate_travel_time(
            distance, self.speed
        )

        # O(p), where p is the number of packages in the truck
        for idx, pkg in enumerate(self.contents):
            if pkg.address == node.address:
                self.truck_time += travel_time
                package = self.contents.pop(idx)
                package.delivery_status = "delivered"
                package.delivery_time = self.truck_time
                self.capacity += 1
                return travel_time

    def travel_to_node(self, node: Node, distance: float) -> timedelta:
        """Calculates travel time to a node"""

        travel_time = SimulationManager.calculate_travel_time(
            distance, self.speed
        )
        return travel_time

    def load_multipe_packages(self, packages: List[Package]) -> None:
        """Load multiple packages into the truck"""
        for package in packages:
            if self.capacity > 0:
                self.load_package(package)
                package.delivery_status = "en route"

    @staticmethod
    def load_trucks(
        trucks: List["Truck"],
        packages: List[Package],
        special_cases: Dict,
        current_time: datetime,
    ) -> List:
        """
        method to handle truck loading logic

        Overall complexity: O(n log n), Δ(n).
        """

        eligible_packages = []

        # destruct packages that need grouped, O(1).
        grouped_packages: List = [
            package
            for package in packages
            if package.id in special_cases["must_be_grouped"]
            and package.delivery_status != "delivered"
            and package.delivery_status != "en route"
        ]

        # destruct delayed packages, O(d)
        delayed_ids = []
        for time_str, package_ids in special_cases["delayed"].items():
            if (
                datetime.strptime(time_str, "%H:%M").time()
                > current_time.time()
            ):
                delayed_ids = package_ids

        # mark delayed packages, O(d)
        for package in packages:
            if package.id in delayed_ids:
                package.delivery_status = "delayed"

        # filter out delayed packages
        # O(n log n) if we have delayed packages, O(1) otherwise.
        if len(delayed_ids) > 0:
            eligible_packages.extend(
                sorted(
                    [
                        package
                        for package in packages
                        if package.id not in delayed_ids
                        and package not in grouped_packages
                    ],
                    key=lambda package: package.delivery_deadline,
                )
            )
        else:
            eligible_packages.extend(packages)

        # greedily load each truck.
        # prioritizing loading by special cases first, then by deadlines.
        # O(t + g + n) -> O(n)
        for truck in trucks:
            to_remove = []
            if truck.id + 1 in special_cases["specific_truck"].keys():
                needed_in_current_truck: List = special_cases[
                    "specific_truck"
                ][truck.id + 1]
                for package in eligible_packages:
                    if (
                        truck.capacity > 0
                        and package.id in needed_in_current_truck
                    ):
                        package.delivery_status = "en route"
                        truck.load_package(package)
                        to_remove.append(package)

                for package in to_remove:
                    eligible_packages.remove(package)

            if len(grouped_packages) > 0 and truck.capacity >= len(
                grouped_packages
            ):
                truck.load_multipe_packages(grouped_packages)
                grouped_packages = []

            while truck.capacity > 0 and len(eligible_packages) > 0:
                package = eligible_packages.pop(0)
                package.delivery_status = "en route"
                truck.load_package(package)

        # combine leftover packages into single list, O(n)
        return [
            p
            for p in packages
            if p.delivery_status == "at hub" or p.delivery_status == "delayed"
        ]
