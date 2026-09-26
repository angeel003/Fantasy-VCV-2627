import sys
import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.findall(r'[^\n]*htmlReloj[^\n]*', text)
for m in matches:
    sys.stdout.buffer.write(m.strip().encode('utf-8') + b'\n')
