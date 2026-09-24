import re

manifest_tag = """<title>Fantasy VCV 26/27</title>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#783b7a">"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if 'rel="manifest"' not in html:
        html = html.replace('<title>Fantasy VCV 26/27</title>', manifest_tag)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

