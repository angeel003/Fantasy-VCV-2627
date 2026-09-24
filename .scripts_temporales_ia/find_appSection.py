with open('dev.html', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        if 'id="appSection"' in line:
            print(repr(line))

