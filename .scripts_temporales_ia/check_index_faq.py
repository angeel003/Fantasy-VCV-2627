import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'(<div class="faq-inner-item">\s*<div class="faq-inner-title">¿Cómo instalar la App\?</div>.*?</div>\s*</div>\s*</div>)', text, re.DOTALL)
if match:
    print(match.group(1))
else:
    print("Not found")
