import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.search(r'id=[\'"]loginSection[\'"]', text)
if m:
    idx = m.start()
    print(text[max(0, idx-100):idx+500])
