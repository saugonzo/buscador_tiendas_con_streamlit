import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(nombre_juego):
    try:
        url = f"https://www.geekystuff.mx/search?query={nombre_juego}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        productos = soup.select("a.sc-hKgILt")  # enlaces a productos

        for producto in productos:
            titulo = producto.get_text(strip=True)
            if nombre_juego.lower() in titulo.lower():
                link = "https://www.geekystuff.mx" + producto.get("href", "")
                
                # Ahora entramos al enlace del producto para obtener precio y disponibilidad
                prod_resp = requests.get(link, timeout=10)
                prod_resp.raise_for_status()
                prod_soup = BeautifulSoup(prod_resp.text, "html.parser")

                agotado = prod_soup.find(string=lambda t: "agotado" in t.lower()) is not None
                if agotado:
                    continue  # lo saltamos si está agotado

                precio_tag = prod_soup.select_one(".sc-bcXHqe span")
                precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no encontrado"

                img_tag = prod_soup.select_one("img.sc-eDLJxc")
                imagen = img_tag.get("src") if img_tag else ""

                return {
                    "titulo": titulo,
                    "precio": precio,
                    "url": link,
                    "imagen": imagen
                }

        return None
    except Exception as e:
        return {"error": str(e)}
