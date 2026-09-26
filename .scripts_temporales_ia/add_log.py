import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = "if (data.predicciones_usuario && data.predicciones_usuario[eq.id_partido]) {"
new = """console.log('Preds para ' + eq.id_partido + ':', data.predicciones_usuario ? data.predicciones_usuario[eq.id_partido] : 'none');
                if (data.predicciones_usuario && data.predicciones_usuario[eq.id_partido]) {"""

if target in text:
    text = text.replace(target, new)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added console log")
else:
    print("Target not found")
