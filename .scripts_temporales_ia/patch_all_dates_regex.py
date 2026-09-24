import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

# For resultadosMap
code = re.sub(
    r'var rawSets = resData\[i\]\[1\];.*?resultadosMap\[resData\[i\]\[0\]\.toString\(\)\.trim\(\)\] = \{ sets: setsStr, parciales: resData\[i\]\[2\],',
    r'var setsStr = parseSheetText(resData[i][1]);\n              var parcStr = parseSheetText(resData[i][2]);\n              resultadosMap[resData[i][0].toString().trim()] = { sets: setsStr, parciales: parcStr,',
    code, flags=re.DOTALL
)

# For porrasMap
code = re.sub(
    r'var rawSets = pData\[i\]\[3\];.*?porrasMap\[upUsr\]\[upPart\] = \{ sets: setsStr, puntos: pData\[i\]\[4\], signo: pData\[i\]\[5\] \};',
    r'var setsStr = parseSheetText(pData[i][3]);\n              porrasMap[upUsr][upPart] = { sets: setsStr, puntos: pData[i][4], signo: pData[i][5] };',
    code, flags=re.DOTALL
)

# For Predicciones_Secretas
code = re.sub(
    r'var rawSets = sData\[i\]\[3\];.*?porrasMap\[spUsr\]\[spPart\] = \{ sets: setsStr, puntos: sData\[i\]\[4\], signo: sData\[i\]\[5\] \};',
    r'var setsStr = parseSheetText(sData[i][3]);\n                  porrasMap[spUsr][spPart] = { sets: setsStr, puntos: sData[i][4], signo: sData[i][5] };',
    code, flags=re.DOTALL
)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

