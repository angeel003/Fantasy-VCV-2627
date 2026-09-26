import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = r'<h2 style="font-size: 1\.55rem; font-weight: 800; color: var\(--text-main\); margin:0; letter-spacing:-0\.5px; line-height:1\.1;">¡Hola \$\{data\.nombre_real \|\| currentUser\}!</h2>\s*<p style="font-size: 0\.8rem; color: var\(--text-muted\); margin: 4px 0 0 0;">\s*<span style="color: var\(--vcv-dorado\); font-weight: 700;">@\$\{currentUser\}</span> • ¡Demuestra quién sabe más!\s*</p>'

new_block = r"""<h2 style="font-size: 1.55rem; font-weight: 800; color: var(--text-main); margin:0; letter-spacing:-0.5px; line-height:1.1; text-align:left;">¡Hola ${data.nombre_real || currentUser}!</h2>
                  <p style="font-size: 0.85rem; color: var(--text-muted); margin: 4px 0 0 0; text-align:left;">
                    <span style="color: var(--vcv-dorado); font-weight: 700;">@${currentUser}</span>
                  </p>"""

if re.search(old_block, text):
    text = re.sub(old_block, new_block, text)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated text")
else:
    print("Could not find the block")
