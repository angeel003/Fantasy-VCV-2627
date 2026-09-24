import re

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Update Play Icon (Streaming link) in Cartelera & History
    # This was already working perfectly, but I'll use play_icon.png
    play_html = r'<a href="${eq.streaming}" target="_blank" style="margin-left:8px; display:inline-block; vertical-align:middle;" title="Ver Streaming Oficial"><img src="files/images/play_icon.png" style="width:16px; height:16px; display:block;"></a>'
    play_hist = r'<a href="${p.streaming}" target="_blank" style="margin-left:8px; display:inline-block; vertical-align:middle;" title="Ver Streaming Oficial"><img src="files/images/play_icon.png" style="width:16px; height:16px; display:block;"></a>'
    
    html = re.sub(r'<a href="\${eq.streaming}".*?</a>', play_html, html)
    html = re.sub(r'<a href="\${p.streaming}".*?</a>', play_hist, html)
    
    # Wait, the code in aa7485f has the emoji version: `&#9654;&#65039;`
    # Let's just find and replace the emoji directly.
    # Ah, regex matching emoji can be tricky. Let's use string replace.
    old_eq_stream = 'let streamIcon = eq.streaming ? ` <a href="${eq.streaming}" target="_blank" style="color:#d32f2f; text-decoration:none; margin-left:6px; font-size:1.1rem;" title="Ver Streaming Oficial">&#9654;&#65039;</a>` : "";'
    old_p_stream = 'let streamIconHist = p.streaming ? ` <a href="${p.streaming}" target="_blank" style="color:#d32f2f; text-decoration:none; margin-left:6px; font-size:1.1rem;" title="Ver Streaming Oficial">&#9654;&#65039;</a>` : "";'
    
    new_eq_stream = 'let streamIcon = eq.streaming ? ` <a href="${eq.streaming}" target="_blank" style="margin-left:8px; display:inline-block; vertical-align:middle;" title="Ver Streaming Oficial"><img src="files/images/play_icon.png" style="width:16px; height:16px; display:block;"></a>` : "";'
    new_p_stream = 'let streamIconHist = p.streaming ? ` <a href="${p.streaming}" target="_blank" style="margin-left:8px; display:inline-block; vertical-align:middle;" title="Ver Streaming Oficial"><img src="files/images/play_icon.png" style="width:16px; height:16px; display:block;"></a>` : "";'
    
    html = html.replace(old_eq_stream, new_eq_stream)
    html = html.replace(old_p_stream, new_p_stream)
    # just in case it doesn't match perfectly, fallback regex:
    html = re.sub(r'let streamIcon = eq.streaming \? ` <a href="\${eq.streaming}".*?</a>` : "";', new_eq_stream, html)
    html = re.sub(r'let streamIconHist = p.streaming \? ` <a href="\${p.streaming}".*?</a>` : "";', new_p_stream, html)

    # 2. Update Admin Panel Time Locks
    old_admin_inputs = r'<div style="display:flex; gap:10px;">\s*<input type="text" id="adm_sets_\${eq.id_partido}".*?>\s*<input type="text" id="adm_parc_\${eq.id_partido}".*?>\s*</div>'
    new_admin_inputs = r"""
                      <div style="display:flex; gap:10px;">
                          <input type="text" id="adm_sets_${eq.id_partido}" class="form-control form-control-sm" placeholder="${now >= ts ? 'Sets (3-1)' : 'Bloqueado (No ha empezado)'}" value="${eq.oficial_sets || ''}" ${now >= ts ? '' : 'disabled'}>
                          <input type="text" id="adm_parc_${eq.id_partido}" class="form-control form-control-sm" placeholder="${now >= ts ? 'Parc (25-20...)' : 'Bloqueado'}" value="${eq.oficial_parciales || ''}" ${now >= ts ? '' : 'disabled'}>
                      </div>
"""
    html = re.sub(old_admin_inputs, new_admin_inputs.strip(), html)
    
    # 3. Remove "Nombre Real" from Add User
    html = re.sub(r'<input type="text" id="addUsrReal".*?>', '', html)
    html = re.sub(r'const nr = document\.getElementById\(\'addUsrReal\'\)\.value\.trim\(\);', '', html)
    html = re.sub(r'nombre_real:\s*nr,?', '', html)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

