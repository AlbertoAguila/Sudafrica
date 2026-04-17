# 🌍 Sudáfrica · Garden Route 2025

App Streamlit del itinerario de viaje a Sudáfrica para compartir con amigos.  
Navega por los 5 días, ve el mapa interactivo y descarga fotos reales de cada lugar.

---

## Puesta en marcha

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Descargar las fotos automáticamente

```bash
python download_images.py
```

El script descarga fotos reales de Wikipedia/Wikimedia Commons para cada lugar del
itinerario (Table Mountain, Knysna Heads, Hermanus, etc.) y las guarda en `images/`.  
Si alguna foto no se encuentra, la app muestra un placeholder de color — nunca da error.

### 3. Lanzar la app

```bash
streamlit run app.py
```

Abre el navegador en **http://localhost:8501**

---

## Compartir con tus amigos

Para que cualquiera pueda verla desde el móvil sin instalar nada:

1. **Sube el proyecto a GitHub** (puede ser repositorio privado)  
   Incluye todos los archivos, incluyendo la carpeta `images/` con las fotos descargadas.

   ```
   git init
   git add .
   git commit -m "Itinerario Sudáfrica 2025"
   git remote add origin https://github.com/tu-usuario/sudafrica-2025.git
   git push -u origin main
   ```

2. **Ve a [share.streamlit.io](https://share.streamlit.io)** e inicia sesión con GitHub

3. **Nueva app:**
   - Repository: `tu-usuario/sudafrica-2025`
   - Branch: `main`
   - Main file path: `app.py`

4. Pulsa **Deploy** → obtendrás una URL pública tipo `sudafrica2025.streamlit.app`

5. **Comparte la URL por WhatsApp** 🎉

---

## Estructura del proyecto

```
viaje-streamlit/
├── app.py                   # App principal (Streamlit)
├── download_images.py       # Descarga fotos de Wikipedia
├── requirements.txt         # Dependencias Python
├── README.md                # Este archivo
└── images/                  # Fotos descargadas automáticamente
    ├── hero.jpg
    ├── pe_donkin.jpg
    ├── pe_beach.jpg
    ├── tsitsikamma_bridge.jpg
    ├── tsitsikamma_coast.jpg
    ├── plett_beach.jpg
    ├── knysna_heads.jpg
    ├── knysna_lagoon.jpg
    ├── wilderness_beach.jpg
    ├── dehoop_zebras.jpg
    ├── dehoop_dunes.jpg
    ├── agulhas_lighthouse.jpg
    ├── agulhas_sign.jpg
    ├── hermanus_whales.jpg
    ├── hermanus_cliffs.jpg
    ├── cpt_table_mountain.jpg
    ├── cpt_bokaap.jpg
    ├── cpt_waterfront.jpg
    └── joburg_skyline.jpg
```

---

## Itinerario

| Día | Fecha | Ruta | Km | Aviso |
|-----|-------|------|----|-------|
| Día 1 | 29 ago | Port Elizabeth → Tsitsikamma → Plettenberg Bay | ~440 km | — |
| Día 2 | 30 ago | Plett → Knysna → Wilderness → De Hoop | ~310 km | ⚠️ Salir 8:30h |
| Día 3 | 31 ago | De Hoop → Cabo Agulhas → Hermanus → Ciudad del Cabo | ~382 km | ⚠️ Salir 7:30h |
| Día 4 | 1 sep | Ciudad del Cabo (mañana libre) → vuelo a Johannesburgo | ✈️ | ✈️ Vuelo 17:30h |
| Día 5 | 2 sep | Johannesburgo · Sandton / Melrose | — | Descanso |
