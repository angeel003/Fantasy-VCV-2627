with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find context around "clasificaciones" or "Ranking"
idx = text.find('clasificacionesSection')
if idx != -1:
    print(text[idx-500:idx+500].encode('ascii', 'ignore').decode('ascii'))
