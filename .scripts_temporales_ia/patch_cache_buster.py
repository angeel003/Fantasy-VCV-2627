import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace scriptURL in fetch calls with a cache-busted URL and add cache: 'no-store'
html = html.replace("fetch(scriptURL, {", "fetch(scriptURL + '?t=' + new Date().getTime(), { cache: 'no-store',")

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

