import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('id="carteleraSection"')
if idx != -1:
    sys.stdout.buffer.write(text[idx:idx+250].encode('utf-8'))
