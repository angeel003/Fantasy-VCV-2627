import re

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace the choppy transform animation with a smooth one that doesn't hold a transform matrix
    html = html.replace('100% { opacity: 1; transform: scale(1) translateY(0); }', 
                        '100% { opacity: 1; transform: none; }')
    
    # Also add standard smooth scrolling to body
    if 'html, body { scroll-behavior: smooth;' not in html:
        html = html.replace('body { font-family:', 'html, body { -webkit-overflow-scrolling: touch; overscroll-behavior-y: auto; }\n    body { font-family:')
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

