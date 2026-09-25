import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m1 = re.search(r'<option value="3-0">.*?</option>', text)
m2 = re.search(r'<option value="0-3">.*?</option>', text)
print(m1.group(0))
print(m2.group(0))
