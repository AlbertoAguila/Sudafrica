#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
"""
download_images.py — Descarga fotos reales de Wikipedia/Wikimedia Commons
para el itinerario de Sudáfrica Garden Route.

Uso:
    python download_images.py
"""
import sys
from pathlib import Path

import requests

IMAGES_DIR = Path("images")
IMAGES_DIR.mkdir(exist_ok=True)

WIKI_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {
    "User-Agent": "SudafricaTripApp/1.0 (educational travel itinerary)"
}

# (nombre_archivo, término de búsqueda en Wikipedia)
DOWNLOADS = [
    ("hero.jpg",               "Garden Route South Africa"),
    ("pe_donkin.jpg",          "Donkin Reserve Port Elizabeth"),
    ("pe_beach.jpg",           "Port Elizabeth beach South Africa"),
    ("tsitsikamma_bridge.jpg", "Tsitsikamma suspension bridge Storms River"),
    ("tsitsikamma_coast.jpg",  "Tsitsikamma National Park coastline"),
    ("plett_beach.jpg",        "Plettenberg Bay beach"),
    ("knysna_heads.jpg",       "Knysna Heads"),
    ("knysna_lagoon.jpg",      "Knysna Lagoon"),
    ("wilderness_beach.jpg",   "Wilderness beach Garden Route"),
    ("dehoop_zebras.jpg",      "De Hoop Nature Reserve zebra"),
    ("dehoop_dunes.jpg",       "De Hoop Nature Reserve dunes"),
    ("agulhas_lighthouse.jpg", "Cape Agulhas lighthouse"),
    ("agulhas_sign.jpg",       "Cape Agulhas southernmost point Africa"),
    ("hermanus_whales.jpg",    "Hermanus whale watching southern right whale"),
    ("hermanus_cliffs.jpg",    "Hermanus cliff path"),
    ("cpt_table_mountain.jpg", "Table Mountain Cape Town"),
    ("cpt_bokaap.jpg",         "Bo-Kaap Cape Town colorful houses"),
    ("cpt_waterfront.jpg",     "V&A Waterfront Cape Town"),
    ("joburg_skyline.jpg",     "Sandton Johannesburg skyline"),
]

_VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
_SKIP_EXTS  = {".svg", ".tif", ".tiff", ".gif", ".ogg", ".ogv", ".pdf"}


def get_wiki_image_url(query: str) -> str:
    """
    Busca en Wikipedia y devuelve la URL de imagen del artículo más relevante.
    Usa thumbnails de 1400px (no tienen rate limit como las originales).
    """
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": 8,
        "prop": "pageimages",
        "piprop": "thumbnail|original",
        "pithumbsize": 1400,
        "format": "json",
    }
    try:
        r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        for page in sorted(pages.values(), key=lambda p: p.get("index", 999)):
            # Intentar thumbnail primero (menos rate-limited)
            thumb = page.get("thumbnail", {}).get("source", "")
            if thumb:
                suffix = Path(thumb.split("?")[0]).suffix.lower()
                if suffix in _VALID_EXTS:
                    return thumb
            # Fallback a original
            orig = page.get("original", {}).get("source", "")
            if orig:
                suffix = Path(orig.split("?")[0]).suffix.lower()
                if suffix in _VALID_EXTS and suffix not in _SKIP_EXTS:
                    return orig
    except Exception as exc:
        print(f"[API error] {exc}", file=sys.stderr)
    return ""


def download_image(filename: str, query: str) -> bool:
    """Descarga una imagen. Retorna True si OK o si ya existía."""
    dest = IMAGES_DIR / filename

    if dest.exists():
        size_kb = dest.stat().st_size // 1024
        print(f"  SKIP  {filename:<35} (ya existe, {size_kb} KB)")
        return True

    print(f"  ...   {filename:<35} buscando '{query}'", end="", flush=True)

    url = get_wiki_image_url(query)
    if not url:
        print(" → ❌  no encontrada en Wikipedia")
        return False

    import time
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=45, stream=True)
            if r.status_code == 429:
                wait = 8 + attempt * 6
                print(f"\n      [rate limit] esperando {wait}s...", end="", flush=True)
                time.sleep(wait)
                continue
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=16_384):
                    f.write(chunk)
            size_kb = dest.stat().st_size // 1024
            print(f" → ✓  OK ({size_kb} KB)")
            return True
        except Exception as exc:
            if attempt < 2:
                time.sleep(5)
            else:
                print(f" → ❌  ERROR: {exc}")
                if dest.exists():
                    dest.unlink()
    return False


def main():
    print("=" * 62)
    print("  Sudáfrica Garden Route 2025 — Descarga de fotos")
    print("  Fuente: Wikipedia / Wikimedia Commons (dominio público)")
    print("=" * 62)
    print()

    ok, fail = 0, 0
    for filename, query in DOWNLOADS:
        if download_image(filename, query):
            ok += 1
        else:
            fail += 1

    print()
    print("=" * 62)
    print(f"  ✓  {ok}/{len(DOWNLOADS)} fotos descargadas en images/")
    if fail:
        print(f"  ✗  {fail} no encontradas → la app usará placeholders de color")
    print("=" * 62)


if __name__ == "__main__":
    main()
