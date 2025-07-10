
import requests
from bs4 import BeautifulSoup

def buscar_tdetlacuache(juego, debug=False):
    try:
        url_base = "https://tdetlacuache.com"
        busqueda = juego.replace(" ", "+")
        url_busqueda = f"https://tdetlacuache.com/search?q={busqueda}"

        res = requests.get(url_busqueda, timeout=10)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        producto = soup.select_one("div.card__information")
        if not producto:
            return None

        nombre_producto = producto.select_one("a.full-unstyled-link").text.strip().lower()
        if juego.lower() not in nombre_producto:
            return None

        precio_tag = producto.select_one("span.price-item.price-item--sale, span.price-item.price-item--regular")
        if not precio_tag:
            return None
        precio = precio_tag.text.strip().replace("$", "").replace("MXN", "").strip()

        agotado = producto.select_one("div.card-information .caption-with-letter-spacing")
        if agotado and "agotado" in agotado.text.lower():
            return None

        link_rel = producto.select_one("a.full-unstyled-link")["href"]
        link = url_base + link_rel

        imagen_tag = producto.find_previous("img")
        imagen = "https:" + imagen_tag["src"] if imagen_tag and imagen_tag.get("src") else None

        return {
            "precio": precio,
            "url": link,
            "imagen": imagen
        }

    except Exception as e:
        if debug:
            print("Error en tdetlacuache:", e)
        return None
