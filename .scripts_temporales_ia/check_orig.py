with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('id="loginSection"')
end = text.find('id="appSection"', start)
print(text[max(0, start-100):start+200])
print('---------')
print(text[max(0, end-200):end+100])
