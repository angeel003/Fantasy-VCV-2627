with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = text.replace('<div id="loginSection" style="padding-top: calc(20px + env(safe-area-inset-top, 0px));">', '<div id="loginSection">')

css_rule = '#loginSection { display: flex; align-items: center; justify-content: center; padding-top: calc(40px + env(safe-area-inset-top, 0px)); padding-bottom: 40px; padding-left: 20px; padding-right: 20px; flex-direction: column; }'
text = re.sub(r'(#loginSection, #appSection, #adminPanelWrapper \{\s*animation: [^\}]+\})', r'\1\n    ' + css_rule, text)

# For header text cut off:
# Old padding: padding: calc(18px + env(safe-area-inset-top, 0px)) 20px 26px 20px;
# Let's increase it more, OR fix the flex/line-height issue on .header-title-text
# .header-title-text has `line-height: 1;`. Let's change it to `line-height: 1.2;` and adjust padding.
text = text.replace('padding: calc(18px + env(safe-area-inset-top, 0px)) 20px 26px 20px;', 'padding: calc(16px + env(safe-area-inset-top, 0px)) 20px 28px 20px;')
text = text.replace('line-height:1;', 'line-height:1.2; padding-bottom: 4px;')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Restored CSS')
