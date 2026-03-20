"""Additional integration tests for sponsorship contract behavior."""

import unittest

from integration.code.inventory import InventoryModule
from integration.code.sponsorship_budget import SponsorshipBudgetModule


class TestIntegrationContractCaseRules(unittest.TestCase):
    """Validate sponsorship constraints and their impact on budget."""

    def setUp(self) -> None:
        self.inventory = InventoryModule(initial_cash=100)
        self.sponsor = SponsorshipBudgetModule(self.inventory)

    def test_duplicate_contract_check_is_case_insensitive(self) -> None:
        self.sponsor.sign_contract("TurboMax", 200)
        with self.assertRaises(ValueError):
            self.sponsor.sign_contract("turbomax", 300)

    def test_receive_payout_requires_exact_registered_key(self) -> None:
        self.sponsor.sign_contract("DriftFuel", 180)
        with self.assertRaises(ValueError):
            self.sponsor.receive_payout("driftfuel")

    def test_penalty_then_payout_keeps_budget_consistent(self) -> None:
        self.sponsor.sign_contract("GripOne", 90)
        self.sponsor.apply_penalty(40)
        self.sponsor.receive_payout("GripOne")
        self.assertEqual(self.inventory.cash_balance, 150)


if __name__ == "__main__":
    unittest.main()
