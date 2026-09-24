import re

with open('dev.html', 'r', encoding='utf-8') as f:
    dev_html = f.read()

prod_url = 'const scriptURL = "https://script.google.com/macros/s/AKfycbyw9L6Te3q2ibdRBaaAwaiPpEPWLbsNdb8JA9yO272DBHgxaZA2l3TLkH9ofAXlQiWfAg/exec";'

idx_html = re.sub(r'const scriptURL =.*?/exec";', prod_url, dev_html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_html)

