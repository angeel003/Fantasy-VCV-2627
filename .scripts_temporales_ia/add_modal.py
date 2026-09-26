import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the bell button to open the modal
text = text.replace('<button class="bell-btn-v2">', '<button class="bell-btn-v2" onclick="document.getElementById(\'notificacionesModal\').style.display=\'flex\'">')

# 2. Add the modal HTML just before the end of the body
modal_html = """
<!-- MODAL NOTIFICACIONES -->
<div id="notificacionesModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:9999; align-items:center; justify-content:center; backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);">
    <div style="background:var(--bg-card); width:90%; max-width:400px; border-radius:16px; padding:24px; box-shadow:0 10px 40px rgba(0,0,0,0.5); position:relative; border: 1px solid var(--border-color);">
        <button onclick="document.getElementById('notificacionesModal').style.display='none'" style="position:absolute; top:12px; right:12px; background:none; border:none; color:var(--text-muted); font-size:1.8rem; cursor:pointer; line-height:1;">&times;</button>
        
        <h3 style="margin-top:0; margin-bottom:20px; color:var(--text-main); font-weight:800; font-family:'Space Grotesk', sans-serif; display:flex; align-items:center; gap:8px;">
            <i data-lucide="bell" style="width:20px; height:20px;"></i> Notificaciones
        </h3>
        
        <div style="background:var(--bg-input); border:1px dashed var(--border-color); border-radius:12px; padding:30px 20px; text-align:center; color:var(--text-muted);">
            <i data-lucide="hammer" style="width:36px; height:36px; margin-bottom:12px; color:var(--primary-color);"></i>
            <p style="margin:0; font-size:0.95rem; line-height:1.5;"><strong>¡En construcción!</strong><br><br>Estoy trabajando para implementar las notificaciones reales más adelante. :)</p>
        </div>
        
        <button onclick="document.getElementById('notificacionesModal').style.display='none'" class="btn btn-primary btn-block mt-4" style="background:var(--primary-color); border:none; font-weight:bold; border-radius:8px;">Entendido</button>
    </div>
</div>
</body>
"""
text = text.replace('</body>', modal_html)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Modal added!")
