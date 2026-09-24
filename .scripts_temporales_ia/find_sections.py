with open('dev.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'prediccionForm' in line or 'Cartelera' in line or 'Próximos Partidos' in line or 'Mis Resultados' in line:
        print(f"{i}: {line.strip()}")

