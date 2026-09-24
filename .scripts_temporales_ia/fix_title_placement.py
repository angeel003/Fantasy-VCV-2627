import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Locate the title and description
title_regex = r'(\s*<h2 id="tituloPrincipalSeccion">.*?</h2>\s*<p[^>]*>.*?</p>\s*)'
match_title = re.search(title_regex, html, re.DOTALL)

if match_title:
    title_chunk = match_title.group(1)
    # Remove it from its current position
    html = html.replace(title_chunk, '')
    
    # We want to place it RIGHT BEFORE the blue div
    blue_div_start = html.find('<div style="background-color: #e3f2fd;')
    
    if blue_div_start != -1:
        # Check if the title is actually better placed right before the blue div
        html = html[:blue_div_start] + title_chunk.strip() + '\n                ' + html[blue_div_start:]

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Moved title OUTSIDE the blue div.")

