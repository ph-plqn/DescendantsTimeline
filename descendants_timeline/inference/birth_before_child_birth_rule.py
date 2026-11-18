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

from descendants_timeline.model.temporal_constraint import (
    ConstraintOperator,
    ConstraintStrength,
    TemporalConstraint,
)

from .date_arithmetic import try_add_years
from .inference_parameters import get_min_parent_age_years


class BirthBeforeChildBirthRule(Rule):
    """Un parent est né au moins N ans avant la naissance de son enfant biologique.

    N est la préférence Gramps « Nb. minimal d'années entre les générations ».
    La règle s'applique à la mère comme au père : une contrainte est émise
    pour chaque enfant biologique ayant une naissance exploitable ; la plus
    serrée (l'enfant le plus précoce) est donc celle qui borne réellement.
    """

    rule_id = "BIRTH_BEFORE_CHILD_BIRTH"
    strength = ConstraintStrength.HARD

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

        child_birth_evidences = (
            context.child_birth_evidences_as_mother(target.owner_id)
            + context.child_birth_evidences_as_father(target.owner_id)
        )

        if not child_birth_evidences:
            return ()

        min_parent_age_years = get_min_parent_age_years()

        constraints = []

        for child_birth in child_birth_evidences:
            # Borne supérieure : on prend la date la plus tardive possible
            # de la naissance de l'enfant.
            child_birth_maximum = child_birth.date.normalized_maximum

            if child_birth_maximum is None:
                continue

            bound = try_add_years(
                child_birth_maximum,
                -min_parent_age_years,
            )

            if bound is None:
                continue

            constraints.append(
                TemporalConstraint(
                    target=target,
                    operator=ConstraintOperator.BEFORE_OR_EQUAL,
                    bound=bound,
                    rule_id=self.rule_id,
                    strength=self.strength,
                    evidences=(child_birth,),
                )
            )

        return tuple(constraints)
