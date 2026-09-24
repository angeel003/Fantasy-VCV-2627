with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="app"')
print(text[max(0, idx):idx+2500].encode('ascii', 'ignore').decode())

