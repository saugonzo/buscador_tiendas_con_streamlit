import requests
from bs4 import BeautifulSoup

def buscar_yegogames(juego_buscado):
    url = f"https://yegogames.com/search?q={juego_buscado.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        productos = soup.select("div.card__information")

        for producto in productos:
            nombre_tag = producto.select_one("h3.card__heading a")
            if not nombre_tag:
                continue

            nombre = nombre_tag.get_text(strip=True)
            if juego_buscado.lower() not in nombre.lower():
                continue

            # Verifica que no esté agotado (por lo general no hay etiqueta clara, así que validamos existencia del botón de compra más adelante si necesario)
            precio_tag = producto.select_one(".price__sale .price-item--sale") or producto.select_one(".price__regular .price-item--regular")
            if not precio_tag:
                continue

            precio = precio_tag.get_text(strip=True)

            link = nombre_tag["href"]
            if not link.startswith("http"):
                link = "https://yegogames.com" + link

            # Imagen
            imagen_tag = producto.find_parent("div.card-wrapper").select_one("img")
            imagen = imagen_tag["src"] if imagen_tag else None
            if imagen and imagen.startswith("//"):
                imagen = "https:" + imagen

            return {
                "nombre": nombre,
                "precio": precio,
                "url": link,
                "imagen": imagen
            }

    except Exception as e:
        return {"error": str(e)}

    return None
