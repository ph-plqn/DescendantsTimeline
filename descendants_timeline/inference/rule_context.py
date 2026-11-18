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

from collections.abc import Mapping
from dataclasses import dataclass, field
from heapq import merge
from types import MappingProxyType

from descendants_timeline.model.genealogy import RawGenealogyData
from descendants_timeline.model.child_ref import ChildRelation
from descendants_timeline.model.event import EventSemantic
from descendants_timeline.model.family_event_ref import FamilyRoleSemantic
from descendants_timeline.model.person_event_ref import EventRoleSemantic
from descendants_timeline.model.temporal_evidence import EvidenceOwnerType, TemporalEvidence
from descendants_timeline.model.temporal_target import TemporalOwnerType


def _build_marriage_evidences_by_parent(data, evidences):
    """Index existing marriage evidence in its original order, once per context."""
    by_parent = {}
    for evidence in evidences:
        if not (
            evidence.semantic is EventSemantic.MARRIAGE
            and evidence.owner_type is EvidenceOwnerType.FAMILY
            and evidence.role is FamilyRoleSemantic.FAMILY
            and evidence.principal_owner_type is TemporalOwnerType.FAMILY
            and evidence.principal_owner_id == evidence.owner_id
        ):
            continue
        family = data.families.get(evidence.owner_id)
        if family is None:
            continue
        if family.parent1_id is not None:
            by_parent.setdefault(family.parent1_id, []).append(evidence)
        if family.parent2_id is not None and family.parent2_id != family.parent1_id:
            by_parent.setdefault(family.parent2_id, []).append(evidence)
    return MappingProxyType({parent: tuple(values) for parent, values in by_parent.items()})


def _build_personal_principal_evidences(evidences):
    """Keep every qualifying birth/death/burial/census/baptism occurrence without deduplication."""
    by_person_and_semantic = {}
    for evidence in evidences:
        if (
            evidence.semantic in (EventSemantic.BIRTH, EventSemantic.DEATH, EventSemantic.BURIAL, EventSemantic.CENSUS, EventSemantic.BAPTISM)
            and evidence.owner_type is EvidenceOwnerType.PERSON
            and evidence.role is EventRoleSemantic.PRINCIPAL
            and evidence.principal_owner_type is TemporalOwnerType.PERSON
            and evidence.principal_owner_id == evidence.owner_id
        ):
            key = (evidence.owner_id, evidence.semantic)
            by_person_and_semantic.setdefault(key, []).append(evidence)
    return MappingProxyType({key: tuple(values) for key, values in by_person_and_semantic.items()})


def _build_divorce_evidences_by_parent(data, evidences):
    """Keep parent and family divorce occurrences in one pass, without deduplication."""
    by_parent = {}
    by_family = {}
    for evidence in evidences:
        if not (
            evidence.semantic is EventSemantic.DIVORCE
            and evidence.owner_type is EvidenceOwnerType.FAMILY
            and evidence.role is FamilyRoleSemantic.FAMILY
            and evidence.principal_owner_type is TemporalOwnerType.FAMILY
            and evidence.principal_owner_id == evidence.owner_id
        ):
            continue
        by_family.setdefault(evidence.owner_id, []).append(evidence)
        family = data.families.get(evidence.owner_id)
        if family is None:
            continue
        if family.parent1_id is not None:
            by_parent.setdefault(family.parent1_id, []).append(evidence)
        if family.parent2_id is not None and family.parent2_id != family.parent1_id:
            by_parent.setdefault(family.parent2_id, []).append(evidence)
    return (
        MappingProxyType({parent: tuple(values) for parent, values in by_parent.items()}),
        MappingProxyType({family: tuple(values) for family, values in by_family.items()}),
    )


