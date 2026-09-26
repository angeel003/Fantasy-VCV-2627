import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'document\.getElementById\(\'displayJugador\'\)\.innerHTML\s*=\s*"[^"]+"\s*\+\s*displayNom;', '', text)
text = re.sub(r'document\.getElementById\(\'displayBadges\'\)\.innerHTML\s*=\s*insigniasHeaderHtml;', '', text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("JS cleaned up to prevent crash")
