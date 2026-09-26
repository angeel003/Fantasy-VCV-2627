import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the guest mode display logic
old_guest_display = "document.getElementById('displayJugador').innerText = \" Modo Invitado\";"
new_guest_display = """document.getElementById('h2-user-name').innerText = "Modo Invitado";
            document.getElementById('h2-user-handle').innerText = "@lectura";
            document.getElementById('h2-user-badges').innerHTML = "";"""

text = text.replace(old_guest_display, new_guest_display)

# Remove the lucide timeout from inside the loop to speed up rendering a bit
text = text.replace("setTimeout(() => { if(window.lucide) lucide.createIcons(); }, 100);", "")
# Instead we already have `lucide.createIcons()` outside the loop in `btnLogin`, but we need to ensure it's called after injection.
# Actually `lucide.createIcons()` is called in `setTimeout` AFTER htmlPartidos is injected.
# Let's just make sure it's called after container.innerHTML = htmlPartidos
text = text.replace("document.getElementById('contenedorPartidos').innerHTML = htmlPartidos;\n            iniciarRelojes();", "document.getElementById('contenedorPartidos').innerHTML = htmlPartidos;\n            iniciarRelojes();\n            if(window.lucide) setTimeout(() => lucide.createIcons(), 50);")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed guest login error and optimized lucide calls.")
