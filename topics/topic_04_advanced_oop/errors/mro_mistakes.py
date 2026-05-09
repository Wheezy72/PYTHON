"""Detect cooperative-super mistakes."""
def missing_base_stage(processor):
    stages = processor.stages()
    return "base" not in stages
