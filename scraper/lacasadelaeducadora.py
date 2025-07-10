
import requests
from bs4 import BeautifulSoup

def buscar_lacasadelaeducadora(nombre_juego):
    url = "https://www.lacasadelaeducadora.com/search?q=" + nombre_juego.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("div", class_="product-item-meta")
    if not producto:
        return None

    titulo = producto.find("a", class_="product-item-meta__title")
    if titulo and nombre_juego.lower() in titulo.text.lower():
        enlace = titulo["href"]
        precio = soup.find("span", class_="price")
        return {
            "precio": precio.text.strip().replace("$", "").replace("MXN", "").strip(),
            "url": "https://www.lacasadelaeducadora.com" + enlace
        }
    return None
