import requests
from bs4 import BeautifulSoup

def buscar_alfaydelta(juego):
    url = "https://alfaydelta.com/search?q=" + juego.replace(" ", "+")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    productos = soup.select(".product-item")
    for producto in productos:
        titulo = producto.select_one(".product-item__title")
        if titulo and juego.lower() in titulo.text.lower():
            agotado = producto.select_one(".badge__text")
            if agotado and "agotado" in agotado.text.lower():
                return None
            precio = producto.select_one(".product__price--original")
            link = producto.select_one("a")["href"]
            if precio and link:
                return {
                    "precio": precio.text.strip(),
                    "url": "https://alfaydelta.com" + link
                }
    return None