import requests
from bs4 import BeautifulSoup

def buscar_elduende(juego):
    url_busqueda = f"https://www.elduende.com.mx/?s={juego}&post_type=product&dgwt_wcas=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url_busqueda, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Caso 1: Redirigió directamente a una página de producto
    if soup.find("body", class_="single-product"):
        nombre = soup.find("h1", class_="product_title").text.strip()
        precio = soup.find("bdi").text.strip()
        imagen_tag = soup.find("img", class_="wp-post-image")
        imagen = imagen_tag["src"] if imagen_tag else ""
        return {
            "nombre": nombre,
            "precio": precio,
            "url": res.url,
            "imagen": imagen
        }

    # Caso 2: Página de resultados múltiples
    contenedor = soup.find("ul", class_="products")
    if not contenedor:
        return None

    producto = contenedor.find("li")
    if not producto:
        return None

    nombre = producto.find("h2", class_="woocommerce-loop-product__title").text.strip()
    precio = producto.find("bdi").text.strip()
    url = producto.find("a", href=True)["href"]
    imagen = producto.find("img", src=True)["src"]

    return {
        "nombre": nombre,
        "precio": precio,
        "url": url,
        "imagen": imagen
    }
