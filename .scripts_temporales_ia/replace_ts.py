with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = '<section id="prediccionesTotalesSection">'
end_marker = '</section>'
idx_start = text.find(start_marker)
idx_end = text.find(end_marker, idx_start)

if idx_start != -1 and idx_end != -1:
    new_section = '''<section id="prediccionesTotalesSection">
        <details class="vcv-faq-master" style="margin-top:-12px; margin-bottom:20px; max-width:100%; border: 1px solid var(--border-color);">
            <summary style="padding:16px; display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.3rem;">🔒</span>
                    <span style="font-size:1.1rem; font-weight:900; color:var(--text-main); letter-spacing:0.5px;">TOP SECRET</span>
                </div>
                <div id="relojTotales" style="font-size:0.75rem; font-weight:800; color:#ef4444; text-align:right;">Calculando...</div>
            </summary>
            <div class="faq-content-v2" style="padding:0 15px 15px 15px; border-top:1px solid rgba(255,255,255,0.05);">
                <p style="font-size: 0.85rem; color: var(--text-muted); margin: 10px 0 15px 0; text-align:left;">
                  Predicción de los <span style="color: var(--vcv-dorado); font-weight: 700;">puntos totales</span> acumulados a final de temporada.
                </p>
                <div id="contenedorPrediccionesTotales"></div>
            </div>
        </details>
    </section>'''
    
    text = text[:idx_start] + new_section + text[idx_end + len(end_marker):]

    # Remove the JS relojTotales block
    js_start = text.find('<div id="relojTotales"')
    if js_start != -1:
        js_block_start = text.rfind('let htmlTot = `', 0, js_start)
        js_block_end = text.find('`;', js_start) + 2
        if js_block_start != -1 and js_block_end != -1:
            text = text[:js_block_start] + 'let htmlTot = "";' + text[js_block_end:]
            
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('SUCCESS')
