"""Results module for race outcomes and rankings."""

from typing import Dict, List, Tuple

from .inventory import InventoryModule
from .race_management import RaceManagementModule


class ResultsModule:
    """Record race outcomes and maintain driver points."""

    def __init__(
        self,
        race_management: RaceManagementModule,
        inventory: InventoryModule,
    ) -> None:
        self.race_management = race_management
        self.inventory = inventory
        self.driver_points: Dict[int, int] = {}

    def record_results(
        self,
        race_id: int,
        ordered_driver_ids: List[int],
        prize_pool: int,
    ) -> None:
        """Record race results, update points, and award prize to winner."""
        if race_id not in self.race_management.races:
            raise ValueError("Race not found.")
        if prize_pool < 0:
            raise ValueError("Prize pool cannot be negative.")

        race = self.race_management.races[race_id]
        if race.completed:
            raise ValueError("Race already completed.")

        entrant_ids = {entry["driver_id"] for entry in race.entrants}
        if set(ordered_driver_ids) != entrant_ids:
            raise ValueError("Results must include all and only race entrants.")

        points_by_position = [10, 6, 3]
        for position, driver_id in enumerate(ordered_driver_ids):
            points = points_by_position[position] if position < len(points_by_position) else 1
            self.driver_points[driver_id] = self.driver_points.get(driver_id, 0) + points

        winner_id = ordered_driver_ids[0]
        self.inventory.update_cash(prize_pool)
        race.completed = True

        for entry in race.entrants:
            vehicle_id = entry["vehicle_id"]
            self.inventory.set_vehicle_available(vehicle_id, True)

        # Keep winner_id available for future expansion (e.g. per-driver wallet payouts).
        _ = winner_id

    def leaderboard(self) -> List[Tuple[int, int]]:
        """Return drivers sorted by points descending then driver id ascending."""
        return sorted(self.driver_points.items(), key=lambda item: (-item[1], item[0]))
