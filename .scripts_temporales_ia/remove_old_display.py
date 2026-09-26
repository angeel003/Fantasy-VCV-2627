import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_display = r"""<div class="row mb-3" style="background:var(--bg-general); border: 2px solid var(--vcv-morado); padding:15px; border-radius:8px; align-items:center;">
                <div class="col-md-12 text-center" style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 8px;">
                    <div style="font-size:1.4rem; font-weight:bold; color:var(--vcv-morado);" id="displayJugador"></div>
                    <div id="displayBadges" style="display:flex; flex-direction:row; flex-wrap:wrap; justify-content:center; align-items:center; gap:6px;"></div>
                </div>
                
            </div>"""

text = text.replace(old_display, "")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Old display removed!")
