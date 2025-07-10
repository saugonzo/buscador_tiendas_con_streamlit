import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(nombre_juego):
    try:
        url = f"https://www.geekystuff.mx/search?query={nombre_juego}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        productos = soup.select("a[href^='/product-page/']")  # enlaces a productos

        for producto in productos:
            titulo = producto.get_text(strip=True)
            if nombre_juego.lower() in titulo.lower():
                link = "https://www.geekystuff.mx" + producto["href"]

                # Ir al enlace del producto
                producto_page = requests.get(link, timeout=10)
                producto_page.raise_for_status()
                prod_soup = BeautifulSoup(producto_page.text, "html.parser")

                # Verificar si el producto está agotado
                agotado_texto = prod_soup.find(string=lambda text: "agotado" in text.lower() or "sin existencias" in text.lower())
                if agotado_texto:
                    continue

                # Extraer precio
                precio_tag = prod_soup.select_one("span[data-hook='formatted-primary-price']")
                precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no disponible"

                # Extraer imagen
                img_tag = prod_soup.select_one("img[src*='geekystuff']")
                imagen = img_tag["src"] if img_tag else ""

                return {
                    "titulo": titulo,
                    "precio": precio,
                    "url": link,
                    "imagen": imagen
                }

        return None
    except Exception as e:
        return {"error": str(e)}
