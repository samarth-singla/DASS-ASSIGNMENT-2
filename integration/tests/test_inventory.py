"""Unit tests for inventory module."""

import unittest

from integration.code.inventory import InventoryModule


class TestInventoryModule(unittest.TestCase):
    """Validate inventory and cash behavior."""

    def setUp(self) -> None:
        self.module = InventoryModule(initial_cash=500)

    def test_add_vehicle_success(self) -> None:
        vehicle = self.module.add_vehicle("Nissan")
        self.assertEqual(vehicle.vehicle_id, 1)
        self.assertEqual(self.module.vehicles[1].name, "Nissan")

    def test_update_cash_success(self) -> None:
        balance = self.module.update_cash(250)
        self.assertEqual(balance, 750)

    def test_update_cash_insufficient(self) -> None:
        with self.assertRaises(ValueError):
            self.module.update_cash(-600)

    def test_add_part_and_tool(self) -> None:
        self.module.add_part("spark plug", 3)
        self.module.add_tool("wrench", 2)
        self.assertEqual(self.module.parts["spark plug"], 3)
        self.assertEqual(self.module.tools["wrench"], 2)


if __name__ == "__main__":
    unittest.main()
