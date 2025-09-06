from data import load_data
from classes import Hashtable, Graph, Node, Truck, Package, SimulationManager
from dijkstas_sp import shortest_path

from datetime import datetime, time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Simulation:
    packages: Hashtable
    trucks: List[Truck]
    distances: Graph
    simulation_manager: SimulationManager
    hub: Node
    special_cases: Dict
    leftover_packages: List = field(default_factory=list)

    def initialize(
        self,
        simulation_start: datetime = datetime(2025, 8, 24, 8),
        simulation_end: datetime = datetime(2025, 8, 25, 0),
    ) -> SimulationManager:
        """initialize the Simulation"""

        self.packages, self.distances = load_data()

        self.simulation_manager = SimulationManager(
            simulation_start,
            simulation_end,
        )

        self.special_cases = {
            "delayed": {
                "09:05": [6, 25, 28, 32],
            },
            "specific_truck": {
                2: [3, 18, 36, 38],
            },
            "must_be_grouped": [13, 14, 15, 16, 19, 20],
            "address_change": [9],
        }

        self.hub = self.distances.get_node(address="HUB")
        self.trucks = [
            Truck(
                id=x,
                current_location=self.hub,
                truck_time=self.simulation_manager.get_current_time(),
            )
            for x in range(0, 2)
        ]

    def start_delivery(self) -> None:
        """
        runs delivery algorithm for the simulation

        Overall Complexity: O(t * p) -> O(n^2)
        """

        # O(t)
        for truck in self.trucks:
            while (
                len(truck.contents) > 0
                and self.simulation_manager.is_simulation_over() is False
            ):
                shortest_paths = shortest_path(
                    truck.current_location, self.distances
                )

                closest_package: Optional[Package] = None
                closest_distance: float = float("inf")
                closest_package_node: Optional[Node] = None

                # O(p)
                for package in truck.contents:
                    destination_node = self.distances.get_node(
                        address=package.address
                    )

                    if destination_node in shortest_paths:
                        distance = shortest_paths[destination_node]
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_package = package
                            closest_package_node = destination_node

                if closest_package is not None:
                    travel_time = truck.deliver_package(
                        closest_package_node, closest_distance
                    )
                    truck.current_location = closest_package_node
                    self.simulation_manager.total_milage += closest_distance
                    self.simulation_manager.packages_delivered += 1
                    self.simulation_manager.advance_time(travel_time)

                    if (
                        self.simulation_manager.get_current_time().time()
                        >= time(10, 30)
                    ):
                        address_change_package = self.packages.get(9)
                        if (
                            address_change_package.address
                            != "410 South State St"
                        ):
                            address_change_package.address = (
                                "410 South State St"
                            )
                            address_change_package.city = "Salt Lake City"
                            address_change_package.zip_code = "84111"
                            self.simulation_manager.log_event(
                                "Package 9 address updated to "
                                + "410 S State St, Salt Lake City, UT 84111."
                            )

                    self.simulation_manager.log_event(
                        f"Truck {truck.id + 1} delivered {closest_package} "
                        + f"to {closest_package.address}."
                    )

    def reload_truck(self, truck: Truck, packages: List) -> None:
        """
        Returns truck to the hub and reloads packages

        Overall Complexity O(n log n)
        """

        # O((V+E) log v) dijkstras
        shortest_paths = shortest_path(truck.current_location, self.distances)
        if self.hub in shortest_paths:
            distance_to_hub = shortest_paths[self.hub]
            travel_time = truck.travel_to_node(self.hub, distance_to_hub)
            truck.current_location = self.hub
            self.simulation_manager.advance_time(travel_time)

        self.simulation_manager.log_event(
            f"Truck {truck.id + 1} returned to the hub."
        )

        # O(n log n)
        leftover_packages = Truck.load_trucks(
            [truck],
            self.leftover_packages,
            self.special_cases,
            self.simulation_manager.get_current_time(),
        )

        self.leftover_packages = leftover_packages
        self.simulation_manager.log_event(
            f"Truck {truck.id + 1} reloaded at the hub."
        )

    def log_truck_contents(self) -> None:
        """Logs the contents of all trucks"""

        for truck in self.trucks:
            log = f"truck {truck.id + 1} contents: \n"
            for package in truck.contents:
                log += (
                    f"ID: {package.id}, address: {package.address}, "
                    + f"loading time: {package.loading_time}, "
                    + f"delivery status: {package.delivery_status}, "
                    + f"delivery deadline: {package.delivery_deadline}, "
                    + f"special notes: {package.special_notes}\n"
                )
            self.simulation_manager.log_event(log)

    def log_leftover_packages(self) -> None:
        """Logs packages left at the hub"""

        log = "Packages left at hub:\n"
        for package in self.leftover_packages:
            log += (
                f"ID: {package.id}, address: {package.address}, "
                + f"delivery status: {package.delivery_status}, "
                + f"delivery deadline: {package.delivery_deadline}, "
                + f"special notes: {package.special_notes}\n"
            )
        self.simulation_manager.log_event(log)

    def run_simulation(self) -> None:
        """Main logic for WGUPS simulation"""

        current_time: datetime = self.simulation_manager.get_current_time()
        package_list = self.packages.values()

        # We do not open until 08:00 AM
        if current_time.time() < time(8, 0):
            target_time = datetime.combine(current_time.date(), time(8, 0))
            time_difference = target_time - current_time

            self.simulation_manager.advance_time(time_difference)
            for truck in self.trucks:
                truck.truck_time = self.simulation_manager.get_current_time()

            self.simulation_manager.log_event("Advanced time to 08:00 AM.")

        # Load truck and keep track on packages left at hub.
        # O(n log n)
        self.leftover_packages: List = Truck.load_trucks(
            self.trucks,
            package_list,
            self.special_cases,
            current_time,
        )

        self.simulation_manager.log_event(
            "Trucks finsihed loading. "
            + f"Loaded {len(package_list)-(len(self.leftover_packages))}, "
            + f"left {len(self.leftover_packages)} at hub.",
        )

        self.log_truck_contents(self)
        self.log_leftover_packages(self)

        while not self.simulation_manager.is_simulation_over():
            # Deliver all loaded packages
            self.start_delivery(self)

            # if we have any leftovers, go grab and deliver them.
            if self.leftover_packages:
                truck_one_to_hub: float = shortest_path(
                    self.trucks[0].current_location, self.distances
                )[self.hub]
                truck_two_to_hub: float = shortest_path(
                    self.trucks[1].current_location, self.distances
                )[self.hub]

                if truck_one_to_hub < truck_two_to_hub:
                    self.reload_truck(
                        self,
                        self.trucks[0],
                        self.leftover_packages,
                    )
                else:
                    self.reload_truck(
                        self,
                        self.trucks[1],
                        self.leftover_packages,
                    )
                self.log_truck_contents(self)
                self.log_leftover_packages(self)
                self.start_delivery(self)

        packages_log = "Final package states:\n"
        for pakage in sorted(self.packages.values(), key=lambda x: x.id):
            packages_log += (
                f"ID: {pakage.id}, address: {pakage.address}, "
                + f"delivery status: {pakage.delivery_status}, "
                + f"delivery time: {pakage.delivery_time}, "
                + f"special notes: {pakage.special_notes}\n"
            )
        self.simulation_manager.log_event(packages_log)

        self.simulation_manager.log_event(
            f"Finished delivering {self.simulation_manager.packages_delivered}"
            + " packages with a total mileage of "
            + str(self.simulation_manager.total_milage),
        )

        for event in self.simulation_manager.events:
            print(f"{event}\n\n")
