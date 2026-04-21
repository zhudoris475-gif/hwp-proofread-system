import urllib.request, json

API_KEY = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic/v1/messages"

headers = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "Content-Type": "application/json"
}
body = json.dumps({
    "model": "astron-code-latest",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "hi"}]
}).encode()

print("Test 1: With proxy")
proxy = urllib.request.ProxyHandler({"https": "http://127.0.0.1:45626"})
opener = urllib.request.build_opener(proxy)
req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
try:
    with opener.open(req, timeout=30) as resp:
        data = json.loads(resp.read())
        print(f"  OK: {data.get('content', [{}])[0].get('text', '')[:30]}")
except Exception as e:
    print(f"  Error: {e}")

print("\nTest 2: Without proxy (direct)")
opener2 = urllib.request.build_opener(urllib.request.ProxyHandler({}))
req2 = urllib.request.Request(URL, data=body, headers=headers, method="POST")
try:
    with opener2.open(req2, timeout=15) as resp:
        data = json.loads(resp.read())
        print(f"  OK: {data.get('content', [{}])[0].get('text', '')[:30]}")
except Exception as e:
    print(f"  Error: {e}")
