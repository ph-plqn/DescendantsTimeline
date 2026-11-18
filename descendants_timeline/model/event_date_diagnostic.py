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

from dataclasses import dataclass

from .event import EventSemantic
from .event_date_compatibility import is_event_date_modifier_compatible


@dataclass(frozen=True, slots=True)
class EventDateDiagnostic:
    semantic: EventSemantic
    modifier_code: int
    is_compatible: bool
    explanation: str


def evaluate_event_date_modifier(
    semantic: EventSemantic,
    modifier_code: int,
) -> EventDateDiagnostic | None:
    compatible = is_event_date_modifier_compatible(semantic, modifier_code)
    if compatible:
        return None

    if modifier_code == 5:
        explanation = (
            f"SPAN décrit une durée alors que {semantic.value} est un événement ponctuel."
        )
    elif modifier_code == 7:
        explanation = (
            "FROM décrit le début d’une période, distinct d’une borne AFTER, "
            f"alors que {semantic.value} est un événement ponctuel."
        )
    elif modifier_code == 8:
        explanation = (
            "TO décrit la fin d’une période, distincte d’une borne BEFORE, "
            f"alors que {semantic.value} est un événement ponctuel."
        )
    else:
        raise NotImplementedError

    return EventDateDiagnostic(
        semantic=semantic,
        modifier_code=modifier_code,
        is_compatible=compatible,
        explanation=explanation,
    )
