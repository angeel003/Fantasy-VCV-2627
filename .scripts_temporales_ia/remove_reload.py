import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'<button\s*id="btnReload"[^>]*>[\s\S]*?</button>', '', text)
text = re.sub(r'document\.getElementById\(\'btnReload\'\)\.addEventListener\([^\)]+\)\s*=>\s*\{[\s\S]*?\}\);', '', text)
text = re.sub(r'document\.getElementById\(\'btnReload\'\)\.addEventListener\(\'click\',\s*function\(\)\s*\{[\s\S]*?\}\);', '', text)

# Just in case
text = re.sub(r'#btnReload\s*\{[^}]+\}', '', text)
text = re.sub(r'#btnReload:hover\s*\{[^}]+\}', '', text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("btnReload fully removed!")
