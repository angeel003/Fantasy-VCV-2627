import re
import shutil

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the scriptURL for PROD
dev_url_pattern = r'const scriptURL = "https://script\.google\.com/macros/s/[^"]+/exec";'
prod_url = 'const scriptURL = "https://script.google.com/macros/s/AKfycbyw9L6Te3q2ibdRBaaAwaiPpEPWLbsNdb8JA9yO272DBHgxaZA2l3TLkH9ofAXlQiWfAg/exec";'

html = re.sub(dev_url_pattern, prod_url, html)

# We NO LONGER DISABLE the APK button in PROD! It remains as is in dev.html

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    print("Successfully built index.html from dev.html (with APK ENABLED)")

# 3. Sync Backend Script
shutil.copyfile('script-dev/Código.js', 'script-prod/Código.js')
print("Successfully copied script-dev to script-prod")

