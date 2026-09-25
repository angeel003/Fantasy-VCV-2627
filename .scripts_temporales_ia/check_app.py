with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('id="appSection"')
print(text[start:start+1500].encode('ascii', 'ignore').decode('ascii'))
