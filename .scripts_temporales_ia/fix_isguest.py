import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_check = """var isGuest = (window.currentUser === null || window.currentUser === "INVITADO" || !window.currentUser);"""
good_check = """// currentUser usa 'let', así que no está en 'window'. Lo comprobamos de forma segura.
            var isGuest = true;
            try {
                if (typeof currentUser !== 'undefined' && currentUser && currentUser !== "INVITADO") {
                    isGuest = false;
                }
            } catch(e) {}"""

if bad_check in html:
    html = html.replace(bad_check, good_check)
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed isGuest check in dev.html")
else:
    print("Check not found.")

