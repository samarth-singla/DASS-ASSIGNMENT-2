"""Integration tests for budget, sponsorship, and maintenance interactions."""

import unittest

from integration.code.inventory import InventoryModule
from integration.code.sponsorship_budget import SponsorshipBudgetModule
from integration.code.vehicle_maintenance import VehicleMaintenanceModule


class TestIntegrationBudgetAndMaintenance(unittest.TestCase):
    """Validate cash and parts interactions across modules."""

    def setUp(self) -> None:
        self.inventory = InventoryModule(initial_cash=400)
        self.maintenance = VehicleMaintenanceModule(self.inventory)
        self.sponsorship = SponsorshipBudgetModule(self.inventory)

        self.vehicle = self.inventory.add_vehicle("Evo X")
        self.inventory.add_part("engine_kit", 6)

    def test_sponsor_payout_then_repair_updates_cash(self) -> None:
        self.sponsorship.sign_contract("NitroCorp", 500)
        self.sponsorship.receive_payout("NitroCorp")

        self.maintenance.apply_wear(self.vehicle.vehicle_id, 40)
        new_condition = self.maintenance.repair_vehicle(
            self.vehicle.vehicle_id,
            "engine_kit",
            part_quantity=3,
            cost_per_part=50,
            condition_gain=25,
        )

        self.assertEqual(new_condition, 85)
        self.assertEqual(self.inventory.cash_balance, 750)
        self.assertEqual(self.inventory.parts["engine_kit"], 3)

    def test_penalty_and_repair_can_fail_on_cash(self) -> None:
        self.sponsorship.apply_penalty(300)
        with self.assertRaises(ValueError):
            self.maintenance.repair_vehicle(
                self.vehicle.vehicle_id,
                "engine_kit",
                part_quantity=4,
                cost_per_part=50,
                condition_gain=20,
            )

    def test_add_tool_and_part_integration_state(self) -> None:
        self.inventory.add_tool("jack", 2)
        self.inventory.add_part("tire_set", 4)
        self.assertEqual(self.inventory.tools["jack"], 2)
        self.assertEqual(self.inventory.parts["tire_set"], 4)

    def test_apply_wear_then_full_restore_cap(self) -> None:
        self.maintenance.apply_wear(self.vehicle.vehicle_id, 90)
        new_condition = self.maintenance.repair_vehicle(
            self.vehicle.vehicle_id,
            "engine_kit",
            part_quantity=1,
            cost_per_part=10,
            condition_gain=200,
        )
        self.assertEqual(new_condition, 100)


if __name__ == "__main__":
    unittest.main()
