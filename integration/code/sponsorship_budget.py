"""Sponsorship and budget module for contract and cash handling."""

from typing import Dict

from .inventory import InventoryModule


class SponsorshipBudgetModule:
    """Manage sponsorship contracts and cash impacts."""

    def __init__(self, inventory: InventoryModule) -> None:
        self.inventory = inventory
        self.contracts: Dict[str, int] = {}

    def sign_contract(self, sponsor_name: str, payout_amount: int) -> None:
        """Register a sponsor with a fixed payout amount."""
        name = sponsor_name.strip()
        if not name:
            raise ValueError("Sponsor name cannot be empty.")
        if payout_amount <= 0:
            raise ValueError("Payout amount must be positive.")
        if name.lower() in (key.lower() for key in self.contracts):
            raise ValueError("Sponsor already signed.")

        self.contracts[name] = payout_amount

    def receive_payout(self, sponsor_name: str) -> int:
        """Apply sponsor payout to cash balance and return new balance."""
        if sponsor_name not in self.contracts:
            raise ValueError("Sponsor contract not found.")
        return self.inventory.update_cash(self.contracts[sponsor_name])

    def apply_penalty(self, amount: int) -> int:
        """Apply a sponsor penalty deduction and return new balance."""
        if amount <= 0:
            raise ValueError("Penalty amount must be positive.")
        return self.inventory.update_cash(-amount)
