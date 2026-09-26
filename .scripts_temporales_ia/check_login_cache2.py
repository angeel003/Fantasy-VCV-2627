import sys
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
if 'cache.get("login_' in text or "cache.get('login_" in text:
    print('Found')
else:
    print('Not found')
