import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_guest_display = """document.getElementById('h2-user-name').innerText = "Modo Invitado";
            document.getElementById('h2-user-handle').innerText = "@lectura";
            document.getElementById('h2-user-badges').innerHTML = "";"""

text = re.sub(r'document\.getElementById\(\'displayJugador\'\)\.innerText = ".*?\sModo Invitado";', new_guest_display, text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed guest login display.")
