# Vercel Serverless Functions - Lectura Dinámica de Datasets

## Solución para Vercel: Vercel Functions

Vercel **SÍ soporta lectura dinámica** mediante **Vercel Functions** (serverless functions en Node.js, Python, etc.).

### ¿Cómo funciona?

1. **Vercel Function** (`/api/datasets.js`) se ejecuta en el servidor
2. Lee dinámicamente el directorio `web/datasets/`
3. Devuelve la lista de JSON en formato JSON
4. El navegador consume ese endpoint con el código existente

---

## Instalación y Configuración

### 1. Estructura de carpetas

```
administracion_de_redes/
├── web/
│   ├── index.html
│   ├── datasets/
│   │   ├── archivo1.json
│   │   ├── archivo2.json
│   │   └── ...
│   ├── css/
│   ├── js/
│   └── ...
├── api/                          👈 Nueva carpeta
│   └── datasets.js              👈 Función Vercel
├── vercel.json                  👈 Configuración (opcional)
└── .gitignore
```

### 2. Archivo `api/datasets.js` (ya incluido)

La función está lista. Solo necesita estar en la carpeta `api/`.

### 3. Configuración en `vercel.json` (opcional)

```json
{
  "builds": [
    {
      "src": "web/**",
      "use": "@vercel/static"
    },
    {
      "src": "api/**",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "^/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/web/$1"
    }
  ]
}
```

---

## Cómo funciona el flujo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Usuario abre https://tu-app.vercel.app                  │
│    └─> Sirve index.html desde /web                         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. JS carga y hace click en "Actualizar lista"              │
│    └─> fetch("/api/datasets")                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Vercel Function (Node.js) se ejecuta                     │
│    ├─> Lee directorio web/datasets/                         │
│    ├─> Filtra solo .json (excepto index.json)               │
│    └─> Devuelve JSON con lista de archivos                  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. JS recibe la lista dinámicamente                          │
│    └─> Llena el select con los archivos disponibles          │
└─────────────────────────────────────────────────────────────┘
```

---

## Pruebas Locales

Vercel proporciona herramienta CLI para probar localmente:

### Instalación de CLI
```bash
npm install -g vercel
```

### Ejecutar en local
```bash
vercel dev
```

Luego accede a `http://localhost:3000` y prueba el endpoint:
```
http://localhost:3000/api/datasets
```

---

## Ventajas

✅ **Lectura completamente dinámica**  
✅ **Funciona en Vercel sin cambios**  
✅ **Gratuito** (Vercel Function free tier: 100k invocaciones/mes)  
✅ **Sin necesidad de regenerar index.json**  
✅ **Automático**: agregar un JSON = se ve inmediatamente  
✅ **Compatible con el código existente** (script.js ya lo soporta)  

---

## Paso a paso para Producción

1. **Crear carpeta `api/`** en raíz del proyecto (hecho ✅)
2. **Crear `api/datasets.js`** (hecho ✅)
3. **Commit a GitHub**
   ```bash
   git add api/datasets.js
   git commit -m "Agrega Vercel Function para lectura dinámica de datasets"
   git push
   ```
4. **Vercel se despliega automáticamente**
5. **Listo**: el endpoint `/api/datasets` funciona dinámicamente

---

## Comparativa Final

| Opción | Desarrollo | Producción Vercel | Dinámico | Esfuerzo |
|--------|-----------|------------------|----------|----------|
| **server.py** | ✅ Perfecto | ❌ No funciona | ✅ Sí | Bajo |
| **index.json** | ⚠️ Manual | ✅ Funciona | ❌ No | Medio |
| **Vercel Function** | ⚠️ Con CLI | ✅ Automático | ✅ Sí | Bajo |

**Recomendación para Vercel**: Usa **Vercel Functions** (esta opción) ✅

