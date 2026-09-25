import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('_sets"')
print(text[start-50:start+600].encode('ascii', 'ignore').decode('ascii'))
