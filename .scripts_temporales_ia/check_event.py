import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r"document\.getElementById\(['\"](?:btnLogin|loginForm)['\"]\)\.addEventListener", text)
if m:
    idx = m.start()
    print('Event listener:', text[idx:idx+500])
else:
    print('Not found')
