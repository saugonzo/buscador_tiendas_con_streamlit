import requests
from bs4 import BeautifulSoup

def buscar_tdetlacuache(nombre_juego):
    url = "https://tdetlacuache.com/search?q=" + nombre_juego.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("a", class_="full-unstyled-link")
    if producto and nombre_juego.lower() in producto.text.lower():
        precio = producto.find_next("span", class_="price-item--last")
        return {
            "precio": precio.text.strip().replace("$", "").replace("MXN", "").strip(),
            "url": "https://tdetlacuache.com" + producto["href"]
        }
    return None