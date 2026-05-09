"""MRO and cooperative super examples for SentinelFlow."""

class AuditBase:
    def stages(self):
        return ["base"]

class ParseMixin(AuditBase):
    def stages(self):
        return ["parse", *super().stages()]

class ValidateMixin(AuditBase):
    def stages(self):
        return ["validate", *super().stages()]

class AuditProcessor(ParseMixin, ValidateMixin):
    pass

def processor_mro_names(cls=AuditProcessor):
    """Inspect class linearization in O(m) for m classes."""
    return tuple(item.__name__ for item in cls.mro())
