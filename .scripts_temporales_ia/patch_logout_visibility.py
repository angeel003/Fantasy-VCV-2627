import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add small text link for normal users to logout
old_badges = r'<div id="displayBadges" style="display:flex; flex-direction:row; flex-wrap:wrap; justify-content:center; align-items:center; gap:6px;"></div>\n                </div>'
new_badges = """<div id="displayBadges" style="display:flex; flex-direction:row; flex-wrap:wrap; justify-content:center; align-items:center; gap:6px;"></div>
                </div>
                <div class="col-md-12 text-center" style="margin-top: 5px;">
                    <a href="#" id="btnLogoutText" style="font-size: 0.8rem; color: #888; text-decoration: underline; cursor: pointer; display: none;">Cerrar sesión</a>
                </div>"""

html = re.sub(old_badges, new_badges, html)

# Add event listener for btnLogoutText
logout_text_logic = """document.getElementById('btnLogoutText').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('btnLogout').click();
});
"""

# inject right before logic for btnLogout
html = html.replace("document.getElementById('btnLogout').addEventListener('click'", logout_text_logic + "document.getElementById('btnLogout').addEventListener('click'")

# Show btnLogoutText only for logged-in users
# find the section where btnReload is shown for users (around 1223)
user_show = r'document\.getElementById\(\'btnReload\'\)\.style\.display = "flex";\s*cargarDatosAntiguos\(\);'
new_user_show = """document.getElementById('btnReload').style.display = "flex"; 
            document.getElementById('btnLogoutText').style.display = "inline-block";
            cargarDatosAntiguos();"""
html = re.sub(user_show, new_user_show, html)

# Hide it when logging out
old_hide = r"document\.getElementById\('btnLogout'\)\.style\.display = 'none';"
new_hide = "document.getElementById('btnLogout').style.display = 'none';\n    document.getElementById('btnLogoutText').style.display = 'none';"
html = re.sub(old_hide, new_hide, html)

# Hide it for guests
guest_show = r"document\.getElementById\('btnLogout'\)\.style\.display = isGuestMode \? \"block\" : \"none\";"
new_guest_show = """document.getElementById('btnLogout').style.display = "block";
            document.getElementById('btnLogoutText').style.display = "none";"""
html = html.replace('document.getElementById(\'btnLogout\').style.display = isGuestMode ? "block" : "none";', new_guest_show)

# Change arrow appearance
old_arrow = r'<button id="btnLogout" style="display:none; position:absolute; left:15px; top:18px; background:transparent; border:none; color:white; font-size:1.4rem; cursor:pointer; padding:0; outline:none; text-shadow:1px 1px 2px rgba\(0,0,0,0\.5\);" title="Cerrar sesión / Volver atrás">⬅️</button>'
new_arrow = r'<button id="btnLogout" style="display:none; position:absolute; left:15px; top:15px; background:transparent; border:none; color:rgba(255,255,255,0.7); font-size:1.5rem; cursor:pointer; padding:0; outline:none; text-shadow:none;" title="Volver atrás">&#10094;</button>'
html = re.sub(old_arrow, new_arrow, html)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

