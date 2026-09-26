import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove Points Text block
text = re.sub(r'<!-- PUNTOS TEXT -->[\s\S]*?<!-- HIDDEN INPUTS -->', '<!-- HIDDEN INPUTS -->', text)

# 2. Remove the "..." and diff points labels inside the grid labels
text = re.sub(r'<span style="color: var\(--secondary-color\);" class="sets-points-label">.*?</span>', '', text)
text = re.sub(r'<span style="color: var\(--secondary-color\);" class="diff-points-label".*?</span>', '', text)

# 3. Change "Club" to "Perfil" in the nav and change icon
text = text.replace('<i data-lucide="shield"></i>\n            <span>Club</span>', '<i data-lucide="user"></i>\n            <span>Perfil</span>')

# 4. Remove the JS that updates these labels
text = re.sub(r'document\.querySelectorAll\(\'\.sets-points-label\'\)\.forEach.*?;\n', '', text)
text = re.sub(r'document\.querySelectorAll\(\'\.diff-points-label\'\)\.forEach.*?;\n', '', text)

# 5. Ensure "Diferencia de puntos" is used consistently
# Right now it might say "Diferencia de Puntos (Opcional)"
text = text.replace('Diferencia de Puntos (Opcional)', 'Diferencia de Puntos')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Modifications done.")
