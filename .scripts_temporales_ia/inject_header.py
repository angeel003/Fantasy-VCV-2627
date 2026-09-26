import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. ADD CSS
css = """
    /* V2 HEADER */
    .app-header-v2 {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 64px;
        background: var(--bg-card);
        border-bottom: 1px solid var(--border-color);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 16px;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .header-brand-v2 h1 {
        font-size: 1.25rem;
        font-weight: 900;
        margin: 0;
        color: var(--text-main);
        letter-spacing: -0.5px;
        font-family: 'Space Grotesk', sans-serif;
    }
    .header-user-v2 {
        font-size: 0.75rem;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 2px;
    }
    .header-user-name {
        font-weight: 700;
        color: var(--text-main);
    }
    .header-user-handle {
        font-family: monospace;
        opacity: 0.8;
    }
    .header-badges-v2 {
        display: flex;
        align-items: center;
        gap: 3px;
    }
    .header-badges-v2 img {
        width: 14px;
        height: 14px;
        border-radius: 50%;
    }
    .header-actions-v2 {
        display: flex;
        align-items: center;
    }
    .bell-btn-v2 {
        background: none;
        border: none;
        color: var(--text-main);
        position: relative;
        padding: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .bell-dot-v2 {
        position: absolute;
        top: 4px;
        right: 4px;
        width: 8px;
        height: 8px;
        background: var(--primary-color);
        border-radius: 50%;
        border: 2px solid var(--bg-card);
    }
    #appSection {
        padding-top: 76px; /* space for header */
    }
</style>
"""
text = text.replace('</style>', css)


# 2. ADD HTML inside appSection
html_header = """
    <header class="app-header-v2">
      <div class="header-brand-v2">
        <h1>VCV Play <span style="color:var(--primary-color);">2627</span></h1>
        <div class="header-user-v2">
          <span class="header-user-name" id="h2-user-name"></span>
          <span class="header-user-handle" id="h2-user-handle"></span>
          <div class="header-badges-v2" id="h2-user-badges"></div>
        </div>
      </div>
      <div class="header-actions-v2">
        <button class="bell-btn-v2">
          <i data-lucide="bell" style="width:22px; height:22px;"></i>
          <span class="bell-dot-v2"></span>
        </button>
      </div>
    </header>
"""
text = text.replace('<section id="carteleraSection">', html_header + '\n    <section id="carteleraSection">')


# 3. POPULATE DATA in JS
js_inject = """
            document.getElementById('h2-user-name').innerText = displayNom;
            document.getElementById('h2-user-handle').innerText = "@" + usr;
            
            let badgesH2 = "";
            misInsignias.forEach(b => {
                badgesH2 += `<img src="${URL_BADGE_GENERIC}" alt="badge">`; // Simple img tag with no tooltip, just the icon (we use the generic URL here, or we can use colored divs)
            });
            document.getElementById('h2-user-badges').innerHTML = badgesH2;
"""

# We need to make the badges actually look right. The user says "los iconos de verificado de este, pero no dicen lo que significan al poner el raton o pulsar encima"
# In `v2.html`, how did I render badges?
# `<div class="badge-icon ${cssColorClass}" onclick="showMobileTooltip('badge-tt-${b.type}', this)" style="cursor:pointer; width:22px; height:22px; display:flex; justify-content:center; align-items:center;">`
# So we can just render the `<img src="${URL_BADGE_GENERIC}">` wrapped in the CSS colored background, or just use the badge div without `onclick` and `tooltip`.
# Wait, let's look at the exact JS used for `insigniasHeaderHtml`.

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("CSS and HTML injected. Need to adjust JS now.")
