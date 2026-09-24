import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

calendar_html = """
    <section class="section-alt" id="calendarioSection">
        <h2 style="margin-bottom: 25px;">📅 Próximos Partidos</h2>
        <div class="form-container" style="max-width: 800px; margin: 0 auto; text-align: left;">
            <div style="display:flex; gap:10px; margin-bottom:20px; flex-wrap:wrap;">
                <select id="calendarTeamSelect" class="form-control" style="flex:2; font-weight:bold; min-width:200px; border:2px solid var(--vcv-dorado);">
                    <option value="">-- Selecciona un Equipo --</option>
                </select>
                <input type="text" id="calendarSearchInput" class="form-control" placeholder="Buscar rival..." style="flex:1; min-width:150px; border:2px solid #ccc;">
            </div>
            
            <div id="calendarResults" style="display:flex; flex-direction:column; gap:12px; max-height:500px; overflow-y:auto; padding-right:5px;">
                <!-- Calendario dinámico -->
            </div>
            
            <p style="color:#888; font-size:0.8rem; margin-top:25px; font-style:italic; text-align:center; padding: 10px; border-top: 1px dashed #ccc;">
                Si alguien ve que hay alguna errata o sabe de algún cambio en algún horario de partido, notifique al correo <a href="mailto:adminfantasyvcv@gmail.com" style="color:#1565c0;">adminfantasyvcv@gmail.com</a> lo antes posible por favor, por el bien de todos.
            </p>
        </div>
    </section>
"""

# Insert right before `<footer>` inside `appSection`.
# Wait, `<footer>` is OUTSIDE `appSection`!
# <div id="appSection" style="display: none;">
#   <section>...</section>
# </div>
# <footer><p>...
idx_footer = html.find('<footer>')
if idx_footer != -1:
    # Go back to find the closing div of appSection
    end_app_section = html.rfind('</div>', 0, idx_footer)
    if end_app_section != -1:
        if 'id="calendarioSection"' not in html:
            html = html[:end_app_section] + calendar_html + "\n" + html[end_app_section:]
            print("Injected HTML before end of appSection")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
        else:
            print("Already injected")
else:
    print("Could not find footer")


