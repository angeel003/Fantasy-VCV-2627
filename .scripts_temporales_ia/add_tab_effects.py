import re

css_inject = """
    /* ---------------------------------------------------
       5. BOTON ATRAS (Pestaña flotante)
       --------------------------------------------------- */
    #btnLogout {
        display: none;
        position: fixed;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        background: var(--vcv-dorado);
        border: none;
        border-radius: 0 12px 12px 0;
        color: var(--vcv-morado);
        font-size: 1.8rem;
        font-weight: bold;
        cursor: pointer;
        padding: 20px 12px 20px 8px;
        box-shadow: 3px 3px 12px rgba(0,0,0,0.4);
        z-index: 99999;
        transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1);
    }
    #btnLogout:hover {
        transform: translateY(-50%) translateX(8px);
    }
    
    @keyframes slideOutRight {
        0% { opacity: 1; transform: none; }
        100% { opacity: 0; transform: translateX(50px); }
    }
    .slide-out-right {
        animation: slideOutRight 0.3s cubic-bezier(0.25, 1, 0.5, 1) forwards !important;
    }
"""

js_old = """document.getElementById('btnLogout').addEventListener('click', function() {
    localStorage.removeItem('vcv_cache_data');
    localStorage.removeItem('vcv_cache_type');
    localStorage.removeItem('vcv_cache_creds');
    window.location.reload();
});"""

js_new = """document.getElementById('btnLogout').addEventListener('click', function() {
    localStorage.removeItem('vcv_cache_data');
    localStorage.removeItem('vcv_cache_type');
    localStorage.removeItem('vcv_cache_creds');
    
    document.getElementById('appSection').classList.add('slide-out-right');
    this.style.transform = 'translateY(-50%) translateX(-100%)'; // Hide tab as well
    
    setTimeout(() => {
        window.location.reload();
    }, 280);
});"""


for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Clean the inline style from btnLogout
    # Search for <button id="btnLogout" style="...">&#10094;</button>
    html = re.sub(r'<button id="btnLogout" style="[^"]*".*?>&#10094;</button>', '<button id="btnLogout" title="Volver atrás">&#10094;</button>', html)
    
    # 2. Inject CSS before </style>
    if '#btnLogout {' not in html:
        html = html.replace('</style>', css_inject + '\n</style>')
        
    # 3. Update the JS
    html = html.replace(js_old, js_new)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

