import requests
from bs4 import BeautifulSoup

def buscar_elduende(juego_buscado):
    url = f"https://elduende.com.mx/search?q={juego_buscado.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        productos = soup.select("li.grid__item")

        for producto in productos:
            nombre_tag = producto.select_one("h3.card__heading a")
            if not nombre_tag:
                continue

            nombre = nombre_tag.get_text(strip=True)
            if juego_buscado.lower() not in nombre.lower():
                continue

            agotado = producto.select_one(".badge--sold-out")
            if agotado:
                continue  # Producto agotado

            precio_tag = producto.select_one(".price__sale .price-item--last, .price__regular .price-item--regular")
            if not precio_tag:
                continue  # Sin precio visible

            precio = precio_tag.get_text(strip=True)

            url_producto = nombre_tag["href"]
            if not url_producto.startswith("http"):
                url_producto = "https://elduende.com.mx" + url_producto

            imagen_tag = producto.find("img")
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
