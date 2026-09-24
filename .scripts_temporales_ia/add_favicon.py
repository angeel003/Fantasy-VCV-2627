import re

favicon_tags = """<title>Fantasy VCV 26/27</title>
<link rel="icon" type="image/png" href="files/images/logo_vcv_tiny.png">
<link rel="apple-touch-icon" href="files/images/logo_vcv_tiny.png">"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # ensure we don't add it twice
    if 'rel="icon"' not in html:
        html = html.replace('<title>Fantasy VCV 26/27</title>', favicon_tags)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

