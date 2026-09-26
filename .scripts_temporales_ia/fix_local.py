import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace eq.es_local with (eq.ubicacion === 'LOCAL')
text = re.sub(r'eq\.es_local', r"(eq.ubicacion === 'LOCAL')", text)

# Also fix the lupa and brujula in v2.html
# "quita los ismbolos de la lupa y la brujula, ya no tiene sentido tenerlos."
# Lupa: btnReload? No, lupa is a search bar maybe?
# Brujula is FAB menu? Let's check where they are in the HTML.
with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Replaced es_local with eq.ubicacion === 'LOCAL'")
