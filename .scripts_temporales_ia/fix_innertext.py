import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r'valSpan\.innerText = next;',
    r'if (valSpan.tagName === "INPUT") valSpan.value = next; else valSpan.innerText = next;',
    text
)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
