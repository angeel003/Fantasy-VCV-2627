import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update text & logo
text = text.replace('La liga de pronósticos oficial del club', 'El juego oficial del club')

old_shield = '<i data-lucide="shield" style="width: 30px; height: 30px;"></i>'
new_logo = '<img src="files/images/logo_vcv_circle.png" style="width: 100%; height: 100%; object-fit: contain; border-radius: 50%;">'
text = text.replace(old_shield, new_logo)


# 2. Inject Bottom Nav CSS
nav_css = """
    /* BOTTOM NAV V2 */
    .bottom-nav-v2 {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: var(--bg-card);
        border-top: 1px solid var(--border-color);
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 9999;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.5);
        padding-bottom: env(safe-area-inset-bottom, 10px);
    }
    .nav-item-v2 {
        background: transparent;
        border: none;
        color: var(--text-muted);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        font-size: 0.65rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s;
        width: 20%;
    }
    .nav-item-v2 i {
        width: 22px;
        height: 22px;
        margin-bottom: 2px;
    }
    .nav-item-v2.active {
        color: var(--secondary-color);
    }
    .nav-item-v2.active i {
        transform: scale(1.15);
    }
    
    /* Hide all sections by default except when active */
    #appSection > section {
        display: none;
        padding-bottom: 80px; /* space for bottom nav */
    }
    #appSection > section.active-tab {
        display: block;
        animation: fadeInTab 0.3s ease;
    }
    @keyframes fadeInTab {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
"""
text = text.replace('</style>', nav_css + '\n  </style>')


# 3. Inject Bottom Nav HTML at the end of appSection
bottom_nav_html = """
    <!-- BOTTOM NAV V2 -->
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
</div> <!-- Closing appSection (we will replace the closing tag) -->
"""
text = text.replace('</div>\n\n    <!-- MODALS PARA ALERTAS -->', bottom_nav_html + '\n\n    <!-- MODALS PARA ALERTAS -->')


# 4. Inject JS logic
js_logic = """
    function switchTabV2(sectionId, btn) {
        // Hide all sections in appSection
        const sections = ['carteleraSection', 'clasificacionesSection', 'historialSection', 'calendarioSection', 'enlacesRfevbSection', 'prediccionesTotalesSection'];
        sections.forEach(s => {
            const el = document.getElementById(s);
            if (el) el.classList.remove('active-tab');
        });
        
        // Show target section
        const target = document.getElementById(sectionId);
        if (target) target.classList.add('active-tab');
        
        // If historial, also show prediccionesTotalesSection right below it (if they were separate)
        if (sectionId === 'historialSection') {
            const extra = document.getElementById('prediccionesTotalesSection');
            if (extra) extra.classList.add('active-tab');
        }

        // Update active button state
        document.querySelectorAll('.nav-item-v2').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    document.addEventListener("DOMContentLoaded", () => {
        // Initialize first tab as active
        const firstSec = document.getElementById('carteleraSection');
        if (firstSec) firstSec.classList.add('active-tab');
    });
"""
text = text.replace('function handleSaveOrModifyV2(idPart) {', js_logic + '\n    function handleSaveOrModifyV2(idPart) {')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated v2.html with Bottom Nav, Logo, and Subtitle.")
