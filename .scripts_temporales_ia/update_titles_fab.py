import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Titles and Descriptions for each section explicitly
def replace_title_desc(section_id, new_title, new_desc, html):
    # Find the section
    start = html.find(f'id="{section_id}"')
    if start == -1: return html
    
    # Go backwards to find <section or <form
    tag_start = html.rfind('<section', 0, start)
    is_form = False
    if tag_start == -1 or html.rfind('<form', 0, start) > tag_start:
        tag_start = html.rfind('<form', 0, start)
        is_form = True
    
    tag_name = 'form' if is_form else 'section'
    end = html.find(f'</{tag_name}>', start)
    if end == -1: return html
    end += len(f'</{tag_name}>')
    
    content = html[tag_start:end]
    
    # Remove existing <h2> and <p> that look like subtitles
    # This is tricky, let's just find the first <h2> and any following <p> and replace them
    h2_match = re.search(r'<h[23][^>]*>.*?</h[23]>', content, re.DOTALL)
    if h2_match:
        # Check if there is a <p> right after
        p_match = re.search(r'<p[^>]*>.*?</p>', content[h2_match.end():h2_match.end()+200], re.DOTALL)
        if p_match:
            content = content[:h2_match.start()] + f'{new_title}\n{new_desc}' + content[h2_match.end() + p_match.end():]
        else:
            content = content[:h2_match.start()] + f'{new_title}\n{new_desc}' + content[h2_match.end():]
            
    html = html[:tag_start] + content + html[end:]
    return html

html = replace_title_desc('prediccionForm', '<h2>Cartelera de Partidos</h2>', '<p style="color:#555; margin-bottom:20px;">Predice los resultados de tus equipos favoritos esta jornada.</p>', html)
html = replace_title_desc('clasificacionesSection', '<h2>Ranking</h2>', '<p style="color:#555; margin-bottom:20px;">Clasificación actual de nuestras ligas privadas según los puntos conseguidos.</p>', html)
html = replace_title_desc('enlacesRfevbSection', '<h2>Enlaces Rfevb</h2>', '<p style="color:#555; margin-bottom:25px;">Consulta cómo van las ligas reales de nuestros equipos en las webs oficiales de la Federación.</p>', html)
html = replace_title_desc('historialSection', '<h2>Mis Predicciones</h2>', '<p style="color:#555; margin-bottom:20px;">Historial completo de tus aciertos y puntos conseguidos en jornadas anteriores.</p>', html)
html = replace_title_desc('calendarioSection', '<h2>Próximos encuentros</h2>', '<p style="color:#555; margin-bottom:20px;">Calendario con todos los horarios y fechas de los partidos futuros programados.</p>', html)
html = replace_title_desc('prediccionesTotalesSection', '<h2>Top Secret</h2>', '<p style="color:#555; margin-bottom:20px;">Predicción de los puntos totales acumulados a final de temporada de cada equipo.</p>', html)

# 2. Re-write the FAB HTML completely
old_fab_start = html.find('<!-- FAB MENU NAV')
old_fab_end = html.find('</script>', old_fab_start) + 9

new_fab = """
    <!-- FAB MENU NAV (Navegación Rápida) FUERA DEL APPSECTION PARA QUE POSITION FIXED FUNCIONE BIEN -->
    <div id="fab-menu" style="position: fixed; bottom: 90px; right: 25px; z-index: 9999; text-align: right; display: none;">
        <div id="fab-links" style="display: none; flex-direction: column; gap: 8px; margin-bottom: 10px; background: rgba(255,255,255,0.95); padding: 12px; border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.25); border: 2px solid var(--vcv-dorado); text-align: left; backdrop-filter: blur(5px);">
            <a id="fab-cartelera" href="#prediccionForm" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none; border-bottom: 1px solid #ddd;">🏐 Cartelera de Partidos</a>
            <a id="fab-ranking" href="#clasificacionesSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none; border-bottom: 1px solid #ddd;">🏆 Ranking</a>
            <a id="fab-enlaces" href="#enlacesRfevbSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none; border-bottom: 1px solid #ddd;">🔗 Enlaces Rfevb</a>
            <a id="fab-historial" href="#historialSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none; border-bottom: 1px solid #ddd;">✅ Mis Predicciones</a>
            <a id="fab-calendario" href="#calendarioSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none; border-bottom: 1px solid #ddd;">📅 Próximos encuentros</a>
            <a id="fab-totales" href="#prediccionesTotalesSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none;">🔮 Top Secret</a>
        </div>
        <button id="fab-btn" onclick="toggleFab()" style="background: var(--vcv-dorado); color: var(--vcv-morado); border: 2px solid var(--vcv-morado); border-radius: 50%; width: 55px; height: 55px; font-size: 24px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer; display: flex; align-items: center; justify-content: center; margin-left: auto; transition: transform 0.2s;">
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
        
        function checkFabVisibility() {
            var appSec = document.getElementById('appSection');
            
            // NO MOSTRAR EN MODO INVITADO
            var isGuest = (window.currentUser === null || window.currentUser === "INVITADO" || !window.currentUser);
            
            if(appSec && appSec.style.display !== 'none' && !isGuest) {
                document.getElementById('fab-menu').style.display = 'block';
                
                // Show/hide specific links based on section visibility
                var cartelera = document.getElementById('prediccionForm');
                var ranking = document.getElementById('clasificacionesSection');
                var enlaces = document.getElementById('enlacesRfevbSection');
                var historial = document.getElementById('historialSection');
                var calendario = document.getElementById('calendarioSection');
                var totales = document.getElementById('prediccionesTotalesSection');
                
                document.getElementById('fab-cartelera').style.display = (cartelera && cartelera.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-ranking').style.display = (ranking && ranking.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-enlaces').style.display = (enlaces && enlaces.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-historial').style.display = (historial && historial.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-calendario').style.display = (calendario && calendario.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-totales').style.display = (totales && totales.style.display !== 'none') ? 'block' : 'none';
                
            } else {
                document.getElementById('fab-menu').style.display = 'none';
                document.getElementById('fab-links').style.display = 'none';
            }
        }
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                checkFabVisibility();
            });
        });
        
        var appSec = document.getElementById('appSection');
        if(appSec) {
            observer.observe(appSec, { attributes: true, subtree: true });
        }
        setInterval(checkFabVisibility, 1000);
    </script>
"""

if old_fab_start != -1:
    html = html[:old_fab_start] + new_fab + html[old_fab_end:]
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Titles updated and FAB logic enhanced.")
else:
    print("Old FAB not found.")

