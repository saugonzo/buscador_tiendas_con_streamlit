import requests
from bs4 import BeautifulSoup

def buscar_canteraludica(juego_buscado):
    url_busqueda = f"https://canteraludica.com/search?q={juego_buscado.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url_busqueda, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        productos = soup.select("li.grid__item")

        for producto in productos:
            titulo_tag = producto.select_one("a.full-unstyled-link")
            nombre = titulo_tag.get_text(strip=True) if titulo_tag else ""
            if juego_buscado.lower() in nombre.lower():
                # Verifica si está agotado
                agotado = producto.find(string=lambda s: "agotado" in s.lower()) is not None
                if agotado:
                    continue

                precio_tag = producto.select_one(".price__container .price-item--last")
                precio = precio_tag.get_text(strip=True).replace("\xa0", " ") if precio_tag else "Precio no disponible"
                link = "https://canteraludica.com" + titulo_tag["href"]
                imagen_tag = producto.select_one("img")
                imagen = "https:" + imagen_tag["src"] if imagen_tag and imagen_tag.get("src", "").startswith("//") else imagen_tag["src"]

                return {
                    "nombre": nombre,
                    "precio": precio,
                    "url": link,
                    "imagen": imagen
                }

    except Exception as e:
        return {"error": str(e)}

    return None
