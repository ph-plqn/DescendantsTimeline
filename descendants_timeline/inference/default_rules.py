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

"""Composition des règles d'inférence activées par défaut."""

from descendants_timeline.inference.baptism_before_death_rule import (
    BaptismBeforeDeathRule,
)
from descendants_timeline.inference.birth_before_baptism_rule import (
    BirthBeforeBaptismRule,
)
from descendants_timeline.inference.birth_before_burial_rule import (
    BirthBeforeBurialRule,
)
from descendants_timeline.inference.birth_before_census_rule import (
    BirthBeforeCensusRule,
)
from descendants_timeline.inference.birth_before_child_birth_rule import (
    BirthBeforeChildBirthRule,
)
from descendants_timeline.inference.birth_before_death_rule import (
    BirthBeforeDeathRule,
)
from descendants_timeline.inference.birth_before_divorce_rule import (
    BirthBeforeDivorceRule,
)
from descendants_timeline.inference.birth_before_marriage_rule import (
    BirthBeforeMarriageRule,
)
from descendants_timeline.inference.birth_maximum_lifespan_from_burial_rule import (
    BirthMaximumLifespanFromBurialRule,
)
from descendants_timeline.inference.birth_maximum_lifespan_from_census_rule import (
    BirthMaximumLifespanFromCensusRule,
)
from descendants_timeline.inference.birth_maximum_lifespan_from_death_rule import (
    BirthMaximumLifespanFromDeathRule,
)
from descendants_timeline.inference.birth_minimum_age_at_marriage_rule import (
    BirthMinimumAgeAtMarriageRule,
)
from descendants_timeline.inference.birth_before_participation_rule import (
    BirthBeforeParticipationRule,
)
from descendants_timeline.inference.census_before_death_rule import (
    CensusBeforeDeathRule,
)
from descendants_timeline.inference.death_after_child_birth_rule import (
    DeathAfterChildBirthRule,
)
from descendants_timeline.inference.death_before_burial_rule import (
    DeathBeforeBurialRule,
)
from descendants_timeline.inference.death_after_participation_rule import (
    DeathAfterParticipationRule,
)
from descendants_timeline.inference.death_maximum_lifespan_from_birth_rule import (
    DeathMaximumLifespanFromBirthRule,
)
from descendants_timeline.inference.divorce_after_marriage_rule import (
    DivorceAfterMarriageRule,
)
from descendants_timeline.inference.divorce_before_death_rule import (
    DivorceBeforeDeathRule,
)
from descendants_timeline.inference.divorce_before_spouse_burial_rule import (
    DivorceBeforeSpouseBurialRule,
)
from descendants_timeline.inference.divorce_before_spouse_death_rule import (
    DivorceBeforeSpouseDeathRule,
)
from descendants_timeline.inference.marriage_after_birth_rule import (
    MarriageAfterBirthRule,
)
from descendants_timeline.inference.marriage_before_death_rule import (
    MarriageBeforeDeathRule,
)
from descendants_timeline.inference.marriage_before_divorce_rule import (
    MarriageBeforeDivorceRule,
)
from descendants_timeline.inference.marriage_before_spouse_burial_rule import (
    MarriageBeforeSpouseBurialRule,
)
from descendants_timeline.inference.marriage_before_spouse_death_rule import (
    MarriageBeforeSpouseDeathRule,
)
from descendants_timeline.inference.marriage_minimum_age_from_birth_rule import (
    MarriageMinimumAgeFromBirthRule,
)


def default_rules():
    """Retourne les règles d'inférence activées par défaut."""
    return (
        BirthBeforeBaptismRule(),
        BirthBeforeBurialRule(),
        BirthBeforeCensusRule(),
        BirthBeforeChildBirthRule(),
        BirthBeforeDeathRule(),
        BirthBeforeMarriageRule(),
        BirthBeforeDivorceRule(),
        BirthBeforeParticipationRule(),
        BirthMaximumLifespanFromBurialRule(),
        BirthMaximumLifespanFromCensusRule(),
        BirthMaximumLifespanFromDeathRule(),
        BirthMinimumAgeAtMarriageRule(),

        BaptismBeforeDeathRule(),
        CensusBeforeDeathRule(),
        MarriageBeforeDeathRule(),
        DivorceBeforeDeathRule(),
        DeathAfterChildBirthRule(),
        DeathAfterParticipationRule(),
        DeathBeforeBurialRule(),
        DeathMaximumLifespanFromBirthRule(),

        MarriageAfterBirthRule(),
        MarriageBeforeDivorceRule(),
        MarriageBeforeSpouseBurialRule(),
        MarriageBeforeSpouseDeathRule(),
        MarriageMinimumAgeFromBirthRule(),

        DivorceAfterMarriageRule(),
        DivorceBeforeSpouseBurialRule(),
        DivorceBeforeSpouseDeathRule(),
    )