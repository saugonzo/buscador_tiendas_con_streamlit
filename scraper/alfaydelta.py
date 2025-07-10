import requests
from bs4 import BeautifulSoup

def buscar_alfaydelta(nombre_juego):
    url = "https://alfaydelta.com/search?q=" + nombre_juego.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("div", class_="product-item")
    if producto:
        titulo = producto.find("span", class_="product-item__title")
        if titulo and nombre_juego.lower() in titulo.text.lower():
            precio = producto.find("span", class_="product__price--original")
            enlace = producto.find("a", class_="product-item__link")
            return {
                "precio": precio.text.strip().replace("$", "").replace("MXN", "").strip(),
                "url": "https://alfaydelta.com" + enlace["href"]
            }
    return None