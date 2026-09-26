import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('id="loginSection"')
if start != -1: sys.stdout.buffer.write(text[start:start+4000].encode('utf-8'))
