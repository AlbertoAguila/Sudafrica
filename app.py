# -*- coding: utf-8 -*-
"""
Sudáfrica · Garden Route 2025 — Streamlit App
Componentes nativos de Streamlit.
HTML solo donde es imprescindible: hero banner, day headers, drive connectors.
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
    page_title="Sudáfrica · Garden Route",
    page_icon="🌍",
)

# ─── PALETA ──────────────────────────────────────────────────────────────────
DAY_COLORS = {
    0: "#4B5563",
    1: "#2D6A4F",
    2: "#0F766E",
    3: "#B45309",
    4: "#185FA5",
    5: "#533AB7",
}
_BG_RGB = {
    0: (75,  85,  99),
    1: (27,  67,  50),
    2: (15, 118, 110),
    3: (180,  83,   9),
    4: (24,  95, 165),
    5: (83,  58, 183),
}

# ─── IMÁGENES ────────────────────────────────────────────────────────────────
IMAGES_DIR = Path("images")
IMAGES_DIR.mkdir(exist_ok=True)

def _make_placeholder(stem: str, w: int, h: int, day: int) -> Image.Image:
    bg = _BG_RGB.get(day, (27, 67, 50))
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)
    draw.rectangle([4, 4, w - 5, h - 5], outline=(149, 213, 178), width=2)
    label = stem.replace("_", " ").upper()
    try:
        draw.text((w // 2, h // 2), label, fill=(149, 213, 178), anchor="mm")
    except TypeError:
        draw.text((10, h // 2 - 8), label, fill=(149, 213, 178))
    return img

def get_img(stem: str, day: int = 0):
    """Devuelve la ruta del archivo (str) si existe, o una PIL Image placeholder."""
    for ext in (".jpg", ".jpeg", ".png"):
        p = IMAGES_DIR / f"{stem}{ext}"
        if p.exists():
            return str(p)
    return _make_placeholder(stem, 700, 450, day)

@st.cache_data
def hero_b64() -> str:
    """Imagen hero en base64 para el HTML del banner. Vacío si no existe."""
    for ext in (".jpg", ".jpeg", ".png"):
        p = IMAGES_DIR / f"hero{ext}"
        if p.exists():
            try:
                img = Image.open(p).convert("RGB").resize((1400, 500))
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=85)
                return base64.b64encode(buf.getvalue()).decode()
            except Exception:
                pass
    return ""

# ─── ITINERARIO ──────────────────────────────────────────────────────────────
DAYS = {
    1: {
        "label": "Día 1", "date": "29 ago",
        "title": "Garden Route comienza",
        "route": "Woodlands → Port Elizabeth → Tsitsikamma → Plettenberg Bay",
        "km": "~440 km", "hours": "~5h", "alert": None,
        "stops": [
            {
                "name": "PORT ELIZABETH (Gqeberha)", "emoji": "🏙️",
                "time": "Mañana · ~45 min", "img": "pe_donkin",
                "gallery": ["pe_donkin", "pe_beach"],
                "activities": [
                    ("🏛️", "Mirador Donkin Reserve + Faro histórico (1861)"),
                    ("🎨", "Route 67 — 67 obras de arte callejero, homenaje a Mandela"),
                    ("🌊", "Hobie Beach / King's Beach junto al océano Índico"),
                ],
                "badges": [],
            },
            {
                "name": "PARQUE NACIONAL TSITSIKAMMA", "emoji": "🌿",
                "time": "Tarde · 2–3h", "img": "tsitsikamma_bridge",
                "gallery": ["tsitsikamma_bridge", "tsitsikamma_coast"],
                "activities": [
                    ("🌉", "Puente colgante Storms River (2 km ida y vuelta, 1.5h)"),
                    ("🚣", "Ruta en kayak por los desfiladeros del río Storms"),
                    ("🐋", "Avistamiento de ballenas jorobadas desde la costa"),
                    ("🃏", "Wild Card incluida — acceso libre al parque"),
                ],
                "badges": ["wild", "book"],
            },
            {
                "name": "PLETTENBERG BAY", "emoji": "🌅",
                "time": "Noche · dormir aquí", "img": "plett_beach",
                "gallery": ["plett_beach"],
                "activities": [
                    ("🏖️", "Primera gran base de la Garden Route"),
                    ("🌇", "Atardecer sobre el océano Índico"),
                ],
                "badges": [],
            },
        ],
        "drives": [
            ("Port Elizabeth", "Tsitsikamma", "~100 km", "~1.5h"),
            ("Tsitsikamma", "Plettenberg Bay", "~80 km", "~1h"),
        ],
    },
    2: {
        "label": "Día 2", "date": "30 ago",
        "title": "La laguna y las dunas",
        "route": "Plett → Knysna → Wilderness → Reserva De Hoop",
        "km": "~310 km", "hours": "~5h",
        "alert": "⚠️  Día largo — salir antes de las 8:30h. La pista de tierra a De Hoop (~50 km) añade tiempo extra.",
        "stops": [
            {
                "name": "KNYSNA — THE HEADS", "emoji": "⛰️",
                "time": "Mañana · 30–45 min", "img": "knysna_heads",
                "gallery": ["knysna_heads", "knysna_lagoon"],
                "activities": [
                    ("👁️", "Mirador East Head — panorámica del canal y el océano"),
                    ("🌊", "Los dos promontorios que flanquean la laguna de Knysna"),
                ],
                "badges": [],
            },
            {
                "name": "WILDERNESS — Dolphin Point", "emoji": "🐬",
                "time": "Mediodía · 20 min", "img": "wilderness_beach",
                "gallery": ["wilderness_beach"],
                "activities": [
                    ("🔭", "Mirador junto a la N2, sin desvío"),
                    ("🏖️", "Vistas de 17 km de playa dorada y puente de Kaaimans"),
                    ("🐋", "Con suerte: delfines y ballenas"),
                ],
                "badges": [],
            },
            {
                "name": "RESERVA NATURAL DE HOOP", "emoji": "🦓",
                "time": "Tarde/noche · dormir aquí", "img": "dehoop_zebras",
                "gallery": ["dehoop_zebras", "dehoop_dunes"],
                "activities": [
                    ("🦓", "Cebras, avestruces, bonteboks y elands desde la entrada"),
                    ("🏜️", "Ruta a las dunas blancas hasta el Índico (5 km, antes 16h)"),
                    ("🌿", "Fynbos y cielo estrellado espectacular"),
                    ("🚗", "Pista de tierra ~50 km en buen estado, no hace falta 4x4"),
                ],
                "badges": ["wild", "warn"],
            },
        ],
        "drives": [
            ("Plettenberg Bay", "Knysna", "~35 km", "~30 min"),
            ("Knysna", "Wilderness", "~60 km", "~45 min"),
            ("Wilderness", "De Hoop Reserve", "~200 km + 50 km pista", "~3h"),
        ],
    },
    3: {
        "label": "Día 3", "date": "31 ago",
        "title": "El fin del continente",
        "route": "De Hoop → Cabo Agulhas → Hermanus → Ciudad del Cabo",
        "km": "~382 km", "hours": "~5h",
        "alert": "⚠️  Salir antes de las 7:30h para llegar a Ciudad del Cabo con luz de tarde.",
        "stops": [
            {
                "name": "CABO DE LAS AGUJAS (Cape Agulhas)", "emoji": "🌍",
                "time": "Mañana · ~1h", "img": "agulhas_lighthouse",
                "gallery": ["agulhas_lighthouse", "agulhas_sign"],
                "activities": [
                    ("📍", "El punto más al sur del continente africano"),
                    ("🌊", "Donde se dividen el océano Índico y el Atlántico"),
                    ("🏛️", "Faro de 1848 — segundo más antiguo de Sudáfrica"),
                    ("🃏", "Entrada con Wild Card"),
                ],
                "badges": ["wild"],
            },
            {
                "name": "HERMANUS", "emoji": "🐳",
                "time": "Mediodía · ~2h", "img": "hermanus_whales",
                "gallery": ["hermanus_whales", "hermanus_cliffs"],
                "activities": [
                    ("🥾", "Cliff Path Walk — sendero por acantilados (2–3 km)"),
                    ("🐋", "Plena temporada de ballenas francas australes (agosto)"),
                    ("⚓", "Old Harbour + Whale House Museum"),
                    ("⛵", "Tour en barco opcional (+1.5h) — reservar antes"),
                ],
                "badges": ["book", "tip"],
            },
            {
                "name": "CIUDAD DEL CABO", "emoji": "🏔️",
                "time": "Llegada ~17h · dormir aquí", "img": "cpt_waterfront",
                "gallery": ["cpt_waterfront", "cpt_table_mountain"],
                "activities": [
                    ("🛣️", "Ruta costera R44 — espectacular, posibles ballenas"),
                    ("⚓", "V&A Waterfront para el atardecer con vistas a Table Mountain"),
                    ("🍽️", "Paseo por Bree Street — corazón gastronómico"),
                ],
                "badges": [],
            },
        ],
        "drives": [
            ("De Hoop Reserve", "Cabo Agulhas", "~85 km", "~1.5h"),
            ("Cabo Agulhas", "Hermanus", "~90 km", "~1.5h"),
            ("Hermanus", "Ciudad del Cabo (R44)", "~120 km", "~2h"),
        ],
    },
    4: {
        "label": "Día 4", "date": "1 sep",
        "title": "Ciudad del Cabo · Vuelo",
        "route": "Ciudad del Cabo → Aeropuerto CPT → Johannesburgo",
        "km": "Vuelo · ~1.400 km", "hours": "~2h vuelo",
        "alert": "✈️  Salir del hotel a las 15:30h · Vuelo CPT→JNB 17:30h · Llegada Joburg ~20:00h",
        "stops": [
            {
                "name": "BO-KAAP", "emoji": "🎨",
                "time": "8:00–9:30h", "img": "cpt_bokaap",
                "gallery": ["cpt_bokaap"],
                "activities": [
                    ("🏘️", "Casas pintadas en colores brillantes, callejuelas empedradas"),
                    ("🕌", "Primera mezquita de Sudáfrica — Auwal Mosque (1794)"),
                    ("📸", "Wale Street y Chiappini Street para las mejores fotos"),
                ],
                "badges": [],
            },
            {
                "name": "TABLE MOUNTAIN", "emoji": "⛰️",
                "time": "9:30–12:00h", "img": "cpt_table_mountain",
                "gallery": ["cpt_table_mountain"],
                "activities": [
                    ("🚡", "Teleférico de 5 min — vistas de 360° desde la cima"),
                    ("🎟️", "Reservar ticket online la noche anterior (hay colas)"),
                    ("🌧️", "Si nublado: V&A Waterfront + museo Zeitz MOCAA"),
                ],
                "badges": ["book"],
            },
            {
                "name": "ÚLTIMO ALMUERZO · CABO", "emoji": "🍽️",
                "time": "12:30–14:00h", "img": "cpt_waterfront",
                "gallery": [],
                "activities": [
                    ("🍳", "The Pot Luck Club (Old Biscuit Mill) — tapas creativas"),
                    ("🦞", "Pier en el V&A Waterfront — marisco con vistas"),
                ],
                "badges": [],
            },
        ],
        "drives": [],
        "flight": True,
    },
    5: {
        "label": "Día 5", "date": "2 sep",
        "title": "Johannesburgo · Final",
        "route": "Johannesburgo — Sandton / Melrose",
        "km": "—", "hours": "Descanso", "alert": None,
        "stops": [
            {
                "name": "JOHANNESBURGO · Sandton", "emoji": "🏙️",
                "time": "Todo el día", "img": "joburg_skyline",
                "gallery": ["joburg_skyline"],
                "activities": [
                    ("😴", "Descanso bien merecido tras la Garden Route"),
                    ("🍜", "Explorar restaurantes y cultura local de Sandton"),
                    ("🛍️", "Sandton City / Nelson Mandela Square"),
                ],
                "badges": [],
            },
        ],
        "drives": [],
        "safety": True,
    },
}

ROUTE_POINTS = [
    {"name": "Port Elizabeth (Gqeberha)", "day": 1, "lat": -33.9608, "lon": 25.6022,
     "emoji": "🏙️", "desc": "Route 67 · Donkin Reserve · Playa del Índico"},
    {"name": "Tsitsikamma",               "day": 1, "lat": -33.9833, "lon": 23.9167,
     "emoji": "🌿", "desc": "Puente colgante · Kayak en Storms River"},
    {"name": "Plettenberg Bay",           "day": 1, "lat": -34.0522, "lon": 23.3716,
     "emoji": "🌅", "desc": "Base nocturna · Garden Route"},
    {"name": "Knysna",                    "day": 2, "lat": -34.0363, "lon": 23.0474,
     "emoji": "⛰️", "desc": "The Heads · Laguna · East Head mirador"},
    {"name": "Wilderness",                "day": 2, "lat": -33.9913, "lon": 22.5849,
     "emoji": "🐬", "desc": "Dolphin Point · 17 km de playa"},
    {"name": "De Hoop Nature Reserve",    "day": 2, "lat": -34.4547, "lon": 20.4329,
     "emoji": "🦓", "desc": "Cebras · Dunas blancas · Cielo estrellado"},
    {"name": "Cabo Agulhas",              "day": 3, "lat": -34.8279, "lon": 20.0077,
     "emoji": "🌍", "desc": "Punta más austral de África · Dos océanos"},
    {"name": "Hermanus",                  "day": 3, "lat": -34.4190, "lon": 19.2352,
     "emoji": "🐳", "desc": "Ballenas francas · Cliff Path"},
    {"name": "Ciudad del Cabo",           "day": 3, "lat": -33.9249, "lon": 18.4241,
     "emoji": "🏔️", "desc": "Table Mountain · Bo-Kaap · V&A Waterfront"},
    {"name": "Johannesburgo",             "day": 5, "lat": -26.2041, "lon": 28.0473,
     "emoji": "✈️", "desc": "Final del viaje · Vuelo desde CPT (Día 4)"},
]

# ─── MAPA FOLIUM ─────────────────────────────────────────────────────────────
def build_map(selected_day: int = 0, height: int = 480, key: str = "map"):
    try:
        day_dates = {1: "29 ago", 2: "30 ago", 3: "31 ago", 4: "1 sep", 5: "2 sep"}
        if selected_day > 0:
            pts = [p for p in ROUTE_POINTS if p["day"] == selected_day]
            clat = sum(p["lat"] for p in pts) / len(pts) if pts else -33.5
            clon = sum(p["lon"] for p in pts) / len(pts) if pts else 22.0
            zoom = 9 if len(pts) <= 2 else 8
        else:
            clat, clon, zoom = -33.5, 22.0, 6

        m = folium.Map(location=[clat, clon], zoom_start=zoom,
                       tiles="CartoDB positron", control_scale=True)

        road_pts = [(p["lat"], p["lon"]) for p in ROUTE_POINTS if p["day"] != 5]
        folium.PolyLine(road_pts, color="#2D6A4F", weight=3, opacity=0.8,
                        dash_array="8 4", tooltip="Garden Route").add_to(m)
        folium.PolyLine([(-33.9249, 18.4241), (-26.2041, 28.0473)],
                        color="#185FA5", weight=2, opacity=0.55, dash_array="5 9",
                        tooltip="✈️ Vuelo CPT → JNB").add_to(m)

        for pt in ROUTE_POINTS:
            color = DAY_COLORS[pt["day"]]
            active = selected_day == 0 or pt["day"] == selected_day
            popup_html = (
                f'<div style="font-family:sans-serif;min-width:180px;padding:4px;">'
                f'<div style="font-size:1.3rem;">{pt["emoji"]}</div>'
                f'<b>{pt["name"]}</b><br>'
                f'<span style="color:#6B7280;font-size:.75rem;">'
                f'Día {pt["day"]} · {day_dates.get(pt["day"],"")}</span><br>'
                f'<span style="font-size:.8rem;">{pt["desc"]}</span></div>'
            )
            folium.CircleMarker(
                location=(pt["lat"], pt["lon"]),
                radius=10 if active else 6,
                color=color, fill=True, fill_color=color,
                fill_opacity=0.95 if active else 0.35, weight=2.5,
                popup=folium.Popup(popup_html, max_width=230),
                tooltip=f"{pt['emoji']} {pt['name']}",
            ).add_to(m)

        st_folium(m, height=height, use_container_width=True, key=key)
    except Exception as e:
        st.warning(f"El mapa no se pudo cargar: {e}")

# ─── COMPONENTES HTML (solo hero, day header, drive connector) ────────────────
def render_hero():
    b64 = hero_b64()
    if b64:
        bg = f'background-image:url("data:image/jpeg;base64,{b64}");background-size:cover;background-position:center;'
    else:
        bg = "background:linear-gradient(135deg,#071a0e 0%,#1B4332 55%,#071a0e 100%);"

    st.markdown(f"""
