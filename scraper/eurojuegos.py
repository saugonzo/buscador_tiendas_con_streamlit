
import requests
from bs4 import BeautifulSoup

def buscar_eurojuegos(nombre_juego):
    url = "https://www.eurojuegos.com.mx/?s=" + nombre_juego.replace(" ", "+") + "&post_type=product"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    producto = soup.find("h2", class_="woocommerce-loop-product__title")
    if not producto:
        return None

    if nombre_juego.lower() in producto.text.lower():
        enlace = producto.find_parent("a")["href"]
        precio = soup.find("span", class_="woocommerce-Price-amount")
        return {
            "precio": precio.text.strip().replace("$", "").strip(),
            "url": enlace
        }
    return None
