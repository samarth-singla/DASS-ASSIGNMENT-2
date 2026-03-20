"""Vehicle maintenance module for wear tracking and repairs."""

from .inventory import InventoryModule


class VehicleMaintenanceModule:
    """Handle vehicle wear and repair operations."""

    def __init__(self, inventory: InventoryModule) -> None:
        self.inventory = inventory

    def apply_wear(self, vehicle_id: int, wear_amount: int) -> int:
        """Reduce vehicle condition by wear amount and return new condition."""
        if wear_amount < 0:
            raise ValueError("Wear amount cannot be negative.")
        if vehicle_id not in self.inventory.vehicles:
            raise ValueError("Vehicle not found.")

        vehicle = self.inventory.vehicles[vehicle_id]
        vehicle.condition = max(0, vehicle.condition - wear_amount)
        return vehicle.condition

    def repair_vehicle(
        self,
        vehicle_id: int,
        part_name: str,
        part_quantity: int,
        cost_per_part: int,
        condition_gain: int,
    ) -> int:
        """Repair a vehicle by consuming parts and cash and increasing condition."""
        if vehicle_id not in self.inventory.vehicles:
            raise ValueError("Vehicle not found.")
        if part_quantity <= 0:
            raise ValueError("Part quantity must be positive.")
        if cost_per_part < 0:
            raise ValueError("Cost per part cannot be negative.")
        if condition_gain <= 0:
            raise ValueError("Condition gain must be positive.")

        key = part_name.strip().lower()
        available_parts = self.inventory.parts.get(key, 0)
        if available_parts < part_quantity:
            raise ValueError("Insufficient parts.")

        total_cost = part_quantity * cost_per_part
        self.inventory.update_cash(-total_cost)
        self.inventory.parts[key] = available_parts - part_quantity

        vehicle = self.inventory.vehicles[vehicle_id]
        vehicle.condition = min(100, vehicle.condition + condition_gain)
        return vehicle.condition
