import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="appSection"')
print(text[max(0, idx-10):idx+300])

