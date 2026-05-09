"""Entry solution for Topic 04."""
from topics.topic_04_advanced_oop.concepts.abcs_protocols import SeverityCapper
from topics.topic_04_advanced_oop.concepts.polymorphism import AddFieldProcessor
from topics.topic_04_advanced_oop.dsa.processor_pipeline import ProcessorPipeline

def build_oop_pipeline(region="unknown"):
    return ProcessorPipeline((SeverityCapper(), AddFieldProcessor("region", region)))