<div style="{bg}padding:4rem 2rem;text-align:center;position:relative;
            min-height:280px;display:flex;align-items:center;justify-content:center;">
    <div style="position:absolute;inset:0;background:rgba(0,0,0,0.55);"></div>
    <div style="position:relative;z-index:1;max-width:820px;margin:0 auto;">
        <p style="font-size:.68rem;letter-spacing:.32em;color:#95D5B2;
                  text-transform:uppercase;margin-bottom:.8rem;">
            Itinerario · Agosto–Septiembre 2025
        </p>
        <h1 style="font-size:clamp(2rem,6vw,4.5rem);color:#FFF;margin:0 0 .8rem;
                   font-weight:900;line-height:1;letter-spacing:-.02em;">
            SUDÁFRICA<br>· GARDEN ROUTE
        </h1>
        <p style="color:rgba(181,224,198,.85);font-size:.95rem;letter-spacing:.06em;margin:0;">
            29 AGO — 2 SEP &nbsp;·&nbsp; 750 km de costa &nbsp;·&nbsp;
            ballenas &nbsp;·&nbsp; bosques &nbsp;·&nbsp; vida salvaje
        </p>
    </div>
</div>
""", unsafe_allow_html=True)


def render_day_header(day_n: int, data: dict, color: str):
    alert_html = ""
    if data.get("alert"):
        alert_html = (
            f'<div style="background:rgba(231,111,81,.12);border-left:4px solid #E76F51;'
            f'border-radius:0 8px 8px 0;padding:.6rem 1rem;margin-top:.8rem;'
            f'font-size:.84rem;color:#fbc8b8;">{data["alert"]}</div>'
        )
    st.markdown(f"""
