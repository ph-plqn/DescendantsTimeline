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

"""Référence d'un évènement depuis une famille."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FamilyRoleSemantic(str, Enum):
    """Signification d'un rôle de famille reconnue par le greffon.

    UNKNOWN ne signifie pas que le rôle est invalide. Il signifie seulement
    que le greffon ne lui attribue actuellement aucune interprétation
    algorithmique particulière.
    """

    UNKNOWN = "UNKNOWN"
    FAMILY = "FAMILY"


@dataclass(frozen=True, slots=True)
class FamilyEventRef:
    """Décrit le rattachement d'une famille à un évènement.

    Responsibilities
    ----------------
    - référencer un évènement existant ;
    - conserver le rôle documentaire provenant de Gramps ;
    - exposer la sémantique de rôle reconnue par le greffon ;
    - garantir ses invariants.

    Does NOT
    --------
    - contenir l'évènement lui-même ;
    - connaître la famille propriétaire de la référence ;
    - accéder à Gramps ;
    - effectuer une inférence temporelle ;
    - modifier l'évènement référencé.
    """

    event_id: str
    semantic_role: FamilyRoleSemantic
    source_role: str

    def __post_init__(self) -> None:
        """Vérifie les invariants de la référence."""

        if not isinstance(self.event_id, str) or not self.event_id.strip():
            raise ValueError("event_id must be a non-empty string")

        if not isinstance(self.semantic_role, FamilyRoleSemantic):
            raise TypeError("semantic_role must be a FamilyRoleSemantic")

        if not isinstance(self.source_role, str) or not self.source_role.strip():
            raise ValueError("source_role must be a non-empty string")
