import re

with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """    }
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
    }"""

if target in text:
    text = text.replace(target, "    }")
    with open('script-v2/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed broken block")
else:
    print("Target not found")
