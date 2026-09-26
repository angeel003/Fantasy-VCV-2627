import re

with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        clearAllCache();
        
    }

    if (action === "load")"""

new = """        clearAllCache();
        return ContentService.createTextOutput(JSON.stringify({"status": "success"})).setMimeType(ContentService.MimeType.JSON);
    }

    if (action === "load")"""

if target in text:
    text = text.replace(target, new)
    with open('script-v2/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed save return statement")
else:
    print("Target not found")
