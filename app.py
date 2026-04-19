# -*- coding: utf-8 -*-
"""
Sudáfrica · Garden Route 2026
Luxury safari aesthetic. Playfair Display + Lato. Earth tones. Zero emojis.
RULE: every st.markdown() HTML block is self-contained — no split divs, ever.
"""
import io
import base64
from pathlib import Path

import streamlit as st
import folium
from streamlit_folium import st_folium
from PIL import Image, ImageDraw

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Sudáfrica · Garden Route 2026",
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&display=swap');

#MainMenu, footer, header { visibility: hidden; }

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #FAFAF7 !important;
    font-family: 'Lato', sans-serif;
    color: #1A1A1A;
}
.block-container {
    padding-top: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}
h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif !important;
    color: #1A1A1A !important;
    font-weight: 600 !important;
}
p, li, span { font-family: 'Lato', sans-serif; }
hr { border: none !important; border-top: 1px solid #DDD8D0 !important; margin: 24px 0 !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background-color: #2C4A3E !important; }
[data-testid="stSidebar"] > div:first-child { padding-top: 2rem; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stCaption p { color: #F2EDE4 !important; font-family: 'Lato', sans-serif !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 { color: #F2EDE4 !important; font-family: 'Playfair Display', serif !important; }
[data-testid="stSidebar"] hr { border-top-color: #3D6357 !important; }
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: #F2EDE4 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 22px !important;
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: #95B8A8 !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background-color: rgba(255,255,255,0.05) !important;
    border-color: #3D6357 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #F2EDE4 !important;
    border-bottom: 1px solid #DDD8D0 !important;
    gap: 0 !important;
    padding: 0 48px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Lato', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #6B6560 !important;
    background-color: transparent !important;
    border-bottom: 2px solid transparent !important;
    padding: 14px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: #2C4A3E !important;
    border-bottom: 2px solid #8B6914 !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-panel"] { background-color: #FAFAF7 !important; }

/* ── Buttons ── */
.stButton > button {
    background-color: #2C4A3E !important;
    color: #FAFAF7 !important;
    border: none !important;
    border-radius: 1px !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 10px 24px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background-color: #8B6914 !important; }

/* ── Metrics ── */
[data-testid="stMetricValue"] { font-family: 'Playfair Display', serif !important; color: #1A1A1A !important; font-size: 26px !important; }
[data-testid="stMetricLabel"] { font-family: 'Lato', sans-serif !important; font-size: 10px !important; letter-spacing: 2px !important; text-transform: uppercase !important; color: #6B6560 !important; }

/* ── Bordered container ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #F2EDE4 !important;
    border: 1px solid #DDD8D0 !important;
    border-radius: 0 !important;
}

/* ── Captions ── */
.stCaption p { font-family: 'Lato', sans-serif !important; color: #6B6560 !important; font-size: 12px !important; letter-spacing: 0.5px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #F2EDE4; }
::-webkit-scrollbar-thumb { background: #2C4A3E; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ─── PALETA ──────────────────────────────────────────────────────────────────
DAY_COLORS = {
    0: "#6B6560",
    1: "#2C4A3E",
    2: "#4A7A68",
    3: "#8B6914",
    4: "#2A4A6B",
    5: "#6B4A2A",
    6: "#5C3D1E",
    7: "#7A4F2A",
    8: "#8B5E3C",
}
_PH_RGB = {
    0: (107, 101, 96),
    1: ( 44,  74, 62),
    2: ( 74, 122,104),
    3: (139, 105, 20),
    4: ( 42,  74,107),
    5: (107,  74, 42),
    6: ( 92,  61, 30),
    7: (122,  79, 42),
    8: (139,  94, 60),
}

# ─── PIL IMAGES ──────────────────────────────────────────────────────────────
IMAGES_DIR = Path("images")
IMAGES_DIR.mkdir(exist_ok=True)

def _make_placeholder(stem: str, day: int) -> Image.Image:
    w, h = 800, 500
    img = Image.new("RGB", (w, h), _PH_RGB.get(day, (44, 74, 62)))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 4],     fill=(139, 105, 20))
    draw.rectangle([0, h - 4, w, h], fill=(139, 105, 20))
    label = stem.replace("_", " ").upper()
    try:
        draw.text((w // 2, h // 2), label, fill=(242, 237, 228), anchor="mm")
    except TypeError:
        draw.text((20, h // 2 - 8), label, fill=(242, 237, 228))
    return img

def get_img(stem: str, day: int = 0):
    for ext in (".jpg", ".jpeg", ".png"):
        p = IMAGES_DIR / f"{stem}{ext}"
        if p.exists():
            return str(p)
    return _make_placeholder(stem, day)

@st.cache_data
def hero_b64() -> str:
    for ext in (".jpg", ".jpeg", ".png"):
        p = IMAGES_DIR / f"hero{ext}"
        if p.exists():
            try:
                img = Image.open(p).convert("RGB").resize((1400, 520))
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=85)
                return base64.b64encode(buf.getvalue()).decode()
            except Exception:
                pass
    return ""

# ─── DATOS DEL ITINERARIO ────────────────────────────────────────────────────
DAYS = {
    6: {
        "title": "Llegada a Sudafrica",
        "label": "25",
        "date": "25 Ago", "km": "~120 km", "hours": "~2h traslado",
        "route": "Vuelo — Port Elizabeth — Woodlands Safari Estate",
        "alert": None,
        "day_intro": (
            "Vuelo MAD → JNB: sale el 24 ago a las 23:45h — llega el 25 ago a las 09:50h a Johannesburgo. "
            "Conexion JNB → PLZ: Airlink 4Z 789, sale 13:20h, llega 15:05h a Port Elizabeth. "
            "Tiempo de conexion en Johannesburgo: ~3h 30min — estar atentos a la puerta de embarque."
        ),
        "stops": [
            {
                "name": "Aeropuerto de Port Elizabeth (Gqeberha)",
                "subtitle": "Llegada y recogida por John X Safaris",
                "time": "Llegada",
                "img": "pe_airport",
                "gallery": ["pe_airport"],
                "activities": [
                    "Vuelo de llegada al aeropuerto de Port Elizabeth",
                    "Recogida por John X Safaris en el aeropuerto",
                    "Tramites de llegada e inicio del traslado al campamento",
                ],
                "badges": [],
                "notes": [],
            },
            {
                "name": "Woodlands Safari Estate — John X Safaris",
                "subtitle": "Colonial Manor construida en 1898 — Base de caza y safari",
                "time": "Tarde — noche",
                "img": "woodlands_lodge",
                "gallery": ["woodlands_lodge"],
                "activities": [
                    "Instalacion en la Colonial Manor — habitaciones con bano en suite",
                    "Primer recorrido del campamento y sus instalaciones",
                    "The Naked Pub — pub historico construido en 1897",
                    "Cena de bienvenida con cocina local, caza y vinos sudafricanos",
                    "Hoguera nocturna compartiendo historias bajo el cielo africano",
                ],
                "badges": [],
                "notes": [
                    "Para coordinar el traslado o solicitar la ubicacion GPS exacta del campamento, contacta con John X Safaris: johnxsafarishunts@gmail.com  ·  +27 82 700 9866",
                ],
            },
        ],
        "drives": [
            ("Aeropuerto Port Elizabeth", "Woodlands Safari Estate", "~120 km", "~2h"),
        ],
    },
    7: {
        "title": "Caza en el Eastern Cape",
        "label": "26-27",
        "date": "26-27 Ago", "km": "—", "hours": "Dias completos en campamento",
        "route": "Woodlands Safari Estate — Southern Concessions — Great Fish River Valley",
        "alert": None,
        "stops": [
            {
                "name": "Southern Concessions — Eastern Cape",
                "subtitle": "Great Fish River Valley — Caza con guias profesionales",
                "time": "Dias completos",
                "img": "woodlands_hunt",
                "gallery": ["woodlands_hunt", "woodlands_sunset"],
                "activities": [
                    "Salidas al amanecer con guias profesionales (Professional Hunters) de John X Safaris",
                    "Caza en las Southern Concessions del Eastern Cape — zona Great Fish River Valley",
                    "Mas de 3 millones de acres de terreno privado con mas de 40 especies de caza",
                    "Regreso al campamento al mediodia para almuerzo y descanso",
                    "Salida vespertina hasta el atardecer",
                    "Cenas opulentas en el comedor colonial — cocina local, caza, vinos sudafricanos",
                    "Hoguera nocturna con los Professional Hunters",
                ],
                "badges": [],
                "notes": [
                    "Woodlands Safari Estate es uno de los mejores destinos de Bufalo del Cabo en Sudafrica",
                ],
            },
        ],
        "drives": [],
    },
    8: {
        "title": "Safari de Observacion",
        "label": "28",
        "date": "28 Ago", "km": "~300 km", "hours": "Dia completo",
        "route": "Woodlands — Addo Elephant National Park — Shamwari Game Reserve — Woodlands",
        "alert": None,
        "stops": [
            {
                "name": "Addo Elephant National Park",
                "subtitle": "Tercer parque nacional mas grande de Sudafrica",
                "time": "Manana",
                "img": "addo_elephants",
                "gallery": ["addo_elephants", "addo_park"],
                "activities": [
                    "Tercer parque nacional mas grande de Sudafrica",
                    "Mas de 600 elefantes africanos en libertad",
                    "Uno de los pocos lugares donde ver los Big 7 — Big 5, tiburon blanco y ballena",
                    "Game drives guiados por el parque",
                    "A ~72 km al norte de Port Elizabeth — 1 a 1.5h desde Woodlands",
                ],
                "badges": ["wild"],
                "notes": [],
            },
            {
                "name": "Shamwari Game Reserve",
                "subtitle": "Reserva privada de lujo — Big 5 y conservacion de felinos",
                "time": "Tarde",
                "img": "shamwari_lion",
                "gallery": ["shamwari_lion", "shamwari_reserve"],
                "activities": [
                    "Reserva privada de lujo — una de las mas prestigiosas de Sudafrica",
                    "Famosa por la reintroduccion de los Big 5 y programa de conservacion de felinos",
                    "Game drives con rangers expertos",
                    "Centro de conservacion y rehabilitacion de animales",
                    "A ~75 km al este de Port Elizabeth — 1 a 1.5h desde Woodlands",
                ],
                "badges": ["book"],
                "notes": [],
            },
            {
                "name": "Ultima noche en Woodlands Safari Estate",
                "subtitle": "Regreso al campamento — cena de despedida",
                "time": "Noche",
                "img": "woodlands_lodge",
                "gallery": [],
                "activities": [
                    "Regreso al campamento por la tarde",
                    "Ultima cena en el comedor colonial antes de iniciar la Garden Route",
                ],
                "badges": [],
                "notes": [],
            },
        ],
        "drives": [
            ("Woodlands", "Addo Elephant NP", "~72 km", "~1.5h"),
            ("Addo", "Shamwari Game Reserve", "~80 km", "~1h"),
            ("Shamwari", "Woodlands Safari Estate", "~75 km", "~1.5h"),
        ],
    },
    1: {
        "title": "Garden Route comienza",
        "date": "29 Ago", "km": "~440 km", "hours": "~5h de conduccion",
        "route": "Woodlands Safari Estate — Port Elizabeth — Tsitsikamma — Plettenberg Bay",
        "alert": None,
        "eyebrow": "Dia 29 &middot; 29 AGO &mdash; Ultima ma&ntilde;ana en Woodlands Safari Estate",
        "day_intro": "Ultima manana en Woodlands Safari Estate. Desayuno en el campamento, recogida del equipaje y despedida del equipo de John X Safaris. El traslado hasta Port Elizabeth dura aproximadamente 2 horas — la primera parada de la Garden Route.",
        "pre_drive": ("Woodlands Safari Estate", "Port Elizabeth", "~120 km", "~2h"),
        "stops": [
            {
                "name": "Port Elizabeth (Gqeberha)",
                "subtitle": "Costa del oceano Indico",
                "time": "45 min",
                "img": "pe_donkin",
                "gallery": ["pe_donkin", "pe_beach"],
                "activities": [
                    "Donkin Reserve — mirador historico con Faro de 1861",
                    "Route 67 — 67 obras de arte callejero en homenaje a Mandela",
                    "Hobie Beach y King's Beach junto al oceano Indico",
                ],
                "badges": [],
            },
            {
                "name": "Parque Nacional Tsitsikamma",
                "subtitle": "Bosques, canones y oceano",
                "time": "2 — 3 horas",
                "img": "tsitsikamma_bridge",
                "gallery": ["tsitsikamma_bridge", "tsitsikamma_coast"],
                "activities": [
                    "Puente colgante sobre el rio Storms River — 2 km ida y vuelta",
                    "Ruta en kayak por los desfiladeros del rio Storms",
                    "Avistamiento de ballenas jorobadas desde la costa",
                    "Wild Card incluida — acceso libre al parque nacional",
                ],
                "badges": ["wild", "book"],
            },
            {
                "name": "Plettenberg Bay",
                "subtitle": "Base nocturna — Garden Route",
                "time": "Noche",
                "img": "plett_beach",
                "gallery": ["plett_beach"],
                "activities": [
                    "Primera gran base de la Garden Route",
                    "Atardecer sobre el oceano Indico",
                ],
                "badges": [],
            },
        ],
        "drives": [
            ("Port Elizabeth", "Tsitsikamma", "100 km", "1.5h"),
            ("Tsitsikamma", "Plettenberg Bay", "80 km", "1h"),
        ],
    },
    2: {
        "title": "La laguna y las dunas",
        "date": "30 Ago", "km": "310 km", "hours": "5h",
        "route": "Plettenberg Bay — Knysna — Wilderness — Reserva De Hoop",
        "alert": "Salir antes de las 8:30h — la pista de tierra a De Hoop anade tiempo extra",
        "stops": [
            {
                "name": "Knysna — The Heads",
                "subtitle": "Laguna y promontorios",
                "time": "30 — 45 min",
                "img": "knysna_heads",
                "gallery": ["knysna_heads", "knysna_lagoon"],
                "activities": [
                    "Mirador East Head — panoramica del canal y el oceano",
                    "Los dos promontorios que flanquean la laguna de Knysna",
                ],
                "badges": [],
            },
            {
                "name": "Wilderness — Dolphin Point",
                "subtitle": "Mirador costero",
                "time": "20 min",
                "img": "wilderness_beach",
                "gallery": ["wilderness_beach"],
                "activities": [
                    "Mirador junto a la N2, sin desvio",
                    "Vistas de 17 km de playa dorada y puente de Kaaimans",
                    "Con suerte: delfines y ballenas en el oceano",
                ],
                "badges": [],
            },
            {
                "name": "Reserva Natural De Hoop",
                "subtitle": "Vida salvaje — dormir aqui",
                "time": "Tarde — noche",
                "img": "dehoop_zebras",
                "gallery": ["dehoop_zebras", "dehoop_dunes"],
                "activities": [
                    "Cebras, avestruces, bonteboks y elands desde la entrada",
                    "Ruta a las dunas blancas hasta el Indico — 5 km, antes de las 16h",
                    "Fynbos y cielo estrellado espectacular",
                    "Pista de tierra de 50 km en buen estado — no hace falta 4x4",
                ],
                "badges": ["wild", "warn"],
            },
        ],
        "drives": [
            ("Plettenberg Bay", "Knysna", "35 km", "30 min"),
            ("Knysna", "Wilderness", "60 km", "45 min"),
            ("Wilderness", "De Hoop Reserve", "200 km + 50 km pista", "3h"),
        ],
    },
    3: {
        "title": "El fin del continente",
        "date": "31 Ago", "km": "382 km", "hours": "5h",
        "route": "De Hoop — Cabo Agulhas — Hermanus — Ciudad del Cabo",
        "alert": "Salir antes de las 7:30h para llegar a Ciudad del Cabo con luz de tarde",
        "stops": [
            {
                "name": "Cabo de las Agujas (Cape Agulhas)",
                "subtitle": "El punto mas austral de Africa",
                "time": "1 hora",
                "img": "agulhas_lighthouse",
                "gallery": ["agulhas_lighthouse", "agulhas_sign"],
                "activities": [
                    "El punto mas al sur del continente africano",
                    "Donde se dividen el oceano Indico y el Atlantico",
                    "Faro de 1848 — segundo mas antiguo de Sudafrica",
                    "Entrada incluida con Wild Card",
                ],
                "badges": ["wild"],
            },
            {
                "name": "Hermanus",
                "subtitle": "Capital mundial del avistamiento de ballenas",
                "time": "2 horas",
                "img": "hermanus_whales",
                "gallery": ["hermanus_whales", "hermanus_cliffs"],
                "activities": [
                    "Cliff Path Walk — sendero por acantilados de 2 a 3 km",
                    "Temporada alta de ballenas francas australes en agosto",
                    "Old Harbour y Whale House Museum",
                    "Tour en barco opcional — 1.5h — reservar con antelacion",
                ],
                "badges": ["book"],
            },
            {
                "name": "Ciudad del Cabo",
                "subtitle": "Llegada — dormir aqui",
                "time": "Llegada aproximada 17h",
                "img": "cpt_waterfront",
                "gallery": ["cpt_waterfront", "cpt_table_mountain"],
                "activities": [
                    "Ruta costera R44 — espectacular, posibles ballenas",
                    "V&A Waterfront para el atardecer con vistas a Table Mountain",
                    "Paseo por Bree Street — corazon gastronomico de la ciudad",
                ],
                "badges": [],
            },
        ],
        "drives": [
            ("De Hoop Reserve", "Cabo Agulhas", "85 km", "1.5h"),
            ("Cabo Agulhas", "Hermanus", "90 km", "1.5h"),
            ("Hermanus", "Ciudad del Cabo — ruta R44", "120 km", "2h"),
        ],
    },
    4: {
        "title": "Ciudad del Cabo — Vuelo",
        "date": "1 Sep", "km": "Vuelo 1.400 km", "hours": "2h 5m vuelo",
        "route": "Ciudad del Cabo — Aeropuerto CPT — Johannesburgo",
        "alert": "Salir del hotel a las 15:00h — Fly Safair FA102 · CPT 17:25h → JNB 19:30h",
        "flight_details": {
            "from_code": "CPT", "from_name": "Ciudad del Cabo",
            "dep": "17:25h", "label": "Fly Safair FA102 · 2h 5m",
            "to_code": "JNB", "to_name": "Johannesburgo",
        },
        "stops": [
            {
                "name": "Bo-Kaap",
                "subtitle": "Barrio historico de Ciudad del Cabo",
                "time": "8:00 — 9:30h",
                "img": "cpt_bokaap",
                "gallery": ["cpt_bokaap"],
                "activities": [
                    "Casas pintadas en colores brillantes, callejuelas empedradas",
                    "Primera mezquita de Sudafrica — Auwal Mosque, 1794",
                    "Wale Street y Chiappini Street para las mejores fotografias",
                ],
                "badges": [],
            },
            {
                "name": "Table Mountain",
                "subtitle": "Monumento natural de Ciudad del Cabo",
                "time": "9:30 — 12:00h",
                "img": "cpt_table_mountain",
                "gallery": ["cpt_table_mountain"],
                "activities": [
                    "Teleferico de 5 min — vistas de 360 grados desde la cima",
                    "Reservar ticket online la noche anterior — hay largas colas",
                    "Si esta nublado: V&A Waterfront o museo Zeitz MOCAA",
                ],
                "badges": ["book"],
            },
            {
                "name": "Ultimo almuerzo en Ciudad del Cabo",
                "subtitle": "Antes del vuelo",
                "time": "12:30 — 14:00h",
                "img": "cpt_waterfront",
                "gallery": [],
                "activities": [
                    "The Pot Luck Club en Old Biscuit Mill — tapas creativas",
                    "Pier en el V&A Waterfront — mariscos con vistas",
                ],
                "badges": [],
            },
        ],
        "drives": [],
        "flight": True,
    },
    5: {
        "title": "Johannesburgo — Ultima noche",
        "date": "2 Sep", "km": "—", "hours": "Descanso",
        "route": "Johannesburgo — Sandton y Melrose",
        "alert": None,
        "stops": [
            {
                "name": "Johannesburgo — Sandton",
                "subtitle": "Ultima noche del viaje",
                "time": "Todo el dia",
                "img": "joburg_skyline",
                "gallery": ["joburg_skyline"],
                "activities": [
                    "Descanso tras la Garden Route",
                    "Explorar restaurantes y cultura local de Sandton",
                    "Sandton City y Nelson Mandela Square",
                ],
                "badges": [],
            },
        ],
        "drives": [],
        "safety": True,
    },
}

ROUTE_POINTS = [
    {"name": "Woodlands Safari Estate", "day": 6, "lat": -33.45, "lon": 26.20,
     "desc": "Dias 25-28 — John X Safaris — Base de caza y safari"},
    {"name": "Addo Elephant National Park", "day": 8, "lat": -33.4833, "lon": 25.7500,
     "desc": "Big 7 — mas de 600 elefantes"},
    {"name": "Shamwari Game Reserve", "day": 8, "lat": -33.3833, "lon": 26.0167,
     "desc": "Big 5 — reserva privada de lujo"},
    {"name": "Aeropuerto Port Elizabeth", "day": 6, "lat": -33.9845, "lon": 25.6172,
     "desc": "Dia 25 — Llegada y recogida por John X Safaris"},
    {"name": "Port Elizabeth", "day": 1, "lat": -33.9608, "lon": 25.6022,
     "desc": "Route 67 · Donkin Reserve · Costa del Indico"},
    {"name": "Tsitsikamma",    "day": 1, "lat": -33.9833, "lon": 23.9167,
     "desc": "Puente colgante · Kayak · Storms River"},
    {"name": "Plettenberg Bay","day": 1, "lat": -34.0522, "lon": 23.3716,
     "desc": "Base nocturna"},
    {"name": "Knysna",         "day": 2, "lat": -34.0363, "lon": 23.0474,
     "desc": "The Heads · Laguna"},
    {"name": "Wilderness",     "day": 2, "lat": -33.9913, "lon": 22.5849,
     "desc": "Dolphin Point · 17 km de playa"},
    {"name": "De Hoop Reserve","day": 2, "lat": -34.4547, "lon": 20.4329,
     "desc": "Cebras · Dunas blancas"},
    {"name": "Cabo Agulhas",   "day": 3, "lat": -34.8279, "lon": 20.0077,
     "desc": "Punta mas austral de Africa"},
    {"name": "Hermanus",       "day": 3, "lat": -34.4190, "lon": 19.2352,
     "desc": "Ballenas francas · Cliff Path"},
    {"name": "Ciudad del Cabo","day": 3, "lat": -33.9249, "lon": 18.4241,
     "desc": "Table Mountain · V&A Waterfront"},
    {"name": "Johannesburgo",  "day": 5, "lat": -26.2041, "lon": 28.0473,
     "desc": "Final del viaje"},
]

# Ruta de conducción en orden cronológico exacto (no deriva de ROUTE_POINTS)
ROAD_ROUTE = [
    (-33.45,   26.20),    # Woodlands — base dias 25-28
    (-33.4833, 25.7500),  # Addo — excursion dia 28
    (-33.3833, 26.0167),  # Shamwari — excursion dia 28
    (-33.45,   26.20),    # Woodlands — regreso noche dia 28
    (-33.9608, 25.6022),  # Port Elizabeth — dia 29
    (-33.9833, 23.9167),  # Tsitsikamma — dia 29
    (-34.0522, 23.3716),  # Plettenberg Bay — dia 29
    (-34.0363, 23.0474),  # Knysna — dia 30
    (-33.9913, 22.5849),  # Wilderness — dia 30
    (-34.4547, 20.4329),  # De Hoop — dia 30
    (-34.8279, 20.0077),  # Cabo Agulhas — dia 31
    (-34.4190, 19.2352),  # Hermanus — dia 31
    (-33.9249, 18.4241),  # Ciudad del Cabo — dia 31 y 1 Sep
]

# ─── MAPA FOLIUM ─────────────────────────────────────────────────────────────
def build_map(selected_day: int = 0, height: int = 460, key: str = "map"):
    try:
        day_dates = {6: "25 Ago", 7: "26-27 Ago", 8: "28 Ago",
                     1: "29 Ago", 2: "30 Ago", 3: "31 Ago", 4: "1 Sep", 5: "2 Sep"}
        if selected_day > 0:
            pts = [p for p in ROUTE_POINTS if p["day"] == selected_day]
            clat = sum(p["lat"] for p in pts) / len(pts) if pts else -33.5
            clon = sum(p["lon"] for p in pts) / len(pts) if pts else 22.0
            zoom = 9 if len(pts) <= 2 else 8
        else:
            clat, clon, zoom = -33.5, 22.0, 6

        m = folium.Map(location=[clat, clon], zoom_start=zoom,
                       tiles="CartoDB positron", control_scale=False)

        folium.PolyLine(ROAD_ROUTE, color="#2C4A3E", weight=2.5,
                        opacity=0.7, dash_array="6 4").add_to(m)
        folium.PolyLine([(-33.9249, 18.4241), (-26.2041, 28.0473)],
                        color="#185FA5", weight=2,
                        opacity=0.6, dash_array="3 9").add_to(m)

        day_label_map = {6:"25", 7:"26-27", 8:"28", 1:"29", 2:"30", 3:"31", 4:"1 Sep", 5:"2 Sep"}
        for pt in ROUTE_POINTS:
            color  = DAY_COLORS.get(pt["day"], "#2C4A3E")
            active = (selected_day == 0 or pt["day"] == selected_day)
            popup_html = (
                f'<div style="font-family:Lato,sans-serif;min-width:180px;padding:8px 4px;">'
                f'<p style="font-size:10px;letter-spacing:2px;color:#8B6914;'
                f'text-transform:uppercase;margin:0 0 4px 0;">'
                f'Dia {day_label_map.get(pt["day"], str(pt["day"]))} &mdash; {day_dates.get(pt["day"], "")}</p>'
                f'<p style="font-weight:600;font-size:13px;color:#1A1A1A;margin:0 0 4px 0;">'
                f'{pt["name"]}</p>'
                f'<p style="font-size:12px;color:#6B6560;margin:0;">{pt["desc"]}</p>'
                f'</div>'
            )
            folium.CircleMarker(
                location=(pt["lat"], pt["lon"]),
                radius=8 if active else 5,
                color=color, fill=True, fill_color=color,
                fill_opacity=0.9 if active else 0.3, weight=2,
                popup=folium.Popup(popup_html, max_width=220),
                tooltip=pt["name"],
            ).add_to(m)

        st_folium(m, height=height, use_container_width=True, key=key)
    except Exception as e:
        st.warning(f"El mapa no se pudo cargar: {e}")

# ─── HTML COMPONENTS ─────────────────────────────────────────────────────────
# Each function emits ONE fully self-contained st.markdown block.
# No div is ever opened in one call and closed in another.

def render_hero():
    st.markdown("""
<div style="background:#2C4A3E; padding:36px 48px; text-align:center;">
  <p style="font-family:'Lato',sans-serif; font-size:11px; letter-spacing:4px; color:#FFB81C; text-transform:uppercase; margin:0 0 10px 0;">Garden Route &middot; Sud&aacute;frica &middot; Agosto 2026</p>
  <h1 style="font-family:'Playfair Display',serif; font-size:42px; font-weight:700; color:#FAFAF7; margin:0 0 12px 0; line-height:1.1;">Sud&aacute;frica &middot; Garden Route</h1>
  <div style="width:50px; height:2px; background:#FFB81C; margin:0 auto 14px;"></div>
  <p style="font-family:'Lato',sans-serif; font-size:14px; color:#C8BFB0; letter-spacing:1px; margin:0;">25 AGO &mdash; 2 SEP &nbsp;&middot;&nbsp; 1.684 km &nbsp;&middot;&nbsp; 8 d&iacute;as &nbsp;&middot;&nbsp; 13 paradas</p>
</div>
<div style="display:flex; height:5px; width:100%;">
  <div style="flex:1; background:#000000;"></div>
  <div style="flex:1; background:#007A4D;"></div>
  <div style="flex:1; background:#FFB81C;"></div>
  <div style="flex:1; background:#DE3831;"></div>
  <div style="flex:1; background:#002395;"></div>
  <div style="flex:1; background:#FFFFFF;"></div>
</div>
""", unsafe_allow_html=True)


def render_stats_bar():
    """Stats bar — single self-contained HTML block."""
    stats = [
        ("1.684 km", "Recorrido"),
        ("8",        "D&iacute;as"),
        ("13",       "Paradas"),
        ("2",        "Oc&eacute;anos"),
        ("5",        "Parques"),
        ("1",        "Pa&iacute;s"),
    ]
    items_html = "".join(
        f'<div style="text-align:center;flex:1;padding:0 6px;">'
        f'<div style="font-family:\'Playfair Display\',serif;font-size:22px;'
        f'font-weight:600;color:#1A1A1A;line-height:1;">{val}</div>'
        f'<div style="font-family:\'Lato\',sans-serif;font-size:10px;letter-spacing:2px;'
        f'text-transform:uppercase;color:#6B6560;margin-top:4px;">{label}</div>'
        f'</div>'
        for val, label in stats
    )
    st.markdown(f"""
<div style="background:#F2EDE4;border-top:1px solid #DDD8D0;
            border-bottom:1px solid #DDD8D0;padding:14px 48px;">
  <div style="display:flex;justify-content:space-around;align-items:center;
              max-width:900px;margin:0 auto;">
    {items_html}
  </div>
</div>
""", unsafe_allow_html=True)


def render_section_title(eyebrow: str, title: str, top: int = 48):
    st.markdown(f"""
<div style="padding:{top}px 48px 24px;background:#FAFAF7;">
  <p style="font-family:'Lato',sans-serif;font-size:11px;letter-spacing:3px;
            color:#8B6914;text-transform:uppercase;margin:0 0 8px 0;">
    {eyebrow}
  </p>
  <h2 style="font-family:'Playfair Display',serif;font-size:36px;
             color:#1A1A1A;margin:0 0 10px 0;font-weight:600;">
    {title}
  </h2>
  <div style="width:48px;height:2px;background:#8B6914;margin:0;"></div>
</div>
""", unsafe_allow_html=True)


def render_day_header(num: int, data: dict, color: str):
    alert_html = ""
    if data.get("alert"):
        alert_html = (
            f'<div style="background:#8B2E2E;color:#F2EDE4;'
            f'padding:10px 48px;font-family:Lato,sans-serif;'
            f'font-size:13px;letter-spacing:0.5px;margin-top:0;">'
            f'{data["alert"]}'
            f'</div>'
        )
    day_display = data.get("label", str(num))
    eyebrow = data.get("eyebrow") or f"Dia {day_display} &middot; {data['date']}"
    st.markdown(f"""
<div style="background:{color};padding:40px 48px 32px;">
  <p style="font-family:'Lato',sans-serif;font-size:11px;letter-spacing:3px;
            color:#8B6914;text-transform:uppercase;margin:0 0 8px 0;">
    {eyebrow}
  </p>
  <h2 style="font-family:'Playfair Display',serif;font-size:32px;
             color:#FAFAF7;margin:0 0 12px 0;font-weight:600;">
    {data['title']}
  </h2>
  <p style="font-family:'Lato',sans-serif;font-size:14px;
            color:rgba(242,237,228,0.75);margin:0 0 10px 0;">
    {data['route']}
  </p>
  <p style="font-family:'Lato',sans-serif;font-size:13px;
            color:rgba(242,237,228,0.50);margin:0;letter-spacing:1px;">
    {data['km']} &nbsp;&middot;&nbsp; {data['hours']} de conduccion
  </p>
</div>
{alert_html}
""", unsafe_allow_html=True)


def render_drive(drv: tuple):
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:16px;
            padding:14px 48px;background:#F2EDE4;
            border-top:1px solid #DDD8D0;border-bottom:1px solid #DDD8D0;
            margin:24px 0;">
  <div style="width:32px;height:1px;background:#8B6914;flex-shrink:0;"></div>
  <p style="font-family:'Lato',sans-serif;font-size:11px;color:#6B6560;
            letter-spacing:2px;text-transform:uppercase;margin:0;">
    {drv[0]} &mdash; {drv[1]} &nbsp;&middot;&nbsp; {drv[2]} &nbsp;&middot;&nbsp; {drv[3]}
  </p>
  <div style="flex:1;height:1px;background:#DDD8D0;"></div>
</div>
""", unsafe_allow_html=True)

# ─── BADGES ──────────────────────────────────────────────────────────────────
_BADGES = {
    "wild": ("info",    "Wild Card — Entrada incluida con el pase SANParks"),
    "book": ("warning", "Reservar con antelacion recomendado"),
    "warn": ("warning", "Aviso — Consultar notas del dia"),
    "tip":  ("info",    "Consejo practico"),
}

def render_badges(badges: list):
    for key in badges:
        if key in _BADGES:
            kind, text = _BADGES[key]
            if kind == "info":
                st.info(text)
            else:
                st.warning(text)

# ─── STOP — native Streamlit, no HTML wrappers ───────────────────────────────
def render_stop(stop: dict, day_n: int):
    st.divider()
    col_img, col_txt = st.columns([2, 3], gap="large")
    with col_img:
        st.image(get_img(stop["img"], day_n), use_container_width=True)
    with col_txt:
        st.markdown(f"### {stop['name']}")
        st.caption(f"{stop['subtitle']}  ·  {stop['time']}")
        st.divider()
        for act in stop["activities"]:
            st.markdown(f"- {act}")
        render_badges(stop.get("badges", []))
        for note in stop.get("notes", []):
            st.info(note)

# ─── GALLERY — native Streamlit ──────────────────────────────────────────────
def render_gallery(day_n: int, data: dict):
    stems: list = []
    for s in data["stops"]:
        for stem in s.get("gallery", []):
            if stem not in stems:
                stems.append(stem)
    stems = stems[:6]
    if not stems:
        return
    st.divider()
    st.caption("G A L E R I A")
    for i in range(0, len(stems), 3):
        row = stems[i:i + 3]
        cols = st.columns(len(row), gap="small")
        for col, stem in zip(cols, row):
            with col:
                st.image(
                    get_img(stem, day_n),
                    use_container_width=True,
                    caption=stem.replace("_", " ").title(),
                )

# ─── DAY PANEL ───────────────────────────────────────────────────────────────
def render_day(day_n: int):
    data   = DAYS[day_n]
    color  = DAY_COLORS[day_n]

    render_day_header(day_n, data, color)

    # Vuelo (dia 4) — native metrics
    if data.get("flight"):
        st.write("")
        fd = data.get("flight_details", {})
        c1, c2, c3 = st.columns(3)
        c1.metric("Origen", fd.get("from_code", "CPT"), fd.get("from_name", "Ciudad del Cabo"))
        c2.metric("Salida", fd.get("dep", "17:25h"), fd.get("label", "aprox. 2h de vuelo"))
        c3.metric("Destino", fd.get("to_code", "JNB"), fd.get("to_name", "Johannesburgo"))

    # Intro del dia (bloque informativo antes de la primera parada)
    if data.get("day_intro"):
        st.info(data["day_intro"])

    # Drive previo a la primera parada
    if data.get("pre_drive"):
        render_drive(data["pre_drive"])

    # Paradas con conectores de ruta
    drives = data.get("drives", [])
    for idx, stop in enumerate(data["stops"]):
        if idx > 0 and idx - 1 < len(drives):
            render_drive(drives[idx - 1])
        render_stop(stop, day_n)

    # Conectores sobrantes
    n = len(data["stops"])
    for drv in drives[n - 1:]:
        render_drive(drv)

    # Aviso de seguridad (dia 5)
    if data.get("safety"):
        st.divider()
        st.warning(
            "**Seguridad en Johannesburgo** — "
            "Moverse siempre en Uber o taxi del hotel. "
            "Nunca a pie de noche fuera de Sandton o Melrose. "
            "No mostrar camara ni objetos de valor en la calle."
        )

    render_gallery(day_n, data)
    st.write("")

# ─── VUELOS ──────────────────────────────────────────────────────────────────
FLIGHTS = [
    {
        "label": "Vuelo 1", "desc": "Salida de Espana",
        "from_": "Madrid (MAD)", "to": "Johannesburgo (JNB)",
        "date": "24 agosto 2026",
        "dep": "23:45h", "arr": "09:50h del 25 ago (+1 dia)",
        "airline": None, "flight_num": None, "duration": None,
        "baggage": "1 cabina 8 kg (20x44x55 cm) + 1 facturado 20 kg (37x68x102 cm) por persona",
        "notes": [],
    },
    {
        "label": "Vuelo 2", "desc": "Conexion a Port Elizabeth",
        "from_": "Johannesburgo (JNB)", "to": "Port Elizabeth (PLZ)",
        "date": "25 agosto 2026",
        "dep": "13:20h", "arr": "15:05h",
        "airline": "Airlink", "flight_num": "4Z 789", "duration": "1h 45m",
        "baggage": None,
        "notes": [
            "Check-in online requiere datos de pasaporte al menos 24h antes",
            "Conexion desde vuelo 1: ~3h 30min en Johannesburgo — estar atentos a la puerta de embarque",
        ],
    },
    {
        "label": "Vuelo 3", "desc": "Ciudad del Cabo a Johannesburgo",
        "from_": "Ciudad del Cabo (CPT)", "to": "Johannesburgo (JNB)",
        "date": "1 septiembre 2026",
        "dep": "17:25h", "arr": "19:30h",
        "airline": "Fly Safair", "flight_num": "FA 102", "duration": "2h 5m",
        "baggage": "1 cabina 7 kg (23x36x56 cm) + 1 facturado con seguro 20 kg (28x52x78 cm)",
        "notes": ["Salir del hotel a las 15:00h como maximo"],
    },
    {
        "label": "Vuelo 4", "desc": "Vuelta a Espana",
        "from_": "Johannesburgo (JNB)", "to": "Madrid (MAD)",
        "date": "3 septiembre 2026",
        "dep": "18:55h", "arr": "05:05h del 4 sep (+1 dia)",
        "airline": None, "flight_num": None, "duration": None,
        "baggage": None,
        "notes": [],
    },
]


def render_flights():
    render_section_title("Vuelos del grupo", "Los Vuelos", top=40)
    for f in FLIGHTS:
        with st.container(border=True):
            col_route, col_detail = st.columns([3, 2], gap="large")
            with col_route:
                st.markdown(
                    f"<p style='font-family:Lato,sans-serif;font-size:10px;letter-spacing:3px;"
                    f"text-transform:uppercase;color:#8B6914;margin:0 0 4px 0;'>"
                    f"{f['label']} &nbsp;&middot;&nbsp; {f['desc']}</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<h3 style='font-family:Playfair Display,serif;font-size:22px;"
                    f"margin:0 0 8px 0;color:#1A1A1A;'>"
                    f"{f['from_']} &rarr; {f['to']}</h3>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<p style='font-family:Lato,sans-serif;font-size:13px;"
                    f"color:#8B6914;margin:0;'>"
                    f"{f['date']} &nbsp;&middot;&nbsp; "
                    f"<strong>{f['dep']}</strong> &rarr; <strong>{f['arr']}</strong>"
                    + (f" &nbsp;&middot;&nbsp; {f['duration']}" if f["duration"] else "")
                    + "</p>",
                    unsafe_allow_html=True,
                )
                if f["airline"] or f["flight_num"]:
                    st.caption(
                        " · ".join(filter(None, [f["airline"], f["flight_num"]]))
                    )
            with col_detail:
                if f["baggage"]:
                    st.markdown(f"**Equipaje** — {f['baggage']}")
                for note in f["notes"]:
                    st.warning(note)
        st.write("")


# ─── RESUMEN ─────────────────────────────────────────────────────────────────
def render_summary():
    render_section_title("Vision general", "El Itinerario", top=40)

    st.markdown(
        "| Dia | Fecha | Ruta | Km | Conduccion | Aviso |\n"
        "|-----|-------|------|----|------------|-------|\n"
        "| **Dia 25 Ago** | 25 Ago | Llegada PE — Woodlands Safari Estate | ~120 km | ~2h traslado | John X Safaris |\n"
        "| **Dia 26-27 Ago** | 26-27 Ago | Caza en Woodlands Safari Estate | — | Dias completos en campamento | — |\n"
        "| **Dia 28 Ago** | 28 Ago | Addo Elephant NP + Shamwari Game Reserve | ~300 km | Dia completo de safari | — |\n"
        "| **Dia 29 Ago** | 29 Ago | Port Elizabeth — Tsitsikamma — Plettenberg Bay | 440 km | 5h | — |\n"
        "| **Dia 30 Ago** | 30 Ago | Plett — Knysna — Wilderness — De Hoop | 310 km | 5h | Salir 8:30h |\n"
        "| **Dia 31 Ago** | 31 Ago | De Hoop — Agulhas — Hermanus — Ciudad del Cabo | 382 km | 5h | Salir 7:30h |\n"
        "| **Dia 1 Sep** | 1 Sep | Ciudad del Cabo — vuelo a Johannesburgo | — | — | Vuelo 17:25h |\n"
        "| **Dia 2 Sep** | 2 Sep | Johannesburgo — Sandton y Melrose | — | — | Descanso |\n"
    )

    render_flights()

    render_section_title("Mapa interactivo", "La Ruta completa")
    build_map(selected_day=0, height=460, key="map_summary")

    render_section_title("Notas de viaje", "Antes de partir")
    with st.container(border=True):
        reminders = [
            ("Wild Card",               "Pase de parques nacionales SANParks. Comprar en sanparks.org. Cubre Tsitsikamma y Cabo Agulhas."),
            ("Conduccion por la izquierda", "Diferente a Europa. Prestar especial atencion en rotondas y adelantamientos."),
            ("No conducir de noche",    "Los animales cruzan las carreteras. Llegar siempre antes del atardecer."),
            ("Transporte en Joburg",    "Usar solo Uber o taxi del hotel. Nunca a pie de noche fuera de Sandton o Melrose."),
            ("Restaurantes en CPT",     "Reservar con semanas de antelacion. The Pot Luck Club, La Colombe."),
            ("Table Mountain",          "Comprar ticket del teleferico online la noche anterior. Colas de hasta 2h sin reserva."),
            ("Ballenas en agosto",      "Temporada alta. Hermanus es el epicentro. Tambien en Tsitsikamma y la R44."),
            ("Reserva De Hoop",         "Llevar comida para la noche — pocos servicios. Pista de tierra en buen estado."),
        ]
        for title, body in reminders:
            st.markdown(f"**{title}** — {body}")
    st.write("")

# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## Sudáfrica 2026")
    st.caption("Garden Route · 25 ago – 2 sep 2026")
    st.divider()

    st.markdown("#### Programa")
    for label, date, route in [
        ("Dia 25", "25 Ago", "Llegada PE — Woodlands Safari Estate"),
        ("Dia 26-27", "26-27 Ago", "Caza en Woodlands Safari Estate"),
        ("Dia 28", "28 Ago", "Addo Elephant NP + Shamwari"),
        ("Dia 29", "29 Ago", "Port Elizabeth — Tsitsikamma — Plett"),
        ("Dia 30", "30 Ago", "Knysna — Wilderness — De Hoop"),
        ("Dia 31", "31 Ago", "Agulhas — Hermanus — Ciudad del Cabo"),
        ("Dia 1 Sep", "1 Sep",  "Ciudad del Cabo — Johannesburgo"),
        ("Dia 2 Sep", "2 Sep",  "Johannesburgo — Sandton"),
    ]:
        st.markdown(f"**{label}** &nbsp; {date}  \n*{route}*")

    st.divider()
    st.markdown("#### Estadísticas")
    c1, c2 = st.columns(2)
    c1.metric("Km", "1.684")
    c2.metric("Días", "8")
    c1.metric("Paradas", "13")
    c2.metric("Parques", "5")

    st.divider()
    with st.expander("Como compartir la app"):
        st.markdown(
            "1. Sube el proyecto a **GitHub**\n"
            "2. Ve a **share.streamlit.io**\n"
            "3. Conecta el repo, selecciona `app.py`\n"
            "4. Deploy — obten URL publica\n"
            "5. Comparte el enlace"
        )

# ════════════════════════════════════════════════════════════════════════════════
# MAIN FLOW
# ════════════════════════════════════════════════════════════════════════════════

render_hero()
render_stats_bar()

render_section_title("Ocho dias, trece paradas", "El Itinerario")

tab_res, tab25, tab2627, tab28, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Resumen",
    "25 Ago · Llegada",
    "26-27 Ago · Caza",
    "28 Ago · Safari",
    "29 Ago · Garden Route",
    "30 Ago · De Hoop",
    "31 Ago · Cabo",
    "1 Sep · CPT",
    "2 Sep · Joburg",
])
with tab_res:  render_summary()
with tab25:    render_day(6)
with tab2627:  render_day(7)
with tab28:    render_day(8)
with tab1:     render_day(1)
with tab2:     render_day(2)
with tab3:     render_day(3)
with tab4:     render_day(4)
with tab5:     render_day(5)

# Esenciales — section title is self-contained HTML; cards are native Streamlit
render_section_title("Informacion practica", "Esenciales del viaje")
tips = [
    ("Wild Card",         "Pase SANParks. Cubre Tsitsikamma y Cabo Agulhas. Comprar en sanparks.org"),
    ("Conduccion",        "Por la izquierda. Carnet internacional recomendado. Gasolineras en la N2."),
    ("Ballenas",          "Agosto es temporada alta. Hermanus es el epicentro mundial del avistamiento."),
    ("Moneda — Rand",     "ZAR. 1 EUR aprox. 20 ZAR. Tarjeta aceptada casi en todo. Efectivo para propinas."),
    ("Clima",             "Invierno austral. Garden Route: 15-20 C. Ciudad del Cabo: posible lluvia y viento."),
    ("Apps",              "Uber, Google Maps offline, WhaleWatchSA, iNaturalist."),
]
cols_tips = st.columns(3)
for i, (title, body) in enumerate(tips):
    with cols_tips[i % 3]:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(body)

# Footer — single self-contained HTML block
st.markdown("""
<div style="padding:40px 48px;text-align:center;
            border-top:1px solid #DDD8D0;background:#FAFAF7;margin-top:32px;">
  <div style="width:48px;height:1px;background:#8B6914;margin:0 auto 16px;"></div>
  <p style="font-family:'Lato',sans-serif;font-size:10px;letter-spacing:4px;
            color:#6B6560;text-transform:uppercase;margin:0;">
    SUD&Aacute;FRICA &nbsp;&middot;&nbsp; GARDEN ROUTE &nbsp;&middot;&nbsp; 2026
  </p>
</div>
""", unsafe_allow_html=True)
