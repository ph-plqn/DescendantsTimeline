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

"""État initial d'une cible temporelle avant inférence."""

from __future__ import annotations

from dataclasses import dataclass

from descendants_timeline.model.temporal import TemporalValue, ValueOrigin
from descendants_timeline.model.temporal_target import TemporalTarget
from descendants_timeline.model.temporal_target_anomaly import (
    TemporalTargetAnomaly,
    TemporalTargetAnomalyType,
)


@dataclass(frozen=True, slots=True)
class TemporalTargetEntry:
    """État Gramps initial associé à une cible temporelle.

    L'objet associe une cible temporelle à la valeur Gramps que le moteur
    d'inférence est autorisé à utiliser, ainsi qu'aux éventuelles anomalies
    structurelles détectées pour cette cible.

    Une anomalie MULTIPLE_PRINCIPAL_EVENTS rend la valeur Gramps ambiguë :
    gramps_value doit alors être UNKNOWN.
    """

    target: TemporalTarget
    gramps_value: TemporalValue
    anomalies: tuple[TemporalTargetAnomaly, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.target, TemporalTarget):
            raise TypeError("target doit être un TemporalTarget.")

        if not isinstance(self.gramps_value, TemporalValue):
            raise TypeError("gramps_value doit être un TemporalValue.")

        if not isinstance(self.anomalies, tuple):
            raise TypeError("anomalies doit être un tuple.")

        if any(
            not isinstance(anomaly, TemporalTargetAnomaly)
            for anomaly in self.anomalies
        ):
            raise TypeError(
                "Chaque anomalie doit être un TemporalTargetAnomaly."
            )

        if len(set(self.anomalies)) != len(self.anomalies):
            raise ValueError(
                "anomalies ne doit pas contenir de doublons."
            )

        has_multiple_principal_events = any(
            anomaly.anomaly_type
            is TemporalTargetAnomalyType.MULTIPLE_PRINCIPAL_EVENTS
            for anomaly in self.anomalies
        )

        if (
            has_multiple_principal_events
            and self.gramps_value.value_origin is not ValueOrigin.UNKNOWN
        ):
            raise ValueError(
                "MULTIPLE_PRINCIPAL_EVENTS exige "
                "gramps_value d'origine UNKNOWN."
            )