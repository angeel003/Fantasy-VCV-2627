with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function onEdit')
if idx != -1:
    print(text[idx:idx+4000].encode('ascii', 'ignore').decode())

