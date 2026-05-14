# Campus Test Studio - Lectura Dinámica de Datasets

## ¿Por qué no puede leer dinámicamente el directorio?

Los navegadores **no pueden acceder directamente al sistema de archivos** por razones de seguridad (Same-Origin Policy, CORS). Necesitas una de estas 3 opciones:

---

## 📌 Opción 1: Servidor Python Local (RECOMENDADO - Completamente dinámico)

El servidor lee el directorio datasets en **tiempo real** sin necesidad de regenerar `index.json`.

### Instalación y uso:
```bash
cd web
python server.py
```

Luego abre: **http://localhost:8000**

✅ **Ventajas:**
- ✨ Lectura dinámica del directorio en tiempo real
- 🔄 Automático: no necesitas regenerar `index.json`
- 📦 Incluye soporte CORS y endpoint `/api/datasets`
- 🚀 Cero configuración

❌ **Desventajas:**
- Solo funciona localmente
- Requiere tener Python en el sistema

---

## 📌 Opción 2: Script de Renombrado + Index.json Estático

Usa `rename_datasets.py` para analizar y renombrar archivos, luego genera `index.json` de forma estática.

### Instalación y uso:
```bash
cd web
python rename_datasets.py
```

Luego sirve con cualquier servidor HTTP (VS Code Live Server, http-server, etc.)

✅ **Ventajas:**
- 📝 Renombra archivos con nombres significativos
- 📦 Funciona con hosting estático (GitHub Pages, Vercel, etc.)
- 🔍 Analiza contenido automáticamente

❌ **Desventajas:**
- 🔄 Necesita ejecutar script manualmente tras añadir nuevos JSONs
- 📄 Genera archivo estático `index.json`

**Uso recomendado:** Producción en hosting estático

---

## 📌 Opción 3: Direct Directory Listing (NO RECOMENDADO)

Algunos servidores pueden listar directorios si lo habilitas, pero **NO es seguro en producción**.

Solo para desarrollo local con servidores específicos.

---

## � Opción 4: Vercel Functions (MEJOR PARA PRODUCCIÓN EN VERCEL)

Si tu app está en **Vercel**, usa **Vercel Functions** para lectura 100% dinámica sin regenerar `index.json`.

Ver: [VERCEL_FUNCTIONS.md](../VERCEL_FUNCTIONS.md)

✅ **Ventajas:**
- ✨ Lectura dinámica en tiempo real en producción
- 🚀 Se ejecuta en el servidor de Vercel
- 💰 Gratuito (100k invocaciones/mes)
- 🔄 Automático: agrega un JSON y aparece al instante

---

## 🚀 Recomendación

| Caso de Uso | Opción |
|-----------|---------|
| Desarrollo local con cambios frecuentes | **Opción 1** (servidor.py) |
| Producción Vercel con lectura dinámica | **Opción 4** (Vercel Functions) |
| Producción estática sin serverless | **Opción 2** (rename_datasets.py) |
| Solo pruebas rápidas | Opción 3 |

---

## Archivo de Inicio Rápido

Para **desarrollo local con lectura dinámica**:
```bash
# Terminal
cd C:\Users\david\python\administracion_de_redes\web
python server.py
```

Luego abre: **http://localhost:8000** en tu navegador

El servidor automáticamente:
- Lee el directorio `datasets/` cada vez que haces clic en "Actualizar lista"
- Sirve los JSONs correctamente
- Maneja CORS para todas las requests

**No necesitas regenerar index.json nunca más.**
