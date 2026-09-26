import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('id="carteleraSection"')
if idx != -1:
    idx_end = text.find('</section>', idx)
    sys.stdout.buffer.write(text[max(0, idx_end-500):min(len(text), idx_end+100)].encode('utf-8'))
