import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove cache script at the bottom
html = re.sub(r'<script>\s*// LÓGICA DE CACHÉ.*?// We can just patch the success blocks to save to localStorage\.\s*</script>', '', html, flags=re.DOTALL)

# 2. Revert the ternary fetch expressions
# guest:
html = html.replace(
    r"(window.mockFetchData ? Promise.resolve({json: () => Promise.resolve(window.mockFetchData)}) : fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login_guest' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } }))",
    r"fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login_guest' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })"
)

# user:
html = html.replace(
    r"(window.mockFetchData ? Promise.resolve({json: () => Promise.resolve(window.mockFetchData)}) : fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } }))",
    r"fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })"
)

# 3. Remove localStorage saves in guest success
guest_save_block = r"""try \{
                if \(!window\.mockFetchData\) \{
                    localStorage\.setItem\('vcv_cache_data', JSON\.stringify\(data\)\);
                    localStorage\.setItem\('vcv_cache_type', 'guest'\);
                    localStorage\.setItem\('vcv_cache_creds', '\{\}'\);
                \}
            \} catch \(e\) \{ console\.warn\("LocalStorage error", e\); \}"""
html = re.sub(guest_save_block, '', html)

# 4. Remove localStorage saves in user success
user_save_block = r"""try \{
                if \(!window\.mockFetchData\) \{
                    localStorage\.setItem\('vcv_cache_data', JSON\.stringify\(data\)\);
                    localStorage\.setItem\('vcv_cache_type', 'user'\);
                    localStorage\.setItem\('vcv_cache_creds', JSON\.stringify\(\{u: usr, p: pwd\}\)\);
                \}
            \} catch \(e\) \{ console\.warn\("LocalStorage error", e\); \}"""
html = re.sub(user_save_block, '', html)

# 5. Restore the back arrow for all users
# Guests
guest_logout = r"document\.getElementById\('btnLogout'\)\.style\.display = \"block\";"
# Users
# In the original, I had it around line 1230:
user_logout = r"document\.getElementById\('btnReload'\)\.style\.display = \"flex\"; \n            document\.getElementById\('btnLogoutText'\)\.style\.display = \"inline-block\";"
new_user_logout = """document.getElementById('btnReload').style.display = "flex";
            document.getElementById('btnLogout').style.display = "block";"""
html = re.sub(user_logout, new_user_logout, html)

# 6. Remove the tiny text link completely
html = re.sub(r'<div class="col-md-12 text-center" style="margin-top: 5px;">\s*<a href="#" id="btnLogoutText".*?</a>\s*</div>', '', html)

# Cleanup any remaining references to btnLogoutText
html = re.sub(r"document\.getElementById\('btnLogoutText'\)\.style\.display = .*?;\s*", '', html)
html = re.sub(r"document\.getElementById\('btnLogoutText'\)\.addEventListener\('click', function\(e\) \{[\s\S]*?\}\);\s*", '', html)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

