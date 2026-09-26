import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = list(re.finditer(r'type="number"', text))
for m in matches[:3]:
    print('---')
    sys.stdout.buffer.write(text[max(0, m.start()-100):min(len(text), m.end()+150)].encode('utf-8'))
