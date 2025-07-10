import requests
from bs4 import BeautifulSoup
import unidecode

def buscar_geekystuff(juego):
    url_base = "https://www.geekystuff.mx"
    busqueda = juego.replace(" ", "+")
    url = f"https://www.geekystuff.mx/search?query=" + busqueda
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    def match(text):
        if not text:
            return False
        normal = unidecode.unidecode(text.lower())
        return all(p in normal for p in unidecode.unidecode(juego.lower()).split())

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        
        productos = soup.select("div.search_res_item_snippet")
        for producto in productos:
            titulo_tag = producto.select_one("div.search_res_item_title")
            precio_tag = producto.select_one("div.isp_product_price")
            link_tag = producto.select_one("a[href]")
            img_tag = producto.select_one("img")
            disponibilidad = producto.text.lower()
            if titulo_tag and match(titulo_tag.text) and "agotado" not in disponibilidad:
                return {
                    "nombre": titulo_tag.text.strip(),
                    "precio": precio_tag.text.strip() if precio_tag else "N/A",
                    "url": link_tag["href"] if link_tag else None,
                    "imagen": img_tag["src"] if img_tag else None
                }
        return None
        

    except Exception as e:
        return None