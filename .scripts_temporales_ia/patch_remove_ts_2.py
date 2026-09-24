with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "if (action === \"login\" || action === \"get_data\") {" in line and "Registrar último Acceso" in new_lines[-1]:
        new_lines.pop() # remove the comment
        skip = True
        continue
    if skip:
        if line.strip() == "}":
            # Count opening vs closing brackets if needed, but since we know it's a 8-9 line block:
            pass
        if "cache.put(" in line or "setValue(new Date())" in line:
            pass
        if "var miNombreReal =" in line:
            skip = False
            new_lines.append(line)
        continue
    new_lines.append(line)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

