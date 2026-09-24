import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add FAB menu right after <div id="appSection" ...>
fab_html = """
    <!-- FAB MENU (Navegación Rápida) -->
    <div id="fab-menu" style="position: fixed; bottom: 25px; right: 25px; z-index: 9999; text-align: right;">
        <div id="fab-links" style="display: none; flex-direction: column; gap: 8px; margin-bottom: 15px; background: rgba(255,255,255,0.95); padding: 12px; border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.25); border: 2px solid var(--vcv-dorado); text-align: left; backdrop-filter: blur(5px);">
            <a href="#clasificacionesSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">🏆 Clasificaciones</a>
            <a href="#prediccionForm" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">🏐 Porras / Partidos</a>
            <a href="#historialSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">✅ Mis Resultados</a>
            <a href="#prediccionesTotalesSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">🔮 Predicción Final</a>
            <a href="#calendarioSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block;">📅 Calendario Total</a>
        </div>
        <button id="fab-btn" onclick="toggleFab()" style="background: var(--vcv-morado); color: var(--vcv-dorado); border: 3px solid var(--vcv-dorado); border-radius: 50%; width: 65px; height: 65px; font-size: 28px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); cursor: pointer; display: flex; align-items: center; justify-content: center; margin-left: auto; transition: transform 0.2s;">
            🧭
        </button>
    </div>
    
    <script>
        function toggleFab() {
            var links = document.getElementById('fab-links');
            var btn = document.getElementById('fab-btn');
            if (links.style.display === 'none' || links.style.display === '') {
                links.style.display = 'flex';
                btn.style.transform = 'rotate(45deg)';
            } else {
                links.style.display = 'none';
                btn.style.transform = 'rotate(0deg)';
            }
        }
    </script>
"""

if 'fab-menu' not in html:
    html = html.replace('<div id="appSection" style="display:none; padding:15px; position:relative; min-height:80vh;">', '<div id="appSection" style="display:none; padding:15px; position:relative; min-height:80vh;">\n' + fab_html)
    
    # Also add smooth scroll
    if 'scroll-behavior: smooth' not in html:
        html = html.replace('html, body {', 'html { scroll-behavior: smooth; }\n    html, body {')
        
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("FAB menu injected in dev.html")
else:
    print("FAB already exists")

