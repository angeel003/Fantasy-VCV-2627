import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'style.display' in line:
        print(f"Line {i+1}: {line.strip()}")
