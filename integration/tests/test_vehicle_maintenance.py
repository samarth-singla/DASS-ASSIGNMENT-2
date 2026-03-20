"""Unit tests for vehicle maintenance module."""

import unittest

from integration.code.inventory import InventoryModule
from integration.code.vehicle_maintenance import VehicleMaintenanceModule


class TestVehicleMaintenanceModule(unittest.TestCase):
    """Validate wear and repair operations."""

    def setUp(self) -> None:
        self.inventory = InventoryModule(initial_cash=500)
        self.vehicle = self.inventory.add_vehicle("Evo")
        self.inventory.add_part("engine_kit", 5)
        self.module = VehicleMaintenanceModule(self.inventory)

    def test_apply_wear_reduces_condition(self) -> None:
        new_condition = self.module.apply_wear(self.vehicle.vehicle_id, 30)
        self.assertEqual(new_condition, 70)

    def test_apply_wear_clamps_to_zero(self) -> None:
        new_condition = self.module.apply_wear(self.vehicle.vehicle_id, 130)
        self.assertEqual(new_condition, 0)

    def test_repair_vehicle_consumes_parts_and_cash(self) -> None:
        self.module.apply_wear(self.vehicle.vehicle_id, 40)
        new_condition = self.module.repair_vehicle(
            self.vehicle.vehicle_id,
            "engine_kit",
            part_quantity=2,
            cost_per_part=50,
            condition_gain=25,
        )
        self.assertEqual(new_condition, 85)
        self.assertEqual(self.inventory.parts["engine_kit"], 3)
        self.assertEqual(self.inventory.cash_balance, 400)

    def test_repair_vehicle_reject_insufficient_parts(self) -> None:
        with self.assertRaises(ValueError):
            self.module.repair_vehicle(
                self.vehicle.vehicle_id,
                "engine_kit",
                part_quantity=8,
                cost_per_part=20,
                condition_gain=10,
            )


if __name__ == "__main__":
    unittest.main()
