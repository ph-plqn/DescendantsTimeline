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

"""Résultat d'inférence associé à une cible temporelle."""

from __future__ import annotations

from dataclasses import dataclass

from descendants_timeline.model.temporal_target_entry import (
    TemporalTargetEntry,
)
from descendants_timeline.model.temporal_constraint import (
    TemporalConstraint,
)
from descendants_timeline.inference.constraint_resolution import (
    ConstraintResolution,
)
from descendants_timeline.inference.reconciled_temporal_domain import (
    ReconciledTemporalDomain,
)
from descendants_timeline.inference.temporal_estimate import (
    TemporalEstimate,
)

@dataclass(frozen=True, slots=True)
class TemporalInferenceResult:
    """Résultat d'inférence associé à une cible temporelle."""

    target_entry: TemporalTargetEntry
    constraint_resolution: ConstraintResolution
    reconciled_domain: ReconciledTemporalDomain
    estimate: TemporalEstimate
    constraints: tuple[TemporalConstraint, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.target_entry, TemporalTargetEntry):
            raise TypeError(
                "target_entry must be a TemporalTargetEntry"
            )

        if not isinstance(
            self.constraint_resolution,
            ConstraintResolution,
        ):
            raise TypeError(
                "constraint_resolution must be a ConstraintResolution"
            )

        if (
            self.constraint_resolution.target
            != self.target_entry.target
        ):
            raise ValueError(
                "constraint_resolution must target target_entry.target"
            )

        if not isinstance(
            self.reconciled_domain,
            ReconciledTemporalDomain,
        ):
            raise TypeError(
                "reconciled_domain must be a ReconciledTemporalDomain"
            )

        if (
            self.reconciled_domain.target
            != self.target_entry.target
        ):
            raise ValueError(
                "reconciled_domain must target target_entry.target"
            )

        if (
            self.reconciled_domain.constraint_resolution
            is not self.constraint_resolution
        ):
            raise ValueError(
                "reconciled_domain.constraint_resolution "
                "must be constraint_resolution"
            )

        if not isinstance(self.estimate, TemporalEstimate):
            raise TypeError(
                "estimate must be a TemporalEstimate"
            )

        if not isinstance(self.constraints, tuple):
            raise TypeError(
                "constraints must be a tuple"
            )

        if not all(
            isinstance(constraint, TemporalConstraint)
            for constraint in self.constraints
        ):
            raise TypeError(
                "constraints must contain only TemporalConstraint objects"
            )

        if any(
            constraint.target != self.target_entry.target
            for constraint in self.constraints
        ):
            raise ValueError(
                "constraints must target target_entry.target"
            )