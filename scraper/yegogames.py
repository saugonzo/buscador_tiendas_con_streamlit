
import requests
from bs4 import BeautifulSoup

def buscar_yegogames(nombre_juego):
    url = "https://yegogames.com/search?q=" + nombre_juego.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("h3", class_="card__heading")
    if not producto:
        return None

    titulo = producto.find("a")
    if titulo and nombre_juego.lower() in titulo.text.lower():
        enlace = titulo["href"]
        precio = soup.find("span", class_="price-item--last")
        return {
            "precio": precio.text.strip().replace("$", "").replace("MXN", "").strip(),
            "url": "https://yegogames.com" + enlace
        }
    return None
