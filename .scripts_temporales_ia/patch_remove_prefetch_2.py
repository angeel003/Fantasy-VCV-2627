with open('dev.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if '// --- PRE-CALENTAMIENTO (PRE-FETCHING) ---' in line:
        skip = True
        continue
    if skip:
        if '}, 500);' in line:
            skip = False
        continue
    new_lines.append(line)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

