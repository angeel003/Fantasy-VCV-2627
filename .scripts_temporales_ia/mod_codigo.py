import re

with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove porrasData loading from the main loop
target_porras = """var porrasData = getSafeData(sheetPorras);
    var porrasMap = {}; 
    for(var i=1; i<porrasData.length; i++) {
        var pUser = porrasData[i][1];
        var pIdPart = porrasData[i][2].toString().trim();
        if(!porrasMap[pUser]) porrasMap[pUser] = {};
        porrasMap[pUser][pIdPart] = { sets: parseSheetText(porrasData[i][3]), puntos: porrasData[i][4], signo: porrasData[i][5] };
    }"""
if target_porras in text:
    text = text.replace(target_porras, "/* porrasData removed from global scope to speed up login */\n")
    print("Removed porrasMap from global")
else:
    print("Target porras not found")

# 2. In login action, remove predicciones_usuario from the JSON payload
target_login = """"predicciones_usuario": porrasMap[usuario] || {},"""
if target_login in text:
    text = text.replace(target_login, "")
    print("Removed predicciones_usuario from login payload")
else:
    print("Target login not found")

# 3. Wait, we still need porrasMap for other things like get_history or get_data!
# Let's restore porrasData inside action === 'get_data' or 'get_history'
target_history = """if (action === "get_history") {"""
new_history = """if (action === "get_history") {
        var porrasData = getSafeData(sheetPorras);
        var porrasMap = {}; 
        for(var i=1; i<porrasData.length; i++) {
            var pUser = porrasData[i][1];
            var pIdPart = porrasData[i][2].toString().trim();
            if(!porrasMap[pUser]) porrasMap[pUser] = {};
            porrasMap[pUser][pIdPart] = { sets: parseSheetText(porrasData[i][3]), puntos: porrasData[i][4], signo: porrasData[i][5] };
        }"""
if target_history in text:
    text = text.replace(target_history, new_history)
    print("Restored porrasMap to get_history")

# 4. Wait, what about 'get_data' ?
target_data = """if (action === "login" || action === "get_data") {"""
# Inside here it loops over porrasMap!
# "for(var pUser in porrasMap) {"
# Let's see if we can just inject porrasData creation right inside get_data / login if needed!
# Actually, if we just want to remove it from login, we can do it.
