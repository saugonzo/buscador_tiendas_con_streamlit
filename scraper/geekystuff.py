import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(juego):
    try:
        url_busqueda = f"https://www.geekystuff.mx/search-results-page/{juego.replace(' ', '%20')}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url_busqueda, headers=headers, timeout=15)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        productos = soup.select("li[data-hook='product-list-grid-item']")

        for producto in productos:
            nombre_tag = producto.select_one("p[data-hook='product-item-name']")
            if not nombre_tag or juego.lower() not in nombre_tag.text.lower():
                continue

            precio_tag = producto.select_one("[data-hook='product-item-price-to-pay']")
            precio = precio_tag.text.strip() if precio_tag else "Precio no disponible"

            enlace_tag = producto.select_one("a[data-hook='product-item-container']")
            url = "https://www.geekystuff.mx" + enlace_tag["href"] if enlace_tag else ""

            imagen_tag = producto.select_one("img")
            imagen = imagen_tag["src"] if imagen_tag else ""

            return {
                "precio": precio,
                "url": url,
                "imagen": imagen
            }

        return None
    except Exception as e:
        return {"error": str(e)}
