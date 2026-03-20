"""Integration tests for cash and inventory boundary conditions."""

import unittest

from integration.code.inventory import InventoryModule
from integration.code.sponsorship_budget import SponsorshipBudgetModule
from integration.code.vehicle_maintenance import VehicleMaintenanceModule


class TestIntegrationInventoryCashBoundaries(unittest.TestCase):
    """Validate cash floor and recovery behaviors in integrated operations."""

    def setUp(self) -> None:
        self.inventory = InventoryModule(initial_cash=120)
        self.maintenance = VehicleMaintenanceModule(self.inventory)
        self.sponsor = SponsorshipBudgetModule(self.inventory)
        self.vehicle = self.inventory.add_vehicle("BoundaryCar")
        self.inventory.add_part("core", 5)
        self.sponsor.sign_contract("EdgeFuel", 200)

    def test_cash_can_reach_exact_zero(self) -> None:
        balance = self.inventory.update_cash(-120)
        self.assertEqual(balance, 0)

    def test_cash_cannot_go_below_zero(self) -> None:
        with self.assertRaises(ValueError):
            self.inventory.update_cash(-121)

    def test_payout_recovers_after_near_zero(self) -> None:
        self.inventory.update_cash(-100)
        balance = self.sponsor.receive_payout("EdgeFuel")
        self.assertEqual(balance, 220)

    def test_repair_with_exact_remaining_cash_succeeds(self) -> None:
        self.maintenance.apply_wear(self.vehicle.vehicle_id, 30)
        balance = self.inventory.update_cash(-20)
        self.assertEqual(balance, 100)
        self.maintenance.repair_vehicle(self.vehicle.vehicle_id, "core", 2, 50, 15)
        self.assertEqual(self.inventory.cash_balance, 0)


if __name__ == "__main__":
    unittest.main()
