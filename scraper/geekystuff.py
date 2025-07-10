import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(juego):
    url = "https://www.geekystuff.mx/search?query=" + juego.replace(" ", "%20")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    productos = soup.select(".search_res_item_snippet")
    for producto in productos:
        titulo = producto.select_one(".search_res_item_title a")
        if titulo and juego.lower() in titulo.text.lower():
            if "agotado" in producto.text.lower():
                return None
            precio = producto.select_one(".isp_product_price")
            link = titulo["href"]
            if precio and link:
                return {
                    "precio": precio.text.strip(),
                    "url": link
                }
    return None