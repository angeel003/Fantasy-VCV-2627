with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<li>Acertar el <b>Resultado Exacto (Sets)</b>:')
if start != -1:
    end = text.find('`;', start)
    chunk = text[start:end]
    
    new_chunk = r"""<li>Acertar el <b>Resultado Exacto (Sets)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.sets} pts</span></li>
                        <li>Acertar el <b>Ganador del partido</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.ganador} pts</span></li>
                        <li>Acertar la <b>Diferencia de puntos exacta</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_exacta} pts</span> extra</li>
                        <li><b>Aproximarse a la diferencia</b> (margen de error de ${data.reglas.max_dist} pts): <span style="color:var(--vcv-rojo); font-weight:bold;">Puntos proporcionales</span> a tu cercanía</li>
                    """
    
    text = text[:start] + new_chunk + text[end:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed index.html directly")
