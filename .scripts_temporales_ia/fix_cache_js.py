import re

def fix_html(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
        
    js_code = """
document.getElementById('btnForceSyncExcel').addEventListener('click', function(e) {
    e.preventDefault();
    const btn = this;
    const originalText = btn.innerHTML;
    btn.innerHTML = '⏳ Borrando Caché...';
    btn.disabled = true;
    
    fetchSeguro(scriptURL, {
        method: 'POST',
        body: JSON.stringify({ action: 'clear_cache', usuario: currentUser, password: currentPassword }),
        headers: { 'Content-Type': 'text/plain;charset=utf-8' }
    })
    .then(r => r.json())
    .then(data => {
        if(data.status === 'success') {
            btn.innerHTML = '✅ ¡Actualizado!';
            setTimeout(() => {
                window.location.href = window.location.pathname + '?v=' + new Date().getTime();
            }, 1000);
        } else {
            btn.innerHTML = originalText;
            btn.disabled = false;
            alert('Error: ' + data.message);
        }
    })
    .catch(err => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        alert('Error de conexión.');
    });
});
"""

    if "Borrando Caché" not in html:
        # Append before the last </script>
        last_script_idx = html.rfind('</script>')
        if last_script_idx != -1:
            html = html[:last_script_idx] + js_code + "\n" + html[last_script_idx:]
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Fixed JS in {filename}")

fix_html('dev.html')
fix_html('index.html')

