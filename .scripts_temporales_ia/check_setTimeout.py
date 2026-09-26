import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = [m.start() for m in re.finditer(r'setTimeout\(\(\) => \{\s*fetchSeguro', text, re.DOTALL)]
for pos in matches:
    print('='*20)
    sys.stdout.buffer.write(text[max(0, pos-100):min(len(text), pos+600)].encode('utf-8'))
