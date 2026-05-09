"""Composable lazy event pipeline."""
class LazyPipeline:
    def __init__(self, stages=()):
        self._stages = tuple(stages)
    def then(self, stage):
        if not callable(stage):
            raise TypeError("stage must be callable")
        return LazyPipeline((*self._stages, stage))
    def run(self, events):
        stream = events
        for stage in self._stages:
            stream = stage(stream)
        return stream
