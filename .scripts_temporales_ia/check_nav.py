with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<nav')
end = text.find('</nav>')
if start != -1:
    print(text[start:end+6].encode('ascii', 'ignore').decode('ascii'))