def _build_birth_occurrence_positions(evidences):
    """Record birth, death and burial occurrence ordinals in one pass, never object identities."""
    by_person = {}
    deaths_by_person = {}
    burials_by_person = {}
    for position, evidence in enumerate(evidences):
        if (
            evidence.semantic is EventSemantic.BIRTH
            and evidence.owner_type is EvidenceOwnerType.PERSON
            and evidence.role is EventRoleSemantic.PRINCIPAL
            and evidence.principal_owner_type is TemporalOwnerType.PERSON
            and evidence.principal_owner_id == evidence.owner_id
        ):
            by_person.setdefault(evidence.owner_id, []).append(position)
        elif (
            evidence.semantic is EventSemantic.DEATH
            and evidence.owner_type is EvidenceOwnerType.PERSON
            and evidence.role is EventRoleSemantic.PRINCIPAL
            and evidence.principal_owner_type is TemporalOwnerType.PERSON
            and evidence.principal_owner_id == evidence.owner_id
        ):
            deaths_by_person.setdefault(evidence.owner_id, []).append(position)
        elif (
            evidence.semantic is EventSemantic.BURIAL
            and evidence.owner_type is EvidenceOwnerType.PERSON
            and evidence.role is EventRoleSemantic.PRINCIPAL
            and evidence.principal_owner_type is TemporalOwnerType.PERSON
            and evidence.principal_owner_id == evidence.owner_id
        ):
            burials_by_person.setdefault(evidence.owner_id, []).append(position)
    return (
        MappingProxyType({person: tuple(values) for person, values in by_person.items()}),
        MappingProxyType({person: tuple(values) for person, values in deaths_by_person.items()}),
        MappingProxyType({person: tuple(values) for person, values in burials_by_person.items()}),
    )


def _build_child_birth_evidences(data, personal_principal_evidences):
    """Index, par parent, les naissances de ses enfants biologiques.

    parent1 est traité comme le père et parent2 comme la mère. Seules les
    relations BIRTH sont retenues, séparément pour chaque parent. Un enfant
    n'est retenu que s'il a exactement une naissance enregistrée, comme pour
    les autres règles. L'ordre des familles puis des enfants est conservé.
    """
    as_mother = {}
    as_father = {}
    for family in data.families.values():
        for child_ref in family.child_refs:
            births = personal_principal_evidences.get(
                (child_ref.person_id, EventSemantic.BIRTH), (),
            )
            if len(births) != 1:
                continue
            birth = births[0]
            if (
                family.parent1_id is not None
                and family.parent1_id != child_ref.person_id
                and child_ref.relation_to_parent1 is ChildRelation.BIRTH
            ):
                as_father.setdefault(family.parent1_id, []).append(birth)
            if (
                family.parent2_id is not None
                and family.parent2_id != child_ref.person_id
                and child_ref.relation_to_parent2 is ChildRelation.BIRTH
            ):
                as_mother.setdefault(family.parent2_id, []).append(birth)
    return (
        MappingProxyType({parent: tuple(values) for parent, values in as_mother.items()}),
        MappingProxyType({parent: tuple(values) for parent, values in as_father.items()}),
    )


_PARTICIPATION_SEMANTICS = (
    EventSemantic.BIRTH,
    EventSemantic.BAPTISM,
    EventSemantic.MARRIAGE,
    EventSemantic.DEATH,
    EventSemantic.BURIAL,
)

_PARTICIPATION_ROLES = (
    EventRoleSemantic.WITNESS,
    EventRoleSemantic.INFORMANT,
)


def _build_participation_evidences(evidences):
    """Index, par personne, ses participations comme témoin ou déclarant.

    Une participation est la référence d'une personne, avec le rôle WITNESS
    ou INFORMANT, à l'évènement d'une autre personne ou d'une famille. Les
    références de la personne à ses propres évènements sont exclues : elles
    ne prouvent rien de plus que son évènement principal.
    """
    by_person = {}
    for evidence in evidences:
        if (
            evidence.owner_type is EvidenceOwnerType.PERSON
            and evidence.role in _PARTICIPATION_ROLES
            and evidence.semantic in _PARTICIPATION_SEMANTICS
            and not (
                evidence.principal_owner_type is TemporalOwnerType.PERSON
                and evidence.principal_owner_id == evidence.owner_id
            )
        ):
            by_person.setdefault(evidence.owner_id, []).append(evidence)
    return MappingProxyType({person: tuple(values) for person, values in by_person.items()})


