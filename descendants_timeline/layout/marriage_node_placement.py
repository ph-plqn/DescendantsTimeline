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

"""Placement logique d'un nœud de mariage dans la timeline."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MarriageNodePlacement:
    """Position logique d'un mariage dans la timeline."""

    family_id: str
    descendant_person_id: str
    spouse_person_id: str
    x: float
    y: float
    descendant_row_index: int
    spouse_row_index: int
    descendant_y: float | None = None
    spouse_y: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.family_id, str) or not self.family_id:
            raise ValueError(
                "family_id must be a non-empty string"
            )

        if (
            not isinstance(self.descendant_person_id, str)
            or not self.descendant_person_id
        ):
            raise ValueError(
                "descendant_person_id must be a non-empty string"
            )

        if (
            not isinstance(self.spouse_person_id, str)
            or not self.spouse_person_id
        ):
            raise ValueError(
                "spouse_person_id must be a non-empty string"
            )

        if not isinstance(self.x, (int, float)):
            raise TypeError(
                "x must be a number"
            )

        if not isinstance(self.y, (int, float)):
            raise TypeError(
                "y must be a number"
            )

        if (
            not isinstance(self.descendant_row_index, int)
            or self.descendant_row_index < 0
        ):
            raise ValueError(
                "descendant_row_index must be a non-negative integer"
            )

        if (
            not isinstance(self.spouse_row_index, int)
            or self.spouse_row_index < 0
        ):
            raise ValueError(
                "spouse_row_index must be a non-negative integer"
            )
