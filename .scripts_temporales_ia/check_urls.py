import re

with open('dev.html', 'r', encoding='utf-8') as f:
    dev = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    prod = f.read()

dev_url = re.search(r'const SCRIPT_URL\s*=\s*[\'"]([^\'"]+)[\'"]', dev)
prod_url = re.search(r'const SCRIPT_URL\s*=\s*[\'"]([^\'"]+)[\'"]', prod)

print('dev URL:', dev_url.group(1) if dev_url else 'None')
print('prod URL:', prod_url.group(1) if prod_url else 'None')
