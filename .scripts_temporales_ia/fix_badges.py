import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_badge_logic = r"""// NO tooltips, NO onclick for the top header badges! Just visual.
                insigniasH2Html += `<div class="${cssColorClass}" style="width:14px; height:14px; border-radius:50%; display:flex; align-items:center; justify-content:center;"><img src="${URL_BADGE_GENERIC}" style="width:8px; height:8px; filter:brightness(0) invert(1);"></div>`;"""

new_badge_logic = r"""// NO tooltips, NO onclick for the top header badges! Just visual.
                insigniasH2Html += `<img src="${URL_BADGE_GENERIC}" class="${cssColorClass}" style="width:14px; height:14px;">`;"""

text = text.replace(old_badge_logic, new_badge_logic)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed badges")
