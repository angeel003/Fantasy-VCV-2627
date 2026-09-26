import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update static HTML
old_static = r"""<section id="prediccionesTotalesSection">
        <div style="padding: 14px; border-radius: 16px; background: linear-gradient\(to right, rgba\(93, 23, 137, 0\.4\), var\(--bg-card\), var\(--bg-card\)\); border: 1px solid var\(--border-color\); position: relative; overflow: hidden; box-shadow: 0 4px 6px -1px rgba\(0,0,0,0\.1\), 0 2px 4px -1px rgba\(0,0,0,0\.06\); margin-top: -12px; margin-bottom: 20px;">
          <div style="display: flex; align-items: center; justify-content: flex-start; font-size: 0\.75rem; margin-bottom: 12px;">
            <span style="display: inline-flex; align-items: center; font-weight: bold; padding: 3px 10px; border-radius: 9999px; background: rgba\(212, 175, 55, 0\.15\); color: var\(--vcv-dorado\); border: 1px solid rgba\(212, 175, 55, 0\.3\);">
              <span style="width: 6px; height: 6px; border-radius: 9999px; background: var\(--vcv-dorado\); margin-right: 6px; animation: pulse 2s cubic-bezier\(0\.4, 0, 0\.6, 1\) infinite;"></span> Misión Final
            </span>
          </div>
          
          <div>
            <h2 style="font-size: 1\.55rem; font-weight: 800; color: var\(--text-main\); margin:0; letter-spacing:-0\.5px; line-height:1\.1; text-align:left;">🔮 Top Secret</h2>
            <p style="font-size: 0\.85rem; color: var\(--text-muted\); margin: 6px 0 0 0; text-align:left;">
              Predicción de los <span style="color: var\(--vcv-dorado\); font-weight: 700;">puntos totales</span> acumulados a final de temporada\.
            </p>
          </div>
        </div>
        <div id="contenedorPrediccionesTotales"></div>
    </section>"""

new_static = r"""<section id="prediccionesTotalesSection">
        <details class="vcv-faq-master" style="margin-top:-12px; margin-bottom:20px; max-width:100%; border: 1px solid var(--border-color);">
            <summary style="padding:16px; display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.3rem;">🔒</span>
                    <span style="font-size:1.1rem; font-weight:900; color:var(--text-main); letter-spacing:0.5px;">TOP SECRET</span>
                </div>
                <div id="relojTotales" style="font-size:0.75rem; font-weight:800; color:#ef4444; text-align:right;">Calculando...</div>
            </summary>
            <div class="faq-content-v2" style="padding:0 15px 15px 15px; border-top:1px solid rgba(255,255,255,0.05);">
                <p style="font-size: 0.85rem; color: var(--text-muted); margin: 10px 0 15px 0; text-align:left;">
                  Predicción de los <span style="color: var(--vcv-dorado); font-weight: 700;">puntos totales</span> acumulados a final de temporada.
                </p>
                <div id="contenedorPrediccionesTotales"></div>
            </div>
        </details>
    </section>"""

text = re.sub(old_static, new_static, text)

# 2. Remove relojTotales from the JS generation
old_js = r"""let htmlTot = `
                <div id="relojTotales" style="font-size:1rem; font-weight:bold; padding:12px; background:var\(--bg-card-alt\); color:var\(--vcv-dorado\); border:1px solid var\(--border-color\); border-radius:12px; text-align:center; margin-bottom:20px;">
                    Calculando tiempo\.\.\.
                </div>`;"""
new_js = r"""let htmlTot = ``;"""

text = re.sub(old_js, new_js, text)


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Top Secret UI to details")
