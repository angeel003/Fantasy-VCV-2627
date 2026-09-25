with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
historial = re.search(r'function renderResultadosPasados\(todos\).*?function renderClasificaciones', text, re.DOTALL)
if historial:
    print('JS Historial:', historial.group(0)[:2000])
