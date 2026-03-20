"""Additional integration tests for mission lifecycle guard behavior."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.mission_planning import MissionPlanningModule
from integration.code.registration import RegistrationModule


class TestIntegrationMissionLifecycleGuards(unittest.TestCase):
    """Validate mission start lifecycle and role list behavior."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.registration.register_member("Kai", "driver")
        self.registration.register_member("Mec", "mechanic")
        self.crew = CrewManagementModule(self.registration)
        self.mission = MissionPlanningModule(self.crew)

    def test_start_mission_twice_raises_error(self) -> None:
        mission = self.mission.create_mission("M1", ["driver"])
        self.mission.start_mission(mission.mission_id)
        with self.assertRaises(ValueError):
            self.mission.start_mission(mission.mission_id)

    def test_list_by_role_returns_empty_for_unknown_role(self) -> None:
        strategists = self.crew.list_by_role("strategist")
        self.assertEqual(strategists, [])

    def test_create_mission_normalizes_role_text(self) -> None:
        mission = self.mission.create_mission("M2", [" Driver ", " mechanic "])
        self.assertEqual(mission.required_roles, ["driver", "mechanic"])


if __name__ == "__main__":
    unittest.main()
