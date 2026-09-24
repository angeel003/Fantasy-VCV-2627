import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# Sets dropdown
html = html.replace('<option value="3-0">Victoria 3-0</option>', '<option value="3-0">${eq.es_derby ? "Gana " + eq.equipo_local + " 3-0" : "Victoria 3-0"}</option>')
html = html.replace('<option value="3-1">Victoria 3-1</option>', '<option value="3-1">${eq.es_derby ? "Gana " + eq.equipo_local + " 3-1" : "Victoria 3-1"}</option>')
html = html.replace('<option value="3-2">Victoria 3-2</option>', '<option value="3-2">${eq.es_derby ? "Gana " + eq.equipo_local + " 3-2" : "Victoria 3-2"}</option>')
html = html.replace('<option value="2-3">Derrota 2-3</option>', '<option value="2-3">${eq.es_derby ? "Gana " + eq.rival + " 3-2" : "Derrota 2-3"}</option>')
html = html.replace('<option value="1-3">Derrota 1-3</option>', '<option value="1-3">${eq.es_derby ? "Gana " + eq.rival + " 3-1" : "Derrota 1-3"}</option>')
html = html.replace('<option value="0-3">Derrota 0-3</option>', '<option value="0-3">${eq.es_derby ? "Gana " + eq.rival + " 3-0" : "Derrota 0-3"}</option>')

# Signo dropdown
html = html.replace('<option value="A favor">A favor (+)</option>', '<option value="A favor">${eq.es_derby ? "A favor de " + eq.equipo_local : "A favor (+)"}</option>')
html = html.replace('<option value="En contra">En contra (-)</option>', '<option value="En contra">${eq.es_derby ? "A favor de " + eq.rival : "En contra (-)"}</option>')

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
print("Patched incrementally!")

