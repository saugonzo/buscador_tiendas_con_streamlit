# scraper/juegodebelugas.py

import requests
from bs4 import BeautifulSoup

def buscar_juegodebelugas(juego: str):
    url_busqueda = f"https://juegodebelugas.com/search?q={juego.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url_busqueda, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    productos = soup.select("li.grid__item")

    for producto in productos:
        titulo_elem = producto.select_one(".card__heading a")
        precio_elem = producto.select_one(".price-item--regular")
        agotado_elem = producto.select_one(".badge--sold-out")
        imagen_elem = producto.select_one("img")

        if not titulo_elem or not precio_elem or agotado_elem:
            continue

        titulo = titulo_elem.get_text(strip=True)
        if juego.lower() in titulo.lower():
            return {
                "titulo": titulo,
                "precio": precio_elem.get_text(strip=True).replace("\xa0", " "),
                "url": "https://juegodebelugas.com" + titulo_elem["href"],
                "imagen": "https:" + imagen_elem["src"] if imagen_elem and "src" in imagen_elem.attrs else ""
            }

    return None
