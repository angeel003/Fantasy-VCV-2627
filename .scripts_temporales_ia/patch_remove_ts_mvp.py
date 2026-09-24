import re

# 1. Modify dev.html
with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_mvp_logic = r"""                      // --- LOGICA JUGADOR DESTACADO ---
                      let destacadoHtml = "";
                      let ts1h = eq\.timestamp \? \(eq\.timestamp \+ \(60 \* 60 \* 1000\)\) : 0;
                      let ts24h = eq\.timestamp \? \(eq\.timestamp \+ \(24 \* 60 \* 60 \* 1000\)\) : 0;
                      
                      if \(eq\.timestamp && nowMs < ts1h\) \{
                          let d = new Date\(ts1h\);
                          let h1 = d\.getHours\(\)\.toString\(\)\.padStart\(2, '0'\); let m1 = d\.getMinutes\(\)\.toString\(\)\.padStart\(2, '0'\);
                          destacadoHtml = `<div class="mvp-box"><div style="color:#666; font-size:0\.9rem; text-align:center;">⏳ La votación del <b>Jugador Destacado</b> se abrirá a las \$\{h1\}:\$\{m1\}</div></div>`;
                      \} else if \(eq\.timestamp && nowMs >= ts1h && nowMs < ts24h\) \{
                          if \(eq\.plantilla && eq\.plantilla\.length > 0\) \{
                              if \(eq\.votos_data && eq\.votos_data\.my_voto\) \{
                                  let resultsArray = Object\.keys\(eq\.votos_data\.votos\)\.map\(j => \{ return \{ nombre: j, votos: eq\.votos_data\.votos\[j\] \}; \}\);
                                  resultsArray\.sort\(\(a,b\) => b\.votos - a\.votos\);
                                  let totalVotos = eq\.votos_data\.total;
                                  let barras = resultsArray\.map\(res => \{
                                      let pct = Math\.round\(\(res\.votos / totalVotos\) \* 100\);
                                      let highlight = \(res\.nombre === eq\.votos_data\.my_voto\) \? 'box-shadow: 0 0 5px var\(--vcv-dorado\); border: 1px solid var\(--vcv-dorado\);' : '';
                                      return `<div class="mvp-bar-bg" style="\$\{highlight\}"><div class="mvp-bar-fill" style="width: \$\{pct\}%;"></div><div class="mvp-bar-text">\$\{res\.nombre\} \$\{res\.nombre === eq\.votos_data\.my_voto \? '\(Tú\)' : ''\}</div><div class="mvp-bar-pct">\$\{pct\}% \(\$\{res\.votos\}\)</div></div>`;
                                  \}\)\.join\(""\);
                                  destacadoHtml = `<div class="mvp-box"><div class="mvp-title">📊 Resultados Jugador Destacado</div>\$\{barras\}</div>`;
                              \} else \{
                                  let opciones = `<option value="">Selecciona un jugador\.\.\.</option>` \+ eq\.plantilla\.map\(j => `<option value="\$\{j\}">\$\{j\}</option>`\)\.join\(""\);
                                  destacadoHtml = `<div class="mvp-box" style="border-color: var\(--vcv-dorado\); background: #fffdf5;"><div class="mvp-title">⭐ ¡Vota al Jugador Destacado!</div><div style="display:flex; gap:10px;"><select class="form-control" id="sel_destacado_\$\{eq\.id_partido\}">\$\{opciones\}</select><button class="btn btn-primary" style="font-weight:bold; white-space:nowrap;" onclick="votarDestacado\(event, '\$\{eq\.id_partido\}'\)">Votar</button></div></div>`;
                              \}
                          \} else \{
                              destacadoHtml = `<div class="mvp-box"><div style="color:#888; font-size:0\.85rem; text-align:center;">Plantilla no disponible para votación\.</div></div>`;
                          \}
                      \} else if \(eq\.timestamp && nowMs >= ts24h && eq\.votos_data && eq\.votos_data\.total > 0\) \{
                          let resultsArray = Object\.keys\(eq\.votos_data\.votos\)\.map\(j => \{ return \{ nombre: j, votos: eq\.votos_data\.votos\[j\] \}; \}\);
                          resultsArray\.sort\(\(a,b\) => b\.votos - a\.votos\);
                          let ganador = resultsArray\[0\];
                          let totalVotos = eq\.votos_data\.total;
                          let pct = Math\.round\(\(ganador\.votos / totalVotos\) \* 100\);
                          let fraseHtml = eq\.frase_destacado \? `<div class="mvp-quote">\$\{eq\.frase_destacado\}</div>` : "";
                          
                          let photoUrl = `files/jugadores/\$\{ganador\.nombre\.replace\(/ /g, '_'\)\}\.png`;
                          let photoHtml = `<img src="\$\{photoUrl\}" onerror="this\.style\.display='none'" style="width:60px; height:60px; border-radius:50%; border:2px solid var\(--vcv-dorado\); background:#fff; margin-bottom:10px; object-fit:cover;">`;
                          
                          destacadoHtml = `<div class="mvp-winner-box"><div style="font-size:0\.85rem; color:#f8f9fa; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px;">⭐ Jugador Destacado ⭐</div>\$\{photoHtml\}<div style="font-size:1\.3rem; font-weight:bold; color:var\(--vcv-dorado\);">\$\{ganador\.nombre\}</div><div style="font-size:0\.8rem; color:#eee; margin-top:2px;">Elegido con el \$\{pct\}% de los votos</div>\$\{fraseHtml\}</div>`;
                      \}
                      // --- FIN LOGICA JUGADOR DESTACADO ---"""

