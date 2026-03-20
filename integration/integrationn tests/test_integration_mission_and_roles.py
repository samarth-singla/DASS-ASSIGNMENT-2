"""Integration tests for mission planning with crew role validation."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.mission_planning import MissionPlanningModule
from integration.code.registration import RegistrationModule


class TestIntegrationMissionAndRoles(unittest.TestCase):
    """Validate mission assignment and role-driven checks."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.crew = CrewManagementModule(self.registration)
        self.mission = MissionPlanningModule(self.crew)

        self.driver = self.registration.register_member("Drake", "driver")
        self.mechanic = self.registration.register_member("Mila", "mechanic")

    def test_create_and_start_mission_with_required_roles(self) -> None:
        mission = self.mission.create_mission("Harbor Setup", ["driver", "mechanic"])
        self.mission.start_mission(mission.mission_id)
        self.assertTrue(self.mission.missions[mission.mission_id].started)

    def test_mission_start_fails_when_role_missing(self) -> None:
        mission = self.mission.create_mission("Intel Run", ["driver", "strategist"])
        with self.assertRaises(ValueError):
            self.mission.start_mission(mission.mission_id)

    def test_assign_role_then_start_mission(self) -> None:
        strategist_candidate = self.registration.register_member("Nina", "mechanic")
        self.crew.assign_role(strategist_candidate.member_id, "strategist")

        mission = self.mission.create_mission("Silent Push", ["driver", "strategist"])
        self.mission.start_mission(mission.mission_id)
        self.assertTrue(self.mission.missions[mission.mission_id].started)

    def test_set_skill_then_list_by_role(self) -> None:
        self.crew.set_skill_level(self.driver.member_id, "control", 9)
        drivers = self.crew.list_by_role("driver")
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].skills["control"], 9)


if __name__ == "__main__":
    unittest.main()
