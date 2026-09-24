import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix past matches logic in Guest Mode
# Search for:
# let esPasado = eq.oficial_sets && eq.oficial_sets.includes("-");
# if (eq.estado === "CERRADO" || eq.visibilidad === "OCULTAR") esPasado = true;
old_esPasado = """let esPasado = eq.oficial_sets && eq.oficial_sets.includes("-");
                if (eq.estado === "CERRADO" || eq.visibilidad === "OCULTAR") esPasado = true;"""
new_esPasado = """let esPasado = eq.oficial_sets && eq.oficial_sets.includes("-");"""
html = html.replace(old_esPasado, new_esPasado)

# 2. Update Promo Banner Text
old_promo_ul = """<ul style="padding-left: 25px; margin-bottom: 15px; font-weight: bold;">
                        <li>Nombre de usuario (ej: @juan_vcv)</li>
                        <li>Contraseña deseada</li>
                        <li>Tu nombre real o mote</li>
                    </ul>"""
new_promo_ul = """<ul style="padding-left: 25px; margin-bottom: 15px; font-weight: bold; font-size: 0.95rem;">
                        <li>Nombre de usuario (ej: @juan_vcv)</li>
                        <li>Contraseña deseada</li>
                        <li>Tu relación con el club (ej: jugador/entrenador, indicando de qué equipo y categoría) para añadir insignias a tu perfil.</li>
                        <li>Qué equipos te gustaría seguir.</li>
                        <li style="margin-top:8px; font-weight:normal;"><i>(Opcional)</i> <b>Liga Privada:</b> Puedes tener una clasificación privada con tus amigos. Escribe en el correo los nombres de usuario de todos los que os queráis unir y qué equipos puntuarán en vuestra clasificación.</li>
                    </ul>"""
html = html.replace(old_promo_ul, new_promo_ul)

# 3. Update FAQ Text in Login Section
# Need to find the FAQ section. It looks like:
# <li><b>Nombre de usuario</b> deseado (necesario para iniciar sesión).</li>
# Let's replace the whole ul block in the FAQ.
old_faq_ul = """<ul style="margin-top: 5px; padding-left: 20px;">
                    <li><b>Nombre de usuario</b> deseado (necesario para iniciar sesión).</li>
                    <li><b>Contraseña</b> deseada.</li>
                    <li>Opcionalmente, tu <b>nombre real</b> o apodo si quieres que tus amigos te reconozcan en las clasificaciones.</li>
                </ul>"""
new_faq_ul = """<ul style="margin-top: 5px; padding-left: 20px;">
                    <li><b>Nombre de usuario</b> deseado (ej: @juan_vcv).</li>
                    <li><b>Contraseña</b> deseada.</li>
                    <li><b>Relación con el club</b> (si juegas o entrenas, dinos en qué equipo/categoría) para añadir insignias a tu perfil.</li>
                    <li><b>Equipos</b> que te gustaría seguir y predecir.</li>
                    <li style="margin-top:5px;"><i>(Opcional)</i> <b>Liga Privada:</b> Puedes tener una clasificación privada con amigos. Escribe los usuarios de todos y los equipos que puntuarán en ella.</li>
                </ul>"""
html = html.replace(old_faq_ul, new_faq_ul)

# 4. Remove "Cartelera Pública" title
# Guest login: document.getElementById('tituloPrincipalSeccion').innerText = "Cartelera Pública";
# Replace with hiding it
html = html.replace('document.getElementById(\'tituloPrincipalSeccion\').innerText = "Cartelera Pública";', "document.getElementById('tituloPrincipalSeccion').style.display = 'none';")

# Normal login needs to make sure it's shown again:
# Normal login sets `Mis Predicciones` but doesn't set display block.
# document.getElementById('tituloPrincipalSeccion').innerText = "Mis Predicciones";
html = html.replace('document.getElementById(\'tituloPrincipalSeccion\').innerText = "Mis Predicciones";', "document.getElementById('tituloPrincipalSeccion').innerText = \"Mis Predicciones\"; document.getElementById('tituloPrincipalSeccion').style.display = 'block';")


with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print("Patched requested texts and logic")

