import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = list(re.finditer(r'<meta name="viewport".*?>', text))
for m in matches:
    sys.stdout.buffer.write(text[m.start():m.end()].encode('utf-8'))
