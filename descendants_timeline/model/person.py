# Copyright (C) 2026 philippe Pouliquen <ph.plqn@proton.me>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <https://www.gnu.org/licenses/>.

"""Modèle d'une personne généalogique."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .person_event_ref import PersonEventRef


class PersonGender(str, Enum):
    """Genre d'une personne normalisé depuis Gramps."""

    MALE = "MALE"
    FEMALE = "FEMALE"
    UNKNOWN = "UNKNOWN"
    OTHER = "OTHER"


@dataclass(frozen=True, slots=True)
class Person:
    """Représente une personne minimale, immuable et indépendante de Gramps."""

    person_id: str
    display_name: str
    gender: PersonGender
    event_refs: tuple[PersonEventRef, ...]
    parent_family_ids: tuple[str, ...]
    family_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.person_id, str) or not self.person_id.strip():
            raise ValueError("person_id must be a non-empty string")

        if not isinstance(self.display_name, str) or not self.display_name.strip():
            raise ValueError("display_name must be a non-empty string")

        if not isinstance(self.gender, PersonGender):
            raise TypeError("gender must be a PersonGender")

        if not isinstance(self.event_refs, tuple):
            raise TypeError("event_refs must be a tuple")

        if not all(isinstance(ref, PersonEventRef) for ref in self.event_refs):
            raise TypeError("event_refs must contain only PersonEventRef objects")

        if not isinstance(self.parent_family_ids, tuple):
            raise TypeError("parent_family_ids must be a tuple")

        if not all(
            isinstance(family_id, str) and family_id.strip()
            for family_id in self.parent_family_ids
        ):
            raise ValueError(
                "parent_family_ids must contain only non-empty strings"
            )

        if not isinstance(self.family_ids, tuple):
            raise TypeError("family_ids must be a tuple")

        if not all(
            isinstance(family_id, str) and family_id.strip()
            for family_id in self.family_ids
        ):
            raise ValueError("family_ids must contain only non-empty strings")
