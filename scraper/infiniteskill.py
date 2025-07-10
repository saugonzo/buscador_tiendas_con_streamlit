import requests
from bs4 import BeautifulSoup

def buscar_infiniteskill(juego: str) -> dict | None:
    url = f"https://www.infiniteskill.com.mx/?s={juego}&post_type=product"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    producto = soup.select_one("li.product")

    if not producto:
        return None

    # Verificar disponibilidad
    if "instock" not in producto.get("class", []):
        return None

    nombre_tag = producto.select_one("h2.woocommerce-loop-product__title")
    precio_tag = producto.select_one("span.price")
    link_tag = producto.select_one("a.woocommerce-LoopProduct-link")
    img_tag = producto.select_one("img")

    if not all([nombre_tag, precio_tag, link_tag]):
        return None

    return {
        "nombre": nombre_tag.text.strip(),
        "precio": precio_tag.text.strip().replace("\xa0", " "),
        "url": link_tag["href"],
        "imagen": img_tag["src"] if img_tag else None,
    }
