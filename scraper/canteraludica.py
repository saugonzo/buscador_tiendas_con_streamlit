import requests
from bs4 import BeautifulSoup

def buscar_canteraludica(juego):
    url = "https://canteraludica.com/search?q=" + juego.replace(" ", "+")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    productos = soup.select(".card__information")
    for producto in productos:
        titulo_tag = producto.select_one(".card__heading a")
        if titulo_tag and juego.lower() in titulo_tag.text.lower():
            if "agotado" in producto.text.lower():
                return None
            precio = producto.select_one(".price-item--last")
            if precio:
                return {
                    "precio": precio.text.strip(),
                    "url": "https://canteraludica.com" + titulo_tag["href"]
                }
    return None