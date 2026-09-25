import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# --- 1. Fix the Generator for local vs visitor & logo ---
start_match = text.find('if (eq.estado === "ABIERTO") {')
end_match = text.find('<div class="reloj-partido" data-ts="${eq.timestamp}"', start_match)

if start_match != -1 and end_match != -1:
    new_card_html = r"""if (eq.estado === "ABIERTO") {
                        let dt = new Date(eq.timestamp);
                        let fechaFormateada = isNaN(dt) ? "" : `${dt.toLocaleDateString()} ${dt.getHours().toString().padStart(2,'0')}:${dt.getMinutes().toString().padStart(2,'0')}`;

                        setTimeout(() => { if(window.lucide) lucide.createIcons(); }, 100);

                        let localTeamName = eq.es_local ? eq.equipo_local : eq.rival;
                        let visitTeamName = eq.es_local ? eq.rival : eq.equipo_local;
                        
                        let localIsVcv = eq.es_local;
                        let visitIsVcv = !eq.es_local;

                        let localLogo = localIsVcv 
                            ? '<img src="files/images/logo_vcv_circle.png" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">' 
                            : localTeamName.substring(0,3).toUpperCase();
                            
                        let visitLogo = visitIsVcv 
                            ? '<img src="files/images/logo_vcv_circle.png" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">' 
                            : visitTeamName.substring(0,3).toUpperCase();

                        htmlPartidos += `
                        <div class="vcv-card-v2" id="card-v2-${eq.id_partido}" data-category="${eq.categoria}">
                            <div class="match-header-strip-v2">
                                <span style="color: ${eq.es_derby ? 'var(--text-gold)' : 'var(--secondary-color)'}; font-weight: 800;">
                                  ${eq.categoria.toUpperCase()} ${eq.es_derby ? '🏆 DERBY' : ''}
                                </span>
                                <span><i data-lucide="calendar" style="width: 12px; height: 12px; display: inline; vertical-align: middle; margin-top:-2px;"></i> ${fechaFormateada}</span>
                            </div>

                            <div class="teams-versus-container-v2">
                                <div class="team-box-v2">
                                  <div class="team-avatar-v2 ${localIsVcv ? 'vcv-local' : ''}">${localLogo}</div>
                                  <span class="team-name-v2">${localTeamName}</span>
                                  <span class="team-role-v2" style="color: var(--success)">LOCAL</span>
                                </div>
                                <div class="vs-divider-v2">VS</div>
                                <div class="team-box-v2">
                                  <div class="team-avatar-v2 ${visitIsVcv ? 'vcv-local' : ''}">${visitLogo}</div>
                                  <span class="team-name-v2">${visitTeamName}</span>
                                  <span class="team-role-v2" style="color: var(--text-muted)">VISITANTE</span>
                                </div>
                            </div>
                            
                            """
    text = text[:start_match] + new_card_html + text[end_match:]

# --- 2. Inject Bottom Nav properly ---
# It should go right before `<div id="toastNotification">` or near the end of the body
bottom_nav_html = """
    <!-- BOTTOM NAV V2 -->
    <div id="bottomNavWrapperV2" style="display:none;">
        <nav class="bottom-nav-v2" id="bottomNavV2">
          <button class="nav-item-v2 active" onclick="switchTabV2('carteleraSection', this)">
            <i data-lucide="volleyball"></i>
            <span>Partidos</span>
          </button>
          <button class="nav-item-v2" onclick="switchTabV2('clasificacionesSection', this)">
            <i data-lucide="trophy"></i>
            <span>Ranking</span>
          </button>
          <button class="nav-item-v2" onclick="switchTabV2('historialSection', this)">
            <i data-lucide="check-circle-2"></i>
            <span>Mis Pronos</span>
          </button>
          <button class="nav-item-v2" onclick="switchTabV2('calendarioSection', this)">
            <i data-lucide="calendar"></i>
            <span>Calendario</span>
          </button>
          <button class="nav-item-v2" onclick="switchTabV2('enlacesRfevbSection', this)">
            <i data-lucide="shield"></i>
            <span>Club</span>
          </button>
        </nav>
    </div>
"""

# Instead of relying on specific divs, just insert it before the first <script src=... or right before </body>
# But wait, we need it to show ONLY when logged in.
# Let's add it right before `<div id="mobileTooltip"`
if '<div id="mobileTooltip"' in text:
    text = text.replace('<div id="mobileTooltip"', bottom_nav_html + '\n<div id="mobileTooltip"')
else:
    text = text.replace('</body>', bottom_nav_html + '\n</body>')

# Update the toggle logic so `bottomNavWrapperV2` is shown when appSection is shown.
# Wait, I can just modify `switchTabV2` to make sure we don't have to hook into the login event.
# Actually, the original login logic does: `document.getElementById('appSection').style.display = "block";`
# Let's inject a mutation observer in JS to automatically show the bottom nav when appSection is visible!
js_nav_observer = """
    // Observer for Bottom Nav
    document.addEventListener("DOMContentLoaded", () => {
        const appSec = document.getElementById('appSection');
        const navWrap = document.getElementById('bottomNavWrapperV2');
        if(appSec && navWrap) {
            const observer = new MutationObserver(() => {
                if(appSec.style.display !== 'none') {
                    navWrap.style.display = 'block';
                } else {
                    navWrap.style.display = 'none';
                }
            });
            observer.observe(appSec, { attributes: true, attributeFilter: ['style'] });
        }
    });
"""
text = text.replace('function switchTabV2(sectionId, btn) {', js_nav_observer + '\n    function switchTabV2(sectionId, btn) {')


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated generator and nav!")
