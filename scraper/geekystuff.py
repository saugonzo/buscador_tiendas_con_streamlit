import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(nombre_juego):
    url = f"https://www.geekystuff.mx/search?query={nombre_juego}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("li", {"data-hook": "product-list-grid-item"})

        for item in items:
            nombre = item.find("p", {"data-hook": "product-item-name"})
            if not nombre:
                continue
            nombre_texto = nombre.get_text(strip=True)

            if nombre_juego.lower() not in nombre_texto.lower():
                continue

            enlace_tag = item.find("a", {"data-hook": "product-item-product-details-link"})
            enlace = enlace_tag["href"] if enlace_tag else ""
            if enlace and not enlace.startswith("http"):
                enlace = "https://www.geekystuff.mx" + enlace

            precio_tag = item.find("span", {"data-hook": "product-item-price-to-pay"})
            precio = precio_tag.get_text(strip=True) if precio_tag else "N/A"

            img_tag = item.find("img")
            imagen = img_tag["src"] if img_tag else None
            return {
                "nombre": nombre_texto,
                "precio": precio,
                "url": enlace,
                "imagen": imagen,
            }

    except Exception:
        return None

    return None
