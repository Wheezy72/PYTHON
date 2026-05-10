"""Tests for Topic 13."""
import unittest
from pathlib import Path
from topics.topic_13_cli_architecture.concepts.config_loading import merge_config
from topics.topic_13_cli_architecture.concepts.logging_patterns import log_record
from topics.topic_13_cli_architecture.errors.cli_errors import require_command, CliUsageError
from topics.topic_13_cli_architecture.dsa.command_router import CommandRouter
from topics.topic_13_cli_architecture.solutions.entry_solution import parse_cli
from topics.topic_13_cli_architecture.solutions.mid_solution import build_router
from topics.topic_13_cli_architecture.solutions.advanced_solution import run_cli
class Topic13Tests(unittest.TestCase):
    def test_cli_architecture(self):
        self.assertEqual(parse_cli(["ingest","events.json"]).source, "events.json")
        self.assertEqual(merge_config({"mode":"dev"},{"mode":"prod","x":None}), {"mode":"prod"})
        self.assertEqual(log_record("info","ready", command="status")["command"], "status")
        with self.assertRaises(CliUsageError): require_command(type("A",(),{})())
        router=CommandRouter(); router.register("x", lambda args: "ok"); self.assertEqual(router.dispatch("x", object()), "ok")
        self.assertEqual(build_router().commands(), ("status","ingest")); self.assertEqual(run_cli(["status"])["status"], "ok"); self.assertEqual(run_cli(["ingest","file"])["ingested_from"], "file")
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_13_cli_architecture/lab").glob("*.md"):
            text=path.read_text(encoding="utf-8").lower()
            for marker in ("def ","class ","import ","from ","return ","```python"): self.assertNotIn(marker,text)
if __name__=="__main__": unittest.main()
