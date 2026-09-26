import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'<h2 id="tituloPrincipalSeccion">.*?esta jornada\.</p>', text, re.DOTALL)
if match:
    sys.stdout.buffer.write(match.group(0).encode('utf-8'))
