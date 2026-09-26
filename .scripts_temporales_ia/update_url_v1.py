import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r'const scriptURL = "https://script\.google\.com/macros/s/.*?/exec";',
    'const scriptURL = "https://script.google.com/macros/s/AKfycbyw9L6Te3q2ibdRBaaAwaiPpEPWLbsNdb8JA9yO272DBHgxaZA2l3TLkH9ofAXlQiWfAg/exec";',
    text
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Script URL updated')
