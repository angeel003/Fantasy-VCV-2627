import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_func = """window.guardarResultadoAdmin = function(e, idPart) {
    e.preventDefault();
    const btn = e.target;
    const sets = document.getElementById(`adm_sets_${idPart}`).value.trim();
    const parc = document.getElementById(`adm_parc_${idPart}`).value.trim();
    
    btn.disabled = true; btn.innerText = "Subiendo...";
    
    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'save_resultado_admin', usuario: currentUser, password: currentPassword, id_partido: idPart, sets: sets, parciales: parc }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })
    .then(res => res.json())
    .then(d => {
        if(d.status === "success") { mostrarToast("✅ Resultado subido al Excel"); } 
        else { alert("Error: " + d.message); }
    })
    .finally(() => { btn.disabled = false; btn.innerText = "💾 Subir Resultado"; });
}"""

# Note: The file might have encoding issues, let's use a regex to match it flexibly
old_func_pattern = re.compile(r"window\.guardarResultadoAdmin\s*=\s*function\(e, idPart\)\s*\{[\s\S]*?\}\s*(?=\n\s*window\.crearUsuarioAdmin)", re.MULTILINE)

new_func = """window.guardarResultadoAdmin = function(e, idPart) {
    e.preventDefault();
    const btn = e.currentTarget || e.target;
    
    // Leer valores, protegiendo si no existen los nuevos inputs
    const elSets = document.getElementById(`adm_sets_${idPart}`);
    const elParc = document.getElementById(`adm_parc_${idPart}`);
    const elStream = document.getElementById(`adm_stream_${idPart}`);
    const elFrase = document.getElementById(`adm_frase_${idPart}`);
    
    const sets = elSets ? elSets.value.trim() : "";
    const parc = elParc ? elParc.value.trim() : "";
    const stream = elStream ? elStream.value.trim() : "";
    const frase = elFrase ? elFrase.value.trim() : "";
    
    btn.disabled = true; btn.innerText = "Subiendo...";
    
    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'save_resultado_admin', usuario: currentUser, password: currentPassword, id_partido: idPart, sets: sets, parciales: parc, streaming: stream, frase: frase }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })
    .then(res => res.json())
    .then(d => {
        if(d.status === "success") { 
            mostrarToast("✅ Resultado subido al Excel"); 
        } else { 
            alert("Error: " + d.message); 
        }
    })
    .catch(err => {
        console.error("Error al guardar:", err);
        alert("El resultado se ha enviado, pero hubo un error de red o timeout.");
    })
    .finally(() => { 
        btn.disabled = false; 
        btn.innerText = "💾 Guardar Todo"; 
    });
}"""

if old_func_pattern.search(html):
    html = old_func_pattern.sub(new_func, html)
    print("Replaced successfully via regex.")
else:
    print("Could not find the function via regex.")

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

