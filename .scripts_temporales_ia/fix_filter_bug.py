import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Inject type="button" to avoid form submissions
text = text.replace(
    '`<button class="cat-filter-btn active" data-filter="all">Todos (${totalCount})</button>`;',
    '`<button type="button" class="cat-filter-btn active" data-filter="all">Todos (${totalCount})</button>`;'
)
text = text.replace(
    'html += `<button class="cat-filter-btn" data-filter="${cat}">${displayName} (${count})</button>`;',
    'html += `<button type="button" class="cat-filter-btn" data-filter="${cat}">${displayName} (${count})</button>`;'
)

# 2. Expose updateCategoryFilter globally and remove MutationObserver
old_iife = """// --- CATEGORY FILTER LOGIC ---
    (function() {
        const contenedor = document.getElementById('contenedorPartidos');
        const wrapper = document.getElementById('categoryFilterWrapper');
        if(!contenedor || !wrapper) return;

        function updateCategoryFilter() {"""

new_iife = """// --- CATEGORY FILTER LOGIC ---
    window.updateCategoryFilter = function() {
        const contenedor = document.getElementById('contenedorPartidos');
        const wrapper = document.getElementById('categoryFilterWrapper');
        if(!contenedor || !wrapper) return;"""

text = text.replace(old_iife, new_iife)

old_observer = """        const observer = new MutationObserver((mutations) => {
            updateCategoryFilter();
        });
        
        observer.observe(contenedor, { childList: true, subtree: true });
    })();"""

new_observer = """    };"""

text = text.replace(old_observer, new_observer)

# 3. Call window.updateCategoryFilter() after rendering the matches
text = text.replace(
    "document.getElementById('contenedorPartidos').innerHTML = htmlPartidos;\n            iniciarRelojes();",
    "document.getElementById('contenedorPartidos').innerHTML = htmlPartidos;\n            if(window.updateCategoryFilter) window.updateCategoryFilter();\n            iniciarRelojes();"
)
text = text.replace(
    "document.getElementById('contenedorPartidos').innerHTML = finalHtml;\n            document.getElementById('loginSection').style.display = \"none\";\n            if(typeof iniciarRelojes === 'function') iniciarRelojes();",
    "document.getElementById('contenedorPartidos').innerHTML = finalHtml;\n            if(window.updateCategoryFilter) window.updateCategoryFilter();\n            document.getElementById('loginSection').style.display = \"none\";\n            if(typeof iniciarRelojes === 'function') iniciarRelojes();"
)


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS filter bug fixed")
