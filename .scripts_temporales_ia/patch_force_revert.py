import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove cache script at the bottom
html = re.sub(r'<script>\s*// LÓGICA DE CACHÉ V2.*?// We can just patch the success blocks to save to localStorage\.\s*</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script>\s*// LÓGICA DE CACHÉ.*?// We can just patch the success blocks to save to localStorage\.\s*</script>', '', html, flags=re.DOTALL)

# 2. Revert the IIFE fetch expressions
# guest:
guest_regex = r"\(\(\(\) => \{[\s\S]*?login_guest[\s\S]*?\}\)\(\)\)"
html = re.sub(guest_regex, r"fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login_guest' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })", html)

# user:
user_regex = r"\(\(\(\) => \{[\s\S]*?action: 'login'[\s\S]*?\}\)\(\)\)"
html = re.sub(user_regex, r"fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })", html)


# 3. Remove localStorage saves in guest success (both V1 and V2)
guest_save_block = r"try \{\s*if \(!window\.isBackgroundRefresh\) \{\s*localStorage\.setItem\('vcv_cache_data'[\s\S]*?\} catch\(e\) \{ console\.warn\(\"Cache error\", e\); \}"
html = re.sub(guest_save_block, '', html)

# 4. Remove localStorage saves in user success
user_save_block = r"try \{\s*if \(!window\.isBackgroundRefresh\) \{\s*localStorage\.setItem\('vcv_cache_data'[\s\S]*?\} catch\(e\) \{ console\.warn\(\"Cache error\", e\); \}"
html = re.sub(user_save_block, '', html)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

