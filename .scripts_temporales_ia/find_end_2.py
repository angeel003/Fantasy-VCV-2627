with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('prediccionesTotalesSection')
print(text[idx+1000:idx+2500])
