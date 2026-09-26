import sys, re
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'SpreadsheetApp.flush(); // To guarantee it\'s written before responding'
if target in text:
    text = text.replace(target, '')
    with open('script-v2/Código.js', 'w', encoding='utf-8') as f2:
        f2.write(text)
    print("Removed flush from Código.js")
else:
    # Try a regex approach in case the comment was slightly different
    match = re.search(r'SpreadsheetApp\.flush\(\);.*?$', text, re.MULTILINE)
    if match:
        text = text[:match.start()] + text[match.end():]
        with open('script-v2/Código.js', 'w', encoding='utf-8') as f2:
            f2.write(text)
        print("Removed flush via regex from Código.js")
    else:
        print("Target flush not found")
