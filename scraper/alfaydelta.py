import requests
from bs4 import BeautifulSoup
import unidecode

def buscar_alfaydelta(juego, debug=False):
    url_base = "https://alfaydelta.com"
    busqueda = juego.replace(" ", "+")
    url = f"https://alfaydelta.com/search?q=" + busqueda
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

        
        productos = soup.select("div.product-item")
        for producto in productos:
            titulo_tag = producto.select_one("span.product-item__title")
            precio_tag = producto.select_one("span.product__price--original")
            link_tag = producto.find("a", href=True)
            img_tag = producto.select_one("img")
            disponibilidad = producto.text.lower()
            if titulo_tag and match(titulo_tag.text) and "agotado" not in disponibilidad:
                return {
                    "nombre": titulo_tag.text.strip(),
                    "precio": precio_tag.text.strip() if precio_tag else "N/A",
                    "url": url_base + link_tag["href"],
                    "imagen": "https:" + img_tag["src"] if img_tag else None
                }
        return None
        

    except Exception as e:
        return None