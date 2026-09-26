import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = """<details class="faq-details">
            <summary class="faq-summary">📱 Cómo instalar la App (Android / iOS)</summary>
            <div class="faq-content">
                <div style="font-size:0.9rem; text-align:left; line-height: 1.5; color:#444;">
                    <p style="margin-bottom:10px;">No necesitas descargar ningún archivo APK. Al entrar en esta web desde tu móvil, haz lo siguiente:</p>
                    <ul style="padding-left:20px; margin-bottom:0;">
                        <li style="margin-bottom:10px;"><b>En Android (Chrome):</b> Tocar los 3 puntitos arriba a la derecha > "Instalar aplicación" (o "Añadir a pantalla de inicio").</li>
                        <li><b>En iPhone (Safari):</b> Tocar el botón de compartir (el cuadrado con la flecha) > "Añadir a la pantalla de inicio".</li>
                    </ul>
                </div>
            </div>
        </details>"""

pattern = r'<details class="faq-details">\s*<summary class="faq-summary">📱 Cómo instalar la App \(Android / iOS\)</summary>.*?</details>'
match = re.search(pattern, text, re.DOTALL)
if match:
    text = text.replace(match.group(0), replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced FAQ block in index.html successfully.")
else:
    print("Failed to find block.")
