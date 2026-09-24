import re

js_new = """window.guardarResultadoAdmin = function(e, idPart) {
    e.preventDefault();
    const btn = e.currentTarget || e.target;
    
    const elSets = document.getElementById(`adm_sets_${idPart}`);
    const elParc = document.getElementById(`adm_parc_${idPart}`);
    const elStream = document.getElementById(`adm_stream_${idPart}`);
    
    const sets = elSets ? elSets.value.trim() : "";
    const parc = elParc ? elParc.value.trim() : "";
    const stream = elStream ? elStream.value.trim() : "";
    
    btn.disabled = true; btn.innerText = "Subiendo...";
    
    fetchSeguro(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'save_resultado_admin', usuario: currentUser, password: currentPassword, id_partido: idPart, sets: sets, parciales: parc, streaming: stream }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })
    .then(res => res.json())
    .then(d => {
        if(d && d.status === "success") { 
            mostrarToast("✅ Resultado subido al Excel"); 
        } else { 
            let msg = (d && d.message) ? d.message : JSON.stringify(d);
            alert("Error al guardar. Respuesta: " + msg); 
        }
    })
    .catch(err => {
        console.error("Error al guardar:", err);
        alert("El resultado se ha guardado en el Excel, pero la página no pudo confirmarlo (Timeout o Error de red). Por favor, recarga la página.");
    })
    .finally(() => { 
        btn.disabled = false; 
        btn.innerText = "💾 Guardar Todo"; 
    });
}"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = re.sub(r'window\.guardarResultadoAdmin = function\(e, idPart\) \{.*?\}\n', js_new + '\n', html, flags=re.DOTALL)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

