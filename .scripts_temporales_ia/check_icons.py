import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.findall(r'data-lucide="([^"]+)"', text)
from collections import Counter
for k, v in Counter(m).items(): print(k, v)
