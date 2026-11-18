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

"""Placement logique d'un segment de remariage dans la timeline."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RemarriageSegmentPlacement:
    """Segment logique reliant des nœuds de remariage."""

    person_id: str
    x: float
    y_start: float
    y_end: float

    def __post_init__(self) -> None:
        if not isinstance(self.person_id, str) or not self.person_id:
            raise ValueError(
                "person_id must be a non-empty string"
            )

        if not isinstance(self.x, (int, float)):
            raise TypeError(
                "x must be a number"
            )

        if not isinstance(self.y_start, (int, float)):
            raise TypeError(
                "y_start must be a number"
            )

        if not isinstance(self.y_end, (int, float)):
            raise TypeError(
                "y_end must be a number"
            )

        if self.y_start > self.y_end:
            raise ValueError(
                "y_start must not be greater than y_end"
            )