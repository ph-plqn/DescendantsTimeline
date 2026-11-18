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

class GrampsDataAdapter:
    def __init__(self, database, *, diagnostics=None):
        self._database = database
        self._diagnostics = diagnostics

    def get_person(self, handle, *, diagnostics=None):
        read_person = self._database.get_person_from_handle
        diagnostics = self._diagnostics if diagnostics is None else diagnostics
        if diagnostics is not None:
            diagnostics.increment("person_api_calls", 1)
        return read_person(handle)

    def get_family(self, handle, *, diagnostics=None):
        read_family = self._database.get_family_from_handle
        diagnostics = self._diagnostics if diagnostics is None else diagnostics
        if diagnostics is not None:
            diagnostics.increment("family_api_calls", 1)
        return read_family(handle)

    def get_event(self, handle, *, diagnostics=None):
        read_event = self._database.get_event_from_handle
        diagnostics = self._diagnostics if diagnostics is None else diagnostics
        if diagnostics is not None:
            diagnostics.increment("event_api_calls", 1)
        return read_event(handle)
