import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Revert #btnReload CSS colors to club colors
old_reload_css = """        background-color: #ffffff;
        color: #333333;
        border: 2px solid #333333;"""
new_reload_css = """        background-color: var(--vcv-dorado);
        color: var(--vcv-morado);
        border: 2px solid var(--vcv-morado);"""
html = html.replace(old_reload_css, new_reload_css)

old_hover_css = """#btnReload:hover {
        background-color: #f0f0f0;"""
new_hover_css = """#btnReload:hover {
        background-color: #b89c45;"""
html = html.replace(old_hover_css, new_hover_css)

# 2. Revert #fab-btn inline style colors
old_fab_style = 'style="background: #ffffff; color: #333333; border: 2px solid #333333; border-radius: 50%; width: 55px; height: 55px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer; display: flex; align-items: center; justify-content: center; margin-left: auto; transition: transform 0.2s;"'
new_fab_style = 'style="background: var(--vcv-dorado); color: var(--vcv-morado); border: 2px solid var(--vcv-morado); border-radius: 50%; width: 55px; height: 55px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer; display: flex; align-items: center; justify-content: center; margin-left: auto; transition: transform 0.2s;"'
html = html.replace(old_fab_style, new_fab_style)

# 3. Add click away listener
# We will insert it inside the <script> block for the FAB menu
js_insert = """
        // Cierra el menú de la lupa al hacer click fuera
        document.addEventListener('click', function(event) {
            var fabMenu = document.getElementById('fab-menu');
            var links = document.getElementById('fab-links');
            var btn = document.getElementById('fab-btn');
            
            if (fabMenu && links && btn) {
                var isClickInside = fabMenu.contains(event.target);
                if (!isClickInside && links.style.display === 'flex') {
                    links.style.display = 'none';
                    btn.style.transform = 'rotate(0deg)';
                }
            }
        });
        
        function checkFabVisibility() {"""

html = html.replace('function checkFabVisibility() {', js_insert)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated colors and added click away listener.")

