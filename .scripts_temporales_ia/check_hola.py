import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('¡Hola')
if idx != -1:
    sys.stdout.buffer.write(text[idx-200:idx+300].encode('utf-8'))
