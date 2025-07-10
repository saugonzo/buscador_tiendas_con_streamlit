import requests
from bs4 import BeautifulSoup

def buscar_elduende(juego, debug=False):
    url_base = "https://www.elduende.com.mx"
    url_busqueda = f"https://www.elduende.com.mx/?s={juego}&post_type=product"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url_busqueda, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        if debug:
            print(f"Error accediendo a {url_busqueda}: {e}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    
    for producto in soup.select(".product-small"):
        titulo_tag = producto.select_one(".woocommerce-loop-product__title")
        if not titulo_tag or juego.lower() not in titulo_tag.text.lower():
            continue
        agotado = producto.select_one(".out-of-stock")
        if agotado:
            continue
        enlace_tag = producto.select_one("a.woocommerce-LoopProduct-link")
        precio_tag = producto.select_one(".price bdi")
        imagen_tag = producto.select_one("img")
        return {
            "precio": precio_tag.text.strip() if precio_tag else "N/A",
            "url": enlace_tag['href'] if enlace_tag else "-",
            "imagen": imagen_tag['src'] if imagen_tag else ""
        }
        

    return None