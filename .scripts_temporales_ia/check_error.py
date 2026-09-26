import sys, re
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
matches = list(re.finditer(r'"error"', text))
for m in matches:
    print('---')
    sys.stdout.buffer.write(text[max(0, m.start()-150):min(len(text), m.end()+150)].encode('utf-8'))
