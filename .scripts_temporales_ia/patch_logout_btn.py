import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove old btnLogout
old_btn = r'\s*<div class="col-md-12 text-center" style="margin-top: 10px;">\s*<button id="btnLogout".*?Sal.*?r / Volver at.*?s</button>\s*</div>'
html = re.sub(old_btn, '', html)

# 2. Insert new btnLogout in header
old_header = r'(<header>\s*<div class="header-content">)'
new_header = r'<header>\n    <button id="btnLogout" style="display:none; position:absolute; left:15px; top:18px; background:transparent; border:none; color:white; font-size:1.4rem; cursor:pointer; padding:0; outline:none; text-shadow:1px 1px 2px rgba(0,0,0,0.5);" title="Cerrar sesión / Volver atrás">⬅️</button>\n    <div class="header-content">'

if re.search(old_header, html):
    html = re.sub(old_header, new_header, html)
    print("Injected new btnLogout in header successfully.")
else:
    print("Could not find header.")

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

