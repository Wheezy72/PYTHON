"""Advanced solution for Topic 11."""
from topics.topic_11_advanced_web_apis.dsa.token_bucket import TokenBucket
from topics.topic_11_advanced_web_apis.errors.http_errors import classify_status

def simulate_api_ingestion(responses, limit=2):
    bucket=TokenBucket(limit); accepted=[]; errors=[]
    for response in responses:
        if not bucket.allow(): errors.append({"error_type":"rate-limited"}); continue
        status=response["status"]; category=classify_status(status)
        if category=="ok": accepted.append(response["json"])
        else: errors.append({"status":status,"error_type":category})
    return {"events":tuple(accepted), "errors":tuple(errors), "remaining_tokens":bucket.tokens}
