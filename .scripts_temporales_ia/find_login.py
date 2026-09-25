with open('prototipo_stitch.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'login', text, re.IGNORECASE)
for m in matches:
    print(text[max(0, m.start()-50):m.end()+100])
