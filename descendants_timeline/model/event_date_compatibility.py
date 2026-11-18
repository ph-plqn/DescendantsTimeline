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

from .event import EventSemantic


def is_event_date_modifier_compatible(
    semantic: EventSemantic,
    modifier_code: int,
) -> bool:
    if semantic in (
        EventSemantic.BIRTH,
        EventSemantic.DEATH,
        EventSemantic.MARRIAGE,
        EventSemantic.BURIAL,
        EventSemantic.DIVORCE,
        EventSemantic.BAPTISM,
        EventSemantic.CENSUS,
    ):
        if modifier_code in (0, 1, 2, 3, 4, 6):
            return True
        if modifier_code in (5, 7, 8):
            return False
    raise NotImplementedError
