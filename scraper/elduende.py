import requests
from bs4 import BeautifulSoup

def buscar_elduende(juego):
    url_base = "#"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(f"#" + juego.replace(" ", "+"), headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Implementación específica del sitio:
        # Aquí se debe personalizar la lógica para extraer nombre, precio, imagen y URL

        producto = soup.find('div')
        if not producto:
            return None

        nombre_producto = producto.get_text(strip=True)
        if juego.lower() not in nombre_producto.lower():
            return None

        agotado = producto.find(string=lambda t: "agotado" in t.lower())
        if agotado:
            return None

        precio = producto.find('span')
        img = producto.find("img")
        enlace = producto.find("a", href=True)

        return {
            "precio": precio.get_text(strip=True) if precio else "N/A",
            "url": url_base + enlace["href"] if enlace else url_base,
            "imagen": img["src"] if img and "src" in img.attrs else None
        }

    except Exception as e:
        return None