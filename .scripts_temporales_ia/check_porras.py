import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('porrasEq.forEach(porra => {')
if idx != -1:
    sys.stdout.buffer.write(text[idx:idx+1000].encode('utf-8'))
