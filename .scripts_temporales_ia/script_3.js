
        function toggleFab() {
            var links = document.getElementById('fab-links');
            var btn = document.getElementById('fab-btn');
            if (links.style.display === 'none' || links.style.display === '') {
                links.style.display = 'flex';
                btn.style.transform = 'rotate(45deg)';
            } else {
                links.style.display = 'none';
                btn.style.transform = 'rotate(0deg)';
            }
        }
        
        
        // Cierra el menú de la lupa al hacer click fuera
        document.addEventListener('click', function(event) {
            var fabMenu = document.getElementById('fab-menu');
            var links = document.getElementById('fab-links');
            var btn = document.getElementById('fab-btn');
            
            if (fabMenu && links && btn) {
                var isClickInside = fabMenu.contains(event.target);
                if (!isClickInside && links.style.display === 'flex') {
                    links.style.display = 'none';
                    btn.style.transform = 'rotate(0deg)';
                }
            }
        });
        
        function checkFabVisibility() {
            var appSec = document.getElementById('appSection');
            
            // NO MOSTRAR EN MODO INVITADO
            // currentUser usa 'let', así que no está en 'window'. Lo comprobamos de forma segura.
            var isGuest = true;
            try {
                if (typeof currentUser !== 'undefined' && currentUser && currentUser !== "INVITADO") {
                    isGuest = false;
                }
            } catch(e) {}
            
            if(appSec && appSec.style.display !== 'none' && !isGuest) {
                document.getElementById('fab-menu').style.display = 'block';
                
                // Show/hide specific links based on section visibility
                var cartelera = document.getElementById('carteleraSection');
                var ranking = document.getElementById('clasificacionesSection');
                var enlaces = document.getElementById('enlacesRfevbSection');
                var historial = document.getElementById('historialSection');
                var calendario = document.getElementById('calendarioSection');
                var totales = document.getElementById('prediccionesTotalesSection');
                
                document.getElementById('fab-cartelera').style.display = (cartelera && cartelera.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-ranking').style.display = (ranking && ranking.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-enlaces').style.display = (enlaces && enlaces.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-historial').style.display = (historial && historial.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-calendario').style.display = (calendario && calendario.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-totales').style.display = (totales && totales.style.display !== 'none') ? 'block' : 'none';
                
            } else {
                document.getElementById('fab-menu').style.display = 'none';
                document.getElementById('fab-links').style.display = 'none';
            }
        }
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                checkFabVisibility();
            });
        });
        
        var appSec = document.getElementById('appSection');
        if(appSec) {
            observer.observe(appSec, { attributes: true, subtree: true });
        }
        setInterval(checkFabVisibility, 1000);
    