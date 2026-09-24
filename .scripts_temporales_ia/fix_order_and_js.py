import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix the JS overwrite
html = re.sub(r"document\.getElementById\('tituloPrincipalSeccion'\)\.innerText = [^;]+;", "", html)

# 2. Extract sections safely
def extract_section(html, section_id):
    start = html.find(f'id="{section_id}"')
    if start == -1: return ""
    
    tag_start = html.rfind('<section', 0, start)
    is_form = False
    if tag_start == -1 or html.rfind('<form', 0, start) > tag_start:
        tag_start = html.rfind('<form', 0, start)
        is_form = True
    
    tag_name = 'form' if is_form else 'section'
    end = html.find(f'</{tag_name}>', start)
    if end == -1: return ""
    end += len(f'</{tag_name}>')
    
    # If the parent is a section, let's grab it (for prediccionForm)
    if section_id == 'prediccionForm':
        parent_start = html.rfind('<section', 0, start)
        if parent_start != -1:
            parent_end = html.find('</section>', start) + 10
            return html[parent_start:parent_end]
            
    return html[tag_start:end]

sec_cartelera = extract_section(html, 'prediccionForm')
sec_ranking = extract_section(html, 'clasificacionesSection')
sec_enlaces = extract_section(html, 'enlacesRfevbSection')
sec_historial = extract_section(html, 'historialSection')
sec_calendario = extract_section(html, 'calendarioSection')
sec_totales = extract_section(html, 'prediccionesTotalesSection')

# Remove them all from the HTML
# We will find the very first index where one of them starts
first_idx = min([html.find(sec) for sec in [sec_cartelera, sec_ranking, sec_enlaces, sec_historial, sec_calendario, sec_totales] if html.find(sec) != -1])

html = html.replace(sec_cartelera, '')
html = html.replace(sec_ranking, '')
html = html.replace(sec_enlaces, '')
html = html.replace(sec_historial, '')
html = html.replace(sec_calendario, '')
html = html.replace(sec_totales, '')

ordered_html = f"""
    {sec_cartelera}
    {sec_ranking}
    {sec_enlaces}
    {sec_historial}
    {sec_calendario}
    {sec_totales}
"""

html = html[:first_idx] + ordered_html + html[first_idx:]

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Fixed JS overwrite and physical order.")

