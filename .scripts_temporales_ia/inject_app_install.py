import re

html_modal = """
<!-- Modal de Instalación de App -->
<div id="installAppModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:9999; justify-content:center; align-items:center; padding:20px;">
    <div style="background:white; border-radius:15px; padding:25px; width:100%; max-width:400px; text-align:center; position:relative;">
        <span onclick="document.getElementById('installAppModal').style.display='none'" style="position:absolute; right:15px; top:10px; font-size:1.8rem; color:#888; cursor:pointer;">&times;</span>
        <h4 style="color:var(--vcv-morado); margin-bottom:15px; font-weight:bold;">📱 Instalar App</h4>
        
        <div id="androidInstall" style="display:none;">
            <p style="font-size:0.95rem; color:#555;">Descarga la aplicación oficial para Android. Se instalará como una App nativa en tu dispositivo.</p>
            <a href="files/app/fantasy-vcv.apk" download class="btn btn-success btn-block mt-3" style="font-weight:bold; font-size:1.1rem; padding:12px;">Descargar APK</a>
        </div>

        <div id="iosInstall" style="display:none;">
            <p style="font-size:0.95rem; color:#555;">Para instalar la App en tu iPhone o iPad:</p>
            <ol style="text-align:left; font-size:0.9rem; color:#444; margin-bottom:20px;">
                <li style="margin-bottom:8px;">Toca el icono de <b>Compartir</b> en la barra inferior de Safari.</li>
                <li>Selecciona <b>"Añadir a la pantalla de inicio"</b>.</li>
            </ol>
            <p style="font-size:0.85rem; color:#888; margin-top:10px;"><i>Nota: Si ya la tenías, bórrala y vuelve a añadirla para forzar la actualización del sistema.</i></p>
        </div>

        <div id="desktopInstall" style="display:none;">
            <p style="font-size:0.95rem; color:#555;">Para la mejor experiencia, abre esta web desde tu móvil Android o iPhone para instalar la aplicación oficial.</p>
        </div>
    </div>
</div>
"""

js_logic = """
function openInstallModal() {
    document.getElementById('installAppModal').style.display = 'flex';
    document.getElementById('androidInstall').style.display = 'none';
    document.getElementById('iosInstall').style.display = 'none';
    document.getElementById('desktopInstall').style.display = 'none';

    let ua = navigator.userAgent || navigator.vendor || window.opera;
    if (/android/i.test(ua)) {
        document.getElementById('androidInstall').style.display = 'block';
    } else if (/iPad|iPhone|iPod/.test(ua) || (navigator.userAgent.includes("Mac") && "ontouchend" in document)) {
        document.getElementById('iosInstall').style.display = 'block';
    } else {
        document.getElementById('desktopInstall').style.display = 'block';
    }
}
"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Add button to header
    header_old = """<div class="header-content">
        <h1 style="margin-bottom: 0px; line-height:1.2;">Fantasy VCV 26/27</h1>
    </div>"""
    header_new = """<div class="header-content">
        <h1 style="margin-bottom: 0px; line-height:1.2;">Fantasy VCV 26/27</h1>
    </div>
    <button onclick="openInstallModal()" class="btn btn-sm" style="position:absolute; right:15px; top:12px; font-weight:bold; font-size:0.8rem; border-radius:20px; padding:4px 10px; background:rgba(255,255,255,0.2); color:white; border:1px solid rgba(255,255,255,0.5);">📱 App</button>"""
    html = html.replace(header_old, header_new)

    # Add Modal HTML just before closing body
    if "installAppModal" not in html:
        html = html.replace("</body>", html_modal + "\n</body>")

    # Add JS logic inside script tag
    if "openInstallModal" not in html:
        html = html.replace("</script>\n</body>", js_logic + "\n</script>\n</body>")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

