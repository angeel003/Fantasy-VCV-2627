import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('id="prediccionesTotalesSection"')
if idx != -1:
    sys.stdout.buffer.write(text[max(0, idx-1000):idx].encode('utf-8'))
