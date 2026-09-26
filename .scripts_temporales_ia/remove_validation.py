import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the numRellenos logic
idx_num = text.find('let numRellenos = (vSet !== "" ? 1 : 0) + (vPuntos !== "" ? 1 : 0) + (vSigno !== "" ? 1 : 0);')
if idx_num != -1:
    idx_end_num = text.find('}', idx_num) + 1
    text = text[:idx_num] + text[idx_end_num:]

# 2. Remove the validacionFallida check
idx_val = text.find('if (validacionFallida) {')
if idx_val != -1:
    idx_end_val = text.find('return; \n    }', idx_val) + 14
    text = text[:idx_val] + text[idx_end_val:]
    
# 3. Remove the initialization of validacionFallida
text = text.replace('let validacionFallida = false;\n', '')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('SUCCESS')
