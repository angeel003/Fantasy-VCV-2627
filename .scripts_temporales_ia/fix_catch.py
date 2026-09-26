import re

with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """  } catch (error) { return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": error.message})).setMimeType(ContentService.MimeType.JSON); }"""
new = """  } catch (error) { 
      var errStr = "";
      try { errStr = error.message || error.toString(); } catch(e) { errStr = "Error parseando la excepción"; }
      if (!errStr || errStr === "undefined") errStr = "Excepción nativa sin mensaje (posible cuota excedida).";
      return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": errStr, "raw_error": JSON.stringify(error)})).setMimeType(ContentService.MimeType.JSON); 
  }"""

if target in text:
    text = text.replace(target, new)
    with open('script-v2/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed global catch")
else:
    print("Target not found")
