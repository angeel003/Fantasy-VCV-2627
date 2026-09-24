import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the input for frase
html = re.sub(
    r'<input type="text" id="adm_frase_\$\{eq\.id_partido\}".*?>',
    '',
    html
)

# Remove the const elFrase and const frase and frase parameter from fetch
html = html.replace('const elFrase = document.getElementById(`adm_frase_${idPart}`);', '')
html = html.replace('const frase = elFrase ? elFrase.value.trim() : "";', '')
html = html.replace(', frase: frase }', ' }')

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

