"""Tests for Topic 09."""
import tempfile, unittest
from pathlib import Path
from topics.topic_09_file_systems_streams.concepts.binary_io import encode_payload, decode_payload
from topics.topic_09_file_systems_streams.concepts.buffers import render_lines
from topics.topic_09_file_systems_streams.dsa.binary_event_codec import encode_event, decode_event
from topics.topic_09_file_systems_streams.dsa.event_log_file import EventLogFile
from topics.topic_09_file_systems_streams.errors.file_not_found import require_file
from topics.topic_09_file_systems_streams.errors.json_decode_errors import parse_json_line
from topics.topic_09_file_systems_streams.errors.path_safety import reject_absolute
from topics.topic_09_file_systems_streams.solutions.entry_solution import roundtrip_json
from topics.topic_09_file_systems_streams.solutions.mid_solution import roundtrip_jsonl
from topics.topic_09_file_systems_streams.solutions.advanced_solution import persist_and_replay

def event(event_id="evt-1"):
    return {"event_id": event_id, "message": "hot"}
class Topic09Tests(unittest.TestCase):
    def test_file_stream_concepts_and_errors(self):
        self.assertEqual(decode_payload(encode_payload("x")), "x")
        self.assertEqual(render_lines(["a", "b"]), "a\nb\n")
        self.assertEqual(decode_event(encode_event(event()))["event_id"], "evt-1")
        with self.assertRaises(ValueError): parse_json_line("{")
        with self.assertRaises(ValueError): reject_absolute(Path.cwd())
    def test_solutions_with_temp_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = {"events": [event("a")]}; self.assertEqual(roundtrip_json(root/"data.json", data), data)
            events = [event("a"), event("b"), event("c")]
            self.assertEqual([e["event_id"] for e in roundtrip_jsonl(root/"events.jsonl", events)], ["a","b","c"])
            log = EventLogFile(root/"log.jsonl").write(events); self.assertEqual(len(log.read_all()), 3); require_file(root/"log.jsonl")
            result = persist_and_replay(root/"adv.jsonl", events, 2); self.assertEqual(result["count"], 3); self.assertEqual([e["event_id"] for e in result["recent"]], ["b","c"])
            with self.assertRaises(ValueError):
                persist_and_replay(root/"negative.jsonl", events, -1)
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_09_file_systems_streams/lab").glob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            for marker in ("def ", "class ", "import ", "from ", "return ", "```python"):
                self.assertNotIn(marker, text)
if __name__ == "__main__": unittest.main()
