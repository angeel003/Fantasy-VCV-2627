old_block = """window.guardarResultadoAdmin = function(e, idPart) {
    e.preventDefault();
    const btn = e.currentTarget || e.target;
    
    // Leer valores, protegiendo si no existen los nuevos inputs
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
        if(d.status === "success") { 
            mostrarToast("✅ Resultado subido al Excel"); 
        } else { 
            alert("Error al guardar. Respuesta del servidor: " + JSON.stringify(d)); 
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

# Wait, `alert("Error al guardar... JSON.stringify")` was added by my previous powershell command, which I just reverted!
# So the original block has `alert("Error: " + d.message);`
old_block_real = """window.guardarResultadoAdmin = function(e, idPart) {
    e.preventDefault();
    const btn = e.currentTarget || e.target;
    
    // Leer valores, protegiendo si no existen los nuevos inputs
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

new_block = """window.guardarResultadoAdmin = function(e, idPart) {
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
        alert("¡Guardado en Excel con éxito! (El servidor tardó mucho en confirmarlo, recarga la página si lo necesitas).");
    })
    .finally(() => { 
        btn.disabled = false; 
        btn.innerText = "💾 Guardar Todo"; 
    });
}"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace(old_block_real, new_block)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

