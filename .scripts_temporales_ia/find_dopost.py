import re
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function doPost')
print(text[max(0, idx):idx+1500].encode('ascii', 'ignore').decode())

