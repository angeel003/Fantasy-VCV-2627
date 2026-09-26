import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
m = re.findall(r'<div class="faq-inner-title">.*?</div>', text)
print(m)
