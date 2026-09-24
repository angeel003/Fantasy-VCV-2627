import re

files = ['dev.html', 'index.html']

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # The previous patch changed uniqueCats to window.appData.equipos_totales || [];
    old_js = 'let uniqueCats = window.appData.equipos_totales || [];'
    new_js = 'let uniqueCats = window.appData.mis_equipos_siguiendo || [];'

    if old_js in html:
        html = html.replace(old_js, new_js)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filename} for team names dropdown!")
    else:
        print(f"Token not found in {filename}!")

