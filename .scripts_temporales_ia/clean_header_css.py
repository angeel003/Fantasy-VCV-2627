import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the old CSS properly
text = re.sub(r'\.app-header-v2\s*\{.*?(?=\.vcv-card-v2)', '', text, flags=re.DOTALL)
text = re.sub(r'\.header-brand-v2\s*h1\s*\{.*?\}', '', text, flags=re.DOTALL)
text = re.sub(r'\.header-user-v2\s*\{.*?\}', '', text, flags=re.DOTALL)
text = re.sub(r'\.header-user-name\s*\{.*?\}', '', text, flags=re.DOTALL)
text = re.sub(r'\.header-user-handle\s*\{.*?\}', '', text, flags=re.DOTALL)
text = re.sub(r'\.header-badges-v2\s*img\s*\{.*?\}', '', text, flags=re.DOTALL)
text = re.sub(r'\.header-actions-v2\s*\{.*?\}', '', text, flags=re.DOTALL)
text = re.sub(r'\.bell-btn-v2\s*\{.*?\}', '', text, flags=re.DOTALL)
text = re.sub(r'\.bell-dot-v2\s*\{.*?\}', '', text, flags=re.DOTALL)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Old CSS cleaned")
