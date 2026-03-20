"""Registration module for crew onboarding."""

from typing import Dict

from .models import ALLOWED_ROLES, CrewMember


class RegistrationModule:
    """Manage crew member registration."""

    def __init__(self) -> None:
        self._members: Dict[int, CrewMember] = {}
        self._next_id = 1

    def register_member(self, name: str, role: str) -> CrewMember:
        """Register a member with validated name and role."""
        clean_name = name.strip()
        clean_role = role.strip().lower()

        if not clean_name:
            raise ValueError("Name cannot be empty.")
        if clean_role not in ALLOWED_ROLES:
            raise ValueError(f"Invalid role: {role}")

        for member in self._members.values():
            if member.name.lower() == clean_name.lower():
                raise ValueError("Member with this name already exists.")

        member = CrewMember(self._next_id, clean_name, clean_role)
        self._members[self._next_id] = member
        self._next_id += 1
        return member

    def get_member(self, member_id: int) -> CrewMember:
        """Return a registered member by id."""
        if member_id not in self._members:
            raise ValueError("Member not found.")
        return self._members[member_id]

    def list_members(self) -> Dict[int, CrewMember]:
        """Return all registered members keyed by id."""
        return dict(self._members)
