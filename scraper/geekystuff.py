import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(nombre_juego):
    try:
        url = f"https://geekystuff.mx/search?q={nombre_juego}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        productos = soup.select(".product-grid-item")

        for producto in productos:
            titulo_tag = producto.select_one(".card__heading a")
            titulo = titulo_tag.get_text(strip=True) if titulo_tag else ""

            if nombre_juego.lower() in titulo.lower():
                disponible = "Agotado" not in producto.text and "agotado" not in producto.text.lower()
                if not disponible:
                    continue

                link = "https://geekystuff.com.mx" + titulo_tag.get("href")

                precio_tag = producto.select_one(".price__sale .price-item--sale") or \
                             producto.select_one(".price__regular .price-item--regular")
                precio = precio_tag.get_text(strip=True).replace("\n", "") if precio_tag else "Precio no encontrado"

                imagen_tag = producto.select_one("img")
                imagen = "https:" + imagen_tag.get("src") if imagen_tag and imagen_tag.get("src") else ""

                return {
                    "titulo": titulo,
                    "precio": precio,
                    "url": link,
                    "imagen": imagen
                }

        return None
    except Exception as e:
        return {"error": str(e)}
