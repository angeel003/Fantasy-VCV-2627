import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = r'<div class="header-subtitle" style="display:flex; align-items:center; gap:5px; flex-wrap:wrap; margin-top:4px;">\s*<span id="h2-user-name".*?</span>\s*<span id="h2-user-handle".*?</span>\s*<div id="h2-user-badges".*?</div>\s*</div>'

new = r"""<div class="header-subtitle" style="display:flex; align-items:center; gap:5px; flex-wrap:wrap; margin-top:4px;">
            <span style="color: #a1a1aa; font-weight:500;">Valladolid Club Voleibol</span>
          </div>"""

text = re.sub(target, new, text, flags=re.DOTALL)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('index.html', 'r', encoding='utf-8') as f:
    text2 = f.read()
text2 = re.sub(target, new, text2, flags=re.DOTALL)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text2)

print('Updated headers')
