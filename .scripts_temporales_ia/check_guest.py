import sys
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('id="btnGuest"')
if idx != -1:
    sys.stdout.buffer.write(text[max(0, idx-100):idx+300].encode('utf-8'))
