import urllib.request, json, ssl

url = "http://127.0.0.1:15721/v1/messages"
headers = {
    "x-api-key": "701c8e66e6515b955f6f8c9cad375d94:Y2E0YjYwODg1NWExNDNjMThiODJkMzZi",
    "anthropic-version": "2023-06-01",
    "Content-Type": "application/json"
}
body = json.dumps({
    "model": "astron-code-latest",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "hi"}]
}).encode()

req = urllib.request.Request(url, data=body, headers=headers, method="POST")
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
        print("SUCCESS!")
        print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'read'):
        print(f"Body: {e.read().decode()}")
