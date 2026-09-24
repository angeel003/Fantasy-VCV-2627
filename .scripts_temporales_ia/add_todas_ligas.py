import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Add "todas_las_ligas: headersLigas.slice(1)" to the returned JSON in action === "login"
json_return_match = re.search(r'return ContentService\.createTextOutput\(JSON\.stringify\(\{\s*"status": "success",\s*"jornada": rondaAbierta,[\s\S]*?\}\)\)', text)

if json_return_match:
    old_json = json_return_match.group(0)
    # inject "todas_las_ligas"
    # first, ensure headersLigas is available. It is defined as: var headersLigas = dataLigas[0];
    new_json = old_json.replace('"ligas": misLigas,', '"ligas": misLigas,\n            "todas_las_ligas": headersLigas.slice(1),')
    text = text.replace(old_json, new_json)
    
    with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added todas_las_ligas to Código.js")
else:
    print("JSON return not found.")
