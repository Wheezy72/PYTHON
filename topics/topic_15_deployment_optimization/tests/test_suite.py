"""Tests for Topic 15."""
import unittest
from pathlib import Path
from topics.topic_15_deployment_optimization.concepts.bytecode import opcode_names
from topics.topic_15_deployment_optimization.concepts.caching import normalized_source
from topics.topic_15_deployment_optimization.errors.performance_errors import require_positive_limit
from topics.topic_15_deployment_optimization.dsa.benchmark_table import BenchmarkTable
from topics.topic_15_deployment_optimization.solutions.entry_solution import inspect_transform
from topics.topic_15_deployment_optimization.solutions.mid_solution import normalize_sources
from topics.topic_15_deployment_optimization.solutions.advanced_solution import deployment_report
class Topic15Tests(unittest.TestCase):
    def test_deployment_optimization(self):
        def transform(x): return x + 1
        self.assertIn("RETURN_VALUE", opcode_names(transform)); self.assertGreater(inspect_transform(transform)["opcode_count"], 0)
        self.assertEqual(normalized_source(" API "), "api"); self.assertEqual(normalize_sources([" A ","a"]), ("a","a"))
        with self.assertRaises(ValueError): require_positive_limit(0)
        table=BenchmarkTable(); table.add("slow",2); table.add("fast",1); self.assertEqual(table.fastest()["name"], "fast")
        report=deployment_report(sum, [1,2,3]); self.assertEqual(report["result"], 6); self.assertTrue(report["profile_contains"])
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_15_deployment_optimization/lab").glob("*.md"):
            text=path.read_text(encoding="utf-8").lower()
            for marker in ("def ","class ","import ","from ","return ","```python"): self.assertNotIn(marker,text)
if __name__=="__main__": unittest.main()
