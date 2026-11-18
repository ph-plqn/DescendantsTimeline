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
from datetime import date

from descendants_timeline.model.temporal import CertaintyLevel


@dataclass(frozen=True, slots=True)
class TemporalEstimate:
    representative_value: date | None
    certainty: CertaintyLevel

    def __post_init__(self) -> None:
        if (
            self.representative_value is not None
            and not isinstance(self.representative_value, date)
        ):
            raise TypeError(
                "representative_value must be a date or None"
            )

        if not isinstance(self.certainty, CertaintyLevel):
            raise TypeError(
                "certainty must be a CertaintyLevel"
            )

        if self.representative_value is None:
            if self.certainty != CertaintyLevel.UNDETERMINED:
                raise ValueError(
                    "certainty must be UNDETERMINED "
                    "when representative_value is None"
                )