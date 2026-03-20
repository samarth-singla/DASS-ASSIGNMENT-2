"""Integration-focused error-path tests to complete branch coverage."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.inventory import InventoryModule
from integration.code.mission_planning import MissionPlanningModule
from integration.code.race_management import RaceManagementModule
from integration.code.registration import RegistrationModule
from integration.code.results import ResultsModule
from integration.code.sponsorship_budget import SponsorshipBudgetModule
from integration.code.vehicle_maintenance import VehicleMaintenanceModule


class TestIntegrationErrorPathsCoverage(unittest.TestCase):
    """Cover remaining branch paths across modules."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=200)
        self.race = RaceManagementModule(self.registration, self.crew, self.inventory)
        self.results = ResultsModule(self.race, self.inventory)
        self.mission = MissionPlanningModule(self.crew)
        self.maintenance = VehicleMaintenanceModule(self.inventory)
        self.sponsorship = SponsorshipBudgetModule(self.inventory)

        self.driver = self.registration.register_member("Kai", "driver")
        self.vehicle = self.inventory.add_vehicle("GT-R")

    def test_registration_empty_name_and_get_missing(self) -> None:
        with self.assertRaises(ValueError):
            self.registration.register_member("   ", "driver")
        with self.assertRaises(ValueError):
            self.registration.get_member(999)

    def test_race_not_found_and_vehicle_validation_paths(self) -> None:
        with self.assertRaises(ValueError):
            self.race.enter_race(999, self.driver.member_id, self.vehicle.vehicle_id)

        race_event = self.race.create_race("City Loop")
        with self.assertRaises(ValueError):
            self.race.enter_race(race_event.race_id, self.driver.member_id, 999)

    def test_results_invalid_race_and_negative_prize(self) -> None:
        with self.assertRaises(ValueError):
            self.results.record_results(999, [self.driver.member_id], prize_pool=100)

        race_event = self.race.create_race("Dock Sprint")
        self.race.enter_race(race_event.race_id, self.driver.member_id, self.vehicle.vehicle_id)
        with self.assertRaises(ValueError):
            self.results.record_results(race_event.race_id, [self.driver.member_id], prize_pool=-1)

    def test_inventory_negative_quantity_paths(self) -> None:
        with self.assertRaises(ValueError):
            self.inventory.add_part("brake", -1)
        with self.assertRaises(ValueError):
            self.inventory.add_tool("spanner", -3)
        with self.assertRaises(ValueError):
            self.inventory.set_vehicle_available(999, True)

    def test_mission_create_and_start_invalid_paths(self) -> None:
        with self.assertRaises(ValueError):
            self.mission.create_mission("   ", ["driver"])
        with self.assertRaises(ValueError):
            self.mission.create_mission("No Roles", ["   "])
        with self.assertRaises(ValueError):
            self.mission.start_mission(999)

    def test_sponsorship_invalid_paths(self) -> None:
        with self.assertRaises(ValueError):
            self.sponsorship.sign_contract("   ", 100)
        with self.assertRaises(ValueError):
            self.sponsorship.sign_contract("FastFuel", 0)
        with self.assertRaises(ValueError):
            self.sponsorship.receive_payout("MissingSponsor")
        with self.assertRaises(ValueError):
            self.sponsorship.apply_penalty(0)

    def test_maintenance_invalid_paths(self) -> None:
        with self.assertRaises(ValueError):
            self.maintenance.apply_wear(self.vehicle.vehicle_id, -1)
        with self.assertRaises(ValueError):
            self.maintenance.apply_wear(999, 10)
        with self.assertRaises(ValueError):
            self.maintenance.repair_vehicle(999, "engine_kit", 1, 10, 5)
        with self.assertRaises(ValueError):
            self.maintenance.repair_vehicle(self.vehicle.vehicle_id, "engine_kit", 0, 10, 5)
        with self.assertRaises(ValueError):
            self.maintenance.repair_vehicle(self.vehicle.vehicle_id, "engine_kit", 1, -1, 5)
        with self.assertRaises(ValueError):
            self.maintenance.repair_vehicle(self.vehicle.vehicle_id, "engine_kit", 1, 10, 0)


if __name__ == "__main__":
    unittest.main()
