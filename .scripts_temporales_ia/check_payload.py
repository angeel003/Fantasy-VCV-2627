with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
import re
m = re.search(r'"reglas": \{[^\}]+\}', text)
if m: print(m.group(0))
