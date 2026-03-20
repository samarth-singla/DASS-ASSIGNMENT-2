"""Integration tests for role transition effects on race and mission flows."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.inventory import InventoryModule
from integration.code.mission_planning import MissionPlanningModule
from integration.code.race_management import RaceManagementModule
from integration.code.registration import RegistrationModule


class TestIntegrationRoleTransitionEffects(unittest.TestCase):
    """Validate how role changes alter downstream module behavior."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.inventory = InventoryModule(initial_cash=300)
        self.race = RaceManagementModule(self.registration, self.crew, self.inventory)
        self.mission = MissionPlanningModule(self.crew)

        self.member = self.registration.register_member("Robin", "mechanic")
        self.vehicle = self.inventory.add_vehicle("ShiftCar")

    def test_mechanic_cannot_enter_race_before_role_change(self) -> None:
        race = self.race.create_race("RoleCheckRace")
        with self.assertRaises(ValueError):
            self.race.enter_race(race.race_id, self.member.member_id, self.vehicle.vehicle_id)

    def test_member_can_enter_race_after_driver_assignment(self) -> None:
        self.crew.assign_role(self.member.member_id, "driver")
        race = self.race.create_race("AfterPromotionRace")
        self.race.enter_race(race.race_id, self.member.member_id, self.vehicle.vehicle_id)
        self.assertEqual(len(self.race.races[race.race_id].entrants), 1)

    def test_member_can_satisfy_strategist_mission_after_role_change(self) -> None:
        self.crew.assign_role(self.member.member_id, "strategist")
        mission = self.mission.create_mission("PlanShift", ["strategist"])
        self.mission.start_mission(mission.mission_id)
        self.assertTrue(self.mission.missions[mission.mission_id].started)

    def test_role_reassignment_updates_role_lists(self) -> None:
        self.crew.assign_role(self.member.member_id, "driver")
        drivers = self.crew.list_by_role("driver")
        mechanics = self.crew.list_by_role("mechanic")
        self.assertEqual(len(drivers), 1)
        self.assertEqual(len(mechanics), 0)


if __name__ == "__main__":
    unittest.main()
