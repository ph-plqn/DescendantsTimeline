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
from .event_date_compatibility import is_event_date_modifier_compatible


def is_event_date_modifier_admissible_as_evidence(
    semantic: EventSemantic,
    modifier_code: int,
) -> bool:
    """Évalue uniquement l'absence d'exclusion liée au modificateur documentaire."""
    return is_event_date_modifier_compatible(semantic, modifier_code)
