import requests
from bs4 import BeautifulSoup
import unidecode

def buscar_elduende(juego):
    url_base = "https://www.elduende.com.mx"
    busqueda = juego.replace(" ", "+")
    url = f"https://www.elduende.com.mx/?s=" + busqueda
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

        
        productos = soup.select("li.product")
        for producto in productos:
            titulo_tag = producto.select_one("h2.woocommerce-loop-product__title")
            precio_tag = producto.select_one("span.woocommerce-Price-amount")
            link_tag = producto.select_one("a.woocommerce-LoopProduct-link")
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