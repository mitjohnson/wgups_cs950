__doc__ = """
WGUPS Routing Program (traveling salesman)
Solution created by Mitchell Johnson for CS950 @ WGU.
Student ID: xxxxxxxxx
"""
from data import load_data
from classes import Hashtable, Graph, Node, Truck, Package, SimulationManager
from dijkstas_sp import shortest_path

from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Simulation:
    packages: Hashtable
    trucks: List[Truck]
    distances: Graph
    simulation_manager: SimulationManager
    hub: Node

    def initialize(
        self,
        simulation_start: datetime = datetime(2025, 8, 24, 8),
        simulation_end: datetime = datetime(2025, 8, 25, 0),
    ) -> SimulationManager:
        """initialize the Simulation"""

        self.packages, self.distances = load_data()
        print("packages arrived at hub.\n")

        self.simulation_manager = SimulationManager(
            simulation_start,
            simulation_end,
        )

        self.hub = self.distances.get_node(address="HUB")
        self.trucks = [
            Truck(id=x, current_location=self.hub) for x in range(0, 2)
        ]
        print("Trucks have fueled up and are ready for delivery\n")

    def run_simulation(self) -> None:

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

        current_time: datetime = self.simulation_manager.get_current_time()
        package_list = self.packages.values()
        leftover_packages: List = Truck.load_trucks(
            self.trucks,
            package_list,
            special_cases,
            current_time,
        )

        self.simulation_manager.log_event(
            "Trucks finsihed loading."
            + f"Loaded {len(package_list)-len(leftover_packages)} in truck, "
            + f"left {len(leftover_packages)} at hub.",
        )

        while not self.simulation_manager.is_simulation_over():
            for truck in self.trucks:
                if truck.contents:
                    shortest_paths = shortest_path(
                        truck.current_location, self.distances
                    )

                    closest_package: Optional[Package] = None
                    closest_distance: float = float("inf")
                    closest_package_node: Optional[Node] = None
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
                        self.simulation_manager.advance_time(travel_time)
                        self.simulation_manager.log_event(
                            f"Truck {truck.id} delivered {closest_package} "
                            + f"to {closest_package.address}."
                        )
        self.simulation_manager.log_event(
            f"Finished at {self.simulation_manager.get_current_time}"
        )

        for event in self.simulation_manager.events:
            print(f"{event}\n")


def main() -> None:

    simulation = Simulation
    simulation.initialize(simulation)
    simulation.run_simulation(simulation)


if __name__ == "__main__":
    main()
