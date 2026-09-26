import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = "action: 'guardar'"
new = "action: 'save'"

if target in text:
    text = text.replace(target, new)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed action payload to 'save'")
else:
    print("Target not found")
