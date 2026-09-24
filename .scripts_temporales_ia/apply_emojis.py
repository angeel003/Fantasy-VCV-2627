import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Cartelera
old_cart_1 = '<h2 id="tituloPrincipalSeccion">Mis Predicciones</h2>'
new_cart_1 = '<h2 id="tituloPrincipalSeccion">🏐 Cartelera de Partidos</h2>\n        <p style="color:#555; margin-bottom:20px; font-weight: 500; font-size: 0.95rem;">Predice los resultados de tus equipos favoritos esta jornada.</p>'
html = html.replace(old_cart_1, new_cart_1)

# Remove the description that might have been accidentally inserted inside the form
html = re.sub(r'<h2>Cartelera de Partidos</h2>\s*<p[^>]*>.*?</p>', '', html)

# 2. Ranking
old_rank = '<h2>Ranking</h2>\n<p style="color:#555; margin-bottom:20px;">Clasificación actual de nuestras ligas privadas según los puntos conseguidos.</p>'
new_rank = '<h2>🏆 Ranking</h2>\n<p style="color:#555; margin-bottom:20px; font-weight: 500; font-size: 0.95rem;">Clasificación actual de nuestras ligas privadas según los puntos conseguidos.</p>'
html = html.replace(old_rank, new_rank)
# fallback if it's just <h2>Ranking</h2>
html = re.sub(r'<h2>Ranking</h2>(?![\s\S]*🏆)', new_rank, html)


# 3. Enlaces
old_enlaces = '<h2>Enlaces Rfevb</h2>\n<p style="color:#555; margin-bottom:25px;">Consulta cómo van las ligas reales de nuestros equipos en las webs oficiales de la Federación.</p>'
new_enlaces = '<h2>🔗 Enlaces Rfevb</h2>\n<p style="color:#555; margin-bottom:25px; font-weight: 500; font-size: 0.95rem;">Consulta cómo van las ligas reales de nuestros equipos en las webs oficiales de la Federación.</p>'
html = html.replace(old_enlaces, new_enlaces)
html = re.sub(r'<h2>Enlaces Rfevb</h2>(?![\s\S]*🔗)', new_enlaces, html)

# 4. Mis Predicciones (Historial)
old_historial = '<h2>Mis Predicciones</h2>\n<p style="color:#555; margin-bottom:20px;">Historial completo de tus aciertos y puntos conseguidos en jornadas anteriores.</p>'
new_historial = '<h2>✅ Mis Predicciones</h2>\n<p style="color:#555; margin-bottom:20px; font-weight: 500; font-size: 0.95rem;">Historial completo de tus aciertos y puntos conseguidos en jornadas anteriores.</p>'
html = html.replace(old_historial, new_historial)
html = re.sub(r'<h2>Mis Predicciones</h2>(?![\s\S]*✅)(?!.*id="tituloPrincipalSeccion")', new_historial, html)

# 5. Próximos encuentros
old_calendario = '<h2>Próximos encuentros</h2>\n<p style="color:#555; margin-bottom:20px;">Calendario con todos los horarios y fechas de los partidos futuros programados.</p>'
new_calendario = '<h2>📅 Próximos encuentros</h2>\n<p style="color:#555; margin-bottom:20px; font-weight: 500; font-size: 0.95rem;">Calendario con todos los horarios y fechas de los partidos futuros programados.</p>'
html = html.replace(old_calendario, new_calendario)
html = re.sub(r'<h2>Próximos encuentros</h2>(?![\s\S]*📅)', new_calendario, html)

# 6. Top Secret
old_totales = '<h2>Top Secret</h2>\n<p style="color:#555; margin-bottom:20px;">Predicción de los puntos totales acumulados a final de temporada de cada equipo.</p>'
new_totales = '<h2>🔮 Top Secret</h2>\n<p style="color:#555; margin-bottom:20px; font-weight: 500; font-size: 0.95rem;">Predicción de los puntos totales acumulados a final de temporada de cada equipo.</p>'
html = html.replace(old_totales, new_totales)
html = re.sub(r'<h2>Top Secret</h2>(?![\s\S]*🔮)', new_totales, html)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Emojis and descriptions applied successfully.")

