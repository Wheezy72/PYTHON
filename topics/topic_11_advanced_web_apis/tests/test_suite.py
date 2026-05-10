"""Tests for Topic 11."""
import unittest
from pathlib import Path
from topics.topic_11_advanced_web_apis.concepts.rest_requests import build_url, build_headers
from topics.topic_11_advanced_web_apis.concepts.pagination import paginate
from topics.topic_11_advanced_web_apis.errors.http_errors import classify_status
from topics.topic_11_advanced_web_apis.errors.retry_errors import should_retry
from topics.topic_11_advanced_web_apis.dsa.token_bucket import TokenBucket
from topics.topic_11_advanced_web_apis.dsa.response_cache import ResponseCache
from topics.topic_11_advanced_web_apis.solutions.entry_solution import build_event_request
from topics.topic_11_advanced_web_apis.solutions.mid_solution import collect_pages
from topics.topic_11_advanced_web_apis.solutions.advanced_solution import simulate_api_ingestion
class Topic11Tests(unittest.TestCase):
    def test_concepts_dsa_and_solutions(self):
        self.assertEqual(build_url("https://api.test/","/events",{"page":1}), "https://api.test/events?page=1")
        self.assertIn("Authorization", build_headers("tok")); self.assertEqual(tuple(paginate([1,2,3],2)), ((1,2),(3,)))
        self.assertEqual(classify_status(429), "rate-limited"); self.assertTrue(should_retry(503,1,3))
        bucket=TokenBucket(1); self.assertTrue(bucket.allow()); self.assertFalse(bucket.allow()); bucket.refill(); self.assertTrue(bucket.allow())
        cache=ResponseCache(); self.assertEqual(cache.get_or_set("a", lambda: 1), 1); self.assertEqual(cache.get_or_set("a", lambda: 2), 1)
        self.assertEqual(build_event_request("https://api", "evt-1")["url"], "https://api/events/evt-1")
        self.assertEqual(collect_pages([1,2,3],2), ((1,2),(3,)))
        out=simulate_api_ingestion([{"status":200,"json":{"id":1}},{"status":500,"json":{}},{"status":200,"json":{"id":2}}],2); self.assertEqual(len(out["events"]),1); self.assertEqual(len(out["errors"]),2)
    def test_lab_files_are_prompt_only(self):
        for path in Path("topics/topic_11_advanced_web_apis/lab").glob("*.md"):
            text=path.read_text(encoding="utf-8").lower()
            for marker in ("def ","class ","import ","from ","return ","```python"): self.assertNotIn(marker,text)
if __name__=="__main__": unittest.main()
