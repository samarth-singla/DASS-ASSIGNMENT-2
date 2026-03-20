"""Unit tests for results module."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.inventory import InventoryModule
from integration.code.race_management import RaceManagementModule
from integration.code.registration import RegistrationModule
from integration.code.results import ResultsModule


class TestResultsModule(unittest.TestCase):
    """Validate result recording, points, and payouts."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.driver1 = self.registration.register_member("Alex", "driver")
        self.driver2 = self.registration.register_member("Rin", "driver")
        self.driver3 = self.registration.register_member("Sam", "driver")
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=500)
        self.car1 = self.inventory.add_vehicle("R34")
        self.car2 = self.inventory.add_vehicle("Supra")
        self.car3 = self.inventory.add_vehicle("RX7")

        self.race_mgmt = RaceManagementModule(self.registration, self.crew, self.inventory)
        self.race = self.race_mgmt.create_race("Harbor Run")
        self.race_mgmt.enter_race(self.race.race_id, self.driver1.member_id, self.car1.vehicle_id)
        self.race_mgmt.enter_race(self.race.race_id, self.driver2.member_id, self.car2.vehicle_id)
        self.race_mgmt.enter_race(self.race.race_id, self.driver3.member_id, self.car3.vehicle_id)

        self.module = ResultsModule(self.race_mgmt, self.inventory)

    def test_record_results_updates_points_and_cash(self) -> None:
        self.module.record_results(
            self.race.race_id,
            [self.driver2.member_id, self.driver1.member_id, self.driver3.member_id],
            prize_pool=300,
        )
        self.assertEqual(self.module.driver_points[self.driver2.member_id], 10)
        self.assertEqual(self.module.driver_points[self.driver1.member_id], 6)
        self.assertEqual(self.inventory.cash_balance, 800)
        self.assertTrue(self.race.completed)

    def test_record_results_reject_missing_entrant(self) -> None:
        with self.assertRaises(ValueError):
            self.module.record_results(
                self.race.race_id,
                [self.driver1.member_id, self.driver2.member_id],
                prize_pool=200,
            )

    def test_record_results_reject_second_completion(self) -> None:
        self.module.record_results(
            self.race.race_id,
            [self.driver1.member_id, self.driver2.member_id, self.driver3.member_id],
            prize_pool=100,
        )
        with self.assertRaises(ValueError):
            self.module.record_results(
                self.race.race_id,
                [self.driver1.member_id, self.driver2.member_id, self.driver3.member_id],
                prize_pool=100,
            )

    def test_leaderboard_sorted(self) -> None:
        self.module.record_results(
            self.race.race_id,
            [self.driver3.member_id, self.driver2.member_id, self.driver1.member_id],
            prize_pool=150,
        )
        self.assertEqual(
            self.module.leaderboard(),
            [
                (self.driver3.member_id, 10),
                (self.driver2.member_id, 6),
                (self.driver1.member_id, 3),
            ],
        )


if __name__ == "__main__":
    unittest.main()
