import requests
from bs4 import BeautifulSoup

def buscar_geekystuff(juego_buscado):
    url = f"https://www.geekystuff.mx/search?type=product&q={juego_buscado.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        productos = soup.select(".search_res_item_snippet")

        for producto in productos:
            nombre_tag = producto.select_one(".search_res_item_title a")
            if not nombre_tag:
                continue

            nombre = nombre_tag.get_text(strip=True)
            if juego_buscado.lower() not in nombre.lower():
                continue

            precio_tag = producto.select_one(".isp_product_price")
            if not precio_tag:
                continue

            precio = precio_tag.get_text(strip=True)

            url_producto = nombre_tag["href"]
            if not url_producto.startswith("http"):
                url_producto = "https://www.geekystuff.mx" + url_producto

            imagen_tag = producto.select_one("img.search_res_img")
            imagen = imagen_tag["src"] if imagen_tag else None

            return {
                "nombre": nombre,
                "precio": precio,
                "url": url_producto,
                "imagen": imagen
            }

    except Exception as e:
        return {"error": str(e)}

    return None
