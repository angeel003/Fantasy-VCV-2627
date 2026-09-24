import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the "Cartelera de Partidos" <h4> from JS
html = html.replace('let htmlPartidos = `<h4 style="color: var(--vcv-morado); margin-bottom: 20px;">Cartelera de Partidos</h4>`;', 'let htmlPartidos = ``;')
# Just in case there are subtle differences in whitespace
html = re.sub(r'let htmlPartidos = `<h4[^>]*>.*?</h4>`;', 'let htmlPartidos = ``;', html)

# 2. Reorganize the HTML layout
# Extract the title and paragraph
title_regex = r'(<h2 id="tituloPrincipalSeccion">.*?</h2>\s*<p[^>]*>.*?</p>)'
match_title = re.search(title_regex, html, re.DOTALL)

if match_title:
    title_html = match_title.group(1)
    # Remove it from its current position
    html = html.replace(title_html, '')
    
    # We want to place it right after the adminPanelWrapper
    # Find adminPanelWrapper end
    admin_end_idx = html.find('</div>', html.find('adminListaPartidos'))
    # actually, adminPanelWrapper is a huge block, let's find the exact string that follows it, which is the <details> for Rules
    details_start = html.find('<details style="margin-bottom: 20px; background: #fff; padding: 10px; border-radius: 8px; border: 1px solid #ccc;">')
    
    if details_start != -1:
        # Insert title_html right before details_start
        html = html[:details_start] + title_html + '\n        ' + html[details_start:]
    else:
        # If the <details> string is slightly different, let's find "Signo"
        signo_idx = html.find('Qu significa Puntos Dif. y Signo')
        if signo_idx == -1: signo_idx = html.find('Qu significa Puntos Dif. y Signo')
        if signo_idx == -1: signo_idx = html.find('Signo?')
        
        details_tag_start = html.rfind('<details', 0, signo_idx)
        if details_tag_start != -1:
            html = html[:details_tag_start] + title_html + '\n        ' + html[details_tag_start:]

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Reorganized Title and User Info.")

