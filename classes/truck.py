from .package import Package
from .graph import Node

from dataclasses import dataclass, field
from typing import List


@dataclass
class Truck:
    id: int
    current_location: Node
    speed: int = 18
    capacity: int = 16
    contents: List = field(default_factory=list)

    def load_package(self, package: Package) -> None:
        """Load packages into the truck"""

        if self.capacity > 0:
            package.delivry_status = "en route"
            self.contents.append(package)
            self.capacity -= 1

    def deliver_package(self) -> str:
        """removes a package and reports package id"""
        package: Package = self.contents.pop(0)
        self.capacity += 1
        return package.id

    def peek_next_delivery(self) -> str:
        """Reports the address of the next delivery in the queue"""

        return self.contents[0].address
