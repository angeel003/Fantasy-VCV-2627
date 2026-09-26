import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('id="e${eq.id_partido}_sets"')
if idx != -1:
    sys.stdout.buffer.write(text[max(0, idx-500):idx+500].encode('utf-8'))
