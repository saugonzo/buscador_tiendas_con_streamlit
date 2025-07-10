import requests
from bs4 import BeautifulSoup

def buscar_canteraludica(juego):
    url = "https://canteraludica.com/search?q=" + juego.replace(" ", "+")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    productos = soup.select(".card-wrapper")
    for producto in productos:
        titulo_tag = producto.select_one(".card__heading a")
        if titulo_tag and juego.lower() in titulo_tag.text.lower():
            if "agotado" in producto.text.lower():
                continue
            precio = producto.select_one(".price-item--last")
            imagen = producto.select_one("img")
            if precio and imagen:
                return {
                    "nombre": titulo_tag.text.strip(),
                    "precio": precio.text.strip(),
                    "url": "https://canteraludica.com" + titulo_tag["href"],
                    "imagen": imagen["src"] if imagen["src"].startswith("http") else "https:" + imagen["src"]
                }
    return None