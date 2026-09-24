import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update HTML
old_html = """                            <input type="password" id="addUsrPwd" class="form-control form-control-sm mb-2" placeholder="Contraseña">
                            
                            <button class="btn btn-sm btn-success btn-block\""""
new_html = """                            <input type="password" id="addUsrPwd" class="form-control form-control-sm mb-2" placeholder="Contraseña">
                            
                            <div style="margin-bottom: 10px; text-align: left; font-size: 0.9rem;">
                                <strong>Añadir a Ligas:</strong>
                                <div id="adminLigasCheckboxes" style="display: flex; flex-direction: column; gap: 3px; max-height: 100px; overflow-y: auto; background: white; padding: 5px; border-radius: 4px; border: 1px solid #ccc; margin-top: 5px;">
                                    <!-- Populated by JS -->
                                </div>
                            </div>

                            <button class="btn btn-sm btn-success btn-block\""""

# Handle encoding differences slightly by using a looser regex
html_match = re.search(r'<input type="password" id="addUsrPwd"[^>]*>[\s\S]*?<button class="btn btn-sm btn-success btn-block"', text)
if html_match:
    old_match = html_match.group(0)
    new_match = '<input type="password" id="addUsrPwd" class="form-control form-control-sm mb-2" placeholder="Contraseña">\n                            <div style="margin-bottom: 10px; text-align: left; font-size: 0.9rem;">\n                                <strong>Añadir a Ligas:</strong>\n                                <div id="adminLigasCheckboxes" style="display: flex; flex-direction: column; gap: 3px; max-height: 100px; overflow-y: auto; background: white; padding: 5px; border-radius: 4px; border: 1px solid #ccc; margin-top: 5px;">\n                                    <!-- Populated by JS -->\n                                </div>\n                            </div>\n                            <button class="btn btn-sm btn-success btn-block"'
    text = text.replace(old_match, new_match)

# 2. Update `crearUsuarioAdmin` JS
old_js = """            var newP = document.getElementById('addUsrPwd').value.trim();
            if(!newU || !newP) { alert("Falta usuario o contraseña"); return; }
            var payload = { action: "add_user", usuario: currentUser, password: currentPassword, new_u: newU, new_p: newP, new_n: newU };"""

new_js = """            var newP = document.getElementById('addUsrPwd').value.trim();
            if(!newU || !newP) { alert("Falta usuario o contraseña"); return; }
            
            var checkboxes = document.querySelectorAll('#adminLigasCheckboxes input[type="checkbox"]');
            var selectedLigas = [];
            checkboxes.forEach(function(cb) {
                if (cb.checked) selectedLigas.push(cb.value);
            });
            
            var payload = { action: "add_user", usuario: currentUser, password: currentPassword, new_u: newU, new_p: newP, new_n: newU, ligas_seleccionadas: selectedLigas };"""

js_match = re.search(r'var newP = document.getElementById\(\'addUsrPwd\'\)\.value\.trim\(\);\s*if\(!newU \|\| !newP\).*?\s*var payload = \{ action: "add_user",.*?\};', text, re.DOTALL)
if js_match:
    text = text.replace(js_match.group(0), new_js)

# 3. Populate checkboxes in login response
# Find where admin features are enabled: `if(isAdmin) { document.getElementById('adminPanelWrapper').style.display = "block";`
admin_vis_match = re.search(r"if\s*\(isAdmin\)\s*\{\s*document\.getElementById\('adminPanelWrapper'\)\.style\.display\s*=\s*'block';", text)
if admin_vis_match:
    pop_ligas_js = """if (isAdmin) {
                document.getElementById('adminPanelWrapper').style.display = 'block';
                
                // POPULATE LIGAS
                var ligasContainer = document.getElementById('adminLigasCheckboxes');
                if (ligasContainer && data.clasificaciones) {
                    ligasContainer.innerHTML = '';
                    var allLigas = Object.keys(data.clasificaciones);
                    allLigas.forEach(function(liga) {
                        var div = document.createElement('div');
                        div.innerHTML = '<label style="margin:0; cursor:pointer;"><input type="checkbox" value="' + liga + '" style="margin-right:5px;"> ' + liga + '</label>';
                        ligasContainer.appendChild(div);
                    });
                }
"""
    text = text.replace(admin_vis_match.group(0), pop_ligas_js)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated dev.html for Admin Ligas checkboxes.")

