from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List


@dataclass
class SimulationManager:
    current_time: datetime
    simulation_end: datetime
    events: List = field(default_factory=list)

    def advance_time(self, travel_time: timedelta) -> None:
        """Advances global time"""

        if travel_time <= self.simulation_end:
            self.current_time += travel_time

    def log_event(self, description: str) -> None:
        """keeps track of simulation events"""

        self.events.append(f"{self.current_time}: {description}")

    def get_current_time(self) -> datetime:
        """Get the current time of the simulation"""

        return self.current_time

    def is_simulation_over(self) -> bool:
        """return true if simulation has ended"""

        return self.current_time >= self.simulation_end

    @staticmethod
    def calculate_travel_time(distance: float, speed: int) -> timedelta:
        """Calculates travel time"""

        return timedelta(minutes=(60 * (distance / speed)))
