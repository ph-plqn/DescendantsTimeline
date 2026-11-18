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

from .date_arithmetic import try_add_months
from .inference_parameters import MAX_PREGNANCY_MONTHS


class DeathAfterChildBirthRule(Rule):
    """Un parent est décédé après la naissance de son enfant biologique.

    - Mère : décès >= naissance de l'enfant (le décès en couches est possible,
      d'où l'opérateur « supérieur ou égal »).
    - Père : décès >= naissance de l'enfant moins la durée maximale de
      grossesse (naissance posthume possible).

    Une contrainte est émise pour chaque enfant biologique ayant une
    naissance exploitable ; la plus serrée (l'enfant le plus tardif) est
    celle qui borne réellement.
    """

    rule_id = "DEATH_AFTER_CHILD_BIRTH"
    strength = ConstraintStrength.HARD

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

        constraints = []

        # Mère : aucun décalage.
        for child_birth in context.child_birth_evidences_as_mother(target.owner_id):
            # Borne inférieure : on prend la date la plus précoce possible
            # de la naissance de l'enfant.
            bound = child_birth.date.normalized_minimum

            if bound is None:
                continue

            constraints.append(self._constraint(target, bound, child_birth))

        # Père : la naissance peut suivre le décès de la durée de grossesse.
        for child_birth in context.child_birth_evidences_as_father(target.owner_id):
            child_birth_minimum = child_birth.date.normalized_minimum

            if child_birth_minimum is None:
                continue

            bound = try_add_months(
                child_birth_minimum,
                -MAX_PREGNANCY_MONTHS,
            )

            if bound is None:
                continue

            constraints.append(self._constraint(target, bound, child_birth))

        return tuple(constraints)

    def _constraint(self, target, bound, child_birth):
        return TemporalConstraint(
            target=target,
            operator=ConstraintOperator.AFTER_OR_EQUAL,
            bound=bound,
            rule_id=self.rule_id,
            strength=self.strength,
            evidences=(child_birth,),
        )
