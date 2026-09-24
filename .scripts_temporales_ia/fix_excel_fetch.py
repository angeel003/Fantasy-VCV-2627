import re

# 1. Update dev.html and index.html to use fetchSeguro and remove fetch
for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace fetch(scriptURL + '?t=' + new Date().getTime() with fetchSeguro(scriptURL
    html = re.sub(r"fetch\(scriptURL \+ '\?t=' \+ new Date\(\)\.getTime\(\),\s*\{", "fetchSeguro(scriptURL, {", html)
    
    # Just in case for add_user
    html = re.sub(r"fetch\(scriptURL,\s*\{", "fetchSeguro(scriptURL, {", html)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

# 2. Update Código.js to map streaming to column 4 instead of 5
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix getting the streaming value
js = js.replace("streaming: resData[i][4] ? resData[i][4].toString().trim() : ''", "streaming: resData[i][3] ? resData[i][3].toString().trim() : ''")

# Fix saving the streaming value
# From:
# sheetResultados.getRange(rowFound, 2).setValue(sets);
# sheetResultados.getRange(rowFound, 3).setValue(parciales);
# sheetResultados.getRange(rowFound, 5).setValue(streaming);
old_save_block = """
            if(rowFound !== -1) {
                sheetResultados.getRange(rowFound, 2).setValue(sets);
                sheetResultados.getRange(rowFound, 3).setValue(parciales);
                sheetResultados.getRange(rowFound, 5).setValue(streaming);
            } else {
                sheetResultados.appendRow([idPart, sets, parciales, "", streaming]);
            }
"""
new_save_block = """
            if(rowFound !== -1) {
                sheetResultados.getRange(rowFound, 2).setValue(sets);
                sheetResultados.getRange(rowFound, 3).setValue(parciales);
                sheetResultados.getRange(rowFound, 4).setValue(streaming);
            } else {
                sheetResultados.appendRow([idPart, sets, parciales, streaming]);
            }
"""
js = js.replace(old_save_block.strip(), new_save_block.strip())

# Also fix the initialization of headers in Código.js
old_header = 'sheetResultados.appendRow(["ID_Partido", "Sets", "Parciales", "Frase_MVP", "Streaming"]);'
new_header = 'sheetResultados.appendRow(["ID_Partido", "Sets", "Parciales", "Streaming"]);'
js = js.replace(old_header, new_header)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(js)

