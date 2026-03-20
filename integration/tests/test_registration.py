"""Unit tests for registration module."""

import unittest

from integration.code.registration import RegistrationModule


class TestRegistrationModule(unittest.TestCase):
    """Validate registration rules."""

    def setUp(self) -> None:
        self.module = RegistrationModule()

    def test_register_member_success(self) -> None:
        member = self.module.register_member("Alex", "driver")
        self.assertEqual(member.member_id, 1)
        self.assertEqual(member.name, "Alex")
        self.assertEqual(member.role, "driver")

    def test_register_member_invalid_role(self) -> None:
        with self.assertRaises(ValueError):
            self.module.register_member("Alex", "chef")

    def test_register_member_duplicate_name(self) -> None:
        self.module.register_member("Alex", "driver")
        with self.assertRaises(ValueError):
            self.module.register_member("alex", "mechanic")


if __name__ == "__main__":
    unittest.main()
