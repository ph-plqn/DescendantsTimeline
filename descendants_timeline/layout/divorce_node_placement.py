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

"""Placement logique d'un nœud de divorce dans la timeline."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DivorceNodePlacement:
    """Position logique d'un divorce dans la timeline."""

    family_id: str
    descendant_person_id: str
    spouse_person_id: str
    x: float
    y: float
    descendant_row_index: int
    spouse_row_index: int
