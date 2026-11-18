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

import logging
from dataclasses import dataclass

from descendants_timeline.inference.rule import Rule
from descendants_timeline.inference.rule_context import RuleContext
from descendants_timeline.model.temporal_constraint import TemporalConstraint
from descendants_timeline.model.temporal_target import TemporalTarget


_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RuleEngine:
    rules: tuple[Rule, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.rules, tuple):
            raise TypeError("rules must be a tuple")

        if not all(
            isinstance(rule, Rule)
            for rule in self.rules
        ):
            raise TypeError(
                "rules must contain only Rule objects"
            )

    def evaluate(
        self,
        target: TemporalTarget,
        context: RuleContext,
    ) -> tuple[TemporalConstraint, ...]:
        constraints: list[TemporalConstraint] = []

        for rule in self.rules:
            if not rule.is_applicable(target, context):
                continue

            try:
                rule_constraints = rule.evaluate(
                    target,
                    context,
                )
            except (ValueError, OverflowError) as error:
                # Donnée aberrante (date hors plage, etc.) : la règle est
                # ignorée pour cette cible, le reste du calcul continue.
                _LOGGER.warning(
                    "DescendantsTimeline: règle %s ignorée (%s)",
                    getattr(rule, "rule_id", type(rule).__name__),
                    error,
                )
                continue

            constraints.extend(rule_constraints)

        return tuple(constraints)