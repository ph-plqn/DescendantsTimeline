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

from descendants_timeline.model.temporal_constraint import (
    ConstraintOperator,
    ConstraintStrength,
    TemporalConstraint,
)
from descendants_timeline.model.temporal_target import TemporalTarget


@dataclass(frozen=True, slots=True)
class ResolvedBound:
    target: TemporalTarget
    value: date
    operator: ConstraintOperator
    strength: ConstraintStrength
    constraints: tuple[TemporalConstraint, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.target, TemporalTarget):
            raise TypeError("target must be a TemporalTarget")

        if not isinstance(self.value, date):
            raise TypeError("value must be a date")

        if not isinstance(self.operator, ConstraintOperator):
            raise TypeError("operator must be a ConstraintOperator")

        if not isinstance(self.strength, ConstraintStrength):
            raise TypeError("strength must be a ConstraintStrength")

        if not isinstance(self.constraints, tuple):
            raise TypeError("constraints must be a tuple")

        if not self.constraints:
            raise ValueError(
                "ResolvedBound must contain at least one constraint"
            )

        if not all(
            isinstance(constraint, TemporalConstraint)
            for constraint in self.constraints
        ):
            raise TypeError(
                "constraints must contain only TemporalConstraint objects"
            )

        for constraint in self.constraints:
            if constraint.target != self.target:
                raise ValueError(
                    "all constraints must have the ResolvedBound target"
                )

            if constraint.bound != self.value:
                raise ValueError(
                    "all constraints must have the ResolvedBound value"
                )

            if constraint.operator is not self.operator:
                raise ValueError(
                    "all constraints must have the ResolvedBound operator"
                )

            if constraint.strength is not self.strength:
                raise ValueError(
                    "all constraints must have the ResolvedBound strength"
                )