import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Hide calendarioSection in Guest Mode
# Search for `document.getElementById('prediccionesTotalesSection').style.display = "none";`
# and add the hiding of calendarioSection and showing of the promo banner.
hide_sections = """document.getElementById('prediccionesTotalesSection').style.display = "none";
            let calSec = document.getElementById('calendarioSection');
            if (calSec) calSec.style.display = "none";
            
            // Mostrar banner promo de invitados
            let promoDiv = document.getElementById('guestPromoBanner');
            if (!promoDiv) {
                promoDiv = document.createElement('div');
                promoDiv.id = 'guestPromoBanner';
                promoDiv.style = "background: linear-gradient(135deg, var(--vcv-morado), #1565c0); color: white; padding: 25px 20px; border-radius: 12px; margin-top: 30px; text-align: left; box-shadow: 0 4px 10px rgba(0,0,0,0.15); border: 2px solid var(--vcv-dorado);";
                promoDiv.innerHTML = `
                    <h3 style="color: var(--vcv-dorado); font-weight: bold; margin-bottom: 15px;">¿Quieres ver más? 🏐</h3>
                    <p style="font-size: 1.05rem; margin-bottom: 15px;">Si quieres acceder a toda la información detallada, <b>resultados pasados</b>, <b>calendario completo de próximos partidos</b> de tus equipos favoritos y <b>jugar en la liga de pronósticos</b>, ¡tienes que registrarte!</p>
                    <p style="font-size: 1rem; margin-bottom: 5px;">Envíanos un correo a <a href="mailto:adminfantasyvcv@gmail.com" style="color: var(--vcv-dorado); font-weight: bold; text-decoration: underline;">adminfantasyvcv@gmail.com</a> con:</p>
                    <ul style="padding-left: 25px; margin-bottom: 15px; font-weight: bold;">
                        <li>Nombre de usuario (ej: @juan_vcv)</li>
                        <li>Contraseña deseada</li>
                        <li>Tu nombre real o mote</li>
                    </ul>
                    <p style="font-size: 0.95rem; opacity: 0.9;"><i>Te crearemos la cuenta y te avisaremos enseguida para que puedas acceder al Fantasy VCV.</i></p>
                `;
                document.getElementById('prediccionForm').parentNode.appendChild(promoDiv);
            }
            promoDiv.style.display = "block";
"""

html = html.replace('document.getElementById(\'prediccionesTotalesSection\').style.display = "none";', hide_sections)

# Hide guestPromoBanner in Normal Login
hide_promo = """document.getElementById('prediccionesTotalesSection').style.display = "none";
            let calSec2 = document.getElementById('calendarioSection');
            if (calSec2) calSec2.style.display = "block";
            let promoDiv2 = document.getElementById('guestPromoBanner');
            if (promoDiv2) promoDiv2.style.display = "none";"""
            
# Normal login also has `document.getElementById('prediccionesTotalesSection').style.display = "none";` before starting to build UI.
# Let's replace the one inside the `login` function properly.
# Actually, the normal login starts displaying sections later. It doesn't hide prediccionesTotalesSection at the very beginning of the success block.
# Let's find `isGuestMode = false;` or just look for the first line of normal login: `currentUser = usr; currentPassword = pwd;`
show_cal = """currentUser = usr; currentPassword = pwd;
            let calSec2 = document.getElementById('calendarioSection');
            if (calSec2) calSec2.style.display = "block";
            let promoDiv2 = document.getElementById('guestPromoBanner');
            if (promoDiv2) promoDiv2.style.display = "none";"""
html = html.replace('currentUser = usr; currentPassword = pwd;', show_cal)


# 2. Filter data.equipos in guest mode BEFORE the forEach
# Find `data.equipos.sort((a, b) => {` inside the guest login block.
guest_sort_and_filter = """
            // FILTRO MODO INVITADO
            let nowTime = new Date().getTime();
            let limitTime = nowTime + (10 * 24 * 60 * 60 * 1000); // 10 days
            
            // Agrupar pasados por equipo para coger solo el más reciente
            let pasadosPorEquipo = {};
            let proximosFiltrados = [];
            
            data.equipos.forEach(eq => {
                let esPasado = eq.oficial_sets && eq.oficial_sets.includes("-");
                if (eq.estado === "CERRADO" || eq.visibilidad === "OCULTAR") esPasado = true;
                
                if (esPasado) {
                    if (!pasadosPorEquipo[eq.equipo_local]) {
                        pasadosPorEquipo[eq.equipo_local] = eq;
                    } else {
                        // Keep the most recent (highest timestamp that is past, or just highest timestamp if multiple)
                        let currentTs = pasadosPorEquipo[eq.equipo_local].timestamp || 0;
                        let newTs = eq.timestamp || 0;
                        if (newTs > currentTs) {
                            pasadosPorEquipo[eq.equipo_local] = eq;
                        }
                    }
                } else {
                    // Es Próximo. Solo incluir si es en los próximos 10 días
                    if (eq.timestamp && eq.timestamp <= limitTime) {
                        proximosFiltrados.push(eq);
                    } else if (!eq.timestamp) {
                        // Si no tiene fecha, lo mostramos? El user dijo "que se vayan a jugar en los proximos 10 dias".
                        // Lo ocultamos por si acaso, o lo mostramos? Mejor lo ocultamos si no hay fecha.
                    }
                }
            });
            
            let pasadosFiltrados = Object.values(pasadosPorEquipo);
            data.equipos = proximosFiltrados.concat(pasadosFiltrados);

            data.equipos.sort((a, b) => {
"""

html = html.replace('data.equipos.sort((a, b) => {', guest_sort_and_filter, 1) # Replace ONLY the first occurrence (which is inside guest login)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print("Patched dev.html for Guest Mode rules")

