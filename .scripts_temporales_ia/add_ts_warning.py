import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Increase size of timer
text = text.replace('id="relojTotales" style="font-size:0.75rem;', 'id="relojTotales" style="font-size:0.95rem;')

# 2. Add the warning box
idx_desc = text.find('puntos totales</span> acumulados a final de temporada.')
if idx_desc != -1:
    idx_end_p = text.find('</p>', idx_desc)
    if idx_end_p != -1:
        warning_html = '''
                <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 10px 12px; margin-bottom: 15px; border-radius: 4px;">
                    <div style="font-weight: 900; color: #ef4444; font-size: 0.85rem; margin-bottom: 4px; display: flex; align-items: center; gap: 5px;">
                        <span style="font-size: 1rem;">🤫</span> ALTO SECRETO
                    </div>
                    <div style="color: var(--text-main); font-size: 0.8rem; line-height: 1.4;">
                        No todo el mundo puede ver esta sección. Si estás viéndola, considérate un afortunado... <strong>¡shhh!</strong>
                    </div>
                </div>'''
        text = text[:idx_end_p + 4] + warning_html + text[idx_end_p + 4:]
        
with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('SUCCESS')
