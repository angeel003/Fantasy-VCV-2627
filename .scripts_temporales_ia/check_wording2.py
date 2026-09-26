import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'ptsText = pSig ===' in l:
        print(f'{i-1}: {lines[i-1].strip()}')
        print(f'{i}: {lines[i].strip()}')
        print(f'{i+1}: {lines[i+1].strip()}')
        print(f'{i+2}: {lines[i+2].strip()}')
