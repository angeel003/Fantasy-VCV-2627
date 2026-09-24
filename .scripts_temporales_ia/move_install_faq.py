import re

faq_app_section = """
        <details class="faq-details">
            <summary class="faq-summary">📱 Cómo instalar la App (Android / iOS)</summary>
            <div class="faq-content">
                <div style="display:flex; justify-content:center; gap:10px; margin-bottom:15px;">
                    <button onclick="document.getElementById('os-android').style.display='block'; document.getElementById('os-ios').style.display='none'; this.style.opacity='1'; document.getElementById('btnIosTab').style.opacity='0.5';" class="btn btn-sm" style="background:#3DDC84; color:white; font-weight:bold; flex:1;" id="btnAndroidTab">Android</button>
                    <button onclick="document.getElementById('os-ios').style.display='block'; document.getElementById('os-android').style.display='none'; this.style.opacity='1'; document.getElementById('btnAndroidTab').style.opacity='0.5';" class="btn btn-sm" style="background:#000000; color:white; font-weight:bold; flex:1; opacity:0.5;" id="btnIosTab">iOS (iPhone)</button>
                </div>
                <div id="os-android" style="display:block;">
                    <p style="font-size:0.9rem; margin-bottom:10px;">Descarga el archivo APK e instálalo como una App nativa (acepta "Instalar de orígenes desconocidos" si tu móvil te avisa).</p>
                    <a href="files/app/fantasy-vcv.apk" download class="btn btn-success btn-sm btn-block" style="font-weight:bold; border-radius:20px;">📥 Descargar APK Oficial</a>
                </div>
                <div id="os-ios" style="display:none; text-align:left;">
                    <p style="font-size:0.9rem; margin-bottom:5px; color:#444;">Debido a las restricciones de Apple, instálala así:</p>
                    <ol style="font-size:0.9rem; padding-left:20px; color:#444; margin-bottom:0;">
                        <li style="margin-bottom:8px;">Abre esta web desde <b>Safari</b>.</li>
                        <li style="margin-bottom:8px;">Toca el icono de <b>Compartir</b> en la barra inferior.</li>
                        <li>Selecciona <b>"Añadir a la pantalla de inicio"</b>.</li>
                    </ol>
                    <p style="font-size:0.8rem; color:#888; margin-top:10px;"><i>Nota: Si ya la tenías instalada, bórrala e instálala de nuevo para actualizar el sistema de la caché.</i></p>
                </div>
            </div>
        </details>
"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Remove the header button
    btn_regex = r'<button onclick="openInstallModal\(\)".*?>📱 App</button>'
    html = re.sub(btn_regex, '', html)

    # 2. Remove the modal
    modal_regex = r'<!-- Modal de Instalación de App -->\s*<div id="installAppModal".*?</div>\s*</div>\s*</div>'
    html = re.sub(modal_regex, '', html, flags=re.DOTALL)
    # Also if the comment was slightly different or missing, do a strict match
    modal_regex2 = r'<div id="installAppModal".*?</div>\s*</div>\s*</div>'
    html = re.sub(modal_regex2, '', html, flags=re.DOTALL)

    # 3. Remove the JS function
    js_regex = r'function openInstallModal\(\) \{.*?\n\}'
    html = re.sub(js_regex, '', html, flags=re.DOTALL)

    # 4. Inject the new details into FAQ
    # We will inject it right after <div class="faq-title">
    html = html.replace('<div class="faq-title">❔ Preguntas Frecuentes y Gestión</div>', '<div class="faq-title">❔ Preguntas Frecuentes y Gestión</div>' + faq_app_section)
    # the emoji might have been mangled to ? so let's use a regex just in case
    html = re.sub(r'<div class="faq-title">.*?Preguntas Frecuentes y.*?</div>', lambda m: m.group(0) + faq_app_section, html)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

