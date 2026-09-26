import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'function fetchSeguro.*?\}', text, re.DOTALL)
if match:
    sys.stdout.buffer.write(text[max(0, match.start()):min(len(text), match.end()+300)].encode('utf-8'))
