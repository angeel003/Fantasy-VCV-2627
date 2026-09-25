with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('MODALS PARA ALERTAS')
if start != -1:
    print(text[start-200:start+200])
else:
    print("MODALS PARA ALERTAS not found!")
