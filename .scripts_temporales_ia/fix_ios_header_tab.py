import re

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Update Header Padding
    # from: padding: 60px 15px;
    # to: padding: calc(40px + env(safe-area-inset-top, 0px)) 15px 40px;
    html = re.sub(r'padding:\s*60px\s*15px;', 'padding: calc(40px + env(safe-area-inset-top, 0px)) 15px 40px;', html)
    
    # 2. Change btnLogout to a fixed tab on the left
    old_btn_regex = r'<button id="btnLogout".*?</button>'
    new_btn = r'<button id="btnLogout" style="display:none; position:fixed; left:0; top:50%; transform:translateY(-50%); background:var(--vcv-dorado); border:none; border-radius:0 12px 12px 0; color:var(--vcv-morado); font-size:1.8rem; font-weight:bold; cursor:pointer; padding:20px 12px 20px 8px; box-shadow:3px 3px 12px rgba(0,0,0,0.4); z-index:99999;" title="Volver atrás">&#10094;</button>'
    
    html = re.sub(old_btn_regex, new_btn, html)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

