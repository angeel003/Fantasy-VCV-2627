import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_admin = r"""if (now - ts < 48 * 60 * 60 * 1000) {
            html += `
            <div class="admin-match-box">
                <div style="font-weight:bold; margin-bottom:8px; color: #e65100;">${eq.equipo_local} vs ${eq.rival} <span style="color:#666; font-size:0.8rem; font-weight:normal;">(${eq.id_partido})</span></div>"""

new_admin = r"""if (now - ts < 48 * 60 * 60 * 1000) {
            let adminLocal = eq.es_local ? eq.equipo_local : eq.rival;
            let adminVisit = eq.es_local ? eq.rival : eq.equipo_local;
            html += `
            <div class="admin-match-box">
                <div style="font-weight:bold; margin-bottom:8px; color: #e65100;">${adminLocal} vs ${adminVisit} <span style="color:#666; font-size:0.8rem; font-weight:normal;">(${eq.id_partido})</span></div>"""

text = text.replace(old_admin, new_admin)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
    
print("Fixed admin loop")
