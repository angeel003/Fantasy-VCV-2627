import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r'`⏳ El plazo de predicciones finales cierra en: \$\{d\}d \$\{h\}h \$\{m\}m \$\{s\}s`',
    r'`⏳ Cierra en: ${d}d ${h}h ${m}m ${s}s`',
    text
)

text = re.sub(
    r'"🔒 PLAZO CERRADO\. Las predicciones son definitivas\."',
    r'"CERRADO"',
    text
)

# Fix background color of red text if it had one
text = re.sub(
    r'el\.style\.backgroundColor = \"#fde8e8\";',
    r'el.style.backgroundColor = "transparent";',
    text
)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated text for clock")
