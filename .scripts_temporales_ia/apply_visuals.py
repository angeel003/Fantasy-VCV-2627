import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Colors
new_colors = """
    :root {
      --primary-color: #7b3382;
      --primary-hover: #8e3c96;
      --secondary-color: #d4af37;
      --secondary-hover: #e5bf43;
      --bg-surface: #190c1f;
      --bg-card: #271330;
      --bg-card-alt: #32193d;
      --bg-input: #1f0f26;
      --border-color: #4c2659;
      --border-glow: rgba(212, 175, 55, 0.4);
      --text-main: #f9f5fa;
      --text-muted: #b7a4be;
      --text-gold: #f3ce5e;
      --success: #2ecc71;
      --danger: #e74c3c;
    }
"""
text = re.sub(r':root\s*\{.*?\}', new_colors.strip(), text, count=1, flags=re.DOTALL)

# Also ensure #loginSection is min-height 100vh
text = re.sub(r'min-height:\s*80vh;', 'min-height: 100vh;', text)

# 2. Update Login Card Text
text = text.replace('<h2>Fantasy VCV 26/27</h2>', '<h2>VCV Play</h2>')
text = text.replace('<p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">Acceso oficial para jugadores y socios</p>', '<p style="font-size: 1rem; font-weight:700; color: var(--text-muted); margin-top: 4px;">26/27</p>')
text = text.replace('👀 Entrar como Invitado (Solo Lectura)', '👀 Entrar como Invitado')


# 3. Rewrite FAQ Container and Styles
# Add FAQ styles to CSS
faq_css = """
    /* FAQ V2 STYLES */
    .vcv-faq-master {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      margin-top: 15px;
      width: 100%;
      max-width: 360px;
      overflow: hidden;
      transition: all 0.3s ease;
    }
    .vcv-faq-master summary {
      padding: 16px;
      font-weight: 800;
      font-size: 0.95rem;
      color: var(--secondary-color);
      cursor: pointer;
      list-style: none;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .vcv-faq-master summary::-webkit-details-marker { display: none; }
    .vcv-faq-master summary::after {
      content: '+';
      font-size: 1.2rem;
      color: var(--secondary-color);
      transition: transform 0.2s ease;
    }
    .vcv-faq-master[open] summary::after {
      content: '−';
      transform: rotate(180deg);
    }
    .vcv-faq-master .faq-content-v2 {
      padding: 0 16px 16px 16px;
      color: var(--text-main);
      font-size: 0.85rem;
      line-height: 1.5;
    }
    .faq-inner-item {
      background: var(--bg-card-alt);
      border-radius: 12px;
      padding: 12px;
      margin-bottom: 12px;
      border: 1px solid var(--border-color);
    }
    .faq-inner-title {
      font-weight: 700;
      color: var(--text-gold);
      margin-bottom: 8px;
      font-size: 0.9rem;
    }
    .faq-inner-item input {
      background: var(--bg-input);
      color: var(--text-main);
      border: 1px solid var(--border-color);
    }
"""
text = text.replace('</style>', faq_css + '\n  </style>')

# Replace the HTML of FAQ
start_faq = text.find('<div class="faq-container">')
end_faq = text.find('</div>\n</div>\n\n<div id="appSection"')

