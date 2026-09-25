with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
import re
match = re.search(r'action === [\'"]login[\'"]', text)
if match:
    start = match.start()
    print(text[start:start+1500])
