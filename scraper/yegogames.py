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
    productos = soup.select("li.grid__item")

    resultados = []

    for producto in productos:
        nombre_tag = producto.select_one("a.card-information__text.h5")
        precio_tag = producto.select_one("span.price-item--regular")
        imagen_tag = producto.select_one("img.motion-reduce")

        # Verifica si tiene botón de "Agotado"
        boton = producto.select_one("button.button[disabled]")

        if nombre_tag and precio_tag:
            nombre = nombre_tag.get_text(strip=True)
            precio = precio_tag.get_text(strip=True)
            url_producto = "https://yegogames.com" + nombre_tag.get("href", "")
            imagen = imagen_tag.get("src", "") if imagen_tag else ""

            disponible = boton is None  # Si hay botón disabled, está agotado

            resultados.append({
                "nombre": nombre,
                "precio": precio,
                "url": url_producto,
                "imagen": imagen,
                "disponible": disponible
            })

    return resultados
