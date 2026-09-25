with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<nav.*?</nav>', text, flags=re.DOTALL)
for m in matches:
    print(m.encode('ascii', 'ignore').decode('ascii'))
