with open('.scripts_temporales_ia/card.html', 'r', encoding='utf-8') as f:
    text = f.read()
    lines = text.split('\n')
    for i in range(max(0, len(lines)-20), len(lines)):
        print(f"Line {i+1}: " + lines[i].encode('ascii', 'ignore').decode('ascii'))
