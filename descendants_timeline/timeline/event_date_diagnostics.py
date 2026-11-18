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

"""Consultation des diagnostics documentaires du modèle de timeline."""

from descendants_timeline.model.event_date_diagnostic import EventDateDiagnostic
from descendants_timeline.timeline.timeline_model import TimelineModel


def get_person_event_date_diagnostics(
    model: TimelineModel,
    person_id: str,
) -> tuple[tuple[str, EventDateDiagnostic], ...]:
    """Retourne les diagnostics des références directes, dans leur ordre initial."""
    person = model.data.persons[person_id]
    seen_event_ids = set()
    diagnostics = []
    for reference in person.event_refs:
        event_id = reference.event_id
        if event_id in seen_event_ids:
            continue
        seen_event_ids.add(event_id)
        diagnostic = model.event_date_diagnostics.get(event_id)
        if diagnostic is not None:
            diagnostics.append((event_id, diagnostic))
    return tuple(diagnostics)


def get_family_event_date_diagnostics(
    model: TimelineModel,
    family_id: str,
) -> tuple[tuple[str, EventDateDiagnostic], ...]:
    """Retourne les diagnostics des références familiales dans leur ordre initial."""
    family = model.data.families[family_id]
    seen_event_ids = set()
    diagnostics = []
    for reference in family.event_refs:
        event_id = reference.event_id
        if event_id in seen_event_ids:
            continue
        seen_event_ids.add(event_id)
        diagnostic = model.event_date_diagnostics.get(event_id)
        if diagnostic is not None:
            diagnostics.append((event_id, diagnostic))
    return tuple(diagnostics)


def get_person_family_event_date_diagnostics(
    model: TimelineModel,
    person_id: str,
) -> tuple[tuple[str, tuple[tuple[str, EventDateDiagnostic], ...]], ...]:
    """Conserve les familles de la personne dans leur ordre, même sans diagnostic."""
    person = model.data.persons[person_id]
    return tuple(
        (family_id, get_family_event_date_diagnostics(model, family_id))
        for family_id in person.family_ids
    )
