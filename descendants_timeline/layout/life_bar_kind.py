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

"""Nature d'une barre de vie dans la timeline."""

from __future__ import annotations

from enum import Enum


class LifeBarKind(str, Enum):
    """Nature de la barre de vie transmise au renderer."""

    NORMAL = "NORMAL"
    REVERSED = "REVERSED"
    ZERO_LENGTH = "ZERO_LENGTH"
    NO_GUARANTEED_INTERVAL = "NO_GUARANTEED_INTERVAL"
