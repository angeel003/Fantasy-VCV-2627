import re

with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """function getSafeData(sheet) {
    if (!sheet) return [];
    var cache = CacheService.getScriptCache();
    var sheetName = sheet.getName();
    var cacheKey = "vcv_sheet_" + sheetName;
    
    var cached = cache.get(cacheKey);
    if (cached) {
        try { return JSON.parse(cached); } catch(e) {}
    }
    
    var lr = sheet.getLastRow();
    var lc = sheet.getLastColumn();
    var data = [];
    if (lr > 0 && lc > 0) {
        data = sheet.getRange(1, 1, lr, lc).getValues();
    }
    
    if (data.length > 0) {
        try {
            var str = JSON.stringify(data);
            if (str.length < 90000) { cache.put(cacheKey, str, 21600); } // 15 second cache
        } catch(e) {}
    }
    return data;
}"""

new = """function getSafeData(sheet) {
    if (!sheet) return [];
    var sheetName = sheet.getName();
    
    var lr = sheet.getLastRow();
    var lc = sheet.getLastColumn();
    
    // Bypass cache for highly mutable sheets to prevent race conditions on login
    if (sheetName === "Porras") {
        if (lr > 0 && lc > 0) return sheet.getRange(1, 1, lr, lc).getValues();
        return [];
    }

    var cache = CacheService.getScriptCache();
    var cacheKey = "vcv_sheet_" + sheetName;
    
    var cached = cache.get(cacheKey);
    if (cached) {
        try { return JSON.parse(cached); } catch(e) {}
    }
    
    var data = [];
    if (lr > 0 && lc > 0) {
        data = sheet.getRange(1, 1, lr, lc).getValues();
    }
    
    if (data.length > 0) {
        try {
            var str = JSON.stringify(data);
            if (str.length < 90000) { cache.put(cacheKey, str, 21600); } 
        } catch(e) {}
    }
    
    return data;
}"""

if target in text:
    text = text.replace(target, new)
    with open('script-v2/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced getSafeData")
else:
    print("Target not found")
