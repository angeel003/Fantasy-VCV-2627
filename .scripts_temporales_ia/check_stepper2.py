import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = list(re.finditer(r'<div class="match-score-stepper">', text))
if not matches:
    matches = list(re.finditer(r'dif_\w+', text))
for m in matches:
    sys.stdout.buffer.write(text[max(0, m.start()-500):min(len(text), m.end()+1500)].encode('utf-8'))
    print('---')
