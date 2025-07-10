import requests
from bs4 import BeautifulSoup

def buscar_lacasadelaeducadora(nombre_juego):
    url = "https://lacasadelaeducadora.com/search?q=" + nombre_juego.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("div", class_="product-item-meta")
    if producto and nombre_juego.lower() in producto.text.lower():
        enlace = producto.find("a", class_="product-item-meta__title")
        precio = producto.find("span", class_="price")
        return {
            "precio": precio.text.strip().replace("$", "").replace("MXN", "").strip(),
            "url": "https://lacasadelaeducadora.com" + enlace["href"]
        }
    return None