with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('● Todos', 'Todos')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed dot symbol from Todos")
