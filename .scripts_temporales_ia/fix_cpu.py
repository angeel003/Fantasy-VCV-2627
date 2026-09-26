import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the innerHTML spam with a check
old_inner = "inputs.innerHTML = '<div style=\"text-align:center; margin-top:15px; padding:12px; background:var(--bg-input); border-radius:12px; border:1px dashed var(--border-color);\"><span style=\"font-size: 0.85rem; color: var(--text-muted); font-weight:bold;\">El plazo para predecir este partido está cerrado.</span></div>';"
new_inner = "if(!inputs.querySelector('span') || inputs.querySelector('span').innerText !== 'El plazo para predecir este partido está cerrado.') { " + old_inner + " }"

text = text.replace(old_inner, new_inner)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed innerHTML spam.")
