import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = list(re.finditer(r'stepper-btn', text))
if matches:
    m = matches[0]
    sys.stdout.buffer.write(text[max(0, m.start()-200):min(len(text), m.end()+500)].encode('utf-8'))
