import re

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Make header relative
    html = html.replace('header { background: var(--vcv-morado);', 'header { position: relative; background: var(--vcv-morado);')
    
    # Change button position to something guaranteed to be visible (top: 45px)
    # The previous was: top:calc(15px + env(safe-area-inset-top, 20px));
    html = re.sub(r'top:calc\(15px \+ env\(safe-area-inset-top, 20px\)\);', 'top: 45px;', html)
    html = re.sub(r'top:max\(15px, env\(safe-area-inset-top\)\);', 'top: 45px;', html)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

