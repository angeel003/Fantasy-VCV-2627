with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'eq\.equipo_local', text)
for m in matches:
    idx = m.start()
    print(text[idx-100:idx+200].encode('ascii', 'ignore').decode('ascii'))
