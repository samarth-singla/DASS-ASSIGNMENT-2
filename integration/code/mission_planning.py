"""Mission planning module for planning and execution readiness."""

from typing import Dict, List

from .crew_management import CrewManagementModule
from .models import Mission


class MissionPlanningModule:
    """Manage missions and validate required role availability."""

    def __init__(self, crew_management: CrewManagementModule) -> None:
        self.crew_management = crew_management
        self.missions: Dict[int, Mission] = {}
        self._next_mission_id = 1

    def create_mission(self, title: str, required_roles: List[str]) -> Mission:
        """Create a mission with normalized required roles."""
        normalized_roles = [role.strip().lower() for role in required_roles if role.strip()]
        if not title.strip():
            raise ValueError("Mission title cannot be empty.")
        if not normalized_roles:
            raise ValueError("Mission must require at least one role.")

        mission = Mission(
            mission_id=self._next_mission_id,
            title=title.strip(),
            required_roles=normalized_roles,
        )
        self.missions[self._next_mission_id] = mission
        self._next_mission_id += 1
        return mission

    def start_mission(self, mission_id: int) -> None:
        """Start mission only when every required role has assigned members."""
        if mission_id not in self.missions:
            raise ValueError("Mission not found.")

        mission = self.missions[mission_id]
        if mission.started:
            raise ValueError("Mission already started.")

        for role in mission.required_roles:
            if not self.crew_management.list_by_role(role):
                raise ValueError(f"Missing required role: {role}")

        mission.started = True
