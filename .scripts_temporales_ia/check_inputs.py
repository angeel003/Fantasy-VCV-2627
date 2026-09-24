with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="row inputs-eq"')
if idx != -1:
    print(repr(text[idx:idx+1500].encode('ascii', 'ignore').decode()))
else:
    print('Not found')

