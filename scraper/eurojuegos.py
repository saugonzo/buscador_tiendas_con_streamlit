import requests
from bs4 import BeautifulSoup

def buscar_eurojuegos(juego_buscado):
    url = f"https://eurojuegos.com.mx/search?type=product&q={juego_buscado.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        productos = soup.select("div.card__content")

        for producto in productos:
            nombre_tag = producto.select_one("h3.card__heading a")
            if not nombre_tag:
                continue

            nombre = nombre_tag.get_text(strip=True)
            if juego_buscado.lower() not in nombre.lower():
                continue

            precio_tag = producto.select_one(".price-item--last")
            if not precio_tag:
                continue  # No hay precio => probablemente agotado

            precio = precio_tag.get_text(strip=True)

            url_producto = nombre_tag["href"]
            if not url_producto.startswith("http"):
                url_producto = "https://eurojuegos.com.mx" + url_producto

            imagen_tag = producto.find_previous("img")
            imagen = imagen_tag["src"] if imagen_tag and "src" in imagen_tag.attrs else None
            if imagen and imagen.startswith("//"):
                imagen = "https:" + imagen

            return {
                "nombre": nombre,
                "precio": precio,
                "url": url_producto,
                "imagen": imagen
            }

    except Exception as e:
        return {"error": str(e)}

    return None