new_mvp_logic = """                      // --- LOGICA JUGADOR DESTACADO ---
                      let destacadoHtml = "";
                      if (eq.plantilla && eq.plantilla.length > 0) {
                          let ts1h = eq.timestamp ? (eq.timestamp + (60 * 60 * 1000)) : 0;
                          let ts24h = eq.timestamp ? (eq.timestamp + (24 * 60 * 60 * 1000)) : 0;
                          
                          if (eq.timestamp && nowMs < ts1h) {
                              let d = new Date(ts1h);
                              let h1 = d.getHours().toString().padStart(2, '0'); let m1 = d.getMinutes().toString().padStart(2, '0');
                              destacadoHtml = `<div class="mvp-box"><div style="color:#666; font-size:0.9rem; text-align:center;">⏳ La votación del <b>Jugador Destacado</b> se abrirá a las ${h1}:${m1}</div></div>`;
                          } else if (eq.timestamp && nowMs >= ts1h && nowMs < ts24h) {
                              if (eq.votos_data && eq.votos_data.my_voto) {
                                  let resultsArray = Object.keys(eq.votos_data.votos).map(j => { return { nombre: j, votos: eq.votos_data.votos[j] }; });
                                  resultsArray.sort((a,b) => b.votos - a.votos);
                                  let totalVotos = eq.votos_data.total;
                                  let barras = resultsArray.map(res => {
                                      let pct = Math.round((res.votos / totalVotos) * 100);
                                      let highlight = (res.nombre === eq.votos_data.my_voto) ? 'box-shadow: 0 0 5px var(--vcv-dorado); border: 1px solid var(--vcv-dorado);' : '';
                                      return `<div class="mvp-bar-bg" style="${highlight}"><div class="mvp-bar-fill" style="width: ${pct}%;"></div><div class="mvp-bar-text">${res.nombre} ${res.nombre === eq.votos_data.my_voto ? '(Tú)' : ''}</div><div class="mvp-bar-pct">${pct}% (${res.votos})</div></div>`;
                                  }).join("");
                                  destacadoHtml = `<div class="mvp-box"><div class="mvp-title">📊 Resultados Jugador Destacado</div>${barras}</div>`;
                              } else {
                                  let opciones = `<option value="">Selecciona un jugador...</option>` + eq.plantilla.map(j => `<option value="${j}">${j}</option>`).join("");
                                  destacadoHtml = `<div class="mvp-box" style="border-color: var(--vcv-dorado); background: #fffdf5;"><div class="mvp-title">⭐ ¡Vota al Jugador Destacado!</div><div style="display:flex; gap:10px;"><select class="form-control" id="sel_destacado_${eq.id_partido}">${opciones}</select><button class="btn btn-primary" style="font-weight:bold; white-space:nowrap;" onclick="votarDestacado(event, '${eq.id_partido}')">Votar</button></div></div>`;
                              }
                          } else if (eq.timestamp && nowMs >= ts24h && eq.votos_data && eq.votos_data.total > 0) {
                              let resultsArray = Object.keys(eq.votos_data.votos).map(j => { return { nombre: j, votos: eq.votos_data.votos[j] }; });
                              resultsArray.sort((a,b) => b.votos - a.votos);
                              let ganador = resultsArray[0];
                              let totalVotos = eq.votos_data.total;
                              let pct = Math.round((ganador.votos / totalVotos) * 100);
                              let fraseHtml = eq.frase_destacado ? `<div class="mvp-quote">${eq.frase_destacado}</div>` : "";
                              
                              let photoUrl = `files/jugadores/${ganador.nombre.replace(/ /g, '_')}.png`;
                              let photoHtml = `<img src="${photoUrl}" onerror="this.style.display='none'" style="width:60px; height:60px; border-radius:50%; border:2px solid var(--vcv-dorado); background:#fff; margin-bottom:10px; object-fit:cover;">`;
                              
                              destacadoHtml = `<div class="mvp-winner-box"><div style="font-size:0.85rem; color:#f8f9fa; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px;">⭐ Jugador Destacado ⭐</div>${photoHtml}<div style="font-size:1.3rem; font-weight:bold; color:var(--vcv-dorado);">${ganador.nombre}</div><div style="font-size:0.8rem; color:#eee; margin-top:2px;">Elegido con el ${pct}% de los votos</div>${fraseHtml}</div>`;
                          }
                      }
                      // --- FIN LOGICA JUGADOR DESTACADO ---"""

html = re.sub(old_mvp_logic, new_mvp_logic, html)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Modify script-dev/Código.js (Remove timestamp write completely)
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_ts_logic = r"""      // Registrar último Acceso si es login o get_data
      if \(action === "login" \|\| action === "get_data"\) \{
          if \(filaUsuario !== -1\) \{
              var cache = CacheService\.getScriptCache\(\);
              if \(!cache\.get\("login_ts_" \+ usuario\)\) \{
                  try \{ sheetUsuarios\.getRange\(filaUsuario, 4\)\.setValue\(new Date\(\)\); \} catch\(e\) \{\}
                  cache\.put\("login_ts_" \+ usuario, "1", 3600\); // 1 hour
              \}
          \}
      \}"""

code = re.sub(old_ts_logic, "", code)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)


