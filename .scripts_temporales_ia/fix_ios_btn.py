import re

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Clean up the ugly undefined in catch blocks
    html = html.replace('err.stack', '(err.stack || "")')
    
    # Replace btnLogout
    html = re.sub(r'<button id="btnLogout".*?</button>', 
                  r'<button id="btnLogout" style="display:none; position:absolute; left:5px; top:max(15px, env(safe-area-inset-top)); background:transparent; border:none; color:rgba(255,255,255,0.9); font-size:2.2rem; cursor:pointer; padding:15px 25px; outline:none; text-shadow:0 2px 4px rgba(0,0,0,0.3); z-index:9999;" title="Volver atrás">&#10094;</button>', 
                  html)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

