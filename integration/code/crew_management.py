"""Crew management module for role and skill operations."""

from typing import Dict, List

from .models import ALLOWED_ROLES, CrewMember
from .registration import RegistrationModule


class CrewManagementModule:
    """Manage crew roles and skill levels."""

    def __init__(self, registration: RegistrationModule) -> None:
        self.registration = registration

    def assign_role(self, member_id: int, new_role: str) -> CrewMember:
        """Assign a validated role to an existing member."""
        role = new_role.strip().lower()
        if role not in ALLOWED_ROLES:
            raise ValueError(f"Invalid role: {new_role}")

        member = self.registration.get_member(member_id)
        member.role = role
        return member

    def set_skill_level(self, member_id: int, skill_name: str, level: int) -> CrewMember:
        """Set a skill level from 1 to 10 for a member."""
        if level < 1 or level > 10:
            raise ValueError("Skill level must be between 1 and 10.")

        member = self.registration.get_member(member_id)
        member.skills[skill_name.strip().lower()] = level
        return member

    def list_by_role(self, role: str) -> List[CrewMember]:
        """Return all members that match a role."""
        clean_role = role.strip().lower()
        members: Dict[int, CrewMember] = self.registration.list_members()
        return [member for member in members.values() if member.role == clean_role]
