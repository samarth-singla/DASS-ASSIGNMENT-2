"""Additional integration tests for duplicates and ranking behavior."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.inventory import InventoryModule
from integration.code.race_management import RaceManagementModule
from integration.code.registration import RegistrationModule
from integration.code.results import ResultsModule


class TestIntegrationDuplicateAndSorting(unittest.TestCase):
    """Validate duplicate checks and ranking consistency."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=200)
        self.race_mgmt = RaceManagementModule(self.registration, self.crew, self.inventory)
        self.results = ResultsModule(self.race_mgmt, self.inventory)

    def test_registration_duplicate_name_blocks_second_member(self) -> None:
        self.registration.register_member("Ari", "driver")
        with self.assertRaises(ValueError):
            self.registration.register_member("ari", "mechanic")

    def test_leaderboard_sort_order_for_tie_points(self) -> None:
        driver1 = self.registration.register_member("D1", "driver")
        driver2 = self.registration.register_member("D2", "driver")
        self.results.driver_points[driver2.member_id] = 10
        self.results.driver_points[driver1.member_id] = 10
        self.assertEqual(
            self.results.leaderboard(),
            [(driver1.member_id, 10), (driver2.member_id, 10)],
        )

    def test_set_skill_rejects_out_of_range_level(self) -> None:
        member = self.registration.register_member("Mira", "mechanic")
        with self.assertRaises(ValueError):
            self.crew.set_skill_level(member.member_id, "tuning", 11)


if __name__ == "__main__":
    unittest.main()
