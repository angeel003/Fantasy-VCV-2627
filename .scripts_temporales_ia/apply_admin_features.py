import re

css_admin_dark = """
    /* ---------------------------------------------------
       6. MODO ADMIN OSCURO
       --------------------------------------------------- */
    body.admin-dark-mode {
        background: #121212 !important;
        color: #eee !important;
    }
    body.admin-dark-mode header {
        background: #000 !important;
        border-bottom: 5px solid var(--vcv-dorado) !important;
    }
    body.admin-dark-mode .admin-panel {
        background: #1e1e1e !important;
        color: #ddd !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.8);
    }
    body.admin-dark-mode .admin-match-box {
        background: #2a2a2a !important;
        border: 1px solid #444 !important;
    }
    body.admin-dark-mode h4, body.admin-dark-mode h5, body.admin-dark-mode label {
        color: var(--vcv-dorado) !important;
    }
"""

admin_toggle_html = """
  <div id="adminToggleContainer" style="display:none; text-align:center; padding: 12px; background:#111; color:white; border-bottom: 2px solid var(--vcv-dorado);">
      <label style="cursor:pointer; display:inline-flex; align-items:center; margin:0; font-weight:bold; color:var(--vcv-dorado);">
          <input type="checkbox" id="adminSwitch" style="margin-right:10px; transform:scale(1.4);"> MODO ADMINISTRADOR
      </label>
  </div>
"""

sheets_link_html = """
      <div style="margin-top: 20px; text-align:center; border-top: 1px solid #444; padding-top: 15px;">
          <a href="https://docs.google.com/spreadsheets/" target="_blank" class="btn btn-outline-warning btn-sm">Abrir Google Sheets</a>
      </div>
"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Add CSS
    if 'body.admin-dark-mode' not in html:
        html = html.replace('</style>', css_admin_dark + '\n</style>')
        
    # 2. Add Admin Toggle just below header
    if 'adminToggleContainer' not in html:
        html = html.replace('</header>', '</header>\n' + admin_toggle_html)
        
    # 3. Add main wrapper to hide regular content in admin mode
    # Wrap #appSection internals? No, we can just hide the 5 tabs/sections.
    # But it's easier to just wrap the sections in a div, or hide them individually.
    # Actually, #appSection contains the tabs and the sections.
    # We can leave #appSection visible, but hide the `app-tabs` and `tab-content` (or all sections).
    # Let's add JS for the toggle.
    js_toggle = """
document.getElementById('adminSwitch').addEventListener('change', function(e) {
    if(e.target.checked) {
        document.body.classList.add('admin-dark-mode');
        document.getElementById('app-tabs').style.display = 'none';
        document.getElementById('clasificacionesSection').style.display = 'none';
        document.getElementById('historialSection').style.display = 'none';
        document.getElementById('prediccionesTotalesSection').style.display = 'none';
        document.getElementById('btnSubmit').style.display = 'none';
        document.getElementById('warningPredicciones').style.display = 'none';
        document.getElementById('prediccionesList').style.display = 'none';
        document.getElementById('tituloPrincipalSeccion').style.display = 'none';
        
        document.getElementById('adminPanelWrapper').style.display = 'block';
    } else {
        document.body.classList.remove('admin-dark-mode');
        document.getElementById('app-tabs').style.display = 'flex';
        // Restore active tab logic roughly (default to predicciones)
        document.getElementById('prediccionesList').style.display = 'block';
        document.getElementById('tituloPrincipalSeccion').style.display = 'block';
        document.getElementById('btnSubmit').style.display = 'block';
        
        document.getElementById('adminPanelWrapper').style.display = 'none';
    }
});
"""
    if 'adminSwitch' not in html.split('<script>')[1]:
        html = html.replace('<script>', '<script>\n' + js_toggle)
        
    # 4. Update the logic that shows adminPanelWrapper by default when isAdmin is true.
    # Instead, we just show the toggle container.
    html = html.replace("document.getElementById('adminPanelWrapper').style.display = \"block\";", "document.getElementById('adminToggleContainer').style.display = \"block\";")
    html = html.replace("document.getElementById('adminPanelWrapper').style.display = \"none\";", "document.getElementById('adminToggleContainer').style.display = \"none\";")
    # Also remove renderAdminPanel from there, we can render it once anyway, but keep it hidden.
    
    # 5. Fix Play Icon
    # Old: ` <a href="${eq.streaming}" target="_blank" style="color:#d32f2f; text-decoration:none; margin-left:6px; font-size:1.1rem;" title="Ver Streaming Oficial">&#9654;&#65039;</a>`
    # (Or similar, there might be unicode issues, so I'll regex it)
    html = re.sub(r'<a href="\${eq.streaming}".*?>.*?</a>', r'<a href="${eq.streaming}" target="_blank" style="margin-left:8px; display:inline-block; vertical-align:middle;" title="Ver Streaming Oficial"><img src="files/images/play_icon.png" style="width:16px; height:16px; display:block;"></a>', html)
    html = re.sub(r'<a href="\${p.streaming}".*?>.*?</a>', r'<a href="${p.streaming}" target="_blank" style="margin-left:8px; display:inline-block; vertical-align:middle;" title="Ver Streaming Oficial"><img src="files/images/play_icon.png" style="width:16px; height:16px; display:block;"></a>', html)
    
    # 6. Admin Panel Locks (renderAdminPanel function)
    # Search for: <input type="text" id="adm_sets_${eq.id_partido}"
    old_admin_box = r'<div style="display:flex; gap:10px;">\s*<input type="text" id="adm_sets_\${eq\.id_partido}".*?>\s*<input type="text" id="adm_parc_\${eq\.id_partido}".*?>\s*</div>'
    
    new_admin_box = r"""
                      <div style="display:flex; gap:10px;">
                          <input type="text" id="adm_sets_${eq.id_partido}" class="form-control form-control-sm" placeholder="${now >= ts ? 'Sets (3-1)' : 'Bloqueado (No ha empezado)'}" value="${eq.oficial_sets || ''}" ${now >= ts ? '' : 'disabled'}>
                          <input type="text" id="adm_parc_${eq.id_partido}" class="form-control form-control-sm" placeholder="${now >= ts ? 'Parc (25-20...)' : 'Bloqueado'}" value="${eq.oficial_parciales || ''}" ${now >= ts ? '' : 'disabled'}>
                      </div>
"""
    html = re.sub(old_admin_box, new_admin_box.strip(), html)
    
    # 7. Add sheets link
    if 'Abrir Google Sheets' not in html:
        html = html.replace('</div> <!-- adminPanelWrapper -->', sheets_link_html + '\n</div> <!-- adminPanelWrapper -->')
        html = html.replace('</div>\n  </div>\n  \n  <div id="toastNotification">', sheets_link_html + '\n</div>\n  </div>\n  \n  <div id="toastNotification">') # Fallback if first replace fails
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

