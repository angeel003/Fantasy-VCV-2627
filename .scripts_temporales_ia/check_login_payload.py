with open('script-prod/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('clasificacionesFormateadas')
if idx != -1:
    print(text[max(0, idx-200):idx+400].encode('ascii', 'ignore').decode())

