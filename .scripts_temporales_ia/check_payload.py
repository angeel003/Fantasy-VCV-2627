import sys
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
if '"predicciones_usuario"' in text:
    print('Found')
else:
    print('Not found')
