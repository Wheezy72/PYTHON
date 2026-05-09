"""Small mixins that add reusable event behavior."""
from copy import deepcopy

class CopyEventMixin:
    def copy_event(self, event):
        return deepcopy(event)

class StageTagMixin:
    stage_name = "stage"
    def mark_stage(self, event):
        copied = self.copy_event(event) if hasattr(self, "copy_event") else dict(event)
        copied["stages"] = (*tuple(copied.get("stages", ())), self.stage_name)
        return copied

class StagedCopyProcessor(CopyEventMixin, StageTagMixin):
    stage_name = "oop"
