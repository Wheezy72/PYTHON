"""Tests for Topic 10."""
import unittest
from pathlib import Path
from topics.topic_10_network_sockets_protocols.concepts.framing import encode_frame, decode_frame
from topics.topic_10_network_sockets_protocols.concepts.socket_lifecycle import parse_endpoint
from topics.topic_10_network_sockets_protocols.errors.timeout_patterns import normalize_timeout
from topics.topic_10_network_sockets_protocols.dsa.protocol_buffer import ProtocolBuffer
from topics.topic_10_network_sockets_protocols.dsa.udp_deduplicator import UdpDeduplicator
from topics.topic_10_network_sockets_protocols.solutions.entry_solution import round_trip_event
from topics.topic_10_network_sockets_protocols.solutions.mid_solution import decode_stream
from topics.topic_10_network_sockets_protocols.solutions.advanced_solution import ingest_protocol_messages
class Topic10Tests(unittest.TestCase):
    def test_concepts_and_dsa(self):
        event={"event_id":"evt-1","severity":4}; frame=encode_frame(event); self.assertEqual(decode_frame(frame), event)
        with self.assertRaises(ValueError): decode_frame(b"bad")
        self.assertEqual(parse_endpoint("localhost:9000"), ("localhost", 9000)); self.assertEqual(normalize_timeout(2), 2.0)
        buffer=ProtocolBuffer(); buffer.feed(frame[:3]); self.assertEqual(buffer.pop_frames(), ()); buffer.feed(frame[3:]); self.assertEqual(buffer.pop_frames(), (frame,))
        dedupe=UdpDeduplicator(); self.assertTrue(dedupe.accept("evt-1")); self.assertFalse(dedupe.accept("evt-1"))
    def test_solutions(self):
        event={"event_id":"evt-1","severity":4}; self.assertEqual(round_trip_event(event), event)
        frames=encode_frame(event)+encode_frame({"event_id":"evt-2"}); decoded, remaining=decode_stream([frames[:5], frames[5:]]); self.assertEqual([e["event_id"] for e in decoded], ["evt-1","evt-2"]); self.assertEqual(remaining, 0)
        out=ingest_protocol_messages([{"type":"event","payload":event},{"type":"event","payload":event},{"type":"bad"}]); self.assertEqual(len(out["events"]), 1); self.assertEqual(len(out["rejected"]), 2)
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_10_network_sockets_protocols/lab").glob("*.md"):
            text=path.read_text(encoding="utf-8").lower()
            for marker in ("def ","class ","import ","from ","return ","```python"): self.assertNotIn(marker,text)
if __name__=="__main__": unittest.main()
