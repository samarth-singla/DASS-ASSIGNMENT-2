"""Unit tests for mission planning module."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.mission_planning import MissionPlanningModule
from integration.code.registration import RegistrationModule


class TestMissionPlanningModule(unittest.TestCase):
    """Validate mission creation and start constraints."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.registration.register_member("Alex", "driver")
        self.registration.register_member("Mia", "mechanic")
        self.crew = CrewManagementModule(self.registration)
        self.module = MissionPlanningModule(self.crew)

    def test_create_mission_success(self) -> None:
        mission = self.module.create_mission("Dock Run", ["driver", "mechanic"])
        self.assertEqual(mission.required_roles, ["driver", "mechanic"])

    def test_start_mission_success_when_roles_present(self) -> None:
        mission = self.module.create_mission("Midnight Setup", ["driver", "mechanic"])
        self.module.start_mission(mission.mission_id)
        self.assertTrue(self.module.missions[mission.mission_id].started)

    def test_start_mission_reject_missing_role(self) -> None:
        mission = self.module.create_mission("Advanced Plan", ["driver", "strategist"])
        with self.assertRaises(ValueError):
            self.module.start_mission(mission.mission_id)

    def test_start_mission_reject_second_start(self) -> None:
        mission = self.module.create_mission("One Shot", ["driver"])
        self.module.start_mission(mission.mission_id)
        with self.assertRaises(ValueError):
            self.module.start_mission(mission.mission_id)


if __name__ == "__main__":
    unittest.main()
