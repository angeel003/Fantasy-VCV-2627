with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'if (action === "login" || action === "get_data") {' in line:
        # Delete from here to the next '}' that closes this block
        for j in range(i, i+15):
            if 'miNombreReal = mapNombresReales' in lines[j]:
                break
            lines[j] = ''
        break

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

