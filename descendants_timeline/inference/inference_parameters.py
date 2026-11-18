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

"""Paramètres généalogiques du moteur d'inférence.

Ces valeurs définissent des seuils de plausibilité utilisés par les règles
d'inférence, qu'elles soient SOFT ou HARD. Elles ne représentent ni des
limites biologiques absolues, ni une validation juridique des événements
généalogiques.
"""

from gramps.gen.config import config

# Valeurs de repli si la clé est absente ou invalide
_DEFAULT_MIN_MARRIAGE_AGE_YEARS = 12
_DEFAULT_MAX_LIFESPAN_YEARS = 125
_DEFAULT_MIN_PARENT_AGE_YEARS = 13

# Durée de grossesse maximale observée. Valeur volontairement large pour que
# les bornes qui en dépendent restent sûres. Ce n'est pas une préférence Gramps.
MAX_PREGNANCY_MONTHS = 13


def _get_int_pref(key, default):
    """Lit une préférence entière de Gramps, avec repli sur une valeur par défaut."""
    try:
        value = int(config.get(key))
        return value if value > 0 else default
    except (AttributeError, ValueError, TypeError, KeyError):
        return default


def get_min_marriage_age_years():
    # Approximation : Gramps n'a pas d'âge minimum au mariage ;
    # on utilise l'écart minimal entre générations (âge minimal à la parentalité).
    return _get_int_pref("behavior.min-generation-years",
                         _DEFAULT_MIN_MARRIAGE_AGE_YEARS)


def get_max_plausible_lifespan_years():
    return _get_int_pref("behavior.max-age-prob-alive",
                         _DEFAULT_MAX_LIFESPAN_YEARS)

def get_min_parent_age_years():
    """Écart minimal entre la naissance d'un parent et celle de son enfant."""
    return _get_int_pref("behavior.min-generation-years",
                         _DEFAULT_MIN_PARENT_AGE_YEARS)
