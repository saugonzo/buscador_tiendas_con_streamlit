import requests
from bs4 import BeautifulSoup

def buscar_eurojuegos(juego):
    url = "https://www.eurojuegos.com.mx/?s=" + juego.replace(" ", "+") + "&post_type=product"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    productos = soup.select(".product")
    for producto in productos:
        titulo = producto.select_one(".woocommerce-loop-product__title")
        if titulo and juego.lower() in titulo.text.lower():
            if "agotado" in producto.text.lower():
                return None
            precio = producto.select_one(".price .woocommerce-Price-amount")
            link = producto.select_one("a")["href"]
            if precio:
                return {
                    "precio": precio.text.strip(),
                    "url": link
                }
    return None