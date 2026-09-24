import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace in resultadosMap
code = code.replace(
    """if(resData[i][0]) { resultadosMap[resData[i][0].toString().trim()] = { sets: resData[i][1], parciales: resData[i][2], frase: resData[i][3] ? resData[i][3].toString().trim() : '', streaming: resData[i][4] ? resData[i][4].toString().trim() : '' }; }""",
    """if(resData[i][0]) { resultadosMap[resData[i][0].toString().trim()] = { sets: parseSheetText(resData[i][1]), parciales: parseSheetText(resData[i][2]), frase: resData[i][3] ? resData[i][3].toString().trim() : '', streaming: resData[i][4] ? resData[i][4].toString().trim() : '' }; }"""
)

# Replace in porrasMap
code = code.replace(
    """porrasMap[pUser][pIdPart] = { sets: porrasData[i][3], puntos: porrasData[i][4], signo: porrasData[i][5] };""",
    """porrasMap[pUser][pIdPart] = { sets: parseSheetText(porrasData[i][3]), puntos: porrasData[i][4], signo: porrasData[i][5] };"""
)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

