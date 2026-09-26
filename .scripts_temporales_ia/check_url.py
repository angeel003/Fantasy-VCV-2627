with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
import re
m = re.findall(r'https://script.google.com/macros/s/[a-zA-Z0-9_-]+/exec', text)
print(m)
