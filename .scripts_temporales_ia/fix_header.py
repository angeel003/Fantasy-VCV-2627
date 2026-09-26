import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_logic = r"""// Populating new Header V2
            document.getElementById('h2-user-name').innerText = displayNom;
            document.getElementById('h2-user-handle').innerText = "@" + usr;"""

new_logic = r"""// Populating new Header V2
            document.getElementById('h2-user-name').innerText = data.nombre_real || usr;
            document.getElementById('h2-user-handle').innerText = "@" + usr;"""

text = text.replace(old_logic, new_logic)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed header names!")
