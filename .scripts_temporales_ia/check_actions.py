import re
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'if \s*\(\s*action \s*===\s*["\']([^"\']+)["\']\s*\)', text)
print(matches)
