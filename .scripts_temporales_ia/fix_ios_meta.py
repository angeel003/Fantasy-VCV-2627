import re

old_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">'
new_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no, viewport-fit=cover">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Update viewport
    if 'viewport-fit=cover' not in html:
        html = html.replace(old_viewport, new_viewport)
    
    # Update btnLogout top
    html = html.replace('top:max(15px, env(safe-area-inset-top));', 'top:calc(15px + env(safe-area-inset-top, 20px));')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

