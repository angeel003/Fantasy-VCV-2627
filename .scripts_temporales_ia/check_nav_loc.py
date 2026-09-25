with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('class="bottom-nav-v2"')
print(text[start-200:start+300])
