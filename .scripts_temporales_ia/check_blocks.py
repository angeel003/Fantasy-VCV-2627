import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'document\.getElementById\([^\)]+\)\.style\.display\s*=\s*"block"', text)
for x in m:
    print(x)
