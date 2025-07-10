
import requests
from bs4 import BeautifulSoup

def buscar_elduende(nombre_juego):
    url = "https://www.elduende.com.mx/?s=" + nombre_juego.replace(" ", "+") + "&post_type=product"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("h2", class_="woocommerce-loop-product__title")
    if not producto:
        return None

    if nombre_juego.lower() in producto.text.lower():
        enlace = producto.find("a")["href"]
        precio = soup.find("span", class_="woocommerce-Price-amount")
        return {
            "precio": precio.text.strip().replace("$", "").strip(),
            "url": enlace
        }
    return None
