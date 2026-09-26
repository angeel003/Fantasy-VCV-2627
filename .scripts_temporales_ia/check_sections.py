import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
sections = re.findall(r'<section[^>]*style="[^"]*display\s*:\s*none[^"]*"[^>]*>', text)
print(sections)
