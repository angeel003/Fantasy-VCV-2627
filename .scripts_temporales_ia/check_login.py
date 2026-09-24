with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('if (action === "login")')
print(text[max(0, idx):idx+2500].encode('ascii', 'ignore').decode())

