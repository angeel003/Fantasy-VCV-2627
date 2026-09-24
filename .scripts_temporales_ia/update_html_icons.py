import re

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace('href="files/images/logo_vcv_tiny.png"', 'href="files/images/logo_vcv_circle.png"')
    html = html.replace('<link rel="apple-touch-icon" href="files/images/logo_vcv_circle.png">', '<link rel="apple-touch-icon" href="files/images/logo_vcv_square_white.png">')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

