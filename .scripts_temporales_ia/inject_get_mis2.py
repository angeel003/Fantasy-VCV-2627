import re

with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """if (action === "get_mis_predicciones") {"""
new = """if (action === "get_mis_predicciones") {
        var pData = getSafeData(sheetPorras);
        var pMap = {};
        var userLower = usuario.toLowerCase();
        for(var i=1; i<pData.length; i++) {
            var pUser = pData[i][1] ? pData[i][1].toString().trim().toLowerCase() : "";
            var pIdPart = pData[i][2] ? pData[i][2].toString().trim() : "";
            if(pUser === userLower) {
                pMap[pIdPart] = { sets: parseSheetText(pData[i][3]), puntos: pData[i][4], signo: pData[i][5] };
            }
        }
        return ContentService.createTextOutput(JSON.stringify({
            "status": "success",
            "predicciones": pMap
        })).setMimeType(ContentService.MimeType.JSON);
    }"""

if target in text:
    text = text.replace(target, new)
else:
    # Inject it if not found (because I already ran the script earlier, wait, I didn't!)
    target = """if (action === "save") {"""
    if target in text:
        text = text.replace(target, new + "\n\n    if (action === \"save\") {")

with open('script-v2/Código.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Injected case-insensitive get_mis_predicciones")
