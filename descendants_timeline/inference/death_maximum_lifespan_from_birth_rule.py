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


class DeathMaximumLifespanFromBirthRule(Rule):
    rule_id = "DEATH_MAXIMUM_LIFESPAN_FROM_BIRTH"
    strength = ConstraintStrength.SOFT

    def is_applicable(
        self,
        target: TemporalTarget,
        context: RuleContext,
    ) -> bool:
        return (
            target.owner_type is TemporalOwnerType.PERSON
            and target.semantic is TargetSemantic.DEATH
        )

    def evaluate(
        self,
        target: TemporalTarget,
        context: RuleContext,
    ) -> tuple[TemporalConstraint, ...]:

        if not self.is_applicable(target, context):
            return ()

        birth_evidences = context.personal_principal_evidences(
            target.owner_id, EventSemantic.BIRTH,
        )

        if len(birth_evidences) != 1:
            return ()

        birth_evidence = birth_evidences[0]

        birth_maximum = birth_evidence.date.normalized_maximum

        max_lifespan_years = get_max_plausible_lifespan_years()

        if birth_maximum is None:
            return ()

        bound = try_add_years(
            birth_maximum,
            max_lifespan_years,
        )

        if bound is None:
            return ()

        return (
            TemporalConstraint(
                target=target,
                operator=ConstraintOperator.BEFORE_OR_EQUAL,
                bound=bound,
                rule_id=self.rule_id,
                strength=self.strength,
                evidences=(birth_evidence,),
            ),
        )
