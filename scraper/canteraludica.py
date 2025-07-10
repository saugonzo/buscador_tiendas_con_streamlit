
import requests
from bs4 import BeautifulSoup

def buscar_canteraludica(nombre_juego):
    url = "https://canteraludica.com/search?q=" + nombre_juego.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("div", class_="card__information")
    if not producto:
        return None

    titulo = producto.find("a")
    if titulo and nombre_juego.lower() in titulo.text.lower():
        precio = soup.find("span", class_="price-item--last")
        enlace = titulo["href"]
        return {
            "precio": precio.text.strip().replace("$", "").replace("MXN", "").strip(),
            "url": "https://canteraludica.com" + enlace
        }
    return None
