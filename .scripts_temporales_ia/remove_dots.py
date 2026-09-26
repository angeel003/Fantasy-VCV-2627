import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'<span style="color: var\(--text-gold\);" class="diff-points-label">\.\.\.</span>', '', text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed ...")
