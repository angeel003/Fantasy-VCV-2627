import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update guest fetch
old_guest_fetch = r"fetch\(scriptURL, \{ method: 'POST', body: JSON\.stringify\(\{ action: 'login_guest' \}\), headers: \{ 'Content-Type': 'text/plain;charset=utf-8' \} \}\)"
new_guest_fetch = r"""((() => { 
        if (window.mockFetchData) { 
            let d = window.mockFetchData; 
            window.mockFetchData = null; 
            return Promise.resolve({json: () => Promise.resolve(d)}); 
        } else { 
            return fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login_guest' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } }); 
        } 
    })())"""
html = re.sub(old_guest_fetch, new_guest_fetch, html)

# 2. Update user fetch
old_user_fetch = r"fetch\(scriptURL, \{ method: 'POST', body: JSON\.stringify\(\{ action: 'login', usuario: usr, password: pwd \}\), headers: \{ 'Content-Type': 'text/plain;charset=utf-8' \} \}\)"
new_user_fetch = r"""((() => { 
        if (window.mockFetchData) { 
            let d = window.mockFetchData; 
            window.mockFetchData = null; 
            return Promise.resolve({json: () => Promise.resolve(d)}); 
        } else { 
            return fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } }); 
        } 
    })())"""
html = re.sub(old_user_fetch, new_user_fetch, html)


# 3. Save to cache on guest success
old_guest_success = r"if\(data\.status === \"success\"\)\s*\{\s*isGuestMode = true;"
new_guest_success = """if(data.status === "success") {
            try {
                if (!window.isBackgroundRefresh) {
                    localStorage.setItem('vcv_cache_data', JSON.stringify(data));
                    localStorage.setItem('vcv_cache_type', 'guest');
                    localStorage.setItem('vcv_cache_creds', '{}');
                }
            } catch(e) { console.warn("Cache error", e); }
            isGuestMode = true;"""
html = re.sub(old_guest_success, new_guest_success, html)


# 4. Save to cache on user success
old_user_success = r"if\(data\.status === \"success\"\)\s*\{\s*currentUser = usr;\s*currentPassword = pwd;"
new_user_success = """if(data.status === "success") {
            try {
                if (!window.isBackgroundRefresh) {
                    localStorage.setItem('vcv_cache_data', JSON.stringify(data));
                    localStorage.setItem('vcv_cache_type', 'user');
                    localStorage.setItem('vcv_cache_creds', JSON.stringify({u: usr, p: pwd}));
                }
            } catch(e) { console.warn("Cache error", e); }
            currentUser = usr; currentPassword = pwd;"""
html = re.sub(old_user_success, new_user_success, html)


# 5. Inject DOMContentLoaded logic at the end
cache_logic = """
<script>
// LÓGICA DE CACHÉ V2 (STALE-WHILE-REVALIDATE - CORREGIDO)
document.addEventListener("DOMContentLoaded", function() {
    const cachedData = localStorage.getItem('vcv_cache_data');
    const cacheCreds = JSON.parse(localStorage.getItem('vcv_cache_creds') || '{}');
    const isGuestCache = localStorage.getItem('vcv_cache_type') === 'guest';
    
    if (cachedData) {
        try {
            const data = JSON.parse(cachedData);
            window.mockFetchData = data; // Set BEFORE click
            
            if (isGuestCache) {
                document.getElementById('btnGuest').click(); // Consumes mockFetchData instantly
                
                // Fetch in background to update
                setTimeout(() => {
                    fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login_guest' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
                    .then(r => r.json())
                    .then(d => {
                        if (d.status === "success" && isGuestMode) {
                            localStorage.setItem('vcv_cache_data', JSON.stringify(d));
                            window.isBackgroundRefresh = true;
                            window.mockFetchData = d;
                            document.getElementById('btnGuest').click();
                            window.isBackgroundRefresh = false;
                            mostrarToast("✅ Datos actualizados en 2º plano");
                        }
                    }).catch(e => console.warn(e));
                }, 1000); // Wait 1 second before doing background fetch just to be safe with UI rendering
                
            } else {
                document.getElementById('loginUsuario').value = cacheCreds.u || "";
                document.getElementById('loginPassword').value = cacheCreds.p || "";
                document.getElementById('btnLogin').click(); // Consumes mockFetchData instantly
                
                // Fetch in background to update
                setTimeout(() => {
                    fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login', usuario: cacheCreds.u, password: cacheCreds.p }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
                    .then(r => r.json())
                    .then(d => {
                        if (d.status === "success" && !isGuestMode && currentUser === cacheCreds.u) {
                            localStorage.setItem('vcv_cache_data', JSON.stringify(d));
                            window.isBackgroundRefresh = true;
                            window.mockFetchData = d;
                            document.getElementById('btnLogin').click();
                            window.isBackgroundRefresh = false;
                            mostrarToast("✅ Datos actualizados en 2º plano");
                        }
                    }).catch(e => console.warn(e));
                }, 1000);
            }
        } catch (e) {
            console.error("Cache parsing error", e);
            localStorage.removeItem('vcv_cache_data');
        }
    }
});
</script>
</body>"""

html = html.replace("</body>", cache_logic)

# 6. Clear cache on logout button (since arrow is visible for all now, this clears it safely)
old_logout = r"document\.getElementById\('btnLogout'\)\.addEventListener\('click', function\(\)\s*\{"
new_logout = """document.getElementById('btnLogout').addEventListener('click', function() {
    localStorage.removeItem('vcv_cache_data');
    localStorage.removeItem('vcv_cache_type');
    localStorage.removeItem('vcv_cache_creds');"""
html = re.sub(old_logout, new_logout, html)


with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

