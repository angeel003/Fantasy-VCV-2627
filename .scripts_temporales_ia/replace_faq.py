import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = """<div class="faq-inner-item">
                <div class="faq-inner-title">¿Cómo instalar la App?</div>
                <div style="font-size:0.85rem; text-align:left; line-height: 1.5;">
                    <p style="margin-bottom:8px;">No necesitas descargar ningún archivo APK. Al entrar en esta web desde tu móvil, haz lo siguiente:</p>
                    <ul style="padding-left:20px; margin-bottom:0;">
                        <li style="margin-bottom:8px;"><b>En Android (Chrome):</b> Tocar los 3 puntitos arriba a la derecha > "Instalar aplicación" (o "Añadir a pantalla de inicio").</li>
                        <li><b>En iPhone (Safari):</b> Tocar el botón de compartir (el cuadrado con la flecha) > "Añadir a la pantalla de inicio".</li>
                    </ul>
                </div>
            </div>"""

# Find the start of the block
pattern = r'<div class="faq-inner-item">\s*<div class="faq-inner-title">¿Cómo instalar la App\?</div>.*?</div>\s*</div>\s*</div>'

# We'll use a regex sub, but we only want to replace the first part before the next faq-inner-item.
# A better way is to split/replace or just use non-greedy matching.
match = re.search(r'(<div class="faq-inner-item">\s*<div class="faq-inner-title">¿Cómo instalar la App\?</div>.*?)<div class="faq-inner-item">', text, re.DOTALL)
if match:
    old_block = match.group(1)
    new_text = text.replace(old_block, replacement + "\n            ")
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Replaced FAQ block successfully.")
else:
    print("Failed to find block.")
