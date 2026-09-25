import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Title to "VCV Play 2627"
old_h2 = '<h2 style="font-size: 1.5rem; font-weight: 800; color:var(--text-main); margin-bottom:4px;">VCV Play</h2>'
new_h2 = '<h2 style="font-size: 1.5rem; font-weight: 900; color:var(--text-main); margin-bottom:4px; letter-spacing: -0.5px;">VCV Play <span style="color:var(--secondary-color);">2627</span></h2>'

# 2. Update subtitle
old_p = '<p style="font-size: 0.9rem; font-weight:500; color: var(--text-muted); margin-top: 4px;">Acceso oficial para la temporada 26/27</p>'
new_p = '<p style="font-size: 0.85rem; font-weight:600; color: var(--text-muted); margin-top: 4px;">La liga de pronósticos oficial del club</p>'

text = text.replace(old_h2, new_h2)
text = text.replace(old_p, new_p)

# 3. Rename Fantasy VCV to VCV Play in FAQ and HTML body (excluding script endpoints/etc.)
# We will just target the FAQ specific text.
old_faq1 = '¿Qué es el Fantasy VCV?'
new_faq1 = '¿Qué es VCV Play?'
text = text.replace(old_faq1, new_faq1)

# Just in case the unicode encoding is different:
text = text.replace('Qu&#233; es el Fantasy VCV?', 'Qu&#233; es VCV Play?')
text = text.replace('Qué es el Fantasy VCV?', 'Qué es VCV Play?')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Texts updated!")
