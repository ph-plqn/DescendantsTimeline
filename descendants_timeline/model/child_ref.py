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

"""Relation d'un enfant avec les deux parents d'une famille."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ChildRelation(str, Enum):
    """Relation d'un enfant avec un parent, normalisée depuis Gramps."""

    ADOPTED = "ADOPTED"
    NONE = "NONE"
    FOSTER = "FOSTER"
    STEPCHILD = "STEPCHILD"
    UNKNOWN = "UNKNOWN"
    BIRTH = "BIRTH"
    SPONSORED = "SPONSORED"


@dataclass(frozen=True, slots=True)
class ChildRef:
    """Décrit la relation d'un enfant avec les deux parents d'une famille.

    Responsibilities
    ----------------
    - référencer une personne existante ;
    - conserver séparément la relation avec parent1 ;
    - conserver séparément la relation avec parent2 ;
    - garantir ses invariants.

    Does NOT
    --------
    - contenir l'objet Person lui-même ;
    - décider si l'enfant appartient au DFS ;
    - interpréter ou corriger les relations saisies dans Gramps ;
    - accéder à Gramps ;
    - modifier la personne ou la famille référencée.
    """

    person_id: str
    relation_to_parent1: ChildRelation
    relation_to_parent2: ChildRelation

    def __post_init__(self) -> None:
        if not isinstance(self.person_id, str) or not self.person_id.strip():
            raise ValueError("person_id must be a non-empty string")

        if not isinstance(self.relation_to_parent1, ChildRelation):
            raise TypeError("relation_to_parent1 must be a ChildRelation")

        if not isinstance(self.relation_to_parent2, ChildRelation):
            raise TypeError("relation_to_parent2 must be a ChildRelation")
