import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = [m.start() for m in re.finditer(r'data\.status === [\'"]success[\'"]\) {', text)]
for pos in matches:
    print('='*20)
    print(text[max(0, pos-200):min(len(text), pos+300)])
