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

from ..model.temporal import TemporalValue
from ..model.temporal_target import TemporalTarget
from .constraint_resolution import ConstraintResolution
from .reconciled_temporal_domain import (
    ReconciledBound,
    ReconciledBoundOrigin,
    ReconciledTemporalDomain,
    ReconciliationConflictType,
)

class TemporalReconciler:
    def reconcile(
        self,
        target: TemporalTarget,
        gramps_value: TemporalValue,
        constraint_resolution: ConstraintResolution,
    ) -> ReconciledTemporalDomain:
        if not isinstance(target, TemporalTarget):
            raise TypeError(
                "target must be a TemporalTarget"
            )

        if not isinstance(gramps_value, TemporalValue):
            raise TypeError(
                "gramps_value must be a TemporalValue"
            )

        if not isinstance(
            constraint_resolution,
            ConstraintResolution,
        ):
            raise TypeError(
                "constraint_resolution must be a ConstraintResolution"
            )

        if constraint_resolution.target != target:
            raise ValueError(
                "constraint_resolution target must match target"
            )

        principal_minimum = None
        principal_maximum = None

        conflict_type = None
        conflicting_bounds = ()

        # ---------------------------------------------------------
        # 1. Les bornes présentes dans Gramps sont souveraines.
        # ---------------------------------------------------------

        if gramps_value.normalized_minimum is not None:
            principal_minimum = ReconciledBound(
                value=gramps_value.normalized_minimum,
                origin=ReconciledBoundOrigin.GRAMPS,
            )

        if gramps_value.normalized_maximum is not None:
            principal_maximum = ReconciledBound(
                value=gramps_value.normalized_maximum,
                origin=ReconciledBoundOrigin.GRAMPS,
            )

        # ---------------------------------------------------------
        # 2. Compléter éventuellement le minimum manquant.
        # ---------------------------------------------------------

        if (
            principal_minimum is None
            and constraint_resolution.refined_minimum is not None
        ):
            inferred_minimum = constraint_resolution.refined_minimum

            if (
                principal_maximum is not None
                and principal_maximum.origin
                == ReconciledBoundOrigin.GRAMPS
                and inferred_minimum.value
                > principal_maximum.value
            ):
                conflict_type = (
                    ReconciliationConflictType.GRAMPS_INFERENCE
                )
                conflicting_bounds = (inferred_minimum,)

            else:
                principal_minimum = ReconciledBound(
                    value=inferred_minimum.value,
                    origin=ReconciledBoundOrigin.INFERENCE,
                    inferred_bound=inferred_minimum,
                )

        # ---------------------------------------------------------
        # 3. Compléter éventuellement le maximum manquant.
        # ---------------------------------------------------------

        if (
            principal_maximum is None
            and constraint_resolution.refined_maximum is not None
        ):
            inferred_maximum = constraint_resolution.refined_maximum

            if (
                principal_minimum is not None
                and principal_minimum.origin
                == ReconciledBoundOrigin.GRAMPS
                and inferred_maximum.value
                < principal_minimum.value
            ):
                conflict_type = (
                    ReconciliationConflictType.GRAMPS_INFERENCE
                )
                conflicting_bounds = (inferred_maximum,)

            else:
                principal_maximum = ReconciledBound(
                    value=inferred_maximum.value,
                    origin=ReconciledBoundOrigin.INFERENCE,
                    inferred_bound=inferred_maximum,
                )
        return ReconciledTemporalDomain(
            target=target,
            gramps_value=gramps_value,
            constraint_resolution=constraint_resolution,
            principal_minimum=principal_minimum,
            principal_maximum=principal_maximum,
            conflict_type=conflict_type,
            conflicting_bounds=conflicting_bounds,
        )