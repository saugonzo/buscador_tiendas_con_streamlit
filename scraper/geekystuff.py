import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(nombre_juego):
    try:
        url = f"https://www.geekystuff.mx/search?query={nombre_juego}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        productos = soup.select("a[href^='/product-page/']")

        for producto in productos:
            link = "https://www.geekystuff.mx" + producto["href"]
            titulo = producto.get_text(strip=True)

            if nombre_juego.lower() not in titulo.lower():
                continue

            # Cargar la página del producto
            detalle = requests.get(link, timeout=10)
            detalle.raise_for_status()
            detalle_soup = BeautifulSoup(detalle.text, "html.parser")

            # Detectar disponibilidad
            boton = detalle_soup.select_one("button[data-hook='add-to-cart']")
            if not boton or "disabled" in boton.attrs:
                continue  # Producto agotado

            # Obtener precio
            precio_tag = detalle_soup.select_one("span[data-hook='formatted-primary-price']")
            precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no disponible"

            # Obtener imagen
            img_tag = detalle_soup.select_one("img[src*='/product-page/']")
            imagen = img_tag["src"] if img_tag else ""

            return {
                "titulo": titulo,
                "precio": precio,
                "url": link,
                "imagen": imagen
            }

        return None
    except Exception as e:
        return {"error": str(e)}
