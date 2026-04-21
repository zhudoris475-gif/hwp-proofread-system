import urllib.request, json

API_KEY = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"

endpoints = [
    ("https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic/v1/messages", "anthropic + astron-code-latest", "astron-code-latest"),
    ("https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic/v1/messages", "anthropic + claude-sonnet-4-20250514", "claude-sonnet-4-20250514"),
]

for url, label, model in endpoints:
    print(f"\n--- {label} ---")
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    body = json.dumps({
        "model": model,
        "max_tokens": 10,
        "messages": [{"role": "user", "content": "hi"}]
    }).encode()

    proxy = urllib.request.ProxyHandler({"https": "http://127.0.0.1:45626"})
    opener = urllib.request.build_opener(proxy)

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with opener.open(req, timeout=60) as resp:
            data = json.loads(resp.read())
            print(f"SUCCESS! Model: {data.get('model')}")
            for c in data.get('content', []):
                print(f"  Response: {c.get('text', '')}")
    except Exception as e:
        err_msg = str(e)
        print(f"Error: {err_msg[:200]}")
        if hasattr(e, 'read'):
            body_text = e.read().decode()[:300]
            print(f"Body: {body_text}")
