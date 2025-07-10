import requests
from bs4 import BeautifulSoup

def buscar_juegodebelugas(juego):
    url = "https://juegodebelugas.com/search?q=" + juego.replace(" ", "+")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    productos = soup.select(".product-grid-item")
    for producto in productos:
        titulo_tag = producto.select_one(".product-title")
        if titulo_tag and juego.lower() in titulo_tag.text.lower():
            if "agotado" in producto.text.lower():
                continue
            precio = producto.select_one(".money")
            imagen_tag = producto.select_one("img")
            link_tag = producto.select_one("a")
            if precio and link_tag and imagen_tag:
                return {
                    "nombre": titulo_tag.text.strip(),
                    "precio": precio.text.strip(),
                    "url": link_tag["href"] if link_tag["href"].startswith("http") else "https://juegodebelugas.com" + link_tag["href"],
                    "imagen": imagen_tag["src"] if imagen_tag["src"].startswith("http") else "https:" + imagen_tag["src"]
                }
    return None