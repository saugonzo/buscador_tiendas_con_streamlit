import requests
from bs4 import BeautifulSoup

def buscar_yegogames(juego, debug=False):
    url_base = "https://www.yegogames.com"
    url_busqueda = f"https://www.yegogames.com/search?q={juego}"
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

    
    for producto in soup.select(".card__information"):
        titulo_tag = producto.select_one("a")
        if not titulo_tag or juego.lower() not in titulo_tag.text.lower():
            continue
        agotado = producto.select_one(".badge--sold-out")
        if agotado:
            continue
        precio_tag = producto.select_one(".price-item--last")
        imagen_tag = producto.find_previous("img")
        return {
            "precio": precio_tag.text.strip() if precio_tag else "N/A",
            "url": "https://www.yegogames.com" + titulo_tag["href"] if titulo_tag else "-",
            "imagen": imagen_tag["src"] if imagen_tag else ""
        }
        

    return None