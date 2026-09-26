import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('¡Hola')
if idx != -1:
    idx_start = text.rfind('data.status === "success"', 0, idx)
    sys.stdout.buffer.write(text[max(0, idx_start):idx+200].encode('utf-8'))
