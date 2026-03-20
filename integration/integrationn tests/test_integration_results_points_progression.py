"""Integration tests for race result points progression across events."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.inventory import InventoryModule
from integration.code.race_management import RaceManagementModule
from integration.code.registration import RegistrationModule
from integration.code.results import ResultsModule


class TestIntegrationResultsPointsProgression(unittest.TestCase):
    """Validate point accumulation and leaderboard stability over races."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=500)
        self.race_mgmt = RaceManagementModule(self.registration, self.crew, self.inventory)
        self.results = ResultsModule(self.race_mgmt, self.inventory)

        self.driver1 = self.registration.register_member("Neo", "driver")
        self.driver2 = self.registration.register_member("Ivy", "driver")
        self.driver3 = self.registration.register_member("Zed", "driver")

        self.car1 = self.inventory.add_vehicle("C1")
        self.car2 = self.inventory.add_vehicle("C2")
        self.car3 = self.inventory.add_vehicle("C3")

    def _run_race(self, race_name: str, order: list[int], prize_pool: int) -> None:
        race = self.race_mgmt.create_race(race_name)
        self.race_mgmt.enter_race(race.race_id, self.driver1.member_id, self.car1.vehicle_id)
        self.race_mgmt.enter_race(race.race_id, self.driver2.member_id, self.car2.vehicle_id)
        self.race_mgmt.enter_race(race.race_id, self.driver3.member_id, self.car3.vehicle_id)
        self.results.record_results(race.race_id, order, prize_pool)

    def test_points_accumulate_across_two_races(self) -> None:
        self._run_race("R1", [self.driver1.member_id, self.driver2.member_id, self.driver3.member_id], 50)
        self._run_race("R2", [self.driver2.member_id, self.driver3.member_id, self.driver1.member_id], 60)
        self.assertEqual(self.results.driver_points[self.driver1.member_id], 13)
        self.assertEqual(self.results.driver_points[self.driver2.member_id], 16)
        self.assertEqual(self.results.driver_points[self.driver3.member_id], 9)

    def test_cash_accumulates_with_multiple_prizes(self) -> None:
        self._run_race("R1", [self.driver3.member_id, self.driver1.member_id, self.driver2.member_id], 80)
        self._run_race("R2", [self.driver1.member_id, self.driver2.member_id, self.driver3.member_id], 70)
        self.assertEqual(self.inventory.cash_balance, 650)

    def test_leaderboard_after_multiple_races(self) -> None:
        self._run_race("R1", [self.driver2.member_id, self.driver1.member_id, self.driver3.member_id], 20)
        self._run_race("R2", [self.driver2.member_id, self.driver3.member_id, self.driver1.member_id], 20)
        leaderboard = self.results.leaderboard()
        self.assertEqual(leaderboard[0][0], self.driver2.member_id)
        self.assertEqual(leaderboard[0][1], 20)

    def test_completed_race_rejects_second_record(self) -> None:
        race = self.race_mgmt.create_race("R3")
        self.race_mgmt.enter_race(race.race_id, self.driver1.member_id, self.car1.vehicle_id)
        self.race_mgmt.enter_race(race.race_id, self.driver2.member_id, self.car2.vehicle_id)
        self.race_mgmt.enter_race(race.race_id, self.driver3.member_id, self.car3.vehicle_id)
        self.results.record_results(
            race.race_id,
            [self.driver1.member_id, self.driver2.member_id, self.driver3.member_id],
            10,
        )
        with self.assertRaises(ValueError):
            self.results.record_results(
                race.race_id,
                [self.driver1.member_id, self.driver2.member_id, self.driver3.member_id],
                10,
            )


if __name__ == "__main__":
    unittest.main()