<div style="background:linear-gradient(135deg,{color}cc,{color}28);
            border:1px solid {color}55;border-radius:12px;
            padding:1.5rem 2rem;margin-bottom:1rem;
            position:relative;overflow:hidden;">
    <div style="font-size:5rem;font-weight:900;color:rgba(255,255,255,.07);
                position:absolute;right:1.5rem;top:50%;
                transform:translateY(-50%);line-height:1;user-select:none;">{day_n}</div>
    <div style="position:relative;z-index:1;">
        <span style="font-size:.65rem;font-weight:600;letter-spacing:.2em;
                     color:rgba(255,255,255,.55);text-transform:uppercase;">
            {data['date'].upper()} · 2025
        </span>
        <h2 style="color:#FFF;margin:.3rem 0 .4rem;font-size:1.45rem;">{data['title']}</h2>
        <p style="font-size:.86rem;color:rgba(255,255,255,.75);margin:.2rem 0;">
            📍 {data['route']}
        </p>
        <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.4rem;">
            <span style="background:rgba(0,0,0,.25);padding:.2rem .65rem;
                         border-radius:16px;font-size:.77rem;color:rgba(255,255,255,.88);">
                🚗 {data['km']}
            </span>
            <span style="background:rgba(0,0,0,.25);padding:.2rem .65rem;
                         border-radius:16px;font-size:.77rem;color:rgba(255,255,255,.88);">
                ⏱️ {data['hours']}
            </span>
        </div>
        {alert_html}
    </div>
