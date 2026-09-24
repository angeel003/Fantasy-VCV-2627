import re

filename = 'index.html'

with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the active APK download button with a disabled "Proximamente" version
active_btn_regex = r'<a href="files/app/fantasy-vcv-2627\.apk" download class="btn btn-success btn-sm btn-block" style="font-weight:bold; border-radius:20px;">📥 Descargar APK Oficial</a>'
disabled_btn = '<a href="#" onclick="event.preventDefault();" class="btn btn-secondary btn-sm btn-block" style="font-weight:bold; border-radius:20px; cursor:not-allowed; opacity:0.7;">📥 Descargar APK Oficial (Próximamente)</a>'

html = re.sub(active_btn_regex, disabled_btn, html)

# Just in case the emoji didn't match
active_btn_regex_2 = r'<a href="files/app/fantasy-vcv-2627\.apk" download class="btn btn-success btn-sm btn-block" style="font-weight:bold; border-radius:20px;">.*?Descargar APK Oficial</a>'
html = re.sub(active_btn_regex_2, disabled_btn, html)


with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print("index.html updated successfully.")

