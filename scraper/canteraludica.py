import requests
from bs4 import BeautifulSoup

def buscar_canteraludica(nombre_juego):
    url = "https://canteraludica.com/search?q=" + nombre_juego.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    card = soup.find("div", class_="card__information")
    if card and nombre_juego.lower() in card.text.lower():
        enlace = card.find("a")["href"]
        precio = soup.find("span", class_="price-item--last")
        return {
            "precio": precio.text.strip().replace("$", "").replace("MXN", "").strip(),
            "url": "https://canteraludica.com" + enlace
        }
    return None