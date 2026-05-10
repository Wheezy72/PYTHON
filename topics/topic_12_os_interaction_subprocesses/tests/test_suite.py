"""Tests for Topic 12."""
import sys, unittest
from pathlib import Path
from topics.topic_12_os_interaction_subprocesses.concepts.signal_models import classify_exit
from topics.topic_12_os_interaction_subprocesses.concepts.subprocess_runner import run_command
from topics.topic_12_os_interaction_subprocesses.errors.shell_safety import reject_shell_string
from topics.topic_12_os_interaction_subprocesses.dsa.process_history import ProcessHistory
from topics.topic_12_os_interaction_subprocesses.solutions.entry_solution import load_runtime_config
from topics.topic_12_os_interaction_subprocesses.solutions.mid_solution import run_checked
from topics.topic_12_os_interaction_subprocesses.solutions.advanced_solution import supervise_commands
class Topic12Tests(unittest.TestCase):
    def test_os_subprocess_solutions(self):
        self.assertEqual(load_runtime_config({"SENTINEL_MODE":"prod"})["mode"], "prod")
        self.assertEqual(classify_exit(0), "success"); self.assertEqual(classify_exit(-15), "signal")
        with self.assertRaises(TypeError): reject_shell_string("echo unsafe")
        result=run_command([sys.executable,"-c","print('ok')"]); self.assertEqual(result.stdout.strip(), "ok")
        self.assertEqual(run_checked([sys.executable,"-c","print('checked')"]).strip(), "checked")
        history=ProcessHistory(); history.add(["x"],1); self.assertEqual(len(history.failures()),1)
        out=supervise_commands([[sys.executable,"-c","print('a')"],[sys.executable,"-c","import sys; sys.exit(2)"]]); self.assertEqual(out["count"],2); self.assertEqual(len(out["failures"]),1)
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_12_os_interaction_subprocesses/lab").glob("*.md"):
            text=path.read_text(encoding="utf-8").lower()
            for marker in ("def ","class ","import ","from ","return ","```python"): self.assertNotIn(marker,text)
if __name__=="__main__": unittest.main()
