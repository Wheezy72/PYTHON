"""Polymorphic processor examples."""
class AddFieldProcessor:
    def __init__(self, key, value):
        self.key = key
        self.value = value
    def process(self, event):
        copied = dict(event)
        copied[self.key] = self.value
        return copied

class DropDebugProcessor:
    def process(self, event):
        copied = dict(event)
        copied.pop("debug", None)
        return copied
