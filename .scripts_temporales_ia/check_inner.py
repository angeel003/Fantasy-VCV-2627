import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if "document.getElementById('summary-text-' + idPart).innerText" in l:
        print(f'{i-5}: {lines[i-5].strip()}')
        print(f'{i-4}: {lines[i-4].strip()}')
        print(f'{i-3}: {lines[i-3].strip()}')
        print(f'{i-2}: {lines[i-2].strip()}')
        print(f'{i-1}: {lines[i-1].strip()}')
        print(f'{i}: {lines[i].strip()}')
