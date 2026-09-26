with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('id="bottomNavWrapperV2"')
print(text[start:start+1000])
