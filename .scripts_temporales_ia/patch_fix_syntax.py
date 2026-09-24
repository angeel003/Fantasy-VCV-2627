with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace(r"\'btnLogout\'", "'btnLogout'")

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

