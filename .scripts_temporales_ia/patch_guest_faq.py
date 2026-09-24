import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

old_block = """                    <li><b>Nombre de usuario</b> deseado (necesario para iniciar sesión).</li>
                    <li><b>Nombre real o alias</b> (opcional, si quieres que se muestre en la clasificación).</li>
                    <li><b>Tu relación con el club:</b> si eres jugador (indica de qué equipo), entrenador, exjugador, etc., para añadirte tu logo de verificado.</li>
                    <li><b>Ligas privadas:</b> si quieres unirte a alguna clasificación en concreto ya creada con tus amigos/equipo.</li>
                    <li><b>Equipos a predecir:</b> a qué equipos quieres poder mandar predicciones (por defecto se te asignarán las categorías más altas del VCV).</li>"""

new_block = """                    <li><b>Nombre de usuario</b> deseado (ej: @juan_vcv).</li>
                    <li><b>Contraseña</b> deseada.</li>
                    <li><b>Relación con el club</b> (si juegas o entrenas, dinos en qué equipo/categoría) para añadir insignias a tu perfil.</li>
                    <li><b>Equipos</b> que te gustaría seguir y predecir.</li>
                    <li style="margin-top:5px;"><i>(Opcional)</i> <b>Liga Privada:</b> Puedes tener una clasificación privada con amigos. Escribe los usuarios de todos y los equipos que puntuarán en ella.</li>"""

html = html.replace(old_block, new_block)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print("Fixed FAQ block")

