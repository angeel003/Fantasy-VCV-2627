import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("el.style.padding = '6px 12px';", "el.style.padding = '2px 6px';")
text = text.replace("el.style.fontSize = '0.75rem';", "el.style.fontSize = '0.65rem';")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Timer style updated!")
