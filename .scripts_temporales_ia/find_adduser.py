import re
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('action === "add_user"')
if idx == -1: idx = text.find("action === 'add_user'")
print(text[max(0, idx-50):idx+1500].encode('ascii', 'ignore').decode())

