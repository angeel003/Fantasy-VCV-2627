import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the CSS for badge-exjugador
text = re.sub(r'\.badge-exjugador \{ filter: grayscale\(100%\) brightness\(0%\); \}', r'.badge-exjugador { filter: grayscale(100%) opacity(0.6) brightness(1.2); }', text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated index.html')
