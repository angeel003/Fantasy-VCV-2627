with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('id="prediccionesTotalesSection" style="display:none;"', 'id="prediccionesTotalesSection"')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed inline display:none for prediccionesTotalesSection.')
