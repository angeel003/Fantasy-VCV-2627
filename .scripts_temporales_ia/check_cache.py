import sys, re
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'var cached = cache\.get\("login_" \+ usuario\);', text)
if match:
    start = max(0, match.start() - 200)
    end = min(len(text), match.end() + 1000)
    sys.stdout.buffer.write(text[start:end].encode('utf-8'))
