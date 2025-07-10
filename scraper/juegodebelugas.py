
import requests
from bs4 import BeautifulSoup

def buscar_juegodebelugas(nombre_juego):
    url = "https://juegodebelugas.com/search?q=" + nombre_juego.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("a", {"class": "full-unstyled-link"})
    if not producto:
        return None

    if nombre_juego.lower() in producto.text.lower():
        enlace = producto["href"]
        precio = soup.find("span", class_="price-item--last")
        return {
            "precio": precio.text.strip().replace("$", "").replace("MXN", "").strip(),
            "url": "https://juegodebelugas.com" + enlace
        }
    return None
