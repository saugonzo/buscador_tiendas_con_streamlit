import requests
from bs4 import BeautifulSoup

def buscar_lacasadelaeducadora(juego):
    url = "https://lacasadelaeducadora.com/search?q=" + juego.replace(" ", "+")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    productos = soup.select(".product-item__info")
    for producto in productos:
        titulo = producto.select_one(".product-item-meta__title")
        if titulo and juego.lower() in titulo.text.lower():
            if "agotado" in producto.text.lower():
                return None
            precio = producto.select_one(".price")
            if precio:
                return {
                    "precio": precio.text.strip(),
                    "url": "https://lacasadelaeducadora.com" + titulo["href"]
                }
    return None