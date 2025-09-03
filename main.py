__doc__ = """
WGUPS Routing Program (traveling salesman)
Solution created by Mitchell Johnson for CS950 @ WGU.
Student ID: xxxxxxxxx
"""

from simulation import Simulation as WGUUPS
from datetime import datetime, time
from typing import Tuple


def get_time_from_user() -> Tuple[datetime, datetime]:
    """Prompts user for simulation time inputs"""

    while True:
        start_time_input = input("Enter a start time (HH:MM AM/PM): ")
        try:
            start_time = datetime.strptime(
                start_time_input.strip().lower(), "%I:%M %p"
            ).time()
            break
        except ValueError:
            print("Invalid start time format. Please try again.\n")

    while True:
        end_time_input = input("Enter an end time (HH:MM AM/PM): ")
        try:
            end_time = datetime.strptime(
                end_time_input.strip().lower(), "%I:%M %p"
            ).time()
            break
        except ValueError:
            print("Invalid end time format. Please try again.\n")

    return (start_time, end_time)


def main(prompt_user: bool) -> None:
    """Main entry point for the program"""

    while prompt_user:
        simulation: WGUUPS = WGUUPS

        print("Welcome to the supervisor dashboard!.\n")

        # Get valid start and end times from user
        valid_times = False
        while not valid_times:
            start_time, end_time = get_time_from_user()

            if start_time < end_time and end_time > time(7, 59):
                valid_times = True
            elif start_time >= end_time:
                print(
                    "Start time must be before end time. Please try again.\n"
                )
            elif end_time <= time(7, 59):
                print("End time must be 08:00 AM at a minimum. Please try again.\n")

        # convert times to datetimes for simulation
        now = datetime.now()
        start_datetime = datetime.combine(now.date(), start_time)
        end_datetime = datetime.combine(now.date(), end_time)

        # begin simulation
        simulation.initialize(
            simulation,
            simulation_start=start_datetime,
            simulation_end=end_datetime,
        )

        simulation.run_simulation(simulation)

        should_continue = (
            input("Run another simulation? (y/N): ").strip().lower()
        )

        # reprompt user or exit
        if should_continue != "y":
            prompt_user = False
            print("Exiting the program. Goodbye!")


if __name__ == "__main__":
    prompt_user = True
    main(prompt_user)
