"""Unit tests for crew management module."""

import unittest

from integration.code.crew_management import CrewManagementModule
from integration.code.registration import RegistrationModule


class TestCrewManagementModule(unittest.TestCase):
    """Validate role and skill management rules."""

    def setUp(self) -> None:
        self.registration = RegistrationModule()
        self.member = self.registration.register_member("Alex", "driver")
        self.module = CrewManagementModule(self.registration)

    def test_assign_role_success(self) -> None:
        updated = self.module.assign_role(self.member.member_id, "mechanic")
        self.assertEqual(updated.role, "mechanic")

    def test_assign_role_invalid(self) -> None:
        with self.assertRaises(ValueError):
            self.module.assign_role(self.member.member_id, "pilot")

    def test_set_skill_level_success(self) -> None:
        updated = self.module.set_skill_level(self.member.member_id, "repair", 8)
        self.assertEqual(updated.skills["repair"], 8)

    def test_set_skill_level_out_of_bounds(self) -> None:
        with self.assertRaises(ValueError):
            self.module.set_skill_level(self.member.member_id, "repair", 11)


if __name__ == "__main__":
    unittest.main()
