import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update #btnReload CSS
old_reload_css = """        background-color: var(--vcv-dorado);
        color: var(--vcv-morado);
        border: 2px solid var(--vcv-morado);"""
new_reload_css = """        background-color: #ffffff;
        color: #333333;
        border: 2px solid #333333;"""
html = html.replace(old_reload_css, new_reload_css)

# Update hover color
old_hover_css = """#btnReload:hover {
        background-color: #b89c45;"""
new_hover_css = """#btnReload:hover {
        background-color: #f0f0f0;"""
html = html.replace(old_hover_css, new_hover_css)

# 2. Update #btnReload HTML
svg_reload = '<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"></polyline><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>'
# The btnReload HTML has an emoji in it. Let's find it.
reload_btn_match = re.search(r'<button id="btnReload"[^>]*>.*?</button>', html, re.DOTALL)
if reload_btn_match:
    old_btn = reload_btn_match.group(0)
    new_btn = '<button id="btnReload" title="Sincronizar y recargar datos">\n    ' + svg_reload + '\n</button>'
    html = html.replace(old_btn, new_btn)

# 3. Update #fab-btn HTML
svg_search = '<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
fab_btn_match = re.search(r'<button id="fab-btn"[^>]*>.*?</button>', html, re.DOTALL)
if fab_btn_match:
    old_fab = fab_btn_match.group(0)
    # We also need to change the style background/color/border of the fab button
    new_fab = '<button id="fab-btn" onclick="toggleFab()" style="background: #ffffff; color: #333333; border: 2px solid #333333; border-radius: 50%; width: 55px; height: 55px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer; display: flex; align-items: center; justify-content: center; margin-left: auto; transition: transform 0.2s;">\n            ' + svg_search + '\n        </button>'
    html = html.replace(old_fab, new_fab)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated icons to SVG and changed colors.")

