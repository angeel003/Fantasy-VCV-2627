import re

proper_polyfill = """
// POLYFILL PARA REINTENTOS AUTOMATICOS (Soluciona los errores 500 y timeouts del primer login)
const fetchSeguro = (url, options, retries = 1) => {
    return fetch(url, options)
        .then(res => res.json().then(data => ({ json: () => Promise.resolve(data) })))
        .catch(err => {
            if (retries > 0) return new Promise(r => setTimeout(r, 1000)).then(() => fetchSeguro(url, options, retries - 1));
            throw new Error("El servidor de Google está saturado (Timeout). Vuelve a pulsar el botón.");
        });
};
"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Fix err.stack
    html = html.replace('err.stack', '(err.stack || "")')
    
    # 2. Fix iOS button
    html = re.sub(r'<button id="btnLogout".*?</button>', 
                  r'<button id="btnLogout" style="display:none; position:absolute; left:5px; top:max(15px, env(safe-area-inset-top)); background:transparent; border:none; color:rgba(255,255,255,0.9); font-size:2.2rem; cursor:pointer; padding:15px 25px; outline:none; text-shadow:0 2px 4px rgba(0,0,0,0.3); z-index:9999;" title="Volver atrás">&#10094;</button>', 
                  html)
    
    # 3. Add Polyfill properly
    if 'fetchSeguro' not in html:
        html = html.replace('<script>', '<script>\n' + proper_polyfill)
        html = html.replace('fetch(scriptURL,', 'fetchSeguro(scriptURL,')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

