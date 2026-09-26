import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. .modal-card-v2
text = text.replace('max-width: 360px;', 'max-width: 500px;')

# 2. .vcv-card-v2
# It appears multiple times, but the main one has background: var(--bg-card);
# We can just add it to all or the main one. Let's just find the main one.
pattern_vcv = r'(\.vcv-card-v2\s*\{[^}]*position: relative;)'
text = re.sub(pattern_vcv, r'\1\n      width: 100%;\n      max-width: 500px;\n      margin-left: auto;\n      margin-right: auto;', text)

# 3. .faq-container in CSS
text = text.replace('max-width: 800px;', 'max-width: 500px;')

# 4. inline styles with max-width:360px
text = text.replace('max-width:360px;', 'max-width:500px;')

# 5. header-container-v2
text = text.replace('max-width: 450px;', 'max-width: 500px;')

# 6. tables and containers
# tables have max-width: 900px; in CSS
text = text.replace('max-width: 900px;', 'max-width: 500px;')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied responsive max-widths")
