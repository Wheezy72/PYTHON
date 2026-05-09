"""Tests for Topic 04: Advanced OOP."""
import unittest
from pathlib import Path
from topics.topic_04_advanced_oop.concepts.mro_cooperative import AuditProcessor, processor_mro_names
from topics.topic_04_advanced_oop.concepts.mixins import StagedCopyProcessor
from topics.topic_04_advanced_oop.concepts.abcs_protocols import EventProcessor, ProcessorProtocol, SeverityCapper
from topics.topic_04_advanced_oop.concepts.polymorphism import AddFieldProcessor, DropDebugProcessor
from topics.topic_04_advanced_oop.dsa.processor_registry import ProcessorRegistry
from topics.topic_04_advanced_oop.dsa.processor_pipeline import ProcessorPipeline
from topics.topic_04_advanced_oop.dsa.stores import InMemoryEventStore
from topics.topic_04_advanced_oop.errors.abstract_contracts import require_processor
from topics.topic_04_advanced_oop.errors.mutation_aliasing import safe_attach_tag, unsafe_attach_tag
from topics.topic_04_advanced_oop.solutions.entry_solution import build_oop_pipeline
from topics.topic_04_advanced_oop.solutions.mid_solution import build_store, configure_registry
from topics.topic_04_advanced_oop.solutions.advanced_solution import run_oop_ingestion

def event(event_id="evt-1", source="sensor", severity=7, tags=None):
    return {"event_id": event_id, "source": source, "severity": severity, "tags": ["edge"] if tags is None else tags, "message": "hot"}

class Topic04Tests(unittest.TestCase):
    def test_concepts_and_errors(self):
        self.assertEqual(AuditProcessor().stages(), ["parse", "validate", "base"])
        self.assertIn("AuditProcessor", processor_mro_names())
        original = event(); marked = StagedCopyProcessor().mark_stage(original)
        self.assertEqual(marked["stages"], ("oop",)); self.assertNotIn("stages", original)
        with self.assertRaises(TypeError): EventProcessor()
        self.assertIsInstance(SeverityCapper(), ProcessorProtocol)
        with self.assertRaises(TypeError): require_processor(object())
        unsafe = event(tags=[]); unsafe_attach_tag(unsafe, "x"); self.assertEqual(unsafe["tags"], ["x"])
        safe = safe_attach_tag(unsafe, "y"); self.assertEqual(safe["tags"], ("x", "y")); self.assertEqual(unsafe["tags"], ["x"])
    def test_dsa_and_solutions(self):
        pipe = ProcessorPipeline((SeverityCapper(5), AddFieldProcessor("region", "eu"), DropDebugProcessor()))
        result = pipe.run({**event(), "debug": True})
        self.assertEqual((result["severity"], result["region"]), (5, "eu")); self.assertNotIn("debug", result)
        registry = ProcessorRegistry(); registry.register("cap", SeverityCapper()); self.assertEqual(registry.names(), ("cap",))
        store = InMemoryEventStore(); store.add(event("a", "s1")); store.add(event("b", "s1")); self.assertEqual(len(store.by_source()["s1"]), 2)
        self.assertEqual(build_oop_pipeline("ap").run(event())["region"], "ap")
        self.assertEqual(configure_registry({"cap": SeverityCapper()}).names(), ("cap",))
        self.assertEqual(len(build_store([event(), event("e2")]).all()), 2)
        output = run_oop_ingestion([event("a", "s1"), event("b", "s2")], (SeverityCapper(), AddFieldProcessor("processed", True)))
        self.assertEqual(output["processor_count"], 2); self.assertTrue(output["events"][0]["processed"])
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_04_advanced_oop/lab").glob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            for marker in ("def ", "class ", "import ", "from ", "return ", "```python"):
                self.assertNotIn(marker, text)
if __name__ == "__main__": unittest.main()
