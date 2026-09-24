import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the old FAB menu that was injected inside appSection
start_fab = html.find('<!-- FAB MENU (Navegación Rápida) -->')
end_fab = html.find('</script>', start_fab) + 9

if start_fab != -1 and end_fab != -1:
    old_fab = html[start_fab:end_fab]
    html = html.replace(old_fab, '')
    print("Old FAB removed.")

# 2. Add the new FAB right before </body>, positioned above the reload button
# Reload button is at bottom: 25px; right: 25px; width: 55px; height: 55px;
# Toast is at bottom: 90px;
# Let's put the FAB at bottom: 90px; right: 25px; (above the reload button).
# We will change Toast to bottom: 160px; just in case.

new_fab = """
    <!-- FAB MENU NAV (Navegación Rápida) FUERA DEL APPSECTION PARA QUE POSITION FIXED FUNCIONE BIEN -->
    <div id="fab-menu" style="position: fixed; bottom: 90px; right: 25px; z-index: 9999; text-align: right; display: none;">
        <div id="fab-links" style="display: none; flex-direction: column; gap: 8px; margin-bottom: 10px; background: rgba(255,255,255,0.95); padding: 12px; border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.25); border: 2px solid var(--vcv-dorado); text-align: left; backdrop-filter: blur(5px);">
            <a href="#clasificacionesSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">🏆 Clasificaciones</a>
            <a href="#prediccionForm" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">🏐 Porras / Partidos</a>
            <a href="#historialSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">✅ Mis Resultados</a>
            <a href="#prediccionesTotalesSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">🔮 Predicción Final</a>
            <a href="#calendarioSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block;">📅 Calendario Total</a>
        </div>
        <button id="fab-btn" onclick="toggleFab()" style="background: var(--vcv-blanco); color: var(--vcv-morado); border: 2px solid var(--vcv-morado); border-radius: 50%; width: 55px; height: 55px; font-size: 24px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer; display: flex; align-items: center; justify-content: center; margin-left: auto; transition: transform 0.2s;">
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
        
        // Mostrar el FAB solo cuando estemos logueados
        function checkFabVisibility() {
            if(window.currentUser) {
                document.getElementById('fab-menu').style.display = 'block';
            } else {
                document.getElementById('fab-menu').style.display = 'none';
            }
        }
        // Lo engancharemos en actualizarVistas
        var oldActualizarVistas = window.actualizarVistas;
        window.actualizarVistas = function(soloCalendario) {
            if(oldActualizarVistas) oldActualizarVistas(soloCalendario);
            checkFabVisibility();
        };
    </script>
"""

# Inject before </body>
if 'FAB MENU NAV' not in html:
    html = html.replace('</body>', new_fab + '\n</body>')
    
    # Adjust Toast Notification position so it doesn't overlap the new FAB
    html = html.replace('bottom: 90px;\n        right: 25px;\n        background: var(--vcv', 'bottom: 160px;\n        right: 25px;\n        background: var(--vcv')
    
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("New FAB injected outside appSection and toast adjusted.")
else:
    print("New FAB already exists")


