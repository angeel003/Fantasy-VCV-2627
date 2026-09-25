import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the H2 (VCV Play)
old_h2 = '<h2 style="font-size: 1.3rem; font-weight: 800; color:var(--text-main); margin-bottom:4px;">Fantasy VCV 26/27</h2>'
new_h2 = '<h2 style="font-size: 1.5rem; font-weight: 800; color:var(--text-main); margin-bottom:4px;">VCV Play</h2>'

# Fix the P (Acceso oficial...)
old_p = '<p style="font-size: 1rem; font-weight:700; color: var(--text-muted); margin-top: 4px;">26/27</p>'
new_p = '<p style="font-size: 0.9rem; font-weight:500; color: var(--text-muted); margin-top: 4px;">Acceso oficial para la temporada 26/27</p>'

if old_h2 in text:
    text = text.replace(old_h2, new_h2)
    print("Replaced H2 successfully.")
else:
    print("H2 not found.")

if old_p in text:
    text = text.replace(old_p, new_p)
    print("Replaced P successfully.")
else:
    print("P not found.")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
