import requests
from bs4 import BeautifulSoup

def buscar_alfaydelta(juego):
    url = f"https://alfaydelta.com/search?q={juego.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    productos = soup.select(".product-item")  # este selector sí existe en el HTML real

    resultados = []
    for producto in productos:
        nombre_tag = producto.select_one(".product-item__title")
        precio_tag = producto.select_one(".product__price--original")
        link_tag = producto.select_one("a")
        imagen_tag = producto.select_one("img")

        if not (nombre_tag and precio_tag and link_tag and imagen_tag):
            continue

        nombre = nombre_tag.get_text(strip=True)
        precio = precio_tag.get_text(strip=True)
        url_producto = "https://alfaydelta.com" + link_tag["href"]
        imagen = imagen_tag.get("src") or imagen_tag.get("data-src")
        imagen = "https:" + imagen if imagen.startswith("//") else imagen

        # Revisar si el producto está agotado
        agotado = producto.select_one(".product-item__badge--sold")
        disponible = not agotado

        resultados.append({
            "nombre": nombre,
            "precio": precio,
            "url": url_producto,
            "imagen": imagen,
            "disponible": disponible
        })

    return resultados
