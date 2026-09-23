import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

old_res = "if(resData[i][0]) { resultadosMap[resData[i][0].toString().trim()] = { sets: resData[i][1], parciales: resData[i][2], frase: resData[i][3] ? resData[i][3].toString().trim() : '' }; }"
new_res = "if(resData[i][0]) { resultadosMap[resData[i][0].toString().trim()] = { sets: resData[i][1], parciales: resData[i][2], frase: resData[i][3] ? resData[i][3].toString().trim() : '', streaming: resData[i][4] ? resData[i][4].toString().trim() : '' }; }"

js_content = js_content.replace(old_res, new_res)

# Also update cp.frase_destacado to map cp.streaming
old_cp = """            cp.frase_destacado = (oRes && oRes.frase) ? oRes.frase : "";
        }"""
new_cp = """            cp.frase_destacado = (oRes && oRes.frase) ? oRes.frase : "";
            cp.streaming = (oRes && oRes.streaming) ? oRes.streaming : "";
        }"""

js_content = js_content.replace(old_cp, new_cp)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

