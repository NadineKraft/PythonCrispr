from roi_source.RoiSource import RoiSource
from scorer.Scorer import Scorer
from target_index.TargetIndex import TargetIndex
from target_sink.TargetSink import TargetSink


class Crispr:

    def __init__(self, roi_source: RoiSource, target_index: TargetIndex, scorer: Scorer, target_sink: TargetSink,
                 score_minimum: float):
        self.roi_source = roi_source
        self.target_index = target_index
        self.scorer = scorer
        self.target_sink = target_sink
        self.score_minimum = score_minimum

    def perform(self):
        with self.roi_source, self.target_index, self.target_sink:
            for roi in self.roi_source.rois():
                print("processing: " + str(roi))
                if self.target_index.is_acceptable(roi):
                    for target in self.target_index.targets(roi):
                        if self.scorer.score(target) >= self.score_minimum:
                            self.target_sink.append(roi, target, self.scorer.score(target))
                else:
                    print("ignoring: " + str(roi))
