with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace safely using strings
old_text = '<li>Puntos por acercarse al diferencial: decaen linealmente hasta llegar a <span style="color:var(--vcv-rojo); font-weight:bold;">${data.reglas.max_dist} pts de diferencia</span></li>'
new_text = '<li><b>Aproximarse a la diferencia</b> (margen de error de ${data.reglas.max_dist} pts): <span style="color:var(--vcv-rojo); font-weight:bold;">Puntos proporcionales</span> a tu cercanía</li>'

if old_text in text:
    text = text.replace(old_text, new_text)
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced safely!")
else:
    print("Text not found in dev.html")
    
