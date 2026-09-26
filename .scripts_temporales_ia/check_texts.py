import sys
import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.finditer(r'Diferencia de puntos', text, re.IGNORECASE)
for m in matches:
    start = m.start()
    sys.stdout.buffer.write(b"==== MATCH ====\n")
    sys.stdout.buffer.write(text[max(0, start-300):start+300].encode('utf-8'))
