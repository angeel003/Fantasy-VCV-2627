import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

for sid in ['carteleraSection', 'clasificacionesSection', 'historialSection', 'calendarioSection', 'enlacesRfevbSection', 'prediccionesTotalesSection']:
    m = re.search(r'<(div|section)[^>]*?id="' + sid + '"', text)
    if m:
        print(f"{sid} is a {m.group(1)}")
    else:
        print(f"{sid} not found")
