with open('partidos_vcv.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

header = lines[0]
seen_ids = set()
unique_lines = [header]

for line in lines[1:]:
    if not line.strip():
        continue
    cols = line.split('\t')
    id_partido = cols[0]
    
    if id_partido not in seen_ids:
        seen_ids.add(id_partido)
        unique_lines.append(line)
    else:
        print(f"Removed duplicate match: {id_partido} - {cols[2]} vs {cols[3]}")

# Write back TXT
with open('partidos_vcv.txt', 'w', encoding='utf-8') as f:
    f.writelines(unique_lines)

# Write back CSV (assuming same lines but with semicolons)
with open('partidos_vcv.csv', 'w', encoding='utf-8') as f:
    for line in unique_lines:
        f.write(line.replace('\t', ';'))

print(f"Done. Final file has {len(unique_lines)} lines (including header).")

