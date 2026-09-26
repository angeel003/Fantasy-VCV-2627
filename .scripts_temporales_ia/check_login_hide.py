with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find all occurrences of loginSection display none
matches = re.finditer(r'loginSection.*?none', text)
for m in matches:
    print(text[max(0, m.start()-50):m.end()+50])
