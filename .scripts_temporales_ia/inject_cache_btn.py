import re

def update_html(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add the button in the admin panel
    # Find btnAdminSync
    old_buttons = '<button id="btnAdminSync" class="btn btn-warning" style="flex:1; font-weight:bold;">🤖 Auto-Permisos</button>\n                            <a href="https://docs.google.com/spreadsheets/" target="_blank" class="btn btn-light" style="flex:1; font-weight:bold; border: 1px solid #ccc;">📊 Abrir Excel</a>'
    
    # We will use regex to be safe about spacing and emojis
    btn_pattern = r'(<button id="btnAdminSync".*?</button>)\s*(<a href="https://docs\.google\.com/spreadsheets/".*?</a>)'
    
    match = re.search(btn_pattern, html)
    if match:
        new_buttons = f"""{match.group(1)}
                            <button id="btnForceSyncExcel" class="btn btn-info" style="flex:1; font-weight:bold; color:white;">🔄 Forzar Caché</button>
                            {match.group(2)}"""
        html = html.replace(match.group(0), new_buttons)

    # 2. Add the JS event listener
    js_code = """
document.getElementById('btnForceSyncExcel').addEventListener('click', function(e) {
    e.preventDefault();
    const btn = this;
    btn.innerHTML = '⏳ Sincronizando...';
    btn.disabled = true;
    
    fetchSeguro(scriptURL, {
        method: 'POST',
        body: JSON.stringify({ action: 'clear_cache', usuario: currentUser, password: currentPassword }),
        headers: { 'Content-Type': 'text/plain;charset=utf-8' }
    })
    .then(r => r.json())
    .then(data => {
        btn.innerHTML = '🔄 Forzar Caché';
        btn.disabled = false;
        if(data.status === 'success') {
            Swal.fire('¡Caché Borrada!', data.message, 'success').then(() => {
                window.location.href = window.location.pathname + '?v=' + new Date().getTime();
            });
        } else {
            Swal.fire('Error', data.message || 'Error desconocido', 'error');
        }
    })
    .catch(err => {
        btn.innerHTML = '🔄 Forzar Caché';
        btn.disabled = false;
        Swal.fire('Error', 'No se pudo conectar con el servidor', 'error');
    });
});
"""
    # Insert js_code before "// Iniciar App"
    if "btnForceSyncExcel" not in html and js_code.strip() not in html:
        html = html.replace("// Iniciar App", js_code + "\n// Iniciar App")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"Updated {filename}")

update_html('dev.html')
update_html('index.html')

