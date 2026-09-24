with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('else if (sheet.getName() === "Usuarios")')
if idx != -1:
    print(text[idx:idx+2500].encode('ascii', 'ignore').decode())

