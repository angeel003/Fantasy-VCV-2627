import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_css = """
    /* V2 TAILWIND-MIMIC HEADER CSS */
    .app-header-v2 {
        position: fixed; top: 0; left: 0; width: 100%;
        background: rgba(22, 10, 25, 0.95);
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid #3e1d45;
        padding: 12px 16px; z-index: 1000;
    }
    .header-container-v2 {
        display: flex; justify-content: space-between; align-items: center;
        max-width: 450px; margin: 0 auto;
    }
    .header-brand-v2 { display: flex; align-items: center; gap: 10px; }
    .header-logo-circle {
        width: 40px; height: 40px; border-radius: 50%;
        background: linear-gradient(to top right, #6a2c70, #d4af37);
        padding: 2px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        display: flex; align-items: center; justify-content: center;
    }
    .header-logo-inner {
        width: 100%; height: 100%; background: #240f28; border-radius: 50%;
        display: flex; align-items: center; justify-content: center; color: #d4af37;
    }
    .header-title-row { display: flex; align-items: center; gap: 6px; }
    .header-title-text { font-family: 'Space Grotesk', sans-serif; font-weight: 900; font-size: 1.125rem; letter-spacing: 0.05em; color: #fff; margin:0; line-height:1; }
    .header-title-badge { background: rgba(212,175,55,0.2); color: #d4af37; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(212,175,55,0.3); }
    .header-subtitle { font-size: 11px; color: #a1a1aa; font-weight: 500; margin:0; margin-top:3px; letter-spacing: -0.02em; }
    
    .header-right-v2 { display: flex; align-items: center; gap: 8px; }
    .header-user-chip {
        display: flex; align-items: center; gap: 6px; background: #221127;
        padding: 6px 10px; border-radius: 20px; border: 1px solid #3e1d45;
    }
    .header-rank { font-size: 12px; color: #d4af37; font-weight: 700; }
    .header-dot { width: 4px; height: 4px; border-radius: 50%; background: #71717a; }
    .header-pts { font-size: 12px; font-weight: 600; color: #e4e4e7; }
    
    .header-bell-btn {
        width: 36px; height: 36px; border-radius: 50%; background: #221127;
        border: 1px solid #3e1d45; color: #d4d4d8; display: flex; align-items: center; justify-content: center;
        position: relative; cursor: pointer;
    }
    .header-bell-dot {
        position: absolute; top: 6px; right: 6px; width: 8px; height: 8px;
        border-radius: 50%; background: #d4af37; border: 2px solid #160a19;
    }
"""

new_header_html = """<header class="app-header-v2" id="tituloPrincipalSeccion" style="display:none;">
    <div class="header-container-v2">
      <!-- Brand Logo / Badge -->
      <div class="header-brand-v2">
        <div class="header-logo-circle">
          <div class="header-logo-inner">
            <i data-lucide="volleyball" style="width:20px; height:20px;"></i>
          </div>
        </div>
        <div>
          <div class="header-title-row">
            <h1 class="header-title-text">VCV PLAY</h1>
            <span class="header-title-badge">26/27</span>
          </div>
          <p class="header-subtitle">Club Voleibol Valencia</p>
        </div>
      </div>

      <!-- User Chip & Notification -->
      <div class="header-right-v2">
        <div class="header-user-chip" id="h2-user-chip">
          <span class="header-rank" id="h2-user-rank">Top -</span>
          <span class="header-dot"></span>
          <span class="header-pts" id="h2-user-pts">0 pts</span>
        </div>
        <button class="header-bell-btn" onclick="document.getElementById('notificacionesModal').style.display='flex'">
          <i data-lucide="bell" style="width:18px; height:18px;"></i>
          <span class="header-bell-dot"></span>
        </button>
      </div>
    </div>
</header>"""

# Replace CSS
css_regex = r'\.app-header-v2\s*\{.*?(?=\s*\/\*|\s*<\/style>|(?:\n\s*\n\s*\.))' # We will just inject it before </style> and remove the old one.
text = re.sub(r'\.app-header-v2\s*\{.*?(?=\.vcv-card-v2)', '', text, flags=re.DOTALL)
# Actually let's just insert before </style>
text = text.replace('</style>', new_css + '\n</style>')

# Replace HTML
html_regex = r'<header class="app-header-v2".*?</header>'
text = re.sub(html_regex, new_header_html, text, flags=re.DOTALL)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Header replaced.")
