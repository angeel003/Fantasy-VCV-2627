# Modificaciones a realizar en tu Google Sheets

Cuando entres a tu Google Sheets online (el real), asegúrate de hacer los siguientes cambios para que todo funcione con las nuevas implementaciones que estamos desarrollando.

## 1. Hoja: Resultados Oficiales
Actualmente tienes 3 columnas (`ID Partido`, `Sets Oficial`, `Parciales Oficial`).
- **Añade una Cuarta Columna (Columna D):** Llámala `Declaraciones Jugador Destacado`. 
  - *Uso:* Aquí pegarás la frase que ha dicho el jugador destacado al terminar el partido. El sistema la cogerá automáticamente.

## 2. Hoja: Plantillas
Tu estructura actual es perfecta (Fila 1 con nombres de equipos y Columna A con los dorsales).
- No necesitas cambiar la estructura. 
- Solo asegúrate de que los nombres de los jugadores coincidan exactamente con cómo vas a llamar a las fotos que subas a GitHub (ej: si el jugador se llama `Yeray`, la foto en tu repo deberá llamarse `Yeray.png`).

## 3. Hoja: Ajustes (Opcional)
- Si en esta hoja tenías alguna columna antigua llamada "Frase MVP" que estabas probando, puedes borrarla tranquilamente, ya que la nueva columna en `Resultados Oficiales` es la que controlará esto.

## 4. Crear hoja de almacenamiento de votos: Votos_Destacado
Para que el script pueda guardar los votos que hacen los usuarios, necesitamos crear una nueva hoja donde se vayan apuntando:
- **Crea una nueva pestaña/hoja** y llámala exactamente: `Votos_Destacado`
- **Fila 1 (Cabeceras):** 
  - Columna A: `ID_Partido`
  - Columna B: `Usuario`
  - Columna C: `Voto` (nombre del jugador por el que votó)
  - Columna D: `Timestamp` (fecha y hora del voto)



### 4. Pestaña 'Usuarios'
- En la **Columna D (Fila 1)** escribe como cabecera: Último Acceso.
- A partir de ahora, cada vez que un usuario inicie sesión, se registrará automáticamente en esa columna la fecha y hora de su entrada al Fantasy.


### 5. Pestaña 'Resultados Oficiales'
- La tabla debe tener exactamente 5 columnas en este orden: ID_Partido (Col A), Sets (Col B), Parciales (Col C), Frase_MVP (Col D), Streaming (Col E).
- A través del panel de administrador de la web, se escribirán automáticamente aquí los datos (incluyendo el enlace de Twitch/YouTube y la frase del Jugador Destacado).
