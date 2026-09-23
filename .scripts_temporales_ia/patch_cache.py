import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# For guest
guest_fetch = r"fetch\(scriptURL, \{ method: 'POST', body: JSON\.stringify\(\{ action: 'login_guest' \}\), headers: \{ 'Content-Type': 'text/plain;charset=utf-8' \} \}\)"
new_guest_fetch = r"(window.mockFetchData ? Promise.resolve({json: () => Promise.resolve(window.mockFetchData)}) : fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login_guest' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } }))"
html = re.sub(guest_fetch, new_guest_fetch, html)

# For user
user_fetch = r"fetch\(scriptURL, \{ method: 'POST', body: JSON\.stringify\(\{ action: 'login', usuario: usr, password: pwd \}\), headers: \{ 'Content-Type': 'text/plain;charset=utf-8' \} \}\)"
new_user_fetch = r"(window.mockFetchData ? Promise.resolve({json: () => Promise.resolve(window.mockFetchData)}) : fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } }))"
html = re.sub(user_fetch, new_user_fetch, html)

# Inject the caching logic at the end of the body
cache_logic = """
<script>
// LÓGICA DE CACHÉ (STALE-WHILE-REVALIDATE)
document.addEventListener("DOMContentLoaded", function() {
    const cachedData = localStorage.getItem('vcv_cache_data');
    const cacheCreds = JSON.parse(localStorage.getItem('vcv_cache_creds') || '{}');
    const isGuestCache = localStorage.getItem('vcv_cache_type') === 'guest';
    
    if (cachedData) {
        try {
            const data = JSON.parse(cachedData);
            window.mockFetchData = data;
            
            if (isGuestCache) {
                document.getElementById('btnGuest').click();
                window.mockFetchData = null;
                
                // Background update
                setTimeout(() => {
                    fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login_guest' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
                    .then(r => r.json())
                    .then(d => {
                        if (d.status === "success" && isGuestMode) {
                            localStorage.setItem('vcv_cache_data', JSON.stringify(d));
                            window.mockFetchData = d;
                            document.getElementById('btnGuest').click();
                            window.mockFetchData = null;
                            mostrarToast("✅ Datos actualizados en 2º plano");
                        }
                    }).catch(e => console.error("Cache update failed:", e));
                }, 500);
            } else {
                document.getElementById('loginUsuario').value = cacheCreds.u || "";
                document.getElementById('loginPassword').value = cacheCreds.p || "";
                document.getElementById('btnLogin').click();
                window.mockFetchData = null;
                
                // Background update
                setTimeout(() => {
                    fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login', usuario: cacheCreds.u, password: cacheCreds.p }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
                    .then(r => r.json())
                    .then(d => {
                        if (d.status === "success" && !isGuestMode && currentUser === cacheCreds.u) {
                            localStorage.setItem('vcv_cache_data', JSON.stringify(d));
                            window.mockFetchData = d;
                            document.getElementById('btnLogin').click();
                            window.mockFetchData = null;
                            mostrarToast("✅ Datos actualizados en 2º plano");
                        }
                    }).catch(e => console.error("Cache update failed:", e));
                }, 500);
            }
        } catch (e) {
            console.error("Error reading cache", e);
            localStorage.removeItem('vcv_cache_data');
        }
    }
});

// Guardar en caché al hacer login real
const originalBtnLogin = document.getElementById('btnLogin').onclick; // (it's addeventlistener though)
// We can just patch the success blocks to save to localStorage.
</script>
</body>"""

html = html.replace("</body>", cache_logic)

# Save to cache on login_guest success
old_guest_success = r"if\(data\.status === \"success\"\)\s*\{\s*isGuestMode = true;"
new_guest_success = """if(data.status === "success") {
            if (!window.mockFetchData) {
                localStorage.setItem('vcv_cache_data', JSON.stringify(data));
                localStorage.setItem('vcv_cache_type', 'guest');
                localStorage.setItem('vcv_cache_creds', '{}');
            }
            isGuestMode = true;"""
html = re.sub(old_guest_success, new_guest_success, html)

# Save to cache on login success
old_login_success = r"if\(data\.status === \"success\"\)\s*\{\s*currentUser = usr;\s*currentPassword = pwd;"
new_login_success = """if(data.status === "success") {
            if (!window.mockFetchData) {
                localStorage.setItem('vcv_cache_data', JSON.stringify(data));
                localStorage.setItem('vcv_cache_type', 'user');
                localStorage.setItem('vcv_cache_creds', JSON.stringify({u: usr, p: pwd}));
            }
            currentUser = usr; currentPassword = pwd;"""
html = re.sub(old_login_success, new_login_success, html)

# Clear cache on logout
old_logout = r"document\.getElementById\('btnLogout'\)\.addEventListener\('click', function\(\)\s*\{"
new_logout = """document.getElementById('btnLogout').addEventListener('click', function() {
    localStorage.removeItem('vcv_cache_data');
    localStorage.removeItem('vcv_cache_type');
    localStorage.removeItem('vcv_cache_creds');"""
html = re.sub(old_logout, new_logout, html)

# Logout button logic: show ONLY if guest mode
# Look for document.getElementById('btnLogout').style.display = "block";
# and change it to document.getElementById('btnLogout').style.display = isGuestMode ? "block" : "none";
html = re.sub(r"document\.getElementById\('btnLogout'\)\.style\.display = \"block\";", r"document.getElementById('btnLogout').style.display = isGuestMode ? \"block\" : \"none\";", html)


with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

