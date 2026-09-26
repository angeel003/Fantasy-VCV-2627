import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update viewport meta to disable zoom
old_meta = r'<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no, viewport-fit=cover">'
new_meta = r'<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, shrink-to-fit=no, viewport-fit=cover">'
if old_meta in text:
    text = text.replace(old_meta, new_meta)
else:
    # Try regex if slight variation
    text = re.sub(r'<meta name="viewport".*?>', new_meta, text, count=1)


# 2. Add touch-action manipulation globally to prevent double tap zoom delay
# We can inject this into body or general reset
text = re.sub(
    r'body \{ font-family: \'Segoe UI\', Tahoma, sans-serif;',
    r'a, button, input, select, textarea { touch-action: manipulation; }\n    body { font-family: \'Segoe UI\', Tahoma, sans-serif;',
    text
)

# 3. Limit appSection to 500px width to match "Hola Angel" block and header/footer
text = re.sub(
    r'#appSection \{\n        padding-top: 60px;\n        padding-bottom: 80px;\n    \}',
    r'#appSection {\n        padding-top: 60px;\n        padding-bottom: 80px;\n        max-width: 500px;\n        margin: 0 auto;\n        width: 100%;\n    }',
    text
)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated zoom and width constraints")
