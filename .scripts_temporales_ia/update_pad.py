import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('padding: 15px !important;', 'padding: 10px !important;')
text = text.replace('padding-left: 0px !important;', 'padding: 0 !important;')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated padding to 10px")
