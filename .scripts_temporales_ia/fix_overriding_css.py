import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """    .sign-btn-v2.selected.sign-plus-v2 {
      background: var(--primary-color);
      color: #fff;
      border-color: var(--primary-hover);
    }
    .sign-btn-v2.selected.sign-minus-v2 {
      background: rgba(231, 76, 60, 0.2);
      color: var(--danger);
      border-color: var(--danger);
    }"""

if target in text:
    text = text.replace(target, '')
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Removed overriding CSS")
else:
    print("Not found")
