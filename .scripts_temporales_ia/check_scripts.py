with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script.*?>', text)
print(scripts)

print("Last 1000 chars of HTML:")
print(text[-1000:])
