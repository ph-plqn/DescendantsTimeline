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

from descendants_timeline.inference.reconciled_temporal_domain import (
    ReconciledBound,
    ReconciledBoundOrigin,
)
from descendants_timeline.inference.temporal_inference_result import TemporalInferenceResult
from descendants_timeline.inference.temporal_target_index_builder import selected_gramps_event_id
from descendants_timeline.model.genealogy import RawGenealogyData
from descendants_timeline.model.temporal import ValueOrigin
from descendants_timeline.model.temporal_target import TemporalOwnerType


def gramps_bound_source_event_id(
    data: RawGenealogyData,
    result: TemporalInferenceResult,
    bound: ReconciledBound,
) -> str | None:
    """Retrouve la source réelle d'une borne Gramps cohérente du domaine."""
    domain = result.reconciled_domain
    if bound.origin is not ReconciledBoundOrigin.GRAMPS:
        return None
    if bound is domain.principal_minimum:
        expected_value = domain.gramps_value.normalized_minimum
    elif bound is domain.principal_maximum:
        expected_value = domain.gramps_value.normalized_maximum
    else:
        return None
    if domain.gramps_value.value_origin is not ValueOrigin.GRAMPS:
        return None
    if result.target_entry.gramps_value != domain.gramps_value:
        return None

    target = result.target_entry.target
    owners = data.persons if target.owner_type is TemporalOwnerType.PERSON else data.families
    if target.owner_id not in owners:
        return None
    event_id = selected_gramps_event_id(data, target)
    if event_id is None:
        return None
    source_value = data.events[event_id].date
    if source_value != domain.gramps_value:
        return None
    if bound.value != expected_value:
        return None
    return event_id


def has_independent_bound_justification(
    bound: ReconciledBound,
    future_event_ids: frozenset[str],
    *,
    data: RawGenealogyData | None = None,
    result: TemporalInferenceResult | None = None,
) -> bool:
    if bound.origin is ReconciledBoundOrigin.GRAMPS and not future_event_ids:
        return True
    if bound.origin is ReconciledBoundOrigin.GRAMPS:
        if data is None or result is None:
            raise NotImplementedError("GRAMPS bound provenance requires data and result")
        event_id = gramps_bound_source_event_id(data, result, bound)
        if event_id is None:
            raise NotImplementedError("GRAMPS bound provenance could not be verified")
        return event_id not in future_event_ids
    if bound.origin is not ReconciledBoundOrigin.INFERENCE:
        raise NotImplementedError
    return any(
        bool(constraint.evidences)
        and all(
            evidence.event_id not in future_event_ids
            for evidence in constraint.evidences
        )
        for constraint in bound.inferred_bound.constraints
    )
