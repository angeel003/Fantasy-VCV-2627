import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_func = """function checkFabVisibility() {
            if(window.currentUser) {
                document.getElementById('fab-menu').style.display = 'block';
            } else {
                document.getElementById('fab-menu').style.display = 'none';
            }
        }"""

new_func = """function checkFabVisibility() {
            var appSec = document.getElementById('appSection');
            if(appSec && appSec.style.display !== 'none') {
                document.getElementById('fab-menu').style.display = 'block';
            } else {
                document.getElementById('fab-menu').style.display = 'none';
            }
        }"""

if old_func in html:
    html = html.replace(old_func, new_func)
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Patched checkFabVisibility in dev.html")
else:
    print("Function not found.")

