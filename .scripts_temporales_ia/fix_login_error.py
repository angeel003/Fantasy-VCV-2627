import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """            iniciarRelojTotales();
        } else {
            msgBox.className = "alert-box alert-danger"; msgBox.innerText = data.message; msgBox.style.display = "block";
        }
    })
    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error: " + err.message + " | " + (err.stack || ""); msgBox.style.display = "block"; })
    .finally(() => { btn.disabled = false; btn.innerText = "Iniciar Sesión"; });"""

new = """            iniciarRelojTotales();
        } else if (data.status === "ok") {
            msgBox.className = "alert-box alert-warning"; 
            msgBox.innerText = "El servidor de Google se estaba despertando de la inactividad (Cold Start). Por favor, vuelve a darle a Iniciar Sesión."; 
            msgBox.style.display = "block";
        } else {
            msgBox.className = "alert-box alert-danger"; 
            msgBox.innerText = data.message || "Error desconocido devuelto por el servidor."; 
            msgBox.style.display = "block";
        }
    })
    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error: " + err.message + " | " + (err.stack || ""); msgBox.style.display = "block"; })
    .finally(() => { btn.disabled = false; btn.innerText = "Iniciar Sesión"; });"""

if target in text:
    text = text.replace(target, new)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed login error handling")
else:
    print("Target not found")
