"""Tests for Topic 14."""
import unittest
from pathlib import Path
from topics.topic_14_security_operations.concepts.hashing import stable_event_hash
from topics.topic_14_security_operations.concepts.signing import sign_message, verify_signature
from topics.topic_14_security_operations.concepts.sanitization import redact_secrets
from topics.topic_14_security_operations.errors.security_errors import require_secret
from topics.topic_14_security_operations.dsa.audit_log import AuditLog
from topics.topic_14_security_operations.solutions.entry_solution import fingerprint_events
from topics.topic_14_security_operations.solutions.mid_solution import sanitize_event
from topics.topic_14_security_operations.solutions.advanced_solution import sign_events, verify_signed_event
class Topic14Tests(unittest.TestCase):
    def test_security_operations(self):
        event={"event_id":"evt-1","metadata":{"token":"abc","region":"eu"}}
        self.assertEqual(stable_event_hash({"b":2,"a":1}), stable_event_hash({"a":1,"b":2}))
        sig=sign_message("longsecret","payload"); self.assertTrue(verify_signature("longsecret","payload",sig))
        self.assertEqual(redact_secrets({"token":"x","safe":"y"})["token"], "<redacted>")
        with self.assertRaises(ValueError): require_secret("short")
        log=AuditLog(); log.append("sign","evt-1"); self.assertEqual(log.all()[0]["action"], "sign")
        self.assertEqual(len(fingerprint_events([event])),1); self.assertEqual(sanitize_event(event)["metadata"]["token"], "<redacted>")
        signed=sign_events([event], "longsecret"); self.assertTrue(verify_signed_event(signed[0], "longsecret"))
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_14_security_operations/lab").glob("*.md"):
            text=path.read_text(encoding="utf-8").lower()
            for marker in ("def ","class ","import ","from ","return ","```python"): self.assertNotIn(marker,text)
if __name__=="__main__": unittest.main()