</div>
""", unsafe_allow_html=True)


def render_drive(drv: tuple):
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:.7rem;'
        f'padding:.42rem .9rem;margin:.4rem 0 .4rem 1rem;'
        f'background:rgba(27,67,50,.06);'
        f'border:1px dashed rgba(45,106,79,.28);border-radius:7px;'
        f'font-size:.76rem;color:#6B7280;">'
        f'🚗 &nbsp;'
        f'<span style="color:#2D6A4F;font-weight:600;">{drv[0]} → {drv[1]}</span>'
        f'&nbsp; {drv[2]} &nbsp;·&nbsp; {drv[3]}'
        f'</div>',
        unsafe_allow_html=True,
    )

# ─── BADGES ──────────────────────────────────────────────────────────────────
_BADGE_MAP = {
    "wild":   ("🃏 Wild Card",      "green"),
    "book":   ("📅 Reservar antes", "orange"),
    "warn":   ("⚠️ Aviso",           "red"),
    "tip":    ("💡 Consejo",          "violet"),
    "flight": ("✈️ Vuelo",            "blue"),
}

def render_badges(badges: list):
    valid = [b for b in badges if b in _BADGE_MAP]
    if not valid:
        return
    cols = st.columns(len(valid))
    for col, key in zip(cols, valid):
        label, color = _BADGE_MAP[key]
        with col:
            try:
                st.badge(label, color=color)
            except AttributeError:
                st.caption(f"`{label}`")

# ─── PARADA ──────────────────────────────────────────────────────────────────
def render_stop(stop: dict, day_n: int):
    st.divider()
    col_img, col_txt = st.columns([1, 2], gap="medium")
    with col_img:
        st.image(get_img(stop["img"], day_n), use_container_width=True)
    with col_txt:
        st.subheader(f"{stop['emoji']} {stop['name']}")
        st.caption(f"⏱ {stop['time']}")
        for ico, txt in stop["activities"]:
            st.markdown(f"- {ico} &nbsp; {txt}")
        render_badges(stop.get("badges", []))

# ─── GALERÍA ─────────────────────────────────────────────────────────────────
def render_gallery(day_n: int, data: dict):
    all_stems = []
    for s in data["stops"]:
        for stem in s.get("gallery", []):
            if stem not in all_stems:
                all_stems.append(stem)
    all_stems = all_stems[:6]
    if not all_stems:
        return

    st.divider()
    st.subheader(f"📷 Galería — Día {day_n}")
    for i in range(0, len(all_stems), 3):
        row = all_stems[i:i + 3]
        cols = st.columns(len(row))
        for col, stem in zip(cols, row):
            with col:
                st.image(
                    get_img(stem, day_n),
                    use_container_width=True,
                    caption=stem.replace("_", " ").title(),
                )

# ─── DÍA ─────────────────────────────────────────────────────────────────────
def render_day(day_n: int):
    data = DAYS[day_n]
    color = DAY_COLORS[day_n]
    render_day_header(day_n, data, color)

    # Tarjeta de vuelo (solo día 4)
    if data.get("flight"):
        st.info(
            "**Vuelo CPT → JNB**  \n"
            "Salida hotel **15:30h** · Vuelo **17:30h** · Llegada JNB **~20:00h**",
            icon="✈️",
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("Origen", "CPT", "Ciudad del Cabo")
        c2.metric("Hora de salida", "17:30h", "~2h vuelo")
        c3.metric("Destino", "JNB", "Johannesburgo")

    # Paradas + conectores de ruta
    drives = data.get("drives", [])
    for idx, stop in enumerate(data["stops"]):
        if idx > 0 and idx - 1 < len(drives):
            render_drive(drives[idx - 1])
        render_stop(stop, day_n)

    # Conectores sobrantes tras la última parada
    n = len(data["stops"])
    for drv in drives[n - 1:]:
        render_drive(drv)

    # Aviso de seguridad (solo día 5)
    if data.get("safety"):
        st.divider()
        st.warning(
            "**Seguridad en Johannesburgo**\n\n"
            "- Moverse **siempre en Uber o taxi del hotel**\n"
            "- Nunca a pie de noche fuera de zonas turísticas\n"
            "- Sandton y Melrose son las zonas más seguras\n"
            "- Guardar el móvil fuera de la vista en la calle\n"
            "- No mostrar cámaras caras ni joyas en público",
            icon="⚠️",
        )

    # Galería del día
    render_gallery(day_n, data)

# ─── RESUMEN ─────────────────────────────────────────────────────────────────
def render_summary():
    st.subheader("📋 Resumen del viaje")
    st.caption("Visión global · Tabla de etapas · Recordatorios esenciales")
    st.divider()

    # Tabla con markdown nativo (sin HTML)
    st.markdown(
        "| Día | Fecha | Ruta | Km | Conducción | Aviso |\n"
        "|-----|-------|------|----|------------|-------|\n"
        "| **Día 1** | 29 ago | PE → Tsitsikamma → Plettenberg Bay | ~440 km | ~5h | — |\n"
        "| **Día 2** | 30 ago | Plett → Knysna → Wilderness → De Hoop | ~310 km | ~5h | ⚠️ Salir 8:30h |\n"
        "| **Día 3** | 31 ago | De Hoop → Agulhas → Hermanus → CPT | ~382 km | ~5h | ⚠️ Salir 7:30h |\n"
        "| **Día 4** | 1 sep | Ciudad del Cabo (mañana libre) | — | — | ✈️ Vuelo 17:30h |\n"
        "| **Día 5** | 2 sep | Johannesburgo — Sandton / Melrose | — | — | Descanso |\n"
    )

    st.divider()
    st.subheader("🗺️ Mapa completo")
    build_map(selected_day=0, height=460, key="map_summary")

    st.divider()
    st.subheader("📌 Recordatorios esenciales")
    reminders = [
        ("🃏", "**Wild Card** — Pase parques nacionales. Comprar en sanparks.org. Cubre Tsitsikamma y Cabo Agulhas."),
        ("🚗", "**Conducir por la IZQUIERDA** — Diferente a Europa. Recordarlo especialmente en rotondas y adelantamientos."),
        ("🌙", "**No conducir de noche** — Los animales cruzan las carreteras. Llegar siempre antes del atardecer."),
        ("🚕", "**En Joburg: solo Uber o taxi del hotel** — Nunca a pie de noche fuera de Sandton o Melrose."),
        ("🍽️", "**Restaurantes Ciudad del Cabo** — Reservar con semanas de antelación. The Pot Luck Club, La Colombe."),
        ("🎟️", "**Table Mountain** — Comprar ticket del teleférico online la noche anterior. Colas de 2h sin reserva."),
        ("🐋", "**Ballenas en agosto** — Temporada alta. Hermanus es el epicentro. También en Tsitsikamma y la R44."),
        ("🌿", "**De Hoop** — Llevar comida para la noche (pocos servicios). Pista de tierra en buen estado."),
    ]
    for icon, text in reminders:
        st.markdown(f"{icon} &nbsp; {text}")

# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.title("🌍 Sudáfrica 2025")
    st.caption("Garden Route · 29 ago – 2 sep")
    st.divider()

    st.subheader("Programa")
    for label, date, route in [
        ("Día 1", "29 ago", "PE → Tsitsikamma → Plett"),
        ("Día 2", "30 ago", "Knysna → Wilderness → De Hoop"),
        ("Día 3", "31 ago", "Agulhas → Hermanus → CPT"),
        ("Día 4", "1 sep",  "Ciudad del Cabo ✈️ Joburg"),
        ("Día 5", "2 sep",  "Johannesburgo · Final"),
    ]:
        st.markdown(f"**{label}** · {date}  \n*{route}*")

    st.divider()
    st.subheader("Estadísticas")
    c1, c2 = st.columns(2)
    c1.metric("Km totales", "1.534")
    c2.metric("Días", "5")
    c1.metric("Destinos", "10")
    c2.metric("Océanos", "2")
    st.metric("Parques nacionales", "3")

    st.divider()
    with st.expander("🔗 Cómo compartir la app"):
        st.markdown(
            "1. Sube el proyecto a **GitHub**\n"
            "2. Ve a **share.streamlit.io**\n"
            "3. Conecta el repo → selecciona `app.py`\n"
            "4. Deploy → URL pública 🎉\n"
            "5. Comparte por WhatsApp"
        )

# ════════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════════

# Hero
render_hero()

# Stats
st.write("")
cols_s = st.columns(6)
for col, (val, label) in zip(cols_s, [
    ("5",    "Días"),
    ("750+", "Kilómetros"),
    ("10",   "Destinos"),
    ("2",    "Océanos"),
    ("3",    "Parques"),
    ("∞",   "Recuerdos"),
]):
    col.metric(label, val)

st.divider()

# Mapa principal
st.subheader("🗺️ La Ruta · Garden Route")
st.caption("750 km · De Port Elizabeth a Ciudad del Cabo")
build_map(selected_day=0, height=480, key="map_main")

st.divider()

# Navegación por días
st.subheader("📅 Itinerario día a día")
tab1, tab2, tab3, tab4, tab5, tab_res = st.tabs([
    "🌿 Día 1 · 29 ago",
    "🦓 Día 2 · 30 ago",
    "🌍 Día 3 · 31 ago",
    "✈️ Día 4 · 1 sep",
    "🏙️ Día 5 · 2 sep",
    "📋 Resumen",
])
with tab1: render_day(1)
with tab2: render_day(2)
with tab3: render_day(3)
with tab4: render_day(4)
with tab5: render_day(5)
with tab_res: render_summary()

st.divider()

# Esenciales
st.subheader("⚡ Esenciales del viaje")
tips = [
    ("🃏", "Wild Card",     "Pase parques nacionales. Cubre Tsitsikamma y Cabo Agulhas. Comprar en **sanparks.org**"),
    ("🚗", "Conducción",    "Se conduce por la **izquierda**. Carnet internacional recomendado. Gasolineras en la N2."),
    ("🐋", "Ballenas",      "Agosto es temporada alta de ballenas francas australes. Hermanus es el epicentro."),
    ("💱", "Moneda · Rand", "Rand (ZAR). 1€ ≈ 20 ZAR. Tarjeta aceptada casi en todo. Efectivo para propinas."),
    ("☀️", "Clima agosto",  "Invierno en Sudáfrica. Garden Route: 15–20 °C. Ciudad del Cabo: lluvia posible."),
    ("📱", "Apps útiles",   "**Uber** · **Google Maps offline** · **WhaleWatchSA** · **iNaturalist**"),
]
tip_cols = st.columns(3)
for i, (emoji, title, body) in enumerate(tips):
    with tip_cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"**{emoji} {title}**")
            st.caption(body)

# Footer
st.divider()
st.markdown(
    "<p style='text-align:center;color:#6B7280;font-size:.8rem;'>"
    "🌍 &nbsp; SUDÁFRICA · GARDEN ROUTE · 2025"
    "</p>",
    unsafe_allow_html=True,
)
