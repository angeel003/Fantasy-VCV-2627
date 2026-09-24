import re

with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace 80px with 15px
text = text.replace('scroll-margin-top: calc(80px + env(safe-area-inset-top, 0px));', 'scroll-margin-top: calc(15px + env(safe-area-inset-top, 0px));')

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated scroll-margin-top to 15px")
