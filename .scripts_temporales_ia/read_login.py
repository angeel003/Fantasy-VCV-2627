with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="loginSection"')
end = text.find('id="appSection"', start)
print(text[max(0, start):end].encode('ascii', 'ignore').decode('ascii'))
