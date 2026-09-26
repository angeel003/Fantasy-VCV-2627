import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = list(re.finditer(r'<div class="stepper-value-v2">', text))
if matches:
    m = matches[0]
    sys.stdout.buffer.write(text[max(0, m.start()-500):min(len(text), m.end()+1000)].encode('utf-8'))
