from mitmproxy import http
import re

with open("banned_keywords.txt") as f:
    BANNED_KEYWORDS = [line.strip().lower() for line in f if line.strip()]

with open("banned_domains.txt") as f:
    BANNED_DOMAINS = [line.strip().lower() for line in f if line.strip()]

def request(flow: http.HTTPFlow) -> None:
    url = flow.request.pretty_url.lower()
    host = flow.request.host.lower()

    for domain in BANNED_DOMAINS:
        if domain in host:
            flow.response = http.HTTPResponse.make(
                403, b"Blocked by local filter: domain", {"Content-Type": "text/html"}
            )
            return

    for keyword in BANNED_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", url):
            flow.response = http.HTTPResponse.make(
                403, b"Blocked by local filter: keyword", {"Content-Type": "text/html"}
            )
            return

    with open("visited_log.txt", "a") as log:
        log.write(url + "\n")
