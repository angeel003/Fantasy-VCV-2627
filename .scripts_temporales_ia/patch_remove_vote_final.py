with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if 'if (action === "vote_destacado") {' in line:
        skip = True
        continue
    if skip:
        if 'if (action === "save") {' in line:
            skip = False
            new_lines.append(line)
        continue
    new_lines.append(line)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

