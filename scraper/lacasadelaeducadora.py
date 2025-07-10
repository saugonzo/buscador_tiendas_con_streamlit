# scraper/lacasadelaeducadora.py

import requests
from bs4 import BeautifulSoup

def buscar_lacasadelaeducadora(juego: str):
    url_busqueda = f"https://www.lacasadelaeducadora.com/search?q={juego.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url_busqueda, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    productos = soup.select(".product-item")

    for producto in productos:
        titulo_elem = producto.select_one(".product-item-meta__title")
        precio_elem = producto.select_one(".price-list .price")
        agotado_elem = producto.select_one(".product-label--sold-out")
        imagen_elem = producto.select_one("img")
        link_elem = titulo_elem.get("href") if titulo_elem else None

        if not titulo_elem or not precio_elem or agotado_elem:
            continue

        titulo = titulo_elem.get_text(strip=True)
        if juego.lower() in titulo.lower():
            return {
                "titulo": titulo,
                "precio": precio_elem.get_text(strip=True).replace("\xa0", " "),
                "url": "https://www.lacasadelaeducadora.com" + link_elem if link_elem else "",
                "imagen": "https:" + imagen_elem["src"] if imagen_elem and "src" in imagen_elem.attrs else ""
            }

    return None
