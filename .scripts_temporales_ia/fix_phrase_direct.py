with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<li>Acertar la <b>Diferencia de puntos exacta</b>')
if start != -1:
    end = text.find('</ul>', start)
    chunk = text[start:end]
    
    # We want to replace the LAST <li>...</li> in this chunk with the new one
    li_start = chunk.rfind('<li>')
    new_chunk = chunk[:li_start] + r"""<li><b>Aproximarse a la diferencia</b> (margen de error de ${data.reglas.max_dist} pts): <span style="color:var(--vcv-rojo); font-weight:bold;">Puntos proporcionales</span> a tu cercanía</li>
                    """
    
    text = text[:start] + new_chunk + text[end:]

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed directly")
