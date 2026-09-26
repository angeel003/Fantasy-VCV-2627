import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = "window.fetchSeguro(window.scriptURL,"
new = "fetchSeguro(scriptURL,"

if target in text:
    text = text.replace(target, new)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed fetchSeguro")
else:
    print("Target not found")
