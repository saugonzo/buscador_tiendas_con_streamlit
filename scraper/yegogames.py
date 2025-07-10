import requests
from bs4 import BeautifulSoup

def buscar_yegogames(juego: str) -> dict | None:
    url_busqueda = f"https://yegogames.com/search?q={juego.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url_busqueda, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        producto = soup.find("div", class_="card__information")
        if not producto:
            return None

        nombre = producto.find("h3").get_text(strip=True)
        if juego.lower() not in nombre.lower():
            return None

        precio_tag = producto.find("span", class_="price-item--regular")
        if not precio_tag:
            return None

        agotado = producto.find("div", class_="badge badge--bottom-left")  # a veces aparece como "Agotado"
        if agotado and "agotado" in agotado.get_text(strip=True).lower():
            return None

        precio = precio_tag.get_text(strip=True).replace("$", "").replace("MXN", "").strip()

        link = producto.find("a", class_="full-unstyled-link")
        url_producto = f"https://yegogames.com{link['href']}" if link else url_busqueda

        imagen_tag = producto.find_parent().find("img")
        imagen_url = "https:" + imagen_tag["src"] if imagen_tag and imagen_tag.get("src") else ""

        return {
            "precio": precio,
            "url": url_producto,
            "imagen": imagen_url
        }

    except Exception as e:
        print(f"Error al buscar en Yego Games: {e}")
        return None