new_faq_html = """<div class="faq-container" style="width:100%; max-width:360px; margin:0 auto; padding:0; background:transparent; border:none; box-shadow:none;">
    <details class="vcv-faq-master" id="masterFaq">
        <summary>Preguntas Frecuentes y Gestión</summary>
        <div class="faq-content-v2">
            
            <div class="faq-inner-item">
                <div class="faq-inner-title">¿Qué es el Fantasy VCV?</div>
                <div>Es la competición privada del club donde participamos prediciendo los resultados de nuestros equipos en cada jornada. ¡Demuestra quién sabe más de voleibol!</div>
            </div>

            <div class="faq-inner-item">
                <div class="faq-inner-title">¿Cómo van las puntuaciones?</div>
                <div>El sistema calcula tus puntos automáticamente al acabar la jornada comparándolo con los resultados oficiales. Sumarás puntos dependiendo de si aciertas el resultado exacto de los sets, si aciertas quién gana el partido, o de lo cerca que te quedes de la diferencia final de puntos. <b>(Una vez inicies sesión verás el apartado exacto con los puntos que se otorgan)</b>.</div>
            </div>

            <div class="faq-inner-item">
                <div class="faq-inner-title">¿Cómo instalar la App?</div>
                <div style="display:flex; justify-content:center; gap:10px; margin-bottom:15px; margin-top:10px;">
                    <button onclick="document.getElementById('os-android').style.display='block'; document.getElementById('os-ios').style.display='none'; this.style.opacity='1'; document.getElementById('btnIosTab').style.opacity='0.5';" class="btn btn-sm" style="background:#3DDC84; color:#000; font-weight:bold; flex:1;" id="btnAndroidTab">Android</button>
                    <button onclick="document.getElementById('os-ios').style.display='block'; document.getElementById('os-android').style.display='none'; this.style.opacity='1'; document.getElementById('btnAndroidTab').style.opacity='0.5';" class="btn btn-sm" style="background:#ffffff; color:#000; font-weight:bold; flex:1; opacity:0.5;" id="btnIosTab">iOS</button>
                </div>
                <div id="os-android" style="display:block;">
                    <p style="font-size:0.85rem; margin-bottom:10px;">Descarga el archivo APK e instálalo como una App nativa.</p>
                    <a href="files/app/fantasy-vcv-2627.apk" download class="btn btn-success btn-sm btn-block" style="font-weight:bold; border-radius:10px;">Descargar APK Oficial</a>
                </div>
                <div id="os-ios" style="display:none; text-align:left;">
                    <ol style="font-size:0.85rem; padding-left:20px; margin-bottom:0;">
                        <li style="margin-bottom:6px;">Abre esta web desde <b>Safari</b>.</li>
                        <li style="margin-bottom:6px;">Toca el icono de <b>Compartir</b>.</li>
                        <li>Selecciona <b>"Añadir a la pantalla de inicio"</b>.</li>
                    </ol>
                </div>
            </div>

            <div class="faq-inner-item">
                <div class="faq-inner-title">Gestionar mi contraseña</div>
                <p style="font-size:0.8rem; margin-bottom:10px;">Puedes cambiar tu contraseña introduciendo tus datos actuales y la nueva contraseña.</p>
                <input type="text" id="cpUsuario" class="form-control mb-2" placeholder="Tu usuario (@usuario)" required style="background:var(--bg-input); color:var(--text-main); border:1px solid var(--border-color);">
                <input type="password" id="cpOldPwd" class="form-control mb-2" placeholder="Contraseña actual" required style="background:var(--bg-input); color:var(--text-main); border:1px solid var(--border-color);">
                <input type="password" id="cpNewPwd" class="form-control mb-2" placeholder="Nueva contraseña" required style="background:var(--bg-input); color:var(--text-main); border:1px solid var(--border-color);">
                <input type="password" id="cpNewPwd2" class="form-control mb-2" placeholder="Repite nueva contraseña" required style="background:var(--bg-input); color:var(--text-main); border:1px solid var(--border-color);">
                <button class="btn btn-primary btn-sm btn-block mt-2" id="btnChangePwd" style="font-weight:bold; background:var(--primary-color); border:none;">Actualizar Contraseña</button>
                <div id="msgChangePwd" class="alert-box mt-2" style="padding:10px; display:none;"></div>
            </div>

            <div class="faq-inner-item">
                <div class="faq-inner-title">Cambiar mi usuario / nombre</div>
                <p style="font-size:0.8rem; margin-bottom:10px;">Rellena este formulario para solicitar el cambio en la base de datos.</p>
                <input type="text" id="rnUsuario" class="form-control mb-2" placeholder="Tu usuario actual (@usuario)" required style="background:var(--bg-input); color:var(--text-main); border:1px solid var(--border-color);">
                <input type="password" id="rnPwd" class="form-control mb-2" placeholder="Tu contraseña actual" required style="background:var(--bg-input); color:var(--text-main); border:1px solid var(--border-color);">
                <hr style="border-color:var(--border-color);">
                <input type="text" id="rnNewUser" class="form-control mb-2" placeholder="Nuevo @usuario (opcional)" style="background:var(--bg-input); color:var(--text-main); border:1px solid var(--border-color);">
                <input type="text" id="rnNewName" class="form-control mb-2" placeholder="Nuevo Nombre Real (opcional)" style="background:var(--bg-input); color:var(--text-main); border:1px solid var(--border-color);">
                <button class="btn btn-primary btn-sm btn-block mt-2" id="btnReqName" style="font-weight:bold; background:var(--primary-color); border:none;">Enviar Solicitud</button>
                <div id="msgReqName" class="alert-box mt-2" style="padding:10px; display:none;"></div>
            </div>

        </div>
    </details>"""

text = text[:start_faq] + new_faq_html + text[end_faq:]

# 4. Add scroll-to-center logic for the master FAQ
faq_js = """
    document.addEventListener("DOMContentLoaded", () => {
        const masterFaq = document.getElementById('masterFaq');
        if (masterFaq) {
            masterFaq.addEventListener('toggle', function() {
                if (this.open) {
                    setTimeout(() => {
                        this.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 150);
                }
            });
        }
    });
</script>
"""
text = text.replace('</script>\n</body>', faq_js + '</body>')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("v2.html updated with lighter colors, centered login, and master FAQ!")
