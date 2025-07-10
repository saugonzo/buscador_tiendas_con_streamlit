import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(nombre_juego):
    url = "https://www.geekystuff.mx/search?query=" + nombre_juego.replace(" ", "%20")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("div", class_="search_res_item_snippet")
    if producto and nombre_juego.lower() in producto.text.lower():
        enlace = producto.find("a", href=True)
        precio = producto.find("div", class_="isp_product_price")
        return {
            "precio": precio.text.strip().replace("MXN", "").replace("$", "").strip(),
            "url": enlace["href"]
        }
    return None