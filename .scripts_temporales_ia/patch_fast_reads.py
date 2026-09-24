import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Add getSafeData helper function at the top of the file, outside any functions
helper_func = """
function getSafeData(sheet) {
    if (!sheet) return [];
    var lr = sheet.getLastRow();
    var lc = sheet.getLastColumn();
    if (lr === 0 || lc === 0) return [];
    return sheet.getRange(1, 1, lr, lc).getValues();
}

function doPost(e) {
"""

code = code.replace("function doPost(e) {", helper_func)

# Replace all occurrences of .getDataRange().getValues() and .getDisplayValues()
# Using regex to find the sheet variable name
code = re.sub(r'(\w+)\.getDataRange\(\)\.getValues\(\)', r'getSafeData(\1)', code)
code = re.sub(r'(\w+)\.getDataRange\(\)\.getDisplayValues\(\)', r'getSafeData(\1)', code)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

