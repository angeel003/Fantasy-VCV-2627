import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'let currentUser = "";', text)
if match:
    start = max(0, match.start() - 200)
    end = min(len(text), match.end() + 200)
    sys.stdout.buffer.write(text[start:end].encode('utf-8'))
