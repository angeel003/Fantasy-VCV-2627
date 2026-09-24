import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the hacky window.actualizarVistas override
hack_js = """        // Lo engancharemos en actualizarVistas
        var oldActualizarVistas = window.actualizarVistas;
        window.actualizarVistas = function(soloCalendario) {
            if(oldActualizarVistas) oldActualizarVistas(soloCalendario);
            checkFabVisibility();
        };"""

if hack_js in html:
    html = html.replace(hack_js, """        // Usamos un observer para mostrarlo automáticamente cuando appSection sea visible
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === "style") {
                    checkFabVisibility();
                }
            });
        });
        var appSec = document.getElementById('appSection');
        if(appSec) {
            observer.observe(appSec, { attributes: true });
        }
        // Llamada inicial por si acaso
        setInterval(checkFabVisibility, 1000);
""")
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Patched dev.html with MutationObserver and setInterval.")
else:
    print("Hack not found.")

