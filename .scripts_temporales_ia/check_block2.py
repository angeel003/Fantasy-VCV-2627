with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
import re
m = re.search(r'motivos\.push\("Dif\. acercada', text)
if m:
    print('YES')
else:
    print('NO')

