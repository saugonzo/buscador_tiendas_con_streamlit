import requests
from bs4 import BeautifulSoup

def buscar_tdetlacuache(juego):
    url = "https://tdetlacuache.com/search?q=" + juego.replace(" ", "+")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    productos = soup.select(".card__information")
    for producto in productos:
        titulo = producto.select_one(".card__heading a")
        if titulo and juego.lower() in titulo.text.lower():
            if "agotado" in producto.text.lower():
                return None
            precio = producto.select_one(".price-item--last")
            if precio:
                return {
                    "precio": precio.text.strip(),
                    "url": "https://tdetlacuache.com" + titulo["href"]
                }
    return None