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
from descendants_timeline.model.temporal_constraint import (
    ConstraintOperator,
    ConstraintStrength,
    TemporalConstraint,
)

from .date_arithmetic import try_add_years
from .inference_parameters import get_max_plausible_lifespan_years


class BirthMaximumLifespanFromBurialRule(Rule):
    rule_id = "BIRTH_MAXIMUM_LIFESPAN_FROM_BURIAL"
    strength = ConstraintStrength.SOFT

    def is_applicable(
        self,
        target: TemporalTarget,
        context: RuleContext,
    ) -> bool:
        return (
            target.owner_type is TemporalOwnerType.PERSON
            and target.semantic is TargetSemantic.BIRTH
        )

    def evaluate(
        self,
        target: TemporalTarget,
        context: RuleContext,
    ) -> tuple[TemporalConstraint, ...]:

        if not self.is_applicable(target, context):
            return ()

        burial_evidences = context.personal_principal_evidences(
            target.owner_id, EventSemantic.BURIAL,
        )

        constraints = []

        max_lifespan_years = get_max_plausible_lifespan_years()

        for burial_evidence in burial_evidences:
            burial_minimum = (
                burial_evidence.date.normalized_minimum
            )

            if burial_minimum is None:
                continue

            bound = try_add_years(
                burial_minimum,
                -max_lifespan_years,
            )

            if bound is None:
                continue

            constraints.append(
                TemporalConstraint(
                    target=target,
                    operator=ConstraintOperator.AFTER_OR_EQUAL,
                    bound=bound,
                    rule_id=self.rule_id,
                    strength=self.strength,
                    evidences=(burial_evidence,),
                )
            )

        return tuple(constraints)
