import os

js_path = r'script-dev\Código.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

login_auth_code = """
    if (action === "login_auth") {
        var dataUsuarios = sheetUsuarios.getDataRange().getValues();
        var valid = false;
        var mapNombresReales = {}; 
        for (var i = 1; i < dataUsuarios.length; i++) {
            var u = dataUsuarios[i][0];
            if(u) { mapNombresReales[u] = dataUsuarios[i][2] ? dataUsuarios[i][2].toString().trim() : u; }
            if (u == usuario && dataUsuarios[i][1] == password) { valid = true; }
        }
        if (!valid) return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Usuario o contraseña incorrectos."})).setMimeType(ContentService.MimeType.JSON);
        
        var miNombreReal = mapNombresReales[usuario] || usuario;
        var sheetInsignias = ss.getSheetByName("Insignias");
        var insigniasMap = {};
        if (sheetInsignias) {
            var dataIns = sheetInsignias.getDataRange().getValues();
            for(var i=1; i<dataIns.length; i++) {
                var usrRow = dataIns[i][0];
                if(!usrRow || usrRow !== usuario) continue;
                if(!insigniasMap[usrRow]) insigniasMap[usrRow] = [];
                var vJug = dataIns[i][1] ? dataIns[i][1].toString().trim() : "";
                var vEnt = dataIns[i][2] ? dataIns[i][2].toString().trim() : "";
                var vStf = dataIns[i][3] ? dataIns[i][3].toString().trim() : "";
                var vExj = dataIns[i][4] ? dataIns[i][4].toString().toUpperCase().trim() : "";
                var vAdm = dataIns[i][5] ? dataIns[i][5].toString().toUpperCase().trim() : "";
                if (vAdm === "X") insigniasMap[usrRow].push({ type: 'admin', text: 'Admin Web' });
                if (vStf) insigniasMap[usrRow].push({ type: 'staff', text: vStf });
                if (vEnt) insigniasMap[usrRow].push({ type: 'entrenador', text: 'Entrenador (' + vEnt + ')' });
                if (vJug) insigniasMap[usrRow].push({ type: 'jugador', text: 'Jugador (' + vJug + ')' });
                if (vExj === "X") insigniasMap[usrRow].push({ type: 'exjugador', text: 'Exjugador VCV' });
            }
        }
        
        return ContentService.createTextOutput(JSON.stringify({
            "status": "success", 
            "nombre_real": miNombreReal, 
            "insignias": insigniasMap,
            "es_admin": esAdminAutenticado
        })).setMimeType(ContentService.MimeType.JSON);
    }
"""

content = content.replace('if (action === "change_password") {', login_auth_code + '\n    if (action === "change_password") {')
content = content.replace('if (action === "login") {', 'if (action === "get_data") {')

vote_destacado_code = """
    if (action === "vote_destacado") {
        var idPart = params.id_partido;
        var jugador = params.jugador;
        var sheetVotos = ss.getSheetByName("Votos_Destacado");
        if (!sheetVotos) {
            sheetVotos = ss.insertSheet("Votos_Destacado");
            sheetVotos.appendRow(["ID_Partido", "Usuario", "Voto", "Timestamp"]);
        }
        var dataVotos = sheetVotos.getDataRange().getValues();
        var userVoted = false;
        for (var i = dataVotos.length - 1; i >= 1; i--) {
            if (dataVotos[i][0] == idPart && dataVotos[i][1] == usuario) {
                sheetVotos.getRange(i + 1, 3).setValue(jugador);
                sheetVotos.getRange(i + 1, 4).setValue(new Date());
                userVoted = true;
                break;
            }
        }
        if (!userVoted) {
            sheetVotos.appendRow([idPart, usuario, jugador, new Date()]);
        }
        return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "¡Voto registrado!"})).setMimeType(ContentService.MimeType.JSON);
    }
"""

content = content.replace('if (action === "save") {', vote_destacado_code + '\n    if (action === "save") {')

get_data_addon = """
        // Lógica de Plantillas y Votos_Destacado
        var plantillasMap = {};
        var sheetPlantillas = ss.getSheetByName("Plantillas");
        if (sheetPlantillas) {
            var dataPlant = sheetPlantillas.getDataRange().getValues();
            var eqHeadersPlant = dataPlant[0];
            for (var c = 1; c < eqHeadersPlant.length; c++) {
                var teamName = eqHeadersPlant[c];
                if (!teamName) continue;
                plantillasMap[teamName] = [];
                for (var r = 1; r < dataPlant.length; r++) {
                    var jugName = dataPlant[r][c];
                    if (jugName) {
                        plantillasMap[teamName].push(jugName.toString().trim());
                    }
                }
            }
        }

        var votosMap = {};
        var sheetVotos = ss.getSheetByName("Votos_Destacado");
        if (sheetVotos) {
            var dataVotos = sheetVotos.getDataRange().getValues();
            for (var v = 1; v < dataVotos.length; v++) {
                var pId = dataVotos[v][0];
                var pUsr = dataVotos[v][1];
                var pVoto = dataVotos[v][2];
                if (!pId) continue;
                if (!votosMap[pId]) votosMap[pId] = { total: 0, votos: {}, my_voto: null };
                votosMap[pId].total++;
                if (!votosMap[pId].votos[pVoto]) votosMap[pId].votos[pVoto] = 0;
                votosMap[pId].votos[pVoto]++;
                if (pUsr == usuario) votosMap[pId].my_voto = pVoto;
            }
        }

        for (var c = 0; c < cartelera.length; c++) {
            var cp = cartelera[c];
            cp.plantilla = plantillasMap[cp.equipo_local] || [];
            cp.votos_data = votosMap[cp.id_partido] || { total: 0, votos: {}, my_voto: null };
            var oRes = resultadosMap[cp.id_partido];
            cp.frase_destacado = oRes && oRes.frase ? oRes.frase : "";
        }
"""

content = content.replace('if(resData[i][0]) { resultadosMap[resData[i][0].toString().trim()] = { sets: resData[i][1], parciales: resData[i][2] }; }', 'if(resData[i][0]) { resultadosMap[resData[i][0].toString().trim()] = { sets: resData[i][1], parciales: resData[i][2], frase: resData[i][3] || "" }; }')
content = content.replace('var rondaAbierta = sheetAjustes.getRange("B2").getValue() || "1";', get_data_addon + '\n        var rondaAbierta = sheetAjustes.getRange("B2").getValue() || "1";')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Script Code updated successfully')

