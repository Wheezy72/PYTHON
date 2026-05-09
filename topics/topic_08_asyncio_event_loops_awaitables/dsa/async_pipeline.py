"""Async pipeline helpers."""
class AsyncPipeline:
    def __init__(self, stages=()):
        self._stages = tuple(stages)
    def then(self, stage):
        if not callable(stage):
            raise TypeError("stage must be callable")
        return AsyncPipeline((*self._stages, stage))
    async def run_one(self, event):
        current = event
        for stage in self._stages:
            current = await stage(current)
        return current
