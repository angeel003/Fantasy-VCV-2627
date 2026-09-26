import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the CSS for badge-exjugador
text = re.sub(r'\.badge-exjugador \{ filter: grayscale\(100%\) brightness\(0%\); \}', r'.badge-exjugador { filter: grayscale(100%) opacity(0.6) brightness(1.2); }', text)

# 2. Update the profile block content
old_title = r'<h2 style="font-size: 1\.15rem; font-weight: bold; color: var\(--text-main\); margin:0;">Pronósticos del Club</h2>\s*<p style="font-size: 0\.8rem; color: var\(--text-muted\); margin: 4px 0 0 0;">\s*Jugador: <span style="color: var\(--vcv-dorado\); font-weight: 700;">@\$\{currentUser\}</span> • \$\{data\.nombre_real !== currentUser \? data\.nombre_real : \'¡Demuestra quién sabe más!\'\}'

new_title = r'<h2 style="font-size: 1.15rem; font-weight: bold; color: var(--text-main); margin:0;">¡Hola ${data.nombre_real || currentUser}!</h2>\n                  <p style="font-size: 0.8rem; color: var(--text-muted); margin: 4px 0 0 0;">\n                    <span style="color: var(--vcv-dorado); font-weight: 700;">@${currentUser}</span> • ¡Demuestra quién sabe más!'

text = re.sub(old_title, new_title, text)

# 3. Update the progress bar to animate
old_bar = r'<div style="background: linear-gradient\(to right, var\(--vcv-morado\), var\(--vcv-dorado\)\); height: 100%; border-radius: 9999px; width: \$\{porcentaje\}%; transition: width 1s ease-in-out;"></div>'

new_bar = r'<style>\n                @keyframes fillProgress {\n                  from { width: 0%; }\n                  to { width: ${porcentaje}%; }\n                }\n                </style>\n                <div style="background: linear-gradient(to right, var(--vcv-morado), var(--vcv-dorado)); height: 100%; border-radius: 9999px; width: ${porcentaje}%; animation: fillProgress 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;"></div>'

text = re.sub(old_bar, new_bar, text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated v2.html')
