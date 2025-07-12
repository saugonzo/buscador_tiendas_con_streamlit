import requests
from bs4 import BeautifulSoup

def buscar_yegogames(juego):
    url = f"https://yegogames.com/search?q={juego}&options%5Bprefix%5D=last"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    productos = soup.select("div.card-wrapper")

    resultados = []

    for producto in productos:
        nombre_tag = producto.select_one("div.card__content a.full-unstyled-link")
        precio_tag = producto.select_one("div.price__container span.price-item--regular")
        imagen_tag = producto.select_one("img.motion-reduce")

        # Verificar si el producto está agotado por el texto 'Agotado'
        agotado_tag = producto.find("span", string=lambda text: text and "agotado" in text.lower())

        if nombre_tag and precio_tag:
            nombre = nombre_tag.get_text(strip=True)
            precio = precio_tag.get_text(strip=True)
            url_producto = "https://yegogames.com" + nombre_tag.get("href", "")
            imagen = imagen_tag.get("src", "") if imagen_tag else ""
            disponible = agotado_tag is None

            resultados.append({
                "nombre": nombre,
                "precio": precio,
                "url": url_producto,
                "imagen": imagen,
                "disponible": disponible
            })

    return resultados
