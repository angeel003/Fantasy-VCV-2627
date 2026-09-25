with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('function iniciarReloj')
print(text[start:start+1500].encode('ascii', 'ignore').decode('ascii'))
