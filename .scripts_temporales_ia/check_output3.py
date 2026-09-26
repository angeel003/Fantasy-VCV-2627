import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('id="prediccionesTotalesSection"')
if idx != -1:
    sys.stdout.buffer.write(text[idx-20:idx+1500].encode('utf-8'))
