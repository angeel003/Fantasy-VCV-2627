with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add safe area margin to modal-card-v2
import re
text = re.sub(r'(\.modal-card-v2\s*\{[^}]*margin-bottom:\s*40px;)', r'\1 margin-top: calc(20px + env(safe-area-inset-top, 0px));', text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added safe area to modal-card-v2')
