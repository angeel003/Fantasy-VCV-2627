with open('prototipo_stitch.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
historial = re.search(r'<section class="view-section" id="view-historial">.*?</section>', text, re.DOTALL)
if historial:
    print('HISTORIAL HTML:', historial.group(0)[:1500])

calendario = re.search(r'<section class="view-section" id="view-calendario">.*?</section>', text, re.DOTALL)
if calendario:
    print('\nCALENDARIO HTML:', calendario.group(0)[:1500])
