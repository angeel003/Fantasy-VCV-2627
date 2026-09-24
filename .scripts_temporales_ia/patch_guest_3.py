import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix the second block's CERRADO check.
# The block looks like this:
#                  if (eq.oficial_sets && eq.oficial_sets.includes("-")) {
#                      esPasado = true;
#                      let sL = parseInt(eq.oficial_sets.split("-")[0]);
#                      let sV = parseInt(eq.oficial_sets.split("-")[1]);
#                      let textoRes = sL > sV ? `<span style="color:#28a745; font-weight:bold; margin-left:5px;">✅ Ganado</span>` : `<span style="color:var(--vcv-rojo); font-weight:bold; margin-left:5px;">❌ Perdido</span>`;
#                      
#                      infoAdicional = `
#                      <div style="margin-top:10px; background:var(--bg-general); border-left:4px solid var(--vcv-morado); padding:10px; border-radius:4px;">
#                          <span style="font-size:0.85rem; color:#666; text-transform:uppercase; letter-spacing:0.5px;">Resultado Oficial</span><br>
#                          <b style="font-size:1.1rem; color:var(--vcv-negro);">${eq.oficial_sets}</b> ${textoRes} <br>
#                          <span style="font-size:0.9rem; color:#555;">(${eq.oficial_parciales})</span>
#                      </div>`;
#                  } else if (eq.estado === "CERRADO" || eq.visibilidad === "OCULTAR") {
#                      esPasado = true;
#                      infoAdicional = `<div style="margin-top:10px;"><span style="background-color:#e2e3e5; color:#383d41; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:0.85rem;">🔒 Partido finalizado</span></div>`;
#                  } else {
#                      infoAdicional = `<div style="margin-top:10px;"><span style="background-color:#d4edda; color:#155724; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:0.85rem;">⏳ Próximamente</span></div>`;
#                  }

# We need to remove `esPasado = true;` from the `else if`. 
# Wait, if we remove `esPasado = true;` from the `else if`, it will be `false`. So it will be treated as `Próximo`. 
# But in guest mode, we ONLY pushed into `data.equipos` the ones that are actual past results (`esPasado=true` in the first filter) OR upcoming within 10 days.
# So if a match is CERRADO but has no score, it will just show "Partido finalizado" but in the "Próximos Partidos" list? 
# Wait, if a match is CERRADO but has no score, maybe we shouldn't even show it, but the user is complaining that round 22 showed up as PAST matches.
# Why did round 22 show up as past matches in the first place?
# Ah! I know! In `appData.equipos`, the sort logic reversed the order or something?
# Let's fix the second block.

block_to_find = 'else if (eq.estado === "CERRADO" || eq.visibilidad === "OCULTAR") {\n                      esPasado = true;'
block_to_replace = 'else if (eq.estado === "CERRADO" || eq.visibilidad === "OCULTAR") {\n                      // esPasado = true; Removed to prevent fake past matches'

html = html.replace(block_to_find, block_to_replace)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print("Patched dev.html second CERRADO check")

