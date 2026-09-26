import re

with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """if (action === "save") {"""
new = """if (action === "get_mis_predicciones") {
        var pData = getSafeData(sheetPorras);
        var pMap = {};
        for(var i=1; i<pData.length; i++) {
            var pUser = pData[i][1];
            var pIdPart = pData[i][2].toString().trim();
            if(!pMap[pUser]) pMap[pUser] = {};
            pMap[pUser][pIdPart] = { sets: parseSheetText(pData[i][3]), puntos: pData[i][4], signo: pData[i][5] };
        }
        return ContentService.createTextOutput(JSON.stringify({
            "status": "success",
            "predicciones": pMap[usuario] || {}
        })).setMimeType(ContentService.MimeType.JSON);
    }

    if (action === "save") {"""

if target in text:
    text = text.replace(target, new)
    with open('script-v2/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Injected get_mis_predicciones")
else:
    print("Target not found")
