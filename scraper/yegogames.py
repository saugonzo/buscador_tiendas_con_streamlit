import requests
from bs4 import BeautifulSoup

def buscar_yegogames(juego_buscado):
    url_busqueda = f"https://yegogames.com/search?q={juego_buscado.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url_busqueda, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        productos = soup.select("div.card__information")
        contenedores = soup.select("li.grid__item")

        for producto, contenedor in zip(productos, contenedores):
            nombre_tag = producto.select_one("a.full-unstyled-link")
            nombre = nombre_tag.get_text(strip=True) if nombre_tag else ""
            if juego_buscado.lower() not in nombre.lower():
                continue

            # Verifica si está agotado
            agotado = contenedor.find(string=lambda s: "agotado" in s.lower()) is not None
            if agotado:
                continue

            precio_tag = producto.select_one(".price-item--last")
            precio = precio_tag.get_text(strip=True).replace("\xa0", " ") if precio_tag else "Precio no disponible"

            url_producto = "https://yegogames.com" + nombre_tag["href"]

            imagen_tag = contenedor.select_one("img")
            imagen = "https:" + imagen_tag["src"] if imagen_tag and imagen_tag.get("src", "").startswith("//") else imagen_tag["src"]

            return {
                "nombre": nombre,
                "precio": precio,
                "url": url_producto,
                "imagen": imagen
            }

    except Exception as e:
        return {"error": str(e)}

    return None
