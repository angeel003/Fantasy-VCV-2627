import re

old_fetch_seguro = """const fetchSeguro = (url, options, retries = 1) => {
    return fetch(url, options)"""
new_fetch_seguro = """const fetchSeguro = (url, options, retries = 1) => {
    const bustUrl = url + (url.includes('?') ? '&' : '?') + 't=' + new Date().getTime();
    return fetch(bustUrl, options)"""

old_btn_reload = """document.getElementById('btnReload').addEventListener('click', function() {
    localStorage.removeItem('vcv_cache_data');
    localStorage.removeItem('vcv_cache_type');
    window.location.reload();
});"""
new_btn_reload = """document.getElementById('btnReload').addEventListener('click', function() {
    localStorage.removeItem('vcv_cache_data');
    localStorage.removeItem('vcv_cache_type');
    window.location.href = window.location.pathname + '?v=' + new Date().getTime();
});"""

old_btn_logout = """setTimeout(() => {
        window.location.reload();
    }, 280);"""
new_btn_logout = """setTimeout(() => {
        window.location.href = window.location.pathname + '?v=' + new Date().getTime();
    }, 280);"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace(old_fetch_seguro, new_fetch_seguro)
    html = html.replace(old_btn_reload, new_btn_reload)
    html = html.replace(old_btn_logout, new_btn_logout)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

