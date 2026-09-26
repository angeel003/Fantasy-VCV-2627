import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove old timer
old_timer = r'<div class="reloj-partido" data-ts="\$\{eq\.timestamp\}" data-eq="\$\{eq\.id_partido\}" style="font-size:0\.75rem; font-weight:bold; padding:4px 8px; background:rgba\(212, 175, 55, 0\.1\); color:var\(--secondary-color\); border: 1px solid var\(--border-glow\); border-radius:4px; display:inline-block; margin-bottom:12px;">Calculando tiempo...</div>'
text = re.sub(old_timer, '', text)

# Inject new timer in the header
old_header = r"""<div class="match-header-strip-v2">
                                <span style="color: \$\{eq\.es_derby \? 'var\(--text-gold\)' : 'var\(--secondary-color\)'\}; font-weight: 800;">
                                  \$\{eq\.categoria\.toUpperCase\(\)\} \$\{eq\.es_derby \? ' DERBY' : ''\}
                                </span>"""

new_header = r"""<div class="match-header-strip-v2">
                                <div style="display:flex; align-items:center; gap:8px;">
                                    <span style="color: ${eq.es_derby ? 'var(--text-gold)' : 'var(--secondary-color)'}; font-weight: 800;">
                                      ${eq.categoria.toUpperCase()} ${eq.es_derby ? ' DERBY' : ''}
                                    </span>
                                    <div class="reloj-partido" data-ts="${eq.timestamp}" data-eq="${eq.id_partido}" style="font-size:0.65rem; font-weight:bold; padding:2px 6px; background:rgba(212, 175, 55, 0.1); color:var(--secondary-color); border: 1px solid var(--border-glow); border-radius:4px; display:inline-block;">Calculando tiempo...</div>
                                </div>"""

text = re.sub(old_header, new_header, text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Timer moved!")
