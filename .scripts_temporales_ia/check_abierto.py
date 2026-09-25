with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('if (eq.estado === "ABIERTO") {')
print(text[max(0, start-200):start].encode('ascii', 'ignore').decode('ascii'))
