import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'<div class="faq-container"[^>]*>', text)
if match:
    print(match.group(0))
