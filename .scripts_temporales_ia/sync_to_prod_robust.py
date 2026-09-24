import re
import shutil

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the scriptURL for PROD
dev_url_pattern = r'const scriptURL = "https://script\.google\.com/macros/s/[^"]+/exec";'
prod_url = 'const scriptURL = "https://script.google.com/macros/s/AKfycbyw9L6Te3q2ibdRBaaAwaiPpEPWLbsNdb8JA9yO272DBHgxaZA2l3TLkH9ofAXlQiWfAg/exec";'

html = re.sub(dev_url_pattern, prod_url, html)

# 2. Disable the APK button in PROD
dev_apk_btn = r'<a href="files/app/fantasy-vcv-2627\.apk"[^>]*>.*?Descargar APK Oficial</a>'
prod_apk_btn = '<a href="#" onclick="event.preventDefault();" class="btn btn-secondary btn-sm btn-block" style="font-weight:bold; border-radius:20px; cursor:not-allowed; opacity:0.7;">🤖 Descargar APK Oficial (Próximamente)</a>'

html = re.sub(dev_apk_btn, prod_apk_btn, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    print("Successfully built index.html from dev.html")

# 3. Sync Backend Script
shutil.copyfile('script-dev/Código.js', 'script-prod/Código.js')
print("Successfully copied script-dev to script-prod")
