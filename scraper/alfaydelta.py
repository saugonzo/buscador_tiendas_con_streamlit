import requests
from bs4 import BeautifulSoup

def buscar_alfaydelta(juego):
    url = f"https://alfaydelta.com/search?q={juego.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    productos = soup.select(".productgrid--item")

    resultados = []
    for producto in productos:
        nombre_tag = producto.select_one(".productitem--title")
        precio_tag = producto.select_one(".price.price--highlight")
        imagen_tag = producto.select_one("img.productitem--image-primary")
        link_tag = producto.select_one("a.full-unstyled-link")

        if not (nombre_tag and precio_tag and link_tag and imagen_tag):
            continue  # saltar si falta algo importante

        nombre = nombre_tag.get_text(strip=True)
        precio = precio_tag.get_text(strip=True)
        url_producto = "https://alfaydelta.com" + link_tag["href"]
        imagen = imagen_tag.get("src") or imagen_tag.get("data-src")
        imagen = "https:" + imagen if imagen.startswith("//") else imagen

        resultados.append({
            "nombre": nombre,
            "precio": precio,
            "url": url_producto,
            "imagen": imagen,
            "disponible": True  # si tiene precio, lo consideramos disponible
        })

    return resultados
