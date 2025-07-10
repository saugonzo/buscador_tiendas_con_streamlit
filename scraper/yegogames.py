import requests
from bs4 import BeautifulSoup
import re

def buscar_yegogames(nombre_juego):
    url_busqueda = f"https://yegogames.com/search?q={nombre_juego.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url_busqueda, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.select_one("div.product-card-wrapper a.full-unstyled-link")
    if not producto:
        return None

    link_producto = "https://yegogames.com" + producto["href"]
    response_producto = requests.get(link_producto, headers=headers)
    soup_producto = BeautifulSoup(response_producto.text, "html.parser")

    # ✅ Verificar disponibilidad real (que se pueda agregar al carrito)
    disponible = soup_producto.select_one("a.product_type_simple.add_to_cart_button")
    if not disponible:
        return None

    # Extraer nombre
    nombre = soup_producto.select_one("h1.product__title").get_text(strip=True)

    # Extraer precio
    precio = soup_producto.select_one("span.price-item--regular")
    if not precio:
        return None
    precio = re.sub(r"[^\d.]", "", precio.text.strip())

    # Extraer imagen
    imagen = soup_producto.select_one("img.product__media") or soup_producto.select_one("img")
    url_imagen = imagen["src"] if imagen else ""

    return {
        "nombre": nombre,
        "precio": precio,
        "url": link_producto,
        "imagen": url_imagen if url_imagen.startswith("http") else f"https:{url_imagen}"
    }
