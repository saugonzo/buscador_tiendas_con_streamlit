import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(juego, debug=False):
    url_base = "https://www.geekystuff.mx"
    url_busqueda = f"https://www.geekystuff.mx/search?type=product&q={juego}"
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

    
    for item in soup.select(".search_res_item_snippet"):
        titulo_tag = item.select_one(".search_res_item_title")
        if not titulo_tag or juego.lower() not in titulo_tag.text.lower():
            continue
        agotado = "agotado" in item.text.lower()
        if agotado:
            continue
        enlace_tag = item.select_one("a")
        precio_tag = item.select_one(".isp_product_price")
        imagen_tag = item.select_one("img")
        return {
            "precio": precio_tag.text.strip() if precio_tag else "N/A",
            "url": enlace_tag['href'] if enlace_tag else "-",
            "imagen": imagen_tag['src'] if imagen_tag else ""
        }
        

    return None