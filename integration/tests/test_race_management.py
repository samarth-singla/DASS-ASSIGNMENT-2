"""Unit tests for race management module."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.inventory import InventoryModule
from integration.code.race_management import RaceManagementModule
from integration.code.registration import RegistrationModule


class TestRaceManagementModule(unittest.TestCase):
    """Validate race setup and entry constraints."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.driver = self.registration.register_member("Alex", "driver")
        self.mechanic = self.registration.register_member("Mia", "mechanic")
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=1000)
        self.car = self.inventory.add_vehicle("R34")
        self.module = RaceManagementModule(self.registration, self.crew, self.inventory)
        self.race = self.module.create_race("Night Sprint")

    def test_enter_race_success(self) -> None:
        self.module.enter_race(self.race.race_id, self.driver.member_id, self.car.vehicle_id)
        self.assertEqual(len(self.race.entrants), 1)
        self.assertFalse(self.inventory.vehicles[self.car.vehicle_id].available)

    def test_enter_race_reject_non_driver(self) -> None:
        with self.assertRaises(ValueError):
            self.module.enter_race(
                self.race.race_id, self.mechanic.member_id, self.car.vehicle_id
            )

    def test_enter_race_reject_unavailable_car(self) -> None:
        self.inventory.set_vehicle_available(self.car.vehicle_id, False)
        with self.assertRaises(ValueError):
            self.module.enter_race(self.race.race_id, self.driver.member_id, self.car.vehicle_id)


if __name__ == "__main__":
    unittest.main()
