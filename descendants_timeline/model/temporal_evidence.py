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

"""Preuve temporelle utilisable par le moteur d'inférence."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .event import EventSemantic
from .family_event_ref import FamilyRoleSemantic
from .person_event_ref import EventRoleSemantic
from .temporal import TemporalValue
from .temporal_target import TemporalOwnerType


class EvidenceOwnerType(str, Enum):
    """Type d'objet dont une référence à l'évènement fournit la preuve."""

    PERSON = "PERSON"
    FAMILY = "FAMILY"


@dataclass(frozen=True, slots=True)
class TemporalEvidence:
    """Preuve temporelle dérivée d'une référence à un évènement.

    ``owner_id`` identifie la personne ou la famille dont la référence
    constitue la preuve.

    ``principal_owner_id`` identifie la personne ou la famille principalement
    concernée par l'évènement.
    """

    owner_type: EvidenceOwnerType
    owner_id: str

    event_id: str
    semantic: EventSemantic
    role: EventRoleSemantic | FamilyRoleSemantic
    date: TemporalValue

    principal_owner_type: TemporalOwnerType
    principal_owner_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.owner_type, EvidenceOwnerType):
            raise TypeError("owner_type must be an EvidenceOwnerType")

        if not isinstance(self.owner_id, str) or not self.owner_id.strip():
            raise ValueError("owner_id must be a non-empty string")

        if not isinstance(self.event_id, str) or not self.event_id.strip():
            raise ValueError("event_id must be a non-empty string")

        if not isinstance(self.semantic, EventSemantic):
            raise TypeError("semantic must be an EventSemantic")

        if self.semantic is EventSemantic.UNKNOWN:
            raise ValueError(
                "EventSemantic.UNKNOWN cannot produce a TemporalEvidence"
            )

        if not isinstance(
            self.role,
            (EventRoleSemantic, FamilyRoleSemantic),
        ):
            raise TypeError(
                "role must be an EventRoleSemantic or FamilyRoleSemantic"
            )

        if self.role in (
            EventRoleSemantic.UNKNOWN,
            FamilyRoleSemantic.UNKNOWN,
        ):
            raise ValueError(
                "an UNKNOWN role cannot produce a TemporalEvidence"
            )

        if not isinstance(self.date, TemporalValue):
            raise TypeError("date must be a TemporalValue")

        if not self.date.is_usable_as_evidence:
            raise ValueError(
                "TemporalEvidence requires a TemporalValue usable as evidence"
            )

        if not isinstance(self.principal_owner_type, TemporalOwnerType):
            raise TypeError(
                "principal_owner_type must be a TemporalOwnerType"
            )

        if (
            not isinstance(self.principal_owner_id, str)
            or not self.principal_owner_id.strip()
        ):
            raise ValueError(
                "principal_owner_id must be a non-empty string"
            )