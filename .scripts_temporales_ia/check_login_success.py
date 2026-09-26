import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'data\.status === [\'"]success[\'"]\) {', text)
if match:
    sys.stdout.buffer.write(text[max(0, match.start()-200):min(len(text), match.end()+200)].encode('utf-8'))
