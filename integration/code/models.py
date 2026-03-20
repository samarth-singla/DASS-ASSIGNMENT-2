"""Shared data models for StreetRace Manager."""

from dataclasses import dataclass, field
from typing import Dict, List


ALLOWED_ROLES = {"driver", "mechanic", "strategist"}


@dataclass
class CrewMember:
    """Represent a crew member and their skills."""

    member_id: int
    name: str
    role: str
    skills: Dict[str, int] = field(default_factory=dict)


@dataclass
class Vehicle:
    """Represent a race vehicle."""

    vehicle_id: int
    name: str
    condition: int = 100
    available: bool = True


@dataclass
class RaceEvent:
    """Represent a race and its participants."""

    race_id: int
    name: str
    entrants: List[Dict[str, int]] = field(default_factory=list)
    completed: bool = False


@dataclass
class Mission:
    """Represent a mission with required roles."""

    mission_id: int
    title: str
    required_roles: List[str]
    started: bool = False
