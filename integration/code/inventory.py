"""Inventory module for vehicles, resources, and cash balance."""

from typing import Dict

from .models import Vehicle


class InventoryModule:
    """Track cars, parts, tools, and cash."""

    def __init__(self, initial_cash: int = 0) -> None:
        self.cash_balance = initial_cash
        self.vehicles: Dict[int, Vehicle] = {}
        self.parts: Dict[str, int] = {}
        self.tools: Dict[str, int] = {}
        self._next_vehicle_id = 1

    def add_vehicle(self, name: str) -> Vehicle:
        """Add a vehicle and return the created vehicle record."""
        vehicle = Vehicle(vehicle_id=self._next_vehicle_id, name=name.strip())
        self.vehicles[self._next_vehicle_id] = vehicle
        self._next_vehicle_id += 1
        return vehicle

    def set_vehicle_available(self, vehicle_id: int, available: bool) -> None:
        """Set vehicle availability state."""
        if vehicle_id not in self.vehicles:
            raise ValueError("Vehicle not found.")
        self.vehicles[vehicle_id].available = available

    def update_cash(self, amount_delta: int) -> int:
        """Apply cash delta and return new cash balance."""
        new_balance = self.cash_balance + amount_delta
        if new_balance < 0:
            raise ValueError("Insufficient cash balance.")
        self.cash_balance = new_balance
        return self.cash_balance

    def add_part(self, part_name: str, quantity: int) -> None:
        """Increase quantity of a spare part."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        key = part_name.strip().lower()
        self.parts[key] = self.parts.get(key, 0) + quantity

    def add_tool(self, tool_name: str, quantity: int) -> None:
        """Increase quantity of a tool."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        key = tool_name.strip().lower()
        self.tools[key] = self.tools.get(key, 0) + quantity
