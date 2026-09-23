import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# For guest
guest_setItem = r"""if \(!window\.mockFetchData\) \{
                localStorage\.setItem\('vcv_cache_data', JSON\.stringify\(data\)\);
                localStorage\.setItem\('vcv_cache_type', 'guest'\);
                localStorage\.setItem\('vcv_cache_creds', '\{\}'\);
            \}"""
safe_guest_setItem = """try {
                if (!window.mockFetchData) {
                    localStorage.setItem('vcv_cache_data', JSON.stringify(data));
                    localStorage.setItem('vcv_cache_type', 'guest');
                    localStorage.setItem('vcv_cache_creds', '{}');
                }
            } catch (e) { console.warn("LocalStorage error", e); }"""
html = html.replace("""if (!window.mockFetchData) {
                localStorage.setItem('vcv_cache_data', JSON.stringify(data));
                localStorage.setItem('vcv_cache_type', 'guest');
                localStorage.setItem('vcv_cache_creds', '{}');
            }""", safe_guest_setItem)

# For user
user_setItem = r"""if \(!window\.mockFetchData\) \{
                localStorage\.setItem\('vcv_cache_data', JSON\.stringify\(data\)\);
                localStorage\.setItem\('vcv_cache_type', 'user'\);
                localStorage\.setItem\('vcv_cache_creds', JSON\.stringify\(\{u: usr, p: pwd\}\)\);
            \}"""
safe_user_setItem = """try {
                if (!window.mockFetchData) {
                    localStorage.setItem('vcv_cache_data', JSON.stringify(data));
                    localStorage.setItem('vcv_cache_type', 'user');
                    localStorage.setItem('vcv_cache_creds', JSON.stringify({u: usr, p: pwd}));
                }
            } catch (e) { console.warn("LocalStorage error", e); }"""
html = html.replace("""if (!window.mockFetchData) {
                localStorage.setItem('vcv_cache_data', JSON.stringify(data));
                localStorage.setItem('vcv_cache_type', 'user');
                localStorage.setItem('vcv_cache_creds', JSON.stringify({u: usr, p: pwd}));
            }""", safe_user_setItem)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

