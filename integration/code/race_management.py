"""Race management module for race creation and entry."""

from typing import Dict

from .crew_management import CrewManagementModule
from .inventory import InventoryModule
from .models import RaceEvent
from .registration import RegistrationModule


class RaceManagementModule:
    """Create races and register race entrants under business rules."""

    def __init__(
        self,
        registration: RegistrationModule,
        crew: CrewManagementModule,
        inventory: InventoryModule,
    ) -> None:
        self.registration = registration
        self.crew = crew
        self.inventory = inventory
        self.races: Dict[int, RaceEvent] = {}
        self._next_race_id = 1

    def create_race(self, name: str) -> RaceEvent:
        """Create and store a new race event."""
        race = RaceEvent(race_id=self._next_race_id, name=name.strip())
        self.races[self._next_race_id] = race
        self._next_race_id += 1
        return race

    def enter_race(self, race_id: int, driver_id: int, vehicle_id: int) -> None:
        """Enter a driver and vehicle into a race after validation."""
        if race_id not in self.races:
            raise ValueError("Race not found.")

        driver = self.registration.get_member(driver_id)
        if driver.role != "driver":
            raise ValueError("Only drivers can enter races.")

        if vehicle_id not in self.inventory.vehicles:
            raise ValueError("Vehicle not found.")
        vehicle = self.inventory.vehicles[vehicle_id]
        if not vehicle.available:
            raise ValueError("Vehicle is not available.")

        self.races[race_id].entrants.append(
            {"driver_id": driver_id, "vehicle_id": vehicle_id}
        )
        vehicle.available = False
