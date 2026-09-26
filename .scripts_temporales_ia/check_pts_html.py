import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = list(re.finditer(r'<div class="points-diff-container-v2">', text))
for m in matches:
    print('---')
    sys.stdout.buffer.write(text[max(0, m.start()-100):min(len(text), m.end()+2500)].encode('utf-8'))
