import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """btn.innerText = '${isPredicted ? "Modificar Predicción" : "Guardar Predicción"}';"""
new = """btn.innerText = 'Guardar Predicción';"""

if target in text:
    text = text.replace(target, new)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed button text")
else:
    print("Target not found")
