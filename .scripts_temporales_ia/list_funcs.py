with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
funcs = re.findall(r'function [^{]+\{', text)
print("Functions:", [f for f in funcs if 'Seccion' in f or 'Tab' in f])
