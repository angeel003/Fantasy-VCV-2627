import sys
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('if (action === "save") {')
if idx != -1:
    sys.stdout.buffer.write(text[idx:idx+2500].encode('utf-8'))
