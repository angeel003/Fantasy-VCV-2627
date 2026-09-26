import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'<h2 id="tituloPrincipalSeccion">.*?</h2>', text)
if match:
    sys.stdout.buffer.write(text[match.start():match.end()+500].encode('utf-8'))
