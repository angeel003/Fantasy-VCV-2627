import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove the broken injections
code = code.replace('if (isWriteAction && typeof clearAllCache === "function") { clearAllCache(); }\n      return ContentService', 'return ContentService')
code = code.replace('if (isWriteAction && typeof clearAllCache === "function") { clearAllCache(); }\n        return ContentService', 'return ContentService')
code = code.replace('if (isWriteAction && typeof clearAllCache === "function") { clearAllCache(); }\n    return ContentService', 'return ContentService')
# generic regex to catch any indentation
code = re.sub(r'if \(isWriteAction && typeof clearAllCache === "function"\) \{ clearAllCache\(\); \}\s+return ContentService', 'return ContentService', code)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

