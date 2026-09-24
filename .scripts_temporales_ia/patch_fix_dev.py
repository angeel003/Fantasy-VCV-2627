import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Revert all fetch lines back to the clean, original version
html = re.sub(r"fetch\(scriptURL \+ '\?t=' \+ new Date\(\)\.getTime\(\), \{ credentials: 'omit', ", "fetch(scriptURL, { ", html)

# 2. Fix the syntax error (\'btnLogout\') and restore the removed load fetch for guest just in case they wanted exactly the official code
# Wait, the official code for Guest has cargarDatosAntiguos(); We'll leave it as is or fix it.
# Actually, the user said "como estuvieran en ese codigo" so I'll just restore the guest login flow.
html = html.replace(
    r'document.getElementById(\'btnLogout\').style.display = "block";\n            iniciarRelojTotales();',
    r'document.getElementById("btnLogout").style.display = "block";\n            cargarDatosAntiguos();\n            iniciarRelojTotales();'
)

# 3. Modify btnLogout so it simply reloads the page
logout_original = """document.getElementById('btnLogout').addEventListener('click', function() {
    localStorage.removeItem('vcv_cache_data');
    localStorage.removeItem('vcv_cache_type');
    localStorage.removeItem('vcv_cache_creds');
    currentUser = null;
    currentPassword = null;
    isGuestMode = false;
    document.getElementById('loginUsuario').value = '';
    document.getElementById('loginPassword').value = '';
    document.getElementById('appSection').style.display = 'none';
    document.getElementById('btnReload').style.display = 'none';
    document.getElementById('btnLogout').style.display = 'none';
    document.getElementById('loginMessage').style.display = 'none';
    document.getElementById('loginSection').style.display = 'flex';
});"""

logout_new = """document.getElementById('btnLogout').addEventListener('click', function() {
    localStorage.removeItem('vcv_cache_data');
    localStorage.removeItem('vcv_cache_type');
    localStorage.removeItem('vcv_cache_creds');
    window.location.reload();
});"""

# Because there might be spacing issues, let's use regex for btnLogout
html = re.sub(
    r"document\.getElementById\('btnLogout'\)\.addEventListener\('click', function\(\) \{.*?\n\}\);",
    logout_new,
    html, flags=re.DOTALL
)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

