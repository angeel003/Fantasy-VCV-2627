import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Give an ID to the RFEVB section if it doesn't have one
rfevb_pattern = r'<section>\s*<h2[^>]*>\s*📊?\s*Clasificaciones Oficiales'
html = re.sub(rfevb_pattern, r'<section id="enlacesRfevbSection">\n        <h2> Clasificaciones Oficiales', html)

# 2. Extract the sections
def extract_section(html, section_id):
    start = html.find(f'id="{section_id}"')
    if start == -1: return ""
    # find the previous <section (or form) tag
    tag_start = html.rfind('<section', 0, start)
    is_form = False
    if tag_start == -1 or html.rfind('<form', 0, start) > tag_start:
        tag_start = html.rfind('<form', 0, start)
        is_form = True
    
    if tag_start == -1: return ""
    
    tag_name = 'form' if is_form else 'section'
    end = html.find(f'</{tag_name}>', start)
    if end == -1: return ""
    end += len(f'</{tag_name}>')
    
    content = html[tag_start:end]
    return content

# The IDs of the sections we want to extract and reorder
sec_cartelera = extract_section(html, 'prediccionForm')
sec_ranking = extract_section(html, 'clasificacionesSection')
sec_enlaces = extract_section(html, 'enlacesRfevbSection')
sec_historial = extract_section(html, 'historialSection')
sec_totales = extract_section(html, 'prediccionesTotalesSection')
sec_calendario = extract_section(html, 'calendarioSection')

# If 'prediccionForm' is wrapped in a section, extract the section instead.
cartelera_parent_start = html.rfind('<section', 0, html.find('id="prediccionForm"'))
if cartelera_parent_start != -1:
    cartelera_parent_end = html.find('</section>', cartelera_parent_start) + 10
    sec_cartelera = html[cartelera_parent_start:cartelera_parent_end]

print("Extracted sections.")

# Replace the titles in the extracted blocks
sec_cartelera = re.sub(r'<h2[^>]*>.*?</h2>', '<h2>Cartelera de Partidos</h2>', sec_cartelera, count=1)
sec_ranking = re.sub(r'<h2[^>]*>.*?</h2>', '<h2>Ranking</h2>', sec_ranking, count=1)
sec_enlaces = re.sub(r'<h2[^>]*>.*?</h2>', '<h2>Enlaces Rfevb</h2>', sec_enlaces, count=1)
sec_historial = re.sub(r'<h2[^>]*>.*?</h2>', '<h2>Mis Predicciones</h2>', sec_historial, count=1)
sec_calendario = re.sub(r'<h2[^>]*>.*?</h2>', '<h2>Próximos encuentros</h2>', sec_calendario, count=1)
sec_totales = re.sub(r'<h2[^>]*>.*?</h2>', '<h2>Top Secret</h2>', sec_totales, count=1)

# Now, we need to remove them from html and inject them in the correct order.
# The correct order:
# 1. Cartelera de Partidos (sec_cartelera)
# 2. Ranking (sec_ranking)
# 3. Enlaces Rfevb (sec_enlaces)
# 4. Mis predicciones (sec_historial)
# 5. Próximos partidos (sec_calendario)
# 6. Top Secret (sec_totales)

ordered_sections = f"""
    {sec_cartelera}
    {sec_ranking}
    {sec_enlaces}
    {sec_historial}
    {sec_calendario}
    {sec_totales}
"""

# Let's write an intelligent replacement
# Find the start of the first section and the end of the last section
start_replace = html.find(sec_cartelera)
if start_replace == -1: start_replace = html.find(sec_ranking)

# We will just replace all of them with empty strings, and then insert ordered_sections where sec_cartelera was.
html = html.replace(sec_ranking, '')
html = html.replace(sec_enlaces, '')
html = html.replace(sec_historial, '')
html = html.replace(sec_calendario, '')
html = html.replace(sec_totales, '')

html = html.replace(sec_cartelera, ordered_sections)

# 3. Update the FAB menu
old_fab_start = html.find('<!-- FAB MENU NAV')
old_fab_end = html.find('</script>', old_fab_start) + 9

if old_fab_start != -1:
    new_fab = """
    <!-- FAB MENU NAV (Navegación Rápida) FUERA DEL APPSECTION PARA QUE POSITION FIXED FUNCIONE BIEN -->
    <div id="fab-menu" style="position: fixed; bottom: 90px; right: 25px; z-index: 9999; text-align: right; display: none;">
        <div id="fab-links" style="display: none; flex-direction: column; gap: 8px; margin-bottom: 10px; background: rgba(255,255,255,0.95); padding: 12px; border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.25); border: 2px solid var(--vcv-dorado); text-align: left; backdrop-filter: blur(5px);">
            <a href="#prediccionForm" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">🏐 Cartelera de Partidos</a>
            <a href="#clasificacionesSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">🏆 Ranking</a>
            <a href="#enlacesRfevbSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">🔗 Enlaces Rfevb</a>
            <a href="#historialSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">✅ Mis Predicciones</a>
            <a href="#calendarioSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block; border-bottom: 1px solid #ddd;">📅 Próximos encuentros</a>
            <a href="#prediccionesTotalesSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: block;">🔮 Top Secret</a>
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
            if(appSec && appSec.style.display !== 'none') {
                document.getElementById('fab-menu').style.display = 'block';
            } else {
                document.getElementById('fab-menu').style.display = 'none';
            }
        }
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === "style") {
                    checkFabVisibility();
                }
            });
        });
        var appSec = document.getElementById('appSection');
        if(appSec) {
            observer.observe(appSec, { attributes: true });
        }
        setInterval(checkFabVisibility, 1000);
    </script>
"""
    html = html[:old_fab_start] + new_fab + html[old_fab_end:]

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Sections reordered and FAB updated.")

