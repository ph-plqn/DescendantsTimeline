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

from descendants_timeline.inference.rule import Rule
from descendants_timeline.inference.rule_context import RuleContext

from descendants_timeline.model.temporal_target import (
    TemporalOwnerType,
    TemporalTarget,
    TargetSemantic,
)

from descendants_timeline.model.event import EventSemantic
from descendants_timeline.model.person_event_ref import EventRoleSemantic
from descendants_timeline.model.temporal_constraint import (
    ConstraintOperator,
    ConstraintStrength,
    TemporalConstraint,
)
from descendants_timeline.model.temporal_evidence import (
    EvidenceOwnerType,
)


class MarriageBeforeSpouseDeathRule(Rule):
    rule_id = "MARRIAGE_BEFORE_SPOUSE_DEATH"
    strength = ConstraintStrength.HARD

    def is_applicable(
        self,
        target: TemporalTarget,
        context: RuleContext,
    ) -> bool:
        return (
            target.owner_type is TemporalOwnerType.FAMILY
            and target.semantic is TargetSemantic.MARRIAGE
        )

    def evaluate(
        self,
        target: TemporalTarget,
        context: RuleContext,
    ) -> tuple[TemporalConstraint, ...]:

        if not self.is_applicable(target, context):
            return ()

        family = context.data.families.get(target.owner_id)

        if family is None:
            return ()

        family_person_ids = {
            person_id
            for person_id in (
                family.parent1_id,
                family.parent2_id,
            )
            if person_id is not None
        }

        death_evidences = context.ordered_death_evidences_for_parents(
            family_person_ids
        )

        constraints = []

        for death_evidence in death_evidences:

            if death_evidence.date.normalized_maximum is None:
                continue

            constraints.append(
                TemporalConstraint(
                    target=target,
                    operator=ConstraintOperator.BEFORE_OR_EQUAL,
                    bound=death_evidence.date.normalized_maximum,
                    rule_id=self.rule_id,
                    strength=self.strength,
                    evidences=(death_evidence,),
                )
            )

        return tuple(constraints)