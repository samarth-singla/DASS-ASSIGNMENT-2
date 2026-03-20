"""Integration tests for registration, race management, and results."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.inventory import InventoryModule
from integration.code.race_management import RaceManagementModule
from integration.code.registration import RegistrationModule
from integration.code.results import ResultsModule


class TestIntegrationDriverRaceResults(unittest.TestCase):
    """Validate end-to-end flow from registration to race results."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=1000)
        self.race_mgmt = RaceManagementModule(self.registration, self.crew, self.inventory)
        self.results = ResultsModule(self.race_mgmt, self.inventory)

        self.driver1 = self.registration.register_member("Alex", "driver")
        self.driver2 = self.registration.register_member("Rin", "driver")
        self.driver3 = self.registration.register_member("Sam", "driver")

        self.car1 = self.inventory.add_vehicle("R34")
        self.car2 = self.inventory.add_vehicle("Supra")
        self.car3 = self.inventory.add_vehicle("RX7")

        self.race = self.race_mgmt.create_race("Night Drift")

    def test_register_enter_race_record_results_success(self) -> None:
        self.race_mgmt.enter_race(self.race.race_id, self.driver1.member_id, self.car1.vehicle_id)
        self.race_mgmt.enter_race(self.race.race_id, self.driver2.member_id, self.car2.vehicle_id)
        self.race_mgmt.enter_race(self.race.race_id, self.driver3.member_id, self.car3.vehicle_id)

        self.results.record_results(
            self.race.race_id,
            [self.driver2.member_id, self.driver1.member_id, self.driver3.member_id],
            prize_pool=350,
        )

        self.assertEqual(self.inventory.cash_balance, 1350)
        self.assertTrue(self.race.completed)
        self.assertTrue(self.inventory.vehicles[self.car1.vehicle_id].available)
        self.assertTrue(self.inventory.vehicles[self.car2.vehicle_id].available)
        self.assertTrue(self.inventory.vehicles[self.car3.vehicle_id].available)

    def test_enter_race_without_registered_driver_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.race_mgmt.enter_race(self.race.race_id, driver_id=999, vehicle_id=self.car1.vehicle_id)

    def test_enter_race_with_non_driver_role_raises(self) -> None:
        mechanic = self.registration.register_member("Mia", "mechanic")
        with self.assertRaises(ValueError):
            self.race_mgmt.enter_race(self.race.race_id, mechanic.member_id, self.car1.vehicle_id)

    def test_record_results_requires_all_entrants(self) -> None:
        self.race_mgmt.enter_race(self.race.race_id, self.driver1.member_id, self.car1.vehicle_id)
        self.race_mgmt.enter_race(self.race.race_id, self.driver2.member_id, self.car2.vehicle_id)
        self.race_mgmt.enter_race(self.race.race_id, self.driver3.member_id, self.car3.vehicle_id)

        with self.assertRaises(ValueError):
            self.results.record_results(
                self.race.race_id,
                [self.driver1.member_id, self.driver2.member_id],
                prize_pool=100,
            )


if __name__ == "__main__":
    unittest.main()
