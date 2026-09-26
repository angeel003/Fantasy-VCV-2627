with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('teams-versus-container-v2')
start = text.find('teams-versus-container-v2', start + 10)
print(text[start-2000:start+2000].encode('ascii', 'ignore').decode('ascii'))
