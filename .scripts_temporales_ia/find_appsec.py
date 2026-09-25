with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'appSection', text)
for m in matches:
    idx = m.start()
    print("Match at", idx, ":")
    print(text[idx-50:idx+200])
