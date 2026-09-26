import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the input's width style in the points difference stepper
text = re.sub(
    r'width:100%; min-width:40px;',
    r'width:46px; max-width:46px;',
    text
)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated width")
