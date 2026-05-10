"""REST request construction without third-party dependencies."""
from urllib.parse import urlencode

def build_url(base, path, query=None):
    url = base.rstrip("/") + "/" + path.lstrip("/")
    if query: url += "?" + urlencode(query)
    return url

def build_headers(token=None):
    headers = {"Accept": "application/json"}
    if token: headers["Authorization"] = f"Bearer {token}"
    return headers
