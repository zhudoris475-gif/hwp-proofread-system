import json

with open(r'C:\Users\doris\.claude\settings.json', 'r', encoding='utf-8') as f:
    s = json.load(f)

env = s.get('env', {})
has_api_key = 'ANTHROPIC_API_KEY' in env
has_auth_token = 'ANTHROPIC_AUTH_TOKEN' in env

api_key_status = "EXISTS - WARNING" if has_api_key else "REMOVED - OK"
auth_token_status = "EXISTS" if has_auth_token else "MISSING"

print(f"ANTHROPIC_API_KEY:     {api_key_status}")
print(f"ANTHROPIC_AUTH_TOKEN:  {auth_token_status}")

if not has_api_key and has_auth_token:
    print("CONFLICT RESOLVED: Only ANTHROPIC_AUTH_TOKEN is set")
elif has_api_key and has_auth_token:
    print("CONFLICT STILL EXISTS: Both keys are set!")
else:
    print("Check needed")
