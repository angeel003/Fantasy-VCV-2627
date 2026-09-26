import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'<div style="background: var\(--bg-card\).*?Ejemplo de reparto.*?</div></p>', text, re.DOTALL)
if match:
    with open('.scripts_temporales_ia/match.txt', 'wb') as out:
        out.write(match.group(0).encode('utf-8'))
    print("Found and saved")
