with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="loginUsuario"')
print(text[max(0, start-200):start+700].encode('ascii', 'ignore').decode('ascii'))[max(0, start-200):start+1000])
