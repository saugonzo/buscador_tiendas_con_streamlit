import requests
from bs4 import BeautifulSoup

def buscar_canteraludica(juego):
    url = f"https://canteraludica.com/search?q={juego.replace(' ', '+')}&options%5Bprefix%5D=last"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    resultados = []
    productos = soup.select("li.grid__item")

    for producto in productos:
        nombre_tag = producto.select_one(".card__heading a")
        precio_tag = producto.select_one(".price__regular .price-item--regular")
        imagen_tag = producto.select_one("img")
        agotado_tag = producto.select_one(".card__badge span")

        nombre = nombre_tag.text.strip() if nombre_tag else "Sin nombre"
        precio = precio_tag.text.strip() if precio_tag else "Sin precio"
        url_producto = "https://canteraludica.com" + nombre_tag["href"] if nombre_tag else ""
        imagen = "https:" + imagen_tag["src"] if imagen_tag else ""

        disponible = True
        if agotado_tag and "Agotado" in agotado_tag.text:
            disponible = False

        resultados.append({
            "nombre": nombre,
            "precio": precio,
            "url": url_producto,
            "imagen": imagen,
            "disponible": disponible
        })

    return resultados
