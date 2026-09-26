import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = list(re.finditer(r'class="points-controls-row-v2"', text))
for m in matches:
    print('---')
    sys.stdout.buffer.write(text[m.start():m.start()+1500].encode('utf-8'))
