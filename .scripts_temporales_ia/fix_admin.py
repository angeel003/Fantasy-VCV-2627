import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the admin panel rendering to use localTeamName vs visitTeamName
old_admin = r"""<div style="font-weight:bold; margin-bottom:8px; color: #e65100;">${eq.equipo_local} vs ${eq.rival} <span style="color:#666; font-size:0.8rem; font-weight:normal;">(${eq.id_partido})</span></div>"""

new_admin = r"""<div style="font-weight:bold; margin-bottom:8px; color: #e65100;">${localTeamName} vs ${visitTeamName} <span style="color:#666; font-size:0.8rem; font-weight:normal;">(${eq.id_partido})</span></div>"""

text = text.replace(old_admin, new_admin)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Admin panel fixed!")
