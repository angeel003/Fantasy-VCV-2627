import re

with open('dev.html', 'r', encoding='utf-8') as f:
    dev_html = f.read()

# Extract the block of admin functions from dev.html
match = re.search(r'(function renderAdminPanel\(equipos\).*?)function getCategoryHTML', dev_html, re.DOTALL)
if match:
    admin_functions = match.group(1)
    
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_html = f.read()
        
    idx_html = re.sub(r'function renderAdminPanel\(equipos\).*?(?=function getCategoryHTML)', admin_functions, idx_html, flags=re.DOTALL)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx_html)
    print("Admin functions synced to index.html successfully.")
else:
    print("Could not find admin functions in dev.html")

