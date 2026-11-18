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

"""Composition pure du modèle de timeline à partir d'une photographie."""

from contextlib import nullcontext

from descendants_timeline.inference.temporal_inference_engine import TemporalInferenceEngine
from descendants_timeline.model.genealogy import RawGenealogyData
from descendants_timeline.timeline.timeline_model import TimelineModel
from descendants_timeline.timeline.timeline_model_builder import TimelineModelBuilder
from descendants_timeline.traversal.descendance_traversal import DescendanceTraversal


class TimelineModelComposer:
    def __init__(
        self,
        traversal: DescendanceTraversal,
        inference_engine: TemporalInferenceEngine,
        model_builder: TimelineModelBuilder,
        *, diagnostics=None,
    ) -> None:
        self._traversal = traversal
        self._inference_engine = inference_engine
        self._model_builder = model_builder
        self._diagnostics = diagnostics

    def __call__(self, data: RawGenealogyData, *, diagnostics=None) -> TimelineModel:
        diagnostics = self._diagnostics if diagnostics is None else diagnostics
        with (
            diagnostics.phase("model")
            if diagnostics is not None
            else nullcontext()
        ):
            with (
                diagnostics.phase("dfs")
                if diagnostics is not None
                else nullcontext()
            ):
                traversal = self._traversal.traverse(data, data.root_person_id)
            if diagnostics is not None:
                diagnostics.increment("dfs_rows", len(traversal.rows))
            if diagnostics is None:
                temporal_results = self._inference_engine.run(data)
            else:
                temporal_results = self._inference_engine.run(data, diagnostics=diagnostics)
            return self._model_builder.build(data, traversal, temporal_results)


    def _iter_compose(self, data):
        """Keep DFS and model assembly whole, and resume inference in order."""
        traversal = self._traversal.traverse(data, data.root_person_id)
        yield "Calcul des dates"
        results = yield from self._inference_engine._iter_run(data)
        yield "Assemblage du modèle"
        return self._model_builder.build(data, traversal, results)
