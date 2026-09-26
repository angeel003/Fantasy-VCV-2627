import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Inject the clock
text = re.sub(
    r'(<span class="team-role-v2"[^>]*>VISITANTE</span>\s*</div>\s*</div>)',
    r'\1\n                            <div style="text-align: center; margin-top: 10px; margin-bottom: 5px;">\n                                <div class="reloj-partido" data-ts="${eq.timestamp}" data-eq="${eq.id_partido}" style="display:inline-block;"></div>\n                            </div>',
    text
)

# 2. Rename "Pronóstico de sets" -> "Resultado"
text = text.replace('Pronóstico de sets', 'Resultado')

# 3. Update the guiaModal texts
old_guia_2 = '<p style="margin-bottom: 10px;"><b>2. Diferencia de puntos:</b> Es la suma total de la ventaja de puntos que consigue un equipo sumando todos los sets.</p>'
new_guia_2 = '<p style="margin-bottom: 10px;"><b>2. Diferencia de puntos:</b> Es la diferencia total de puntos al final del partido entre ambos equipos (la suma de todos los sets).</p>'

old_guia_3 = '<p style="margin-bottom: 0;"><b>3. Signo:</b> Indica si esa diferencia de puntos será a favor del VCV (+) o del equipo rival (-).</p>'
new_guia_3 = '<p style="margin-bottom: 0;"><b>3. Signo:</b> Indica si la diferencia de puntos será a favor (+) o en contra (-) del equipo <b>LOCAL</b>.</p>'

text = text.replace(old_guia_2, new_guia_2)
text = text.replace(old_guia_3, new_guia_3)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Clock injected and texts updated")
