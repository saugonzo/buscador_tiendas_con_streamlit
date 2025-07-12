import requests
from bs4 import BeautifulSoup

def buscar_alfaydelta(juego):
    url_busqueda = f"https://www.alfaydelta.com.mx/search?q={juego}"
    response = requests.get(url_busqueda, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    resultados = []
    productos = soup.select(".productgrid--item")

    for producto in productos:
        nombre = producto.select_one(".productitem--title")
        precio = producto.select_one(".money")
        link_tag = producto.select_one("a")
        imagen_tag = producto.select_one("img")

        if not (nombre and precio and link_tag and imagen_tag):
            continue  # Saltar si falta algún dato importante

        url = "https://www.alfaydelta.com.mx" + link_tag["href"]
        nombre = nombre.text.strip()
        precio = precio.text.strip().replace("\n", "")
        imagen = "https:" + imagen_tag.get("src", "")

        # Determinar si está disponible (no dice "Agotado")
        agotado = producto.select_one(".productitem--badge")
        disponible = not (agotado and "agotado" in agotado.text.lower())

        resultados.append({
            "nombre": nombre,
            "precio": precio,
            "url": url,
            "imagen": imagen,
            "disponible": disponible
        })

    return resultados
