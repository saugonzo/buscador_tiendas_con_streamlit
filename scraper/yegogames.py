import requests
from bs4 import BeautifulSoup

def buscar_yegogames(juego):
    url = "https://yegogames.com/search?q=" + juego.replace(" ", "+")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    productos = soup.select(".productgrid--item")
    for producto in productos:
        titulo_tag = producto.select_one(".productitem--title")
        if titulo_tag and juego.lower() in titulo_tag.text.lower():
            if "agotado" in producto.text.lower():
                continue
            precio = producto.select_one(".productitem--price")
            imagen = producto.select_one("img")
            link_tag = producto.select_one("a")
            if precio and imagen and link_tag:
                return {
                    "nombre": titulo_tag.text.strip(),
                    "precio": precio.text.strip(),
                    "url": "https://yegogames.com" + link_tag["href"],
                    "imagen": imagen["src"] if imagen["src"].startswith("http") else "https:" + imagen["src"]
                }
    return None