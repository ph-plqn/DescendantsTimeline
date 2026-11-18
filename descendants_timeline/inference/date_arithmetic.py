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

"""Opérations calendaires utilisées par le moteur d'inférence."""

from __future__ import annotations

import calendar
from datetime import date


def add_years(value: date, years: int) -> date:
    """
    Décale une date d'un nombre entier d'années.

    Si la date est un 29 février et que l'année résultante
    n'est pas bissextile, le résultat est fixé au 1er mars.
    """

    if not isinstance(value, date):
        raise TypeError("value must be a date")

    if not isinstance(years, int):
        raise TypeError("years must be an integer")

    target_year = value.year + years

    try:
        return value.replace(year=target_year)
    except ValueError:
        # Le seul cas attendu ici est le 29 février
        # déplacé vers une année non bissextile.
        if value.month == 2 and value.day == 29:
            return date(target_year, 3, 1)

        raise


def try_add_years(value: date, years: int) -> date | None:
    """
    Comme add_years, mais renvoie None si le résultat sort de la plage
    de dates représentables (année < 1 ou > 9999).

    Une borne de plausibilité hors plage n'a pas de sens : l'appelant
    ignore alors simplement la contrainte correspondante.
    """

    target_year = value.year + years

    if not date.min.year <= target_year <= date.max.year:
        return None

    try:
        return add_years(value, years)
    except (ValueError, OverflowError):
        return None


def add_months(value: date, months: int) -> date:
    """
    Décale une date d'un nombre entier de mois.

    Si le jour n'existe pas dans le mois d'arrivée (par exemple le 31 vers
    un mois de 30 jours), le résultat est ramené au dernier jour de ce mois.
    """

    if not isinstance(value, date):
        raise TypeError("value must be a date")

    if not isinstance(months, int):
        raise TypeError("months must be an integer")

    total_months = value.year * 12 + (value.month - 1) + months
    target_year, month_index = divmod(total_months, 12)
    target_month = month_index + 1
    last_day = calendar.monthrange(target_year, target_month)[1]

    return date(target_year, target_month, min(value.day, last_day))


def try_add_months(value: date, months: int) -> date | None:
    """
    Comme add_months, mais renvoie None si le résultat sort de la plage
    de dates représentables (année < 1 ou > 9999).

    Une borne de plausibilité hors plage n'a pas de sens : l'appelant
    ignore alors simplement la contrainte correspondante.
    """

    target_year = (value.year * 12 + (value.month - 1) + months) // 12

    if not date.min.year <= target_year <= date.max.year:
        return None

    try:
        return add_months(value, months)
    except (ValueError, OverflowError):
        return None
