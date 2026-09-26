import sys
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if '"login"' in l or "'login'" in l:
        print(f'{i}: {l.strip()}')
