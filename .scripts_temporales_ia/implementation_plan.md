# Plan de Implementación: Carga en 2 fases y "Jugador Destacado"

Vamos a reestructurar la forma en que la web carga los datos para que el acceso sea instantáneo, y añadiremos el sistema de votación para el mejor jugador de cada partido.

## Cambios Propuestos

### Componente: Backend (Google Apps Script)
Se realizarán las siguientes modificaciones en `script-dev/Código.js`:

#### [MODIFY] `script-dev/Código.js`
- **Fase 1 (Login rápido):** Se modificará la acción `login` para que únicamente lea la hoja de `Usuarios` y `Insignias`. Si las credenciales son correctas, devolverá inmediatamente un "OK" junto con los datos básicos del usuario, pero sin los partidos.
- **Fase 2 (Carga de datos):** Se creará una nueva acción llamada `get_data`. Esta acción será la encargada de leer el resto de hojas pesadas (`Porras`, `Resultados Oficiales`, `Ajustes`, `Ligas`, etc.) y devolver todo el paquete de partidos y puntuaciones al usuario.
- **Lógica de Jugador Destacado:** Se añadirá la lectura de la hoja `Plantillas` y `Votos_Destacado`. Se enviará al cliente la lista de jugadores disponibles por equipo.
- **Acción de votar:** Se creará una acción `vote_destacado` para que el script pueda registrar el voto del usuario en la hoja `Votos_Destacado`.

### Componente: Frontend (HTML/JS)
Se realizarán las siguientes modificaciones en `dev.html`:

#### [MODIFY] `dev.html`
- **Interfaz de Carga:** Tras hacer clic en "Entrar", si la contraseña es correcta (Fase 1), se ocultará el panel de login y se mostrará un indicador amigable ("Descargando cartelera de partidos...") mientras por debajo se realiza la segunda petición (Fase 2) para traer todo.
- **Interfaz de Jugador Destacado:**
  - Se añadirá la lógica para que las votaciones se abran exactamente **1 hora después** del inicio oficial del partido (`timestamp + 3600000` ms).
  - Se incluirá un selector desplegable con los jugadores del equipo para poder votar.
  - Se mostrará una barra de progreso con el porcentaje de votos si el usuario ya ha votado.
  - Si el partido finalizó (o pasaron más de 24h), se mostrará al Jugador Destacado ganador junto con su foto obtenida desde el repositorio (ej: `files/jugadores/Nombre.png`) y sus declaraciones (extraídas de `Resultados Oficiales`).

## Plan de Verificación

### Pruebas Manuales
- Iniciar sesión y comprobar visualmente que la entrada es inmediata y luego carga los partidos (dos fases).
- Simular un partido cuya fecha fue hace 1h y comprobar que permite votar.
- Simular un partido cuya fecha fue hace 2 días y comprobar que muestra el ganador, las barras de porcentaje, la foto y las declaraciones.

