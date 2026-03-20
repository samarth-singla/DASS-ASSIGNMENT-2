"""Additional integration tests for vehicle availability race cycles."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.inventory import InventoryModule
from integration.code.race_management import RaceManagementModule
from integration.code.registration import RegistrationModule
from integration.code.results import ResultsModule


class TestIntegrationReuseVehicleCycles(unittest.TestCase):
    """Ensure vehicles move through unavailable and available states correctly."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=300)
        self.race_mgmt = RaceManagementModule(self.registration, self.crew, self.inventory)
        self.results = ResultsModule(self.race_mgmt, self.inventory)

        self.driver_a = self.registration.register_member("A", "driver")
        self.driver_b = self.registration.register_member("B", "driver")
        self.car_a = self.inventory.add_vehicle("CarA")
        self.car_b = self.inventory.add_vehicle("CarB")

    def test_vehicle_unavailable_immediately_after_entry(self) -> None:
        race = self.race_mgmt.create_race("R1")
        self.race_mgmt.enter_race(race.race_id, self.driver_a.member_id, self.car_a.vehicle_id)
        self.assertFalse(self.inventory.vehicles[self.car_a.vehicle_id].available)

    def test_vehicle_released_after_result_submission(self) -> None:
        race = self.race_mgmt.create_race("R2")
        self.race_mgmt.enter_race(race.race_id, self.driver_a.member_id, self.car_a.vehicle_id)
        self.race_mgmt.enter_race(race.race_id, self.driver_b.member_id, self.car_b.vehicle_id)
        self.results.record_results(race.race_id, [self.driver_a.member_id, self.driver_b.member_id], 50)
        self.assertTrue(self.inventory.vehicles[self.car_a.vehicle_id].available)
        self.assertTrue(self.inventory.vehicles[self.car_b.vehicle_id].available)

    def test_reuse_same_vehicle_in_new_race_after_release(self) -> None:
        race1 = self.race_mgmt.create_race("R3")
        self.race_mgmt.enter_race(race1.race_id, self.driver_a.member_id, self.car_a.vehicle_id)
        self.race_mgmt.enter_race(race1.race_id, self.driver_b.member_id, self.car_b.vehicle_id)
        self.results.record_results(race1.race_id, [self.driver_b.member_id, self.driver_a.member_id], 20)

        race2 = self.race_mgmt.create_race("R4")
        self.race_mgmt.enter_race(race2.race_id, self.driver_a.member_id, self.car_a.vehicle_id)
        self.assertFalse(self.inventory.vehicles[self.car_a.vehicle_id].available)


if __name__ == "__main__":
    unittest.main()
