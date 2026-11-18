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

register(
    VIEW,
    id="descendants_timeline",
    name=_("Descendants Timeline"),
    description=_("Timeline of descendants and their lifespans."),
    version="1.2.0",
    gramps_target_version="6.0",
    status=STABLE,
    fname="descendants_timeline_plugin.py",
    viewclass="create_descendants_timeline_view",
    category=("Ancestry", _("Charts")),
    authors=["Philippe Pouliquen"],
    authors_email=["ph.plqn@proton.me"],
    order=END,
)

register(
    GENERAL,
    id="descendants_timeline_selector_init",
    name=_("Descendants Timeline selector icon"),
    description=_("Prepare the Descendants Timeline icon for the view selector."),
    version="1.2.0",
    gramps_target_version="6.0",
    status=STABLE,
    fname="descendants_timeline_selector_init.py",
    authors=["Philippe Pouliquen"],
    authors_email=["ph.plqn@proton.me"],
    load_on_reg=True,
)
