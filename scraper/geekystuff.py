
import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(nombre_juego):
    url = "https://www.geekystuff.mx/search?query=" + nombre_juego.replace(" ", "%20")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("div", class_="search_res_item_title")
    if not producto:
        return None

    titulo = producto.find("a")
    if titulo and nombre_juego.lower() in titulo.text.lower():
        enlace = titulo["href"]
        precio = soup.find("div", class_="isp_product_price")
        return {
            "precio": precio.text.strip().replace("MXN", "").replace("$", "").strip(),
            "url": enlace
        }
    return None
