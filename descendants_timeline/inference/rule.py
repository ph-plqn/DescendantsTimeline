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

from abc import ABC, abstractmethod

from descendants_timeline.inference.rule_context import RuleContext
from descendants_timeline.model.temporal_constraint import (
    ConstraintStrength,
    TemporalConstraint,
)
from descendants_timeline.model.temporal_target import TemporalTarget


class Rule(ABC):
    rule_id: str
    strength: ConstraintStrength

    @abstractmethod
    def is_applicable(
        self,
        target: TemporalTarget,
        context: RuleContext,
    ) -> bool:
        ...

    @abstractmethod
    def evaluate(
        self,
        target: TemporalTarget,
        context: RuleContext,
    ) -> tuple[TemporalConstraint, ...]:
        ...