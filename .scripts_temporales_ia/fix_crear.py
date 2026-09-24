import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_func = """window.crearUsuarioAdmin = function(e) {
    e.preventDefault();
    const btn = e.target;
    const nu = document.getElementById('addUsrName').value.trim();
    const np = document.getElementById('addUsrPwd').value.trim();
    
    
    if(!nu || !np) { alert("Usuario y Contraseña son obligatorios"); return; }
    
    btn.disabled = true; btn.innerText = "Creando...";
    
    fetchSeguro(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'add_user', usuario: currentUser, password: currentPassword, new_u: nu, new_p: np, new_n: "" }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })"""

new_func = """window.crearUsuarioAdmin = function(e) {
    e.preventDefault();
    const btn = e.target;
    const nu = document.getElementById('addUsrName').value.trim();
    const np = document.getElementById('addUsrPwd').value.trim();
    
    
    if(!nu || !np) { alert("Usuario y Contraseña son obligatorios"); return; }
    
    // Obtener ligas seleccionadas
    const checkboxes = document.querySelectorAll('#adminLigasCheckboxes input[type="checkbox"]');
    const selectedLigas = [];
    checkboxes.forEach(cb => {
        if (cb.checked) selectedLigas.push(cb.value);
    });
    
    btn.disabled = true; btn.innerText = "Creando...";
    
    fetchSeguro(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'add_user', usuario: currentUser, password: currentPassword, new_u: nu, new_p: np, new_n: "", ligas_seleccionadas: selectedLigas }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })"""

# Loosen regex for matching just in case of whitespace/encoding diffs
import textwrap

idx = text.find('window.crearUsuarioAdmin = function(e) {')
end_idx = text.find('.then(res => res.json())', idx)

if idx != -1 and end_idx != -1:
    orig_chunk = text[idx:end_idx]
    
    # We just need to replace the JSON.stringify call and insert the checkbox logic
    # Find JSON.stringify
    json_idx = orig_chunk.find('JSON.stringify({')
    json_end_idx = orig_chunk.find('})', json_idx)
    
    if json_idx != -1 and json_end_idx != -1:
        inner_json = orig_chunk[json_idx:json_end_idx+2]
        new_inner = inner_json.replace('})', ', ligas_seleccionadas: selectedLigas })')
        
        # Now find the place to insert checkbox logic (before btn.disabled)
        btn_dis_idx = orig_chunk.find('btn.disabled = true;')
        
        checkbox_logic = """
    const checkboxes = document.querySelectorAll('#adminLigasCheckboxes input[type="checkbox"]');
    const selectedLigas = [];
    checkboxes.forEach(cb => {
        if (cb.checked) selectedLigas.push(cb.value);
    });
    
    """
        
        modified_chunk = orig_chunk[:btn_dis_idx] + checkbox_logic + orig_chunk[btn_dis_idx:json_idx] + new_inner + orig_chunk[json_end_idx+2:]
        
        text = text[:idx] + modified_chunk + text[end_idx:]
        
        with open('dev.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Updated window.crearUsuarioAdmin")
else:
    print("Not found.")

