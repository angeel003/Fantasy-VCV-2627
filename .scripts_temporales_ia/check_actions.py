import sys, re
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.findall(r'action === [\'"](.*?)[\'"]', text)
print(matches)
