import re

animation_css = """
    /* ---------------------------------------------------
       2. TRANSICIONES Y ANIMACIONES (Fade-in)
       --------------------------------------------------- */
    @keyframes fadeScaleIn {
        0% { opacity: 0; transform: scale(0.98) translateY(15px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }
    #loginSection, #appSection, #adminPanelWrapper {
        animation: fadeScaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if 'fadeScaleIn' not in html:
        # inject after body { ... }
        html = re.sub(r'(body \{[^}]+\})', r'\1\n' + animation_css, html)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

