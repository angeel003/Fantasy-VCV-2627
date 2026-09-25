# Documentación Técnica y Arquitectura: Fantasy VCV 26/27

Este documento es una especificación técnica completa (PRD/Technical Summary) de la aplicación **Fantasy VCV 26/27**. Está diseñado para proporcionar todo el contexto necesario a un agente de IA (como Google Stitch) para migrar o reconstruir la aplicación en su Versión 2.

---

## 1. Stack Tecnológico Actual
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6). Sin frameworks pesados. Implementado como una **PWA** (Progressive Web App) con `manifest.json` y `sw.js` (Service Worker).
- **Backend / API**: **Google Apps Script (GAS)**, expuesto como una Web App (Endpoint único que procesa peticiones `POST`).
- **Base de Datos**: **Google Sheets** (100% serverless, usado como base de datos relacional básica).
- **Despliegue**: Frontend distribuido como PWA y/o archivo `.apk` (Android) generado mediante *Bubblewrap / PWA Builder*.

---

## 2. Estructura de la Base de Datos (Google Sheets)
El backend lee y escribe en pestañas (sheets) específicas:

1. **`Usuarios`**:
   - Columnas: `Usuario` (@nombre), `Password`, `NombreReal`, `Estado` (Activo/Baja), `Insignias` (Jugador, Staff, Socio, etc.), `Admin` (TRUE/FALSE).
2. **`Partidos`**:
   - Columnas: `ID_Partido`, `Jornada`, `Categoria` (Ej: SM2, 1ª Masc), `Equipo_VCV`, `Rival`, `Es_Local` (TRUE/FALSE), `Fecha_Hora` (Timestamp), `Estado` (PROGRAMADO, EN JUEGO, FINALIZADO), `Res_Sets`, `Res_Puntos`, `Res_Signo`, `Bloqueado` (Booleano de seguridad).
3. **`Predicciones`**:
   - Almacena las apuestas. Filas por usuario, columnas por `ID_Partido`. El cruce guarda un JSON stringificado: `{"sets":"3-1", "puntos":"14", "signo":"+"}`.
4. **`Ligas`**:
   - Gestiona las Ligas Privadas. La columna A tiene los `@usuarios`. La fila 1 tiene los nombres de las ligas (Ej: `General`, `Amigos`, `Veteranos`). Si hay una "X" en la celda, el usuario pertenece a esa liga.
5. **`Configuracion`**:
   - Parámetros del sistema: `Jornada_Activa`, URLs oficiales de la RFEVB, textos del sistema.

---

## 3. Contrato de la API (Backend Apps Script)
El frontend se comunica con el servidor haciendo `fetch` POST al `SCRIPT_URL`. Todo viaja en el `body` como un JSON stringificado y el servidor responde con JSON.

### Endpoints (Acciones del Payload)

#### `action: "login"`
- **Input**: `{ "action": "login", "usuario": "@...", "password": "..." }`
- **Output**: JSON con TODO el estado inicial de la app:
  - `status`: "success" | "error"
  - `jornada`: Jornada actual activa.
  - `equipos`: Array de partidos de la jornada actual (solo los de esta jornada).
  - `todos_partidos`: Historial completo de partidos de jornadas anteriores para el historial.
  - `clasificaciones`: Objeto con las tablas de clasificación calculadas *on-the-fly* por el servidor para cada Liga Privada.
  - `ligas`: Array de ligas a las que pertenece el usuario.
  - `insignias`: Objeto que asocia usuarios con sus roles visuales.
  - `is_admin`: Booleano para inyectar panel de control.

#### `action: "save"`
- **Input**: `{ "action": "save", "usuario": "...", "password": "...", "predicciones": { "PARTIDO_1": {"sets":"3-1", "puntos":"15", "signo":"+"} } }`
- **Comportamiento**: Escribe en la hoja `Predicciones`. El servidor valida primero que el partido NO esté "bloqueado" por tiempo.

