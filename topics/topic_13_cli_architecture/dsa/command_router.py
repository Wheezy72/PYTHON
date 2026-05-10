"""Dictionary-backed command router."""
class CommandRouter:
    def __init__(self): self._handlers={}
    def register(self, name, handler):
        if not callable(handler): raise TypeError("handler must be callable")
        self._handlers[name]=handler
    def dispatch(self, name, args): return self._handlers[name](args)
    def commands(self): return tuple(self._handlers)
