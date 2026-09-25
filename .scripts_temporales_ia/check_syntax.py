with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('for(var idPart in preds)')
print(text[max(0, idx-100):idx+800])
