import requests
from bs4 import BeautifulSoup

def buscar_tdetlacuache(juego):
    url = "https://tdetlacuache.com/search?q=" + juego.replace(" ", "+")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    productos = soup.select(".grid-product__content")
    for producto in productos:
        titulo_tag = producto.select_one(".grid-product__title")
        if titulo_tag and juego.lower() in titulo_tag.text.lower():
            if "agotado" in producto.text.lower():
                continue
            precio = producto.select_one(".grid-product__price")
            imagen_tag = producto.find_previous("img")
            link_tag = producto.find_previous("a")
            if precio and imagen_tag and link_tag:
                return {
                    "nombre": titulo_tag.text.strip(),
                    "precio": precio.text.strip(),
                    "url": "https://tdetlacuache.com" + link_tag["href"],
                    "imagen": imagen_tag["src"] if imagen_tag["src"].startswith("http") else "https:" + imagen_tag["src"]
                }
    return None