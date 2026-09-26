import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'\} else \{\s*msgBox\.className = "alert-box alert-danger"; msgBox\.innerText = data\.message; msgBox\.style\.display = "block";\s*\}', text)

if match:
    new = """} else if (data.status === "ok") {
            msgBox.className = "alert-box alert-warning"; msgBox.innerText = "El servidor se estaba despertando (Cold Start). Vuelve a pulsar Iniciar Sesión."; msgBox.style.display = "block";
        } else {
            msgBox.className = "alert-box alert-danger"; msgBox.innerText = data.message || "Error desconocido devuelto por el servidor."; msgBox.style.display = "block";
        }"""
    text = text[:match.start()] + new + text[match.end():]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed index via regex")
else:
    print("Still not found in index")
