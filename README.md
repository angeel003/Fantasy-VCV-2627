# VCV Play 26/27

Bienvenido al repositorio oficial del **VCV Play 26/27**, una aplicación web interactiva diseñada para gestionar una liga de pronósticos (porras) de partidos de voleibol.

## 🏐 Sobre el Proyecto

Esta aplicación permite a los usuarios registrados (y visitantes en modo invitado) consultar la cartelera de partidos, realizar predicciones de resultados (sets) y competir en una clasificación general. Todo el sistema está diseñado para ser rápido, seguro y fácil de administrar sin necesidad de bases de datos complejas.

### ✨ Características Principales
* **Sistema de Usuarios y Permisos:** Autenticación básica con soporte para cambio de contraseñas y solicitudes de cambio de nombre de usuario. Diferentes permisos por usuario para predecir sobre equipos específicos.
* **Modo Invitado:** Acceso de solo lectura para ver la cartelera pública de partidos y los pronósticos globales sin necesidad de registro.
* **Cierre Automático de Predicciones:** El sistema bloquea automáticamente los pronósticos 15 minutos antes de la hora oficial de inicio de cada partido.
* **Panel de Administración Integrado:** Los administradores pueden introducir resultados oficiales en directo y sincronizar usuarios desde la misma interfaz web.
* **Clasificaciones Dinámicas:** Cálculo automático de puntos y generación de tablas de clasificación por ligas.
* **Historial Privado:** Cada usuario puede revisar el rendimiento de sus pronósticos pasados frente a los resultados reales.
* **Smart Cache System:** Un sistema avanzado de caché (TTL 6 horas) en el servidor que garantiza tiempos de carga ultrarrápidos (0.1s), invalidándose automáticamente solo cuando se detectan nuevas escrituras (nuevos pronósticos, resultados oficiales, etc.).

---

## 🏗️ Arquitectura Técnica

El proyecto sigue una arquitectura *Serverless* apoyada enteramente en el ecosistema de Google Workspace:

* **Frontend:** HTML, CSS y JavaScript vainilla. Estilizado con Bootstrap 4. Funciona como una Single Page Application (SPA) que se comunica con la API mediante `fetch`.
* **Backend (API):** Google Apps Script (`Código.js`). Recibe peticiones POST, procesa la lógica de negocio y devuelve JSON.
* **Base de Datos:** Google Sheets. Almacena las configuraciones, usuarios, ligas, partidos, porras y resultados oficiales.

---

## 📂 Estructura del Repositorio

* `index.html` - Interfaz principal del usuario (Entorno de Producción).
* `dev.html` - Interfaz para pruebas y desarrollo.
* `script-prod/` - Carpeta con el código backend (`Código.js`) de producción.
* `script-dev/` - Carpeta con el código backend para el entorno de desarrollo.
* `instrucciones_excel.md` - Guía detallada sobre cómo administrar y rellenar la base de datos (Google Sheets).
* `backups/` - Copias de seguridad automáticas del estado completo del proyecto en diferentes momentos clave.
* `changelog.txt` - Registro histórico de parches, mejoras y bugs solucionados.

---

## 🚀 Despliegue y Configuración

### 1. Configurar la Base de Datos
Crea una hoja de cálculo en Google Sheets siguiendo la estructura definida en `instrucciones_excel.md`. 

### 2. Desplegar el Backend (Apps Script)
1. Abre tu Google Sheet y ve a **Extensiones > Apps Script**.
2. Pega el contenido de `script-prod/Código.js`.
3. Haz clic en **Implementar > Nueva implementación**.
4. Selecciona el tipo **Aplicación web**.
5. Configura:
   * Ejecutar como: **Yo** (tu cuenta de Google).
   * Quién tiene acceso: **Cualquier persona**.
6. Autoriza los permisos de Google.
7. Copia la **URL de la aplicación web** generada.

### 3. Conectar el Frontend
1. Abre `index.html` (o `dev.html`).
2. Localiza la constante `scriptURL` al principio de la etiqueta `<script>`.
3. Reemplaza el valor con la URL que copiaste en el paso anterior.
4. Sube tu archivo `.html` a cualquier servidor estático (GitHub Pages, Vercel, Netlify, o tu propio hosting).

---

## 🛠️ Notas de Desarrollo (Troubleshooting)

* **Problemas de CORS / JSON (Error `<!DOCTYPE HTML>`):** Google Apps Script sufre de colisión de cookies si se lanzan múltiples peticiones seguidas en la misma sesión de navegador usando `fetch`. El proyecto usa `credentials: 'omit'` y variables `?t=` en la URL para evitarlo.
* **Lentitud o Timeout (Error 500):** Para evitar bloqueos por lectura simultánea en Google Sheets (Arranque en Frío), el backend incluye un sistema de `CacheService` agresivo. Nunca elimines la función `clearAllCache()` ni la declares de forma síncrona en cada lectura.
