import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = "document.getElementById('summary-text-' + idPart).innerText = `${s} | ${p} pts | ${signText}`;"
if target in text:
    text = text.replace(target, '')
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Deleted innerText assignment")
else:
    print("Target not found")
