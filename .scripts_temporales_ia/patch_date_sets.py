import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_res_logic = r"""      var resData = getSafeData\(sheetResultados\);
      var resultadosMap = \{\}; 
      for\(var i=1; i<resData\.length; i\+\+\) \{
          if\(resData\[i\]\[0\]\) \{ resultadosMap\[resData\[i\]\[0\]\.toString\(\)\.trim\(\)\] = \{ sets: resData\[i\]\[1\], parciales: resData\[i\]\[2\], frase: resData\[i\]\[3\] \? resData\[i\]\[3\]\.toString\(\)\.trim\(\) : '', streaming: resData\[i\]\[4\] \? resData\[i\]\[4\]\.toString\(\)\.trim\(\) : '' \}; \}
      \}"""

new_res_logic = """      var resData = getSafeData(sheetResultados);
      var resultadosMap = {}; 
      for(var i=1; i<resData.length; i++) {
          if(resData[i][0]) { 
              var rawSets = resData[i][1];
              var setsStr = "";
              if (rawSets && typeof rawSets.getDate === 'function') {
                  setsStr = rawSets.getDate() + "-" + (rawSets.getMonth() + 1);
              } else if (rawSets !== undefined && rawSets !== null) {
                  setsStr = rawSets.toString().trim();
              }
              resultadosMap[resData[i][0].toString().trim()] = { sets: setsStr, parciales: resData[i][2], frase: resData[i][3] ? resData[i][3].toString().trim() : '', streaming: resData[i][4] ? resData[i][4].toString().trim() : '' }; 
          }
      }"""

code = re.sub(old_res_logic, new_res_logic, code)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

