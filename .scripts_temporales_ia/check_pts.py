import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'let [^\n]*puntos[^\n]*\n.*?</button>', text, re.DOTALL)
if match:
    with open('.scripts_temporales_ia/check_pts.txt', 'wb') as out:
        out.write(match.group(0).encode('utf-8'))
