with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('class="admin-match-box"')
if start != -1: print(text[start:start+500])
