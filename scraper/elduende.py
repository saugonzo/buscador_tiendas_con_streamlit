import requests
from bs4 import BeautifulSoup

def buscar_elduende(juego: str):
    url_busqueda = f"https://www.elduende.com.mx/?s={juego}&post_type=product&dgwt_wcas=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url_busqueda, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.select_one("ul.products li.product a.woocommerce-LoopProduct-link")
    if not producto:
        return None

    url_producto = producto["href"]
    response_producto = requests.get(url_producto, headers=headers)
    soup_producto = BeautifulSoup(response_producto.text, "html.parser")

    # Verificamos si el producto está agotado
    agotado = soup_producto.find(string=lambda t: "¡Avísame cuando esté disponible!" in t)
    if agotado:
        return None

    titulo = soup_producto.select_one("h1.product_title").get_text(strip=True)
    precio = soup_producto.select_one("p.price").get_text(strip=True)
    imagen_tag = soup_producto.select_one("figure.woocommerce-product-gallery__wrapper img")
    imagen = imagen_tag["src"] if imagen_tag else ""

    return {
        "nombre": titulo,
        "precio": precio,
        "url": url_producto,
        "imagen": imagen,
    }
