import re
with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

appSection = html[html.find('id="appSection"'):]
# Just print the IDs in order of appearance
import xml.etree.ElementTree as ET
# too malformed for ET, let's just find indices
sections = ['prediccionForm', 'clasificacionesSection', 'historialSection', 'prediccionesTotalesSection', 'calendarioSection', 'enlaces']
for sec in sections:
    print(f"{sec}: {html.find(sec)}")

