"""Unit tests for sponsorship and budget module."""

import unittest

from integration.code.inventory import InventoryModule
from integration.code.sponsorship_budget import SponsorshipBudgetModule


class TestSponsorshipBudgetModule(unittest.TestCase):
    """Validate sponsor contract and budget effects."""

    def setUp(self) -> None:
        self.inventory = InventoryModule(initial_cash=200)
        self.module = SponsorshipBudgetModule(self.inventory)

    def test_sign_contract_and_receive_payout(self) -> None:
        self.module.sign_contract("NitroCorp", 500)
        balance = self.module.receive_payout("NitroCorp")
        self.assertEqual(balance, 700)

    def test_sign_contract_reject_duplicate(self) -> None:
        self.module.sign_contract("GripTech", 300)
        with self.assertRaises(ValueError):
            self.module.sign_contract("GripTech", 250)

    def test_apply_penalty_deducts_cash(self) -> None:
        balance = self.module.apply_penalty(50)
        self.assertEqual(balance, 150)

    def test_apply_penalty_reject_insufficient_cash(self) -> None:
        with self.assertRaises(ValueError):
            self.module.apply_penalty(300)


if __name__ == "__main__":
    unittest.main()
