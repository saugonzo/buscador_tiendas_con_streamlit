import requests
from bs4 import BeautifulSoup

def buscar_alfaydelta(juego, debug=False):
    try:
        url_base = "https://alfaydelta.com"
        busqueda = juego.replace(" ", "+")
        url_busqueda = f"https://alfaydelta.com/search?q={busqueda}"

        res = requests.get(url_busqueda, timeout=10)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")

        
producto = soup.select_one("div.card__information")
if not producto:
    return None
nombre_producto = producto.select_one("a.full-unstyled-link").text
if juego.lower() not in nombre_producto.lower():
    return None
precio = producto.select_one(".price__container").text
url_producto = url_base + producto.select_one("a.full-unstyled-link")["href"]
imagen = url_base + producto.find_previous("img")["src"]
disponible = True if "$" in precio else False


        return {
            "precio": precio.strip(),
            "url": url_producto,
            "imagen": imagen
        } if disponible else None

    except Exception as e:
        if debug:
            print(f"Error en buscar_alfaydelta: {e}")
        return None