with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('body { font-family: \'Segoe UI\', Tahoma, sans-serif; background: var(--bg-general); margin: 0; color: var(--vcv-negro); }', 'body { font-family: \'Segoe UI\', Tahoma, sans-serif; background: var(--bg-general); margin: 0; color: var(--vcv-negro); overflow-x: hidden; }')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("overflow-x hidden added")
