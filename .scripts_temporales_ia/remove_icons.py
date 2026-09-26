import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove FAB menu completely
fab_pattern = r'<!-- FAB MENU NAV[\s\S]*?</div>\s*<script>\s*function toggleFab\(\)[\s\S]*?setInterval\(checkFabVisibility,\s*1000\);\s*</script>'
text = re.sub(fab_pattern, '', text)

# Remove btnReload
reload_pattern = r'<button class="icon-btn"\s*id="btnReload"[\s\S]*?</button>'
text = re.sub(reload_pattern, '', text)

# Also, there's some JS that references btnReload, it's fine if it's display=none but better to remove
text = re.sub(r'document\.getElementById\(\'btnReload\'\)\.style\.display\s*=\s*"[^"]+";', '', text)
text = re.sub(r'document\.getElementById\(\'btnReload\'\)\.addEventListener\([^\)]+\);', '', text)


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
    
print("Removed lupa and brujula")