#### `action: "load"`
- Devuelve las predicciones ya guardadas por el usuario para la jornada activa, para poblar los inputs de la interfaz.

#### `action: "add_user"` (Admin)
- Permite a los administradores crear cuentas nuevas directamente desde el frontend e inscribirlas en ligas privadas enviando el array `ligas_seleccionadas`.

---

## 4. Funcionalidades y Pantallas del Frontend

### 4.1. Pantalla de Inicio y Login
- Login con validación servidor.
- Botón "Entrar como Invitado" (vista de solo lectura ocultando partes de la app).
- Sección de FAQs y Gestión (acordeones HTML nativos `<details>`):
  - Qué es la app, reglas de puntuación.
  - Instrucciones de instalación (APK para Android, Safari PWA para iOS).
  - Formularios para: Cambiar Contraseña y Solicitar Cambio de Nombre.

### 4.2. Intranet de Administrador (Oculto por defecto)
Si `is_admin == true`, se renderiza una caja azul especial en el inicio:
- Crear nuevos usuarios e inscribirlos en ligas mediante checkboxes generados dinámicamente.
- Subir resultados rápidos: Permite al admin insertar el resultado oficial de un partido en vivo para que recalcule las clasificaciones al instante.

### 4.3. Cartelera de Partidos (Pronósticos)
- Lista de partidos activos (filtrados del array `equipos`).
- **Seguridad**: Si faltan menos de 15 minutos para la `Fecha_Hora` oficial, el backend manda `bloqueado: true` y el frontend deshabilita los inputs mostrando un candado.
- **Inputs Clave por Partido**:
  - **Sets**: Resultado exacto en sets (Ej: 3-0, 3-2, etc.).
  - **Diferencia de Puntos**: Valor absoluto numérico (Ej: 14 pts).
  - **Signo**: A favor (+) o En contra (-). Esto es crucial para la regla de negocio del VCV.
- Botón global (Floating Action Button o Bottom Navbar en V2) para enviar `action: "save"`.

### 4.4. Ranking (Clasificaciones)
- Tablas de clasificación generadas automáticamente por el backend.
- Separadas por pestañas/botones según las **Ligas Privadas** a las que pertenezca el usuario (Ej: "Liga General", "1ª Masculina").

### 4.5. Mis Predicciones (Historial)
- Lista de todos los partidos anteriores del usuario.
- Muestra el Pronóstico del usuario vs Resultado Oficial de la Federación.
- Muestra los puntos ganados (o perdidos) y medallas en base a si hizo pleno (sets y puntos exactos).

### 4.6. Enlaces Oficiales & Top Secret
- Links directos a la web oficial RFEVB/EsVoley para ver actas reales.
- **Top Secret**: Pestaña lúdica que muestra los puntos estimados de temporada de cada equipo del club mediante un algoritmo.

---

## 5. Reglas de Negocio Clave a Respetar en la Migración

1. **El Signo en los Puntos**: El usuario *debe* especificar el signo de la diferencia de puntos (+ si gana el VCV, - si pierde). Sin esto, la validación de aciertos en Google Apps Script fallará o dará puntos incorrectos.
2. **PWA Constraints**: Las llamadas a API deben usar una función envolvente de seguridad (ej: `fetchSeguro()`) con intentos automáticos (retry), porque a veces las conexiones de Apps Script desde móviles en 4G/5G fallan a la primera.
3. **Arrays de Google Sheets**: El backend asume que las peticiones se hacen a una URL `https://script.google.com/macros/s/.../exec`. El frontend debe gestionar siempre el estado de "Cargando..." para el usuario, ya que Apps Script tarda de 1 a 3 segundos en responder.
4. **Notch de iOS**: El diseño debe incluir espaciado seguro arriba (`env(safe-area-inset-top)`) y abajo (`env(safe-area-inset-bottom)`) para PWA en modo fullscreen.