@dataclass(frozen=True, slots=True)
class RuleContext:
    data: RawGenealogyData
    evidences: tuple[TemporalEvidence, ...]
    _marriage_evidences_by_parent: Mapping[str, tuple[TemporalEvidence, ...]] = field(
        init=False, repr=False, compare=False,
    )
    _personal_principal_evidences: Mapping[tuple[str, EventSemantic], tuple[TemporalEvidence, ...]] = field(
        init=False, repr=False, compare=False,
    )
    _divorce_evidences_by_parent: Mapping[str, tuple[TemporalEvidence, ...]] = field(
        init=False, repr=False, compare=False,
    )
    _birth_occurrence_positions: Mapping[str, tuple[int, ...]] = field(
        init=False, repr=False, compare=False,
    )

    _death_occurrence_positions: Mapping[str, tuple[int, ...]] = field(
        init=False, repr=False, compare=False,
    )

    _burial_occurrence_positions: Mapping[str, tuple[int, ...]] = field(
        init=False, repr=False, compare=False,
    )

    _divorce_evidences_by_family: Mapping[str, tuple[TemporalEvidence, ...]] = field(
        init=False, repr=False, compare=False,
    )

    _participation_evidences: Mapping[str, tuple[TemporalEvidence, ...]] = field(
        init=False, repr=False, compare=False,
    )

    _child_birth_evidences_as_mother: Mapping[str, tuple[TemporalEvidence, ...]] = field(
        init=False, repr=False, compare=False,
    )

    _child_birth_evidences_as_father: Mapping[str, tuple[TemporalEvidence, ...]] = field(
        init=False, repr=False, compare=False,
    )

    def __post_init__(self) -> None:
        if not isinstance(self.data, RawGenealogyData):
            raise TypeError("data must be a RawGenealogyData")

        if not isinstance(self.evidences, tuple):
            raise TypeError("evidences must be a tuple")

        if not all(
            isinstance(evidence, TemporalEvidence)
            for evidence in self.evidences
        ):
            raise TypeError(
                "evidences must contain only TemporalEvidence objects"
            )
        object.__setattr__(
            self, "_marriage_evidences_by_parent",
            _build_marriage_evidences_by_parent(self.data, self.evidences),
        )
        object.__setattr__(
            self, "_personal_principal_evidences",
            _build_personal_principal_evidences(self.evidences),
        )
        divorce_parents, divorce_families = _build_divorce_evidences_by_parent(self.data, self.evidences)
        object.__setattr__(self, "_divorce_evidences_by_parent", divorce_parents)
        object.__setattr__(self, "_divorce_evidences_by_family", divorce_families)
        birth_positions, death_positions, burial_positions = _build_birth_occurrence_positions(self.evidences)
        object.__setattr__(self, "_birth_occurrence_positions", birth_positions)
        object.__setattr__(self, "_death_occurrence_positions", death_positions)
        object.__setattr__(self, "_burial_occurrence_positions", burial_positions)
        object.__setattr__(
            self, "_participation_evidences",
            _build_participation_evidences(self.evidences),
        )
        as_mother, as_father = _build_child_birth_evidences(
            self.data, self._personal_principal_evidences,
        )
        object.__setattr__(self, "_child_birth_evidences_as_mother", as_mother)
        object.__setattr__(self, "_child_birth_evidences_as_father", as_father)

    def marriage_evidences_for_parent(self, person_id):
        return self._marriage_evidences_by_parent.get(person_id, ())

    def personal_principal_evidences(self, person_id, semantic):
        return self._personal_principal_evidences.get((person_id, semantic), ())

    def divorce_evidences_for_parent(self, person_id):
        return self._divorce_evidences_by_parent.get(person_id, ())

    def ordered_birth_evidences_for_parents(self, person_ids):
        streams = (
            zip(
                self._birth_occurrence_positions.get(person_id, ()),
                self.personal_principal_evidences(person_id, EventSemantic.BIRTH),
            )
            for person_id in person_ids
        )
        return tuple(
            evidence
            for _, evidence in merge(*streams, key=lambda item: item[0])
        )

    def ordered_death_evidences_for_parents(self, person_ids):
        streams = (
            zip(
                self._death_occurrence_positions.get(person_id, ()),
                self.personal_principal_evidences(person_id, EventSemantic.DEATH),
            )
            for person_id in person_ids
        )
        return tuple(
            evidence
            for _, evidence in merge(*streams, key=lambda item: item[0])
        )

    def ordered_burial_evidences_for_parents(self, person_ids):
        streams = (
            zip(
                self._burial_occurrence_positions.get(person_id, ()),
                self.personal_principal_evidences(person_id, EventSemantic.BURIAL),
            )
            for person_id in person_ids
        )
        return tuple(
            evidence
            for _, evidence in merge(*streams, key=lambda item: item[0])
        )

    def divorce_evidences_for_family(self, family_id):
        return self._divorce_evidences_by_family.get(family_id, ())

    def participation_evidences(self, person_id):
        """Participations d'une personne comme témoin ou déclarant."""
        return self._participation_evidences.get(person_id, ())

    def child_birth_evidences_as_mother(self, person_id):
        """Naissances des enfants biologiques de cette personne, comme mère."""
        return self._child_birth_evidences_as_mother.get(person_id, ())

    def child_birth_evidences_as_father(self, person_id):
        """Naissances des enfants biologiques de cette personne, comme père."""
        return self._child_birth_evidences_as_father.get(person_id, ())
