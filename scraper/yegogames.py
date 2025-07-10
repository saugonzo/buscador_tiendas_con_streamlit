import requests
from bs4 import BeautifulSoup

def buscar_yegogames(nombre_juego):
    url = f"https://yegogames.com/search?q={nombre_juego.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    productos = soup.select("li.grid__item")

    for producto in productos:
        nombre = producto.select_one("div.card__content a").text.strip().lower()
        if nombre_juego.lower() in nombre:
            disponibilidad = producto.text.lower()
            if "agotado" not in disponibilidad:
                link = "https://yegogames.com" + producto.select_one("div.card__content a")["href"]
                precio = producto.select_one(".price").text.strip().replace("\n", " ")
                imagen = producto.select_one("img")["src"]
                if imagen.startswith("//"):
                    imagen = "https:" + imagen
                return {
                    "nombre": nombre,
                    "precio": precio,
                    "url": link,
                    "imagen": imagen
                }

    return None
