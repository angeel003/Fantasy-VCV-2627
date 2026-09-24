import re

filename = 'script-dev/Código.js'
with open(filename, 'r', encoding='utf-8') as f:
    js = f.read()

old_cartelera = """        var cartelera = [];
        var todosPartidos = [];
        for(var i=0; i<partidos.length; i++) { 
            if(partidos[i].permitido) {
                todosPartidos.push(partidos[i]);
                if(partidos[i].visibilidad === "MOSTRAR") {
                    cartelera.push(partidos[i]);
                }
            } 
        }"""

new_cartelera = """        var cartelera = [];
        var todosPartidos = [];
        var idsEnCartelera = {};
        var idsEnTodos = {};
        
        for(var i=0; i<partidos.length; i++) { 
            if(partidos[i].permitido) {
                var pId = partidos[i].id_partido;
                
                if(!idsEnTodos[pId]) {
                    todosPartidos.push(partidos[i]);
                    idsEnTodos[pId] = partidos[i];
                } else {
                    idsEnTodos[pId].es_derby = true;
                }
                
                if(partidos[i].visibilidad === "MOSTRAR") {
                    if(!idsEnCartelera[pId]) {
                        cartelera.push(partidos[i]);
                        idsEnCartelera[pId] = partidos[i];
                    } else {
                        idsEnCartelera[pId].es_derby = true;
                    }
                }
            } 
        }"""

js = js.replace(old_cartelera, new_cartelera)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(js)
    print("Patched deduplication and es_derby detection correctly!")

