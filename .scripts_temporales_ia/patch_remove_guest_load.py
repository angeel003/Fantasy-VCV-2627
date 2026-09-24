import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# In the Guest login flow, remove cargarDatosAntiguos()
html = re.sub(
    r'document\.getElementById\(\'btnLogout\'\)\.style\.display = "block";\s*cargarDatosAntiguos\(\);\s*iniciarRelojTotales\(\);',
    r'document.getElementById(\'btnLogout\').style.display = "block";\n            iniciarRelojTotales();',
    html, count=1
)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

