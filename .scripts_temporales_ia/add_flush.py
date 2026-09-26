import re

with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "¡Predicciones guardadas!"})).setMimeType(ContentService.MimeType.JSON);"""
new = """SpreadsheetApp.flush(); clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "¡Predicciones guardadas!"})).setMimeType(ContentService.MimeType.JSON);"""

if target in text:
    text = text.replace(target, new)
    with open('script-v2/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added SpreadsheetApp.flush() to save action")
else:
    print("Target not found")
