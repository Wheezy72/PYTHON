"""CLI config merge helpers."""
def merge_config(defaults, overrides):
    merged=dict(defaults); merged.update({k:v for k,v in overrides.items() if v is not None}); return merged
