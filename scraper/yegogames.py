# scraper/yegogames.py

import requests
from bs4 import BeautifulSoup

def buscar_yegogames(juego: str) -> dict | None:
    url = f"https://yegogames.com/search?q={juego.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        productos = soup.select("li.grid__item")

        for prod in productos:
            info = prod.select_one("div.card__information")
            if not info:
                continue

            nombre_tag = info.select_one("h3.card__heading a")
            if not nombre_tag:
                continue
            nombre = nombre_tag.get_text(strip=True)
            if juego.lower() not in nombre.lower():
                continue

            # Revisamos precio (oferta o regular)
            precio_tag = info.select_one(".price-item--sale") or info.select_one(".price-item--regular")
            if not precio_tag:
                continue

            # Si está marcado como agotado, lo descartamos
            agotado = prod.select_one(".badge--bottom-left")
            if agotado and "agotado" in agotado.get_text(strip=True).lower():
                continue

            precio = precio_tag.get_text(strip=True)
            link = nombre_tag["href"]
            if not link.startswith("http"):
                link = "https://yegogames.com" + link

            img = prod.select_one("img")
            imagen = img["src"] if img and img.get("src") else ""
            if imagen.startswith("//"):
                imagen = "https:" + imagen

            return {
                "nombre": nombre,
                "precio": precio,
                "url": link,
                "imagen": imagen
            }

    except Exception as e:
        print("Error al buscar en YegoGames:", e)

    return None
