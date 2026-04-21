import urllib.request, json

NEW_KEY = "80ca081f1860c42aaf03e5689adca8ad:NjU1OWNiYWEwYjQyZDllYTQzZjc3ZmZl"
OLD_KEY = "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi"
URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic/v1/messages"

models = [
    "astron-code-latest",
    "claude-sonnet-4-20250514",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "claude-haiku-4-5-20251001",
]

for key_label, api_key in [("NEW KEY", NEW_KEY), ("OLD KEY", OLD_KEY)]:
    print(f"\n{'='*60}")
    print(f"Testing with {key_label}")
    print(f"{'='*60}")
    for model in models:
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        body = json.dumps({
            "model": model,
            "max_tokens": 5,
            "messages": [{"role": "user", "content": "hi"}]
        }).encode()

        proxy = urllib.request.ProxyHandler({"https": "http://127.0.0.1:45626"})
        opener = urllib.request.build_opener(proxy)
        req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
        try:
            with opener.open(req, timeout=30) as resp:
                data = json.loads(resp.read())
                print(f"  OK: {model} -> {data.get('content', [{}])[0].get('text', '')[:30]}")
        except Exception as e:
            err = str(e)[:120]
            if hasattr(e, 'read'):
                try:
                    err_body = json.loads(e.read().decode())
                    code = err_body.get('error', {}).get('code', '')
                    msg = err_body.get('error', {}).get('message', '')[:80]
                    print(f"  FAIL: {model} (code={code}) {msg}")
                except:
                    print(f"  FAIL: {model} {err}")
            else:
                print(f"  FAIL: {model} {err}")
