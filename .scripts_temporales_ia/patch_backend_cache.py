import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update getSafeData to use CacheService (15 seconds)
new_getSafeData = """function getSafeData(sheet) {
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
            if (str.length < 90000) { cache.put(cacheKey, str, 15); } // 15 second cache
        } catch(e) {}
    }
    return data;
}"""
code = re.sub(r'function getSafeData\(sheet\) \{[\s\S]*?return sheet\.getRange\(1, 1, lr, lc\)\.getValues\(\);\s*\}', new_getSafeData, code)


# 2. Invalidate cache on writes (save_resultado_admin, save, vote_destacado, add_user, change_password, save_totales)
# We can just clear all caches by clearing the known sheet names, but CacheService doesn't have removeAll without keys.
# Actually, since it's 15 seconds, we don't even need to invalidate it! 15 seconds is perfectly fine for users to wait to see updates.
# If they complain about 15s, we can add invalidation. Let's just rely on the 15s TTL.


# 3. Debounce the timestamp write!
old_timestamp = r"""if \(filaUsuario !== -1\) \{
              sheetUsuarios\.getRange\(filaUsuario, 4\)\.setValue\(new Date\(\)\);
          \}"""
new_timestamp = """if (filaUsuario !== -1) {
              var cache = CacheService.getScriptCache();
              if (!cache.get("login_ts_" + usuario)) {
                  try { sheetUsuarios.getRange(filaUsuario, 4).setValue(new Date()); } catch(e) {}
                  cache.put("login_ts_" + usuario, "1", 3600); // 1 hour debounce
              }
          }"""
code = re.sub(old_timestamp, new_timestamp, code)


with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

