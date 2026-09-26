import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_js = r"""document.getElementById('displayJugador').innerHTML = "👤 " + displayNom;
            
            let misInsignias = data.insignias[usr] || [];
            let insigniasHeaderHtml = "";
            let isAdmin = false;
            
            misInsignias.forEach(b => {
                if (b.type === 'admin') isAdmin = true;
                let cssColorClass = getBadgeCSS(b.type);
                insigniasHeaderHtml += `<img src="${URL_BADGE_GENERIC}" class="badge-header ${cssColorClass}" title="${b.text}" onclick="showMobileTooltip(event, '${b.text}')">`;
            });
            document.getElementById('displayBadges').innerHTML = insigniasHeaderHtml;"""

new_js = r"""document.getElementById('displayJugador').innerHTML = "👤 " + displayNom;
            
            // Populating new Header V2
            document.getElementById('h2-user-name').innerText = displayNom;
            document.getElementById('h2-user-handle').innerText = "@" + usr;
            
            let misInsignias = data.insignias[usr] || [];
            let insigniasHeaderHtml = "";
            let insigniasH2Html = "";
            let isAdmin = false;
            
            misInsignias.forEach(b => {
                if (b.type === 'admin') isAdmin = true;
                let cssColorClass = getBadgeCSS(b.type);
                insigniasHeaderHtml += `<img src="${URL_BADGE_GENERIC}" class="badge-header ${cssColorClass}" title="${b.text}" onclick="showMobileTooltip(event, '${b.text}')">`;
                
                // NO tooltips, NO onclick for the top header badges! Just visual.
                insigniasH2Html += `<div class="${cssColorClass}" style="width:14px; height:14px; border-radius:50%; display:flex; align-items:center; justify-content:center;"><img src="${URL_BADGE_GENERIC}" style="width:8px; height:8px; filter:brightness(0) invert(1);"></div>`;
            });
            document.getElementById('displayBadges').innerHTML = insigniasHeaderHtml;
            document.getElementById('h2-user-badges').innerHTML = insigniasH2Html;
            
            // Render lucide icons in the newly injected HTML
            lucide.createIcons();"""

text = text.replace(old_js, new_js)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("JS injected")
