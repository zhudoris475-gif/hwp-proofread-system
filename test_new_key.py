import urllib.request, json

API_KEY = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"

endpoints = [
    ("https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic/v1/messages", "anthropic"),
    ("https://maas-coding-api.cn-huabei-1.xf-yun.com/v2/v1/messages", "v2"),
]

for url, label in endpoints:
    print(f"\n--- Testing {label}: {url} ---")
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

    proxy = urllib.request.ProxyHandler({"https": "http://127.0.0.1:45626"})
    opener = urllib.request.build_opener(proxy)

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with opener.open(req, timeout=30) as resp:
            data = json.loads(resp.read())
            print(f"SUCCESS! Model: {data.get('model')}")
            for c in data.get('content', []):
                print(f"  Response: {c.get('text', '')}")
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'read'):
            body_text = e.read().decode()[:300]
            print(f"Body: {body_text}")
