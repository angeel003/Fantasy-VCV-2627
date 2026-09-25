with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('prediccionesTotalesSection')
print(text[idx+2000:idx+4000])
