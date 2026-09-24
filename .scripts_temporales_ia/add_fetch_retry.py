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
    
    # Remove the broken polyfill
    html = re.sub(r'// POLYFILL PARA REINTENTOS AUTOMATICOS.*?(?=<)', '', html, flags=re.DOTALL)
    
    # Inject the proper polyfill
    html = html.replace('<script>', '<script>\n' + proper_polyfill)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

